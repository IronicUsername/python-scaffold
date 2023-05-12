"""Define fixtures and plugins to be used across test files."""
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, ContextManager, Generator

import pytest
from test_python_scaffold import models as test_models
from test_python_scaffold.fixtures.sftp import SFTP_TESTING_BASE_FOLDER

from python_scaffold import settings

pytest_plugins = [
    "test_python_scaffold.fixtures.api",
    "test_python_scaffold.fixtures.database",
    "test_python_scaffold.fixtures.sftp",
]


@pytest.fixture(autouse=True)
def _set_necessary_settings(
    patch_settings: Callable[[list[test_models.PatchSetting]], ContextManager[None]]
) -> Generator[None, None, None]:
    """Set settings for testing environment."""
    settings_to_patch = [
        test_models.PatchSetting(name="external_api_base_url", new_setting="http://external.api.localhost"),
        test_models.PatchSetting(name="external_api_auth_url", new_setting="http://external.api.auth.localhost"),
        test_models.PatchSetting(name="sftp_base_working_directory", new_setting=SFTP_TESTING_BASE_FOLDER),
    ]

    with patch_settings(settings_to_patch):
        yield


@pytest.fixture(scope="session")
def project_test_root_path() -> Path:
    """Provide path to project root."""
    return Path(__file__).parent.resolve() / "test_app"


@pytest.fixture(scope="session")
def project_test_data_path() -> Path:
    """Provide path to project root."""
    return Path(__file__).parent.resolve() / "data"


@pytest.fixture()
def patch_settings() -> Callable[[list[test_models.PatchSetting]], ContextManager[None]]:
    """Set a new value in settings and reset afterwards."""

    @contextmanager
    def _patch(settings_to_patch: list[test_models.PatchSetting]) -> Generator[None, None, None]:
        for setting in settings_to_patch:
            setattr(settings, setting.name, setting.new_setting)
        yield

    return _patch
