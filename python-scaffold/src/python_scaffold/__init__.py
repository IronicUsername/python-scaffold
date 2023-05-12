"""Main package to handel the main logic of the app."""
from ._settings import Settings
from ._utils import LOG_LEVEL

settings = Settings()

__all__ = ["LOG_LEVEL"]
__version__ = "0.1.0"
