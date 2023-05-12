"""Module to store the testing models."""
from typing import Any

import pydantic


class PatchSetting(pydantic.BaseModel):
    """Describe the data structure for a patched setting."""

    name: str
    new_setting: Any
