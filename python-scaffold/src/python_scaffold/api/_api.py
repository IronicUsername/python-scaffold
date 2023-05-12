"""Module that describes the service's API behavior."""

import logging
from copy import deepcopy
from typing import Any

import uvicorn
from fastapi import FastAPI, Request
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware
from uvicorn.config import LOGGING_CONFIG

from .. import database, settings
from .._logging import LOG_FORMAT, configure_logging
from . import _routes as routes
from . import _utils as api_utils

_LOGGER = logging.getLogger(__name__)
_MAIN_LOGGER_CONF = None

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
@repeat_every(seconds=settings.healthcheck_interval_api)
def healthcheck_api_task() -> None:
    """Check if the API is up and running."""
    api_utils.healthcheck()


@app.on_event("startup")
@repeat_every(seconds=settings.healthcheck_interval_database)
def healthcheck_database_task() -> None:
    """Check if the database can be reached."""
    with database.get_database_session(database_dsn=settings.database_dsn) as session:
        api_utils.healthcheck_database(session=session)


@app.on_event("startup")
def startup_event() -> None:
    """Handle actions before starting the application."""
    global _MAIN_LOGGER_CONF
    if _MAIN_LOGGER_CONF is None:
        _MAIN_LOGGER_CONF = deepcopy(LOGGING_CONFIG)
        _MAIN_LOGGER_CONF["formatters"]["default"]["fmt"] = deepcopy(LOG_FORMAT)
        _MAIN_LOGGER_CONF["formatters"]["access"]["fmt"] = deepcopy(LOG_FORMAT)
    configure_logging(settings.log_level)


app.include_router(routes.router, prefix="")


@app.middleware("http")
async def log_request_types(request: Request, call_next: Any) -> Any:
    """Log the type of requests made."""
    _LOGGER.info(f"{request.method}-{request.url.path} was requested.")
    return await call_next(request)


def start() -> None:
    """Start running package."""
    configure_logging(settings.log_level)
    database.setup_database()

    uvicorn.run(
        "python_scaffold.api:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_dev_mode,
        log_config=_MAIN_LOGGER_CONF,  # https://github.com/tiangolo/fastapi/issues/1508#issuecomment-638365277
    )
