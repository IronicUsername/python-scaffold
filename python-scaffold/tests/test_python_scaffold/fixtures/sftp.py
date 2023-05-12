"""SSH related fixtures."""
import os
import stat
from contextlib import contextmanager
from copy import deepcopy
from typing import Any, Callable, ContextManager, Generator, Iterator
from uuid import uuid4

import pytest
from paramiko import SFTPClient
from paramiko.client import AutoAddPolicy, SSHClient

from python_scaffold import settings

_SFTP_BASE_FOLDER = f"/home/{settings.sftp_username.get_secret_value()}"
SFTP_TESTING_BASE_FOLDER = f"{_SFTP_BASE_FOLDER}/tests"


@pytest.fixture(scope="session")
def sftp_session_provider() -> Callable[[], ContextManager[SFTPClient]]:
    """SFTP session provider."""

    @contextmanager
    def _get_session() -> Generator[SFTPClient, None, None]:
        def _is_directory(sftp_client: SFTPClient, sftp_server_path: str) -> bool:
            try:
                return stat.S_ISDIR(sftp_client.stat(sftp_server_path).st_mode or 0)
            except IOError:
                return False

        def _remove_data(sftp_client: SFTPClient, sftp_server_path: str) -> None:
            sftp_files = sftp_client.listdir(path=sftp_server_path)

            for sftp_file in sftp_files:
                filepath = os.path.join(sftp_server_path, sftp_file)
                if _is_directory(sftp_client=sftp_client, sftp_server_path=filepath):
                    _remove_data(sftp_client=sftp_client, sftp_server_path=filepath)
                else:
                    sftp_client.remove(filepath)

            # NOTE: edgecase - it we do not want (and can) delete the users home directory
            if sftp_server_path != sftp_client.normalize("."):
                sftp_client.rmdir(sftp_server_path)

        def _setup_dev_environment(sftp_client: SFTPClient) -> None:
            sftp_client.mkdir(SFTP_TESTING_BASE_FOLDER)

        try:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(
                hostname=settings.sftp_hostname,
                username=settings.sftp_username.get_secret_value(),
                password=settings.sftp_password.get_secret_value(),
                port=settings.sftp_port,
            )
        except Exception:  # noqa: B902
            pytest.fail("No SSH server available.")

        sftp = ssh.open_sftp()

        sftp.chdir(_SFTP_BASE_FOLDER)  # reset "cursor" to home directory / default entry point
        _remove_data(sftp_client=sftp, sftp_server_path=sftp.normalize("."))
        _setup_dev_environment(sftp_client=sftp)
        yield sftp
        _remove_data(sftp_client=sftp, sftp_server_path=sftp.normalize("."))

        sftp.close()
        ssh.close()

    return _get_session


@pytest.fixture()
def sftp_session(sftp_session_provider: Callable[[], ContextManager[SFTPClient]]) -> Iterator[SFTPClient]:
    """Create a clean sftp server session."""
    with sftp_session_provider() as session:
        yield session


@pytest.fixture()
def upload_data_to_sftp() -> Callable[[SFTPClient, list[dict[str, Any]]], list[dict[str, Any]]]:
    """Upload a batch of data to the sftp server."""

    def _upload_data_to_sftp(sftp_client: SFTPClient, sftp_file_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        all_created_paths = deepcopy(sftp_file_data)
        sftp_client.chdir(SFTP_TESTING_BASE_FOLDER)

        for sftp_file in all_created_paths:
            file_path = f"{sftp_client.getcwd()}/{sftp_file.get('filename', f'{uuid4()}.csv')}"

            with sftp_client.open(file_path, "w") as new_sftp_file:
                new_sftp_file.write(sftp_file.get("filedata", "Test file"))  # type: ignore
            sftp_file["sftp_path"] = file_path

        return all_created_paths

    return _upload_data_to_sftp
