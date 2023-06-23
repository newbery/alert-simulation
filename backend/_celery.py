import shlex
import time
from functools import cached_property
from subprocess import run, Popen, DEVNULL

from amqp import ChannelError  # type: ignore
from fastapi import BackgroundTasks
from celery import Celery, Task  # type: ignore

from .redis_helpers import connect, reset_counts, read_counts, update_counts
from .settings import Config, Settings
from .messenger import generate_message, generate_phone_number, send_message


celery = Celery("backend", broker="redis://localhost:6379/0")
quiet = dict(stdout=DEVNULL, stderr=DEVNULL, stdin=DEVNULL)


def init(config: Config, settings: Settings, background: BackgroundTasks) -> None:
    """Initialize the simulation setup.

    In this case, that means initialize celery workers and queue up messages.
    """

    # Option #1: Init a single worker, with multiple processes
    # number_of_workers = 1
    # concurrency = settings.number_of_processes

    # Option #2: Init multiple workers, each with a single process
    number_of_workers = settings.number_of_processes
    concurrency = 1

    reset_celery(celery)
    background.add_task(init_workers, number_of_workers, concurrency=concurrency)

    # Queue up the message tasks
    number_of_messages = settings.number_of_messages
    for i in range(number_of_messages):
        queue_task(config, settings)


def ready(config: Config, settings: Settings) -> dict:
    """Check if the simulation setup is ready"""
    return check_if_ready(config, settings)


def start(
    config: Config, settings: Settings, background: BackgroundTasks
) -> None:
    """Start the simulation"""
    start_workers(celery)


def status(config: Config) -> dict:
    """Get the running results of the simulation"""
    return read_counts(connect())


def reset(config: Config) -> None:
    """Teardown/reset the simulation"""
    reset_celery(celery)
    reset_counts(connect())


def init_workers(
    number_of_workers: int,
    concurrency: int = 1,
    pool: str = "prefork",
):
    """Start the celery workers in 'non-consuming' mode with '-Q' blank.

    TODO: This uses the celery command line for now. Maybe refactor to
    use celery.control instead.
    """
    command = (
        f"celery -A backend._celery worker -Q --loglevel=INFO"
        f" --pool={pool} --concurrency={concurrency}"
    )
    for i in range(number_of_workers):
        full_command = command + f" -n simworker{i+1}@%h"
        Popen(shlex.split(full_command), **quiet)  # type: ignore


def check_if_ready(config: Config, settings: Settings) -> dict:
    """Check if the celery workers and messages are ready"""

    # Check if all the workers are running
    command = "celery -A backend._celery status"
    result = run(shlex.split(command), capture_output=True, text=True)
    output = result.stdout.strip()
    workers_ready = output.count("simworker") >= settings.number_of_processes

    # Check if all the messages are queued
    with celery.connection() as conn:
        try:
            queue = conn.channel().queue_declare("celery", passive=True)
            queue_count = queue.message_count
        except ChannelError:
            queue_count = 0
        queue_ready = queue_count >= settings.number_of_messages

    return {"ready": workers_ready and queue_ready}


def start_workers(celery: Celery) -> None:
    """Shutdown all celery workers and purge the queue."""
    celery.control.add_consumer("celery")


def reset_celery(celery: Celery) -> None:
    """Shutdown all celery workers and purge the queue."""
    celery.control.shutdown()

    # As a fallback, let's also stop workers from the command line.
    # We do this since in some cases, the non command line version
    # appears to re-queue messages. Let's fix this later.
    # Ignore the error message from this:
    #   "Error: No nodes replied within time constraint"
    command = "celery -A backend._celery control shutdown"
    Popen(shlex.split(command), **quiet)  # type: ignore

    # TODO: There is probably a better way to wait for workers to shutdown
    # Experiment with something like the workers_exist function below.
    time.sleep(2)

    celery.control.purge()


# def workers_exist(celery: Celery) -> bool:
#     ping = celery.control.inspect().ping()
#     print(ping)
#     return bool(ping)


def queue_task(config: Config, settings: Settings) -> None:
    args = [generate_message(), generate_phone_number()]
    kwargs = {
        "failure_rate": settings.failure_rate,
        "delaydist": (config.message_time_mean, config.message_time_stdev),
    }
    message_task.apply_async(args=args, kwargs=kwargs)


class RedisTask(Task):
    def __init__(self):
        super().__init__()
        self._redis = connect()

    @cached_property
    def redis(self):
        return self._redis


@celery.task(base=RedisTask, bind=True)
def message_task(
    self,
    message: str,
    phone_number: str,
    *,
    failure_rate: float = 0.0,
    delaydist: tuple[float, float],
) -> bool:
    delay, failed = send_message(message, phone_number, failure_rate, delaydist)
    return bool(update_counts(self.redis, delay, failed))
