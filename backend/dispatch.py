"""
If I have time, I would like to try a few different variations of the
backend implementation. This Backend dispatch class is intended to make
that easier by abstracting out the expected common interface and providing
a way to switch between them via environment configs.
"""
from typing import Annotated

from fastapi import BackgroundTasks, Depends

from . import _celery, _process_pool
from .settings import Config, Settings

IMPLEMENTATIONS = {
    "processpool": _process_pool,
    "celery": _celery,
}


class Backend:
    def __init__(self, config: Config, background: BackgroundTasks):
        self.config = config
        self.background = background
        self.backend = IMPLEMENTATIONS[config.impl]

    def init(self, settings: Settings) -> bool:
        return self.backend.init(self.config, settings, self.background)

    def ready(self, settings: Settings) -> dict:
        return self.backend.ready(self.config, settings)

    def start(self, settings: Settings) -> None:
        self.backend.start(self.config, settings, self.background)

    def status(self) -> dict:
        return self.backend.status(self.config)

    def reset(self) -> None:
        self.backend.reset(self.config)


Backend = Annotated[Backend, Depends(Backend)]  # type: ignore
