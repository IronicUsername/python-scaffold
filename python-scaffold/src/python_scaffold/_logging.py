"""Module that handles logger setup."""
import logging

from pythonjsonlogger import jsonlogger

from . import LOG_LEVEL

# Adapted from https://docs.python.org/3.9/library/logging.html#logrecord-attributes
LOG_FORMAT = "%(asctime)%(levelname)%(message)%(name)"
LOG_FORMATTER = jsonlogger.JsonFormatter(LOG_FORMAT)  # type: ignore[no-untyped-call]


def _raise_test_plugin_logging_level_to_error() -> None:
    """Raise the default test plugin logging level to `ERROR`.

    Some test plugin loggers have a default logging level of `debug`. This severely hinders
    debug-ability of code, since test plugin logs will swamp `stdout` if any test fails.

    To resolve this, we raise the default logging level of test plugin to `ERROR` here.

    """
    logging.getLogger("flake8").setLevel(logging.ERROR)
    logging.getLogger("filelock").setLevel(logging.ERROR)


def configure_logging(log_level: str) -> None:
    """Configure the project logging.

    This function configures the project logging, all loggers instantiated after calling
    this function will inherit this configuration.

    This function should be called at the very start of running the application, else loggers
    with different configurations may be instantiated.

    """
    _raise_test_plugin_logging_level_to_error()

    log_handler = logging.StreamHandler()
    log_handler.setFormatter(LOG_FORMATTER)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(str(LOG_LEVEL[log_level]))

    # add logger
    root_logger.addHandler(log_handler)

    # set our logger to same level as main application running
    logging.getLogger("uvicorn").setLevel(log_level)
    logging.getLogger("fastapi").setLevel(log_level)

    logging.info("Logger setup successfully.")
