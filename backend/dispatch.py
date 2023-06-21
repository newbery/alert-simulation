
"""
If I have time, I would like to try a few different variations of the
backend implementation. This dispatch module is intended to make that
easier by abstracting out the expected common interface and providing
a way to switch between them via environment configs or maybe even user
settings submitted via the frontend.
"""
from fastapi import BackgroundTasks

from . import _celery
from .settings import Config, Settings

impl = {
    "celery": _celery,
}


async def init(config: Config, settings: Settings, background: BackgroundTasks):    
    result = await impl[config.impl].init(config, settings, background)
    return result


async def ready(config: Config, settings: Settings):    
    result = await impl[config.impl].ready(config, settings)
    return result


async def start(config: Config, settings: Settings):    
    result = await impl[config.impl].start(config, settings)
    return result


async def status(config: Config):
    result = await impl[config.impl].status(config)
    return result


async def reset(config: Config):
    result = await impl[config.impl].reset(config)
    return result
