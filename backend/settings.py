from functools import cache
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel, BaseSettings
from humps import camelize


class Settings(BaseModel):
    """User-controlled settings"""

    session_id: str | None = None
    session_key: str | None = None

    number_of_messages: int = 1000
    number_of_processes: int = 4
    failure_rate: float = 0.0
    monitoring_interval: float = 1.0

    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


# TODO: Mutable module globals are not ideal. Persist in Redis instead.
current_settings = Settings()


def check_session(
    request_settings: Settings, create: bool = False
) -> tuple[bool, dict]:
    """Check if request session matches the current session.
    Return current settings if it doesn't match or None otherwise.

    The "create" argument is a way to signal that it's okay to start a
    new session if one doesn't already exist. There is a small possibility
    of a race condition in this case but probably acceptable.

    `session_id`: a unique session id generated the server during session
    initializating and is echoed back in the response if it matches the
    current session.

    `session_key`: a management key entered by the user when attempting
    to join an existing session. This value must match the `management_key`
    maintained in the config and is never echoed back in the response.
    """
    request_id = request_settings.session_id
    request_key = request_settings.session_key
    request_settings.session_key = ""  # Don't leak the management key

    # maybe start a new session
    if current_settings.session_id is None and all((create, request_id)):
        reset_settings(**request_settings.dict())

    # default result
    result_dict = current_settings.dict()

    current_id = current_settings.session_id
    management_key = config().management_key

    # request session matches current session
    if request_id == current_id:
        session_ok = True

    # management override matches all sessions
    elif current_id and management_key and request_key == management_key:
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
    message_time_mean: float = 10.0
    message_time_stdev: float = 2.0

    # Set to a non-empty string to enable management session override.
    # It's probably better to put this value in the ".env" file rather
    # than here in the code. Leave it blank to disable overrides.
    management_key: str = "some-secret-key"  # TODO: remove this value from code

    # The following enables some magic provided by pydantic to
    # collect environment overrides from a ".env" file.
    class Config:
        env_file = ".env"


@cache
def config():
    return Config()


Config = Annotated[_Config, Depends(config)]
