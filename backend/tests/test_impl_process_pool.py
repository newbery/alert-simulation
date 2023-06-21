import pytest

import backend._process_pool as impl


@pytest.fixture
def config():
    return impl.Config()


@pytest.fixture
def settings():
    return impl.Settings()


async def test_init(config, settings, mocker):
    """The 'init' func should do nothing and return nothing"""
    background = mocker.Mock()
    result = await impl.init(config, settings, background)

    background.add_task.assert_not_called()
    assert result is None


async def test_ready(config, settings):
    """The 'ready' func should do nothing and return True"""
    result = await impl.ready(config, settings)

    assert result == {"ready": True}


async def test_start(config, settings, mocker):
    """The 'start' func should queue up a background task and return nothing"""
    background = mocker.Mock()
    result = await impl.start(config, settings, background)

    background.add_task.assert_called_once_with(impl.start_tasks, config, settings)
    assert result is None


async def test_status(config, mocker):
    """The 'status' func should return the current counts"""
    counts = {"count": 1, "failed": 2, "average_time": 3}
    mocker.patch.object(impl, "connect")
    mocker.patch.object(impl, "read_counts", lambda c: counts)
    result = await impl.status(config)

    assert result == counts


async def test_reset(config, mocker):
    """The 'reset' func should shutdown the executor, reset counts,
    and return nothing.
    """
    executor = mocker.patch.object(impl, "_executor")
    reset_counts = mocker.patch.object(impl, "reset_counts")
    result = await impl.reset(config)

    executor.shutdown.assert_called_once()
    reset_counts.assert_called_once()
    assert result is None
