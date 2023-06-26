import os
from concurrent import futures
from typing import Callable

from fastapi import BackgroundTasks

from .redis_helpers import connect, reset_counts, read_counts, update_counts
from .settings import Config, Settings, reset_settings
from .messenger import generate_message, generate_phone_number, send_message


def init(config: Config, settings: Settings, background: BackgroundTasks) -> dict:
    """Initialize the simulation setup"""
    # All work is done during 'start' so nothing to do here
    return {}


def ready(config: Config, settings: Settings) -> dict:
    """Check if the simulation setup is ready"""
    # Again, nothing to do so just respond 'ready'
    return {"ready": True}


def start(
    config: Config, settings: Settings, background: BackgroundTasks
) -> dict:
    """Start the simulation"""
    print("Before start tasks")
    start_tasks(config, settings)
    print("After start tasks")
    return {}


def status(config: Config, settings: Settings) -> dict:
    """Get the running results of the simulation"""
    return read_counts(connect())


def reset(config: Config, settings: Settings) -> dict:
    """Teardown/reset the simulation"""
    reset_simulation()
    return {}


# executor needs to be a global so "reset_simulation" can reach it
executor: futures.Executor | None = None


def reset_simulation():
    """"""
    global executor

    # This little shuffle is to avoid a potential race condition
    # in the loop that is adding more tasks to the executor.
    # It turns off the loop before shutting down the executor.
    executor_, executor = executor, None

    # reset counts and settings early in case the next bit takes a while
    # redis_conn = connect()
    # reset_counts(redis_conn)
    reset_settings()

    if executor_ is not None:
        print("Start executor shutdown")
        executor_.shutdown(wait=True, cancel_futures=True)
        print("Finished executor shutdown")
        
        # reset counts once more in case any stragglers snuck in during shutdown
        # reset_counts(redis_conn)

        
def set_executor(e: futures.Executor | None) -> None:
    """"""
    global executor
    if executor is None:
        executor = e
    else:
        # This shouldn't happen but, just in case it does, let's initiate a reset.
        reset_simulation()
        set_executor(e)


def start_tasks(config: Config, settings: Settings) -> None:
    """Start all the message tasks using a locally managed pool of processes"""
    redis = connect()
    reset_counts(redis)
    tasks = []

    number_of_processes = settings.number_of_processes
    number_of_messages = settings.number_of_messages

    kwargs = {
        "failure_rate": settings.failure_rate,
        "time_mean": config.message_time_mean,
        "time_stdev": config.message_time_stdev,
    }

    def update(task):
        try:
            delay, failed = task.result()
            update_counts(redis, delay, failed)
        except futures.CancelledError:
            # We can get here after a reset, so just ignore it
            pass

    set_executor(futures.ProcessPoolExecutor(max_workers=number_of_processes))

    for _ in range(number_of_messages):
        if executor is not None:
            task = executor.submit(message_task, **kwargs)
            task.add_done_callback(update)
            tasks.append(task)


def message_task(
    *,
    failure_rate: float,
    time_mean: float,
    time_stdev: float,
    time_seed: Callable = os.getpid,
) -> tuple[float, float]:
    """
    Simulate sending a emergency message that just waits for a random time.

    The `seed` func is needed to insure a new random seed for each "process".
    The default is `os.getpid` which is good enough for a multiprocess backend.
    For a multi-threaded backend, this should maybe be `threading.get_ident`.
    """

    message = generate_message()
    phone_number = generate_phone_number()
    delaydist = (time_mean, time_stdev, time_seed())
    delay, failed = send_message(message, phone_number, failure_rate, delaydist)
    return delay, failed
