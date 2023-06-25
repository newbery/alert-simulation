from concurrent import futures

from fastapi import BackgroundTasks

from .redis_helpers import connect, reset_counts, read_counts, update_counts
from .settings import Config, Settings, check_session, reset_settings
from .messenger import generate_message, generate_phone_number, send_message


def init(config: Config, settings: Settings, background: BackgroundTasks) -> dict:
    """Initialize the simulation setup"""
    # All work is done during 'start' but first check if another session exists.
    session_ok, response_dict = check_session(settings, create=True)
    return response_dict


def ready(config: Config, settings: Settings) -> dict:
    """Check if the simulation setup is ready"""
    # Again, nothing to wait for but check if another session exists
    session_ok, response_dict = check_session(settings)
    if not session_ok:
        return response_dict
    return response_dict | {"ready": True}


def start(
    config: Config, settings: Settings, background: BackgroundTasks
) -> dict:
    """Start the simulation"""
    session_ok, response_dict = check_session(settings)
    if session_ok:
        print("Before start tasks")
        start_tasks(config, settings)
        print("After start tasks")
    return response_dict


def status(config: Config, settings: Settings) -> dict:
    """Get the running results of the simulation"""
    session_ok, response_dict = check_session(settings)
    if not session_ok:
        return response_dict
    return response_dict | read_counts(connect())


def reset(config: Config, settings: Settings) -> dict:
    """Teardown/reset the simulation"""
    global executor

    session_ok, response_dict = check_session(settings)
    if not session_ok:
        return response_dict

    # This little shuffle is to avoid a potential race condition
    # in the loop that is adding more tasks to the executor.
    # It turns off the loop before shutting down the executor.
    executor_, executor = executor, None

    # reset counts and settings early in case the next bit takes a while
    reset_counts(connect())
    reset_settings()

    if executor_ is not None:
        print("Start executor shutdown")
        executor_.shutdown(wait=True, cancel_futures=True)
        print("Finished executor shutdown")
        
        # reset counts once more in case any stragglers snuck in during shutdown
        reset_counts(connect())
    
    return response_dict


# executor needs to be a global so "reset" can reach it
executor: futures.Executor | None = None


def set_executor(e: futures.Executor | None) -> None:
    global executor
    executor = e


def start_tasks(config: Config, settings: Settings) -> None:
    """Start all the message tasks using a locally managed pool of processes"""
    redis = connect()
    tasks = []

    number_of_processes = settings.number_of_processes
    number_of_messages = settings.number_of_messages

    kwargs = {
        "time_mean": config.message_time_mean,
        "time_stdev": config.message_time_stdev,
        "failure_rate": settings.failure_rate,
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
    *, time_mean: float, time_stdev: float, failure_rate: float
) -> tuple[float, float]:
    message = generate_message()
    phone_number = generate_phone_number()
    delaydist = (time_mean, time_stdev)
    delay, failed = send_message(message, phone_number, failure_rate, delaydist)
    return delay, failed
