import pytest

import backend._process_pool as impl


@pytest.fixture
def config():
    return impl.Config()


@pytest.fixture
def settings():
    return impl.Settings()


def test_init(config, settings, mocker):
    """The 'init' func should do nothing and return an empty dict"""
    background = mocker.Mock()
    result = impl.init(config, settings, background)

    background.add_task.assert_not_called()
    assert result == {}


def test_ready(config, settings):
    """The 'ready' func should do nothing and return True"""
    result = impl.ready(config, settings)

    assert result == {"ready": True}


def test_start(config, settings, mocker):
    """The 'start' func should queue up a background task and return an empty dict"""
    background = mocker.Mock()
    start_tasks = mocker.patch.object(impl, "start_tasks")
    result = impl.start(config, settings, background)

    background.add_task.assert_not_called()
    start_tasks.assert_called_with(config, settings)
    assert result == {}


def test_status(config, settings, mocker):
    """The 'status' func should return the current counts"""
    counts = {"count": 1, "failed": 2, "average_time": 3}
    mocker.patch.object(impl, "connect")
    mocker.patch.object(impl, "read_counts", lambda c: counts)
    result = impl.status(config, settings)

    assert result == counts


def test_reset(config, settings, mocker):
    """The 'reset' func should shutdown the executor
    and return an empty dict.
    """
    executor = mocker.patch.object(impl, "executor")
    result = impl.reset(config, settings)

    executor.shutdown.assert_called_once()
    assert result == {}
