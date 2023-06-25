from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, BaseSettings
from humps import camelize


class Settings(BaseModel):
    """User-controlled settings"""
    
    session_id: str | None = None
    session_name: str = "anon"
    session_secret: str = "some-key-phrase"

    number_of_messages: int = 1000
    number_of_processes: int = 4
    failure_rate: float = 0.0
    monitoring_interval: float = 1.0

    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


# TODO: Mutable module globals are not ideal. Persist in Redis instead.
current_settings = Settings()


def check_session(settings: Settings, create: bool = False) -> tuple[bool, dict]:
    """Check if request session matches the current session.
    Return current settings if it doesn't match or None otherwise.

    The "create" argument is a way to signal that it's okay to start a
    new session if one doesn't already exist. There is a small possibility
    of a race condition in this case but probably acceptable.
    
    `session_id`: a unique session id generated in the browser and
    echoed back in the response if it matches the current session.

    `session_name`: a public name for the current session which is echoed
    back in the response.

    `session_secret`: a private secret entered by the user at the beginning
    of a session to protect their session. The secret is never echoed back
    in the response however it's not encrypted or hashed so don't use secrets
    you wouldn't want other people to see. 
    
    An optional `management_secret` can be used to override the private secret
    validation. See Config class in this module.

    """
    request_id = settings.session_id
    request_name = settings.session_name
    request_secret = settings.session_secret

    # maybe start a new session
    if current_settings.session_id is None and all((create, request_id, request_name, request_secret)):
        reset_settings(**settings.dict())
        result = current_settings.dict()

    current_id = current_settings.session_id
    current_name = current_settings.session_name
    current_secret = current_settings.session_secret
    management_secret = config().management_secret
    
    # default result
    result_dict = current_settings.dict()
    del result_dict["session_secret"]  # Don't leak this

    # request session matches current session
    if (request_id, request_name, request_secret) == (current_id, current_name, current_secret):
        session_ok = True

    # management override matches all sessions
    elif current_id and management_secret and request_secret == management_secret:
        result_dict["management_override"] = True
        session_ok = True

    # can't join current session
    else:
        session_ok = False

    return session_ok, result_dict


def reset_settings(**kwargs) -> None:
    global current_settings
    current_settings = Settings(**kwargs)


class _Config(BaseSettings):
    """Application configuration"""

    # Needed for dispatch module (processpool or celery)
    impl: str = "processpool"

    # We're using standard defaults for now so these url settings
    # are just unused placeholders for now.
    redis_url: str = "redis://redis:6379"
    rabbitmq_url: str = "redis://redis:6379"

    # The time it takes to send messages should be distributed as follows.
    # These values are in seconds.
    message_time_mean: float = 5.0
    message_time_stdev: float = 2.0
    
    # Set to a non-empty string to enable management session override.
    # It's probably best to put this value in the ".env" file rather
    # than here in the code.
    management_secret: str = ""

    # The following enables some magic provided by pydantic to
    # collect environment overrides from a ".env" file.
    class Config:
        env_file = ".env"


@lru_cache()
def config():
    return Config()


Config = Annotated[_Config, Depends(config)]
