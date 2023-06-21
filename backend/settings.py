
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, BaseSettings
from humps import camelize


class Settings(BaseModel):
    """User-controlled settings"""
    number_of_messages: int = 1000
    number_of_processes: int = 10
    failure_rate: float = 0.0
    monitoring_interval: float = 5

    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class _Config(BaseSettings):
    """Application configuration"""
    
    # Needed for dispatch module
    impl: str = "celery"

    # We're using standard defaults for now so these url settings
    # are just unused placeholders for now.
    redis_url: str = "redis://redis:6379"
    rabbitmq_url: str = "redis://redis:6379"
    
    # The time it takes to send messages should be distributed as follows.
    # These values are in seconds.
    message_time_mean: float = 5.0
    message_time_stdev: float = 2.0

    # The number of messages to process in each batch
    # (this is ignored in the "all in one" case)
    batch_size: int = 1

    # The following enables some magic provided by pydantic to
    # collect environment overrides from a ".env" file.
    class Config:
        env_file = ".env"


@lru_cache()
def config():
    return Config()


Config = Annotated[_Config, Depends(config)]
