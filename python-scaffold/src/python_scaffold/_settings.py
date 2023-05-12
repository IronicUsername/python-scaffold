import logging
import sys
from functools import lru_cache

import pydantic

from ._utils import LOG_LEVEL

_LOGGER = logging.getLogger(__name__)


class Settings(pydantic.BaseSettings):
    """Parse environment variables to optionally validate them."""

    version: str = "0.1.0"

    is_dev_mode: bool = bool(sys.flags.dev_mode)
    log_level: str = str(LOG_LEVEL.INFO)

    # api
    host: str = "0.0.0.0"
    port: int = 8001
    cors_allowed_origins: list[pydantic.AnyHttpUrl] = []
    external_api_auth_url: pydantic.AnyHttpUrl
    external_api_base_url: pydantic.AnyHttpUrl

    healthcheck_interval_api: int = 2
    healthcheck_interval_database: int = 2

    # database
    database_dsn: pydantic.PostgresDsn | str = pydantic.parse_obj_as(
        pydantic.PostgresDsn, "postgresql://postgres:postgres@localhost:5432/postgres"
    )
    database_schema_name: str = "python_scaffold_test"

    # sftp
    sftp_hostname: str
    sftp_port: int
    sftp_username: pydantic.SecretStr
    sftp_password: pydantic.SecretStr | None
    sftp_pkey: pydantic.SecretStr | None
    sftp_base_working_directory: str = ""

    class Config:
        """Config of the app settings."""

        env_file = ".env"
        env_file_encoding = "utf-8"

    @pydantic.validator("log_level")
    def check_log_level_name(cls, log_level: str) -> str:
        """Assert that the given log level exists."""
        _LOGGER.debug(f"Checking given loglevel '{log_level}'.")

        existing_log_levels = list(logging._nameToLevel)
        if log_level.upper() not in existing_log_levels:
            raise ValueError(f'Must provide an existing log level: {", ".join(existing_log_levels)}')
        return log_level

    @pydantic.validator("cors_allowed_origins")
    def check_cors_allowed_origins(cls, cors_allowed_origins: list[pydantic.AnyHttpUrl]) -> list[str]:
        """Assert that the given CORS configuration is valid.

        In development/testing, we use `*` per default.

        In production, CORS must not contain `*` (checked via `AnyHttpUrl` type).

        """
        if bool(sys.flags.dev_mode):
            return ["*"]

        if len(cors_allowed_origins) == 0:
            _LOGGER.warning("No CORS whatsoever allowed at the moment!! " "Set `CORS_ALLOWED_ORIGINS` to change this")

        return [str(origin) for origin in cors_allowed_origins]

    @classmethod
    @lru_cache(1)
    def get(cls) -> "Settings":
        """Get a cached Settings file."""
        return cls()
