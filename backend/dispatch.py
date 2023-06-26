"""
If I have time, I would like to try a few different variations of the
backend implementation. This Backend dispatch class is intended to make
that easier by abstracting out the expected common interface and providing
a way to switch between them via environment configs.

This is also a convenient location to make the check_session call.
"""
from typing import Annotated

from fastapi import BackgroundTasks, Depends

from . import _celery, _process_pool
from .settings import Config, Settings, check_session

IMPLEMENTATIONS = {
    "processpool": _process_pool,
    "celery": _celery,
}


class Backend:
    def __init__(self, config: Config, tasks: BackgroundTasks):
        self.config = config
        self.tasks = tasks
        self.backend = IMPLEMENTATIONS[config.impl]

    def call(self, method: str, settings: Settings, *args, create=False) -> dict:
        ok, session_dict = check_session(settings, create=create)
        if ok:
            func = getattr(self.backend, method)
            result_dict = func(self.config, settings, *args)
            return session_dict | result_dict
        return session_dict

    def init(self, settings: Settings) -> dict:
        return self.call("init", settings, self.tasks, create=True)

    def ready(self, settings: Settings) -> dict:
        return self.call("ready", settings)

    def start(self, settings: Settings) -> dict:
        return self.call("start", settings, self.tasks)

    def status(self, settings: Settings) -> dict:
        return self.call("status", settings)

    def reset(self, settings: Settings) -> dict:
        return self.call("reset", settings)


Backend = Annotated[Backend, Depends(Backend)]  # type: ignore
