import pytest


@pytest.fixture(scope="session")
def celery_config():
    # Disabling celery during test runs
    return {"broker_url": "redis://"}
