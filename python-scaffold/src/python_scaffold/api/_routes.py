from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from .. import database
from . import _utils as api_utils

router = APIRouter()


@router.get("/healthcheck")
def healthcheck_api() -> dict[str, bool]:
    """Return successfully, if the API is up and running."""
    return api_utils.healthcheck()


@router.get("/healthcheck-database")
def healthcheck_database(session: Session = Depends(database.database_session)) -> dict[str, bool]:
    """Return successfully, if the database can be reached."""
    return api_utils.healthcheck_database(session)
