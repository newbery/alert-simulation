import pytest

import backend._celery as impl


@pytest.fixture
def config():
    return impl.Config()


@pytest.fixture
def settings():
    return impl.Settings()


def test_init(config, settings, mocker):
    """The 'init' func should background a task to initialize the Celery workers,
    then add a task to the Celery queue for each message to be sent, and finally
    return an empty dict.
    """
    background = mocker.Mock()
    queue_task = mocker.patch.object(impl, "queue_task")
    result = impl.init(config, settings, background)

    number_of_workers = settings.number_of_processes
    background.add_task.assert_called_once_with(
        impl.init_workers, number_of_workers, concurrency=1
    )
    number_of_messages = settings.number_of_messages
    queue_task.call_count = number_of_messages
    assert result == {}


def test_ready(config, settings, mocker):
    """The 'ready' func should check if the initialization set up has completed.
    If not completed then return False. If completed then return True.
    """
    check = mocker.patch.object(impl, "check_if_ready")

    # not ready
    check.return_value = {"ready": False}
    result = impl.ready(config, settings)
    check.assert_called_once_with(config, settings)
    assert result == {"ready": False}

    # ready
    check.return_value = {"ready": True}
    result = impl.ready(config, settings)
    check.assert_called_with(config, settings)
    assert result == {"ready": True}


def test_start(config, settings, mocker):
    """The 'start' func should broadcast to the waiting workers to start
    consuming from the Celery queue. This function should return an empty dict.
    """
    background = None
    start_workers = mocker.patch.object(impl, "start_workers")
    result = impl.start(config, settings, background)

    start_workers.assert_called_once()
    assert result == {}


def test_status(config, settings, mocker):
    """The 'status' func should return the current counts"""
    counts = {"count": 1, "failed": 2, "average_time": 3}
    mocker.patch.object(impl, "connect")
    mocker.patch.object(impl, "read_counts", lambda c: counts)
    result = impl.status(config, settings)

    assert result == counts


def test_reset(config, settings, mocker):
    """The 'reset' func should reset the celery app, reset counts,
    and return an empty dict.
    """
    reset_celery = mocker.patch.object(impl, "reset_celery")
    reset_counts = mocker.patch.object(impl, "reset_counts")
    result = impl.reset(config, settings)

    reset_celery.assert_called_once()
    reset_counts.assert_called_once()
    assert result == {}
