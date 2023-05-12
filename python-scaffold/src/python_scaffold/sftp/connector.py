"""Connection logic to a sftp/ssh server."""
import logging
from contextlib import contextmanager
from typing import Any, Generator

from paramiko import AuthenticationException, RSAKey, SFTPClient
from paramiko.client import AutoAddPolicy, SSHClient

_LOGGER = logging.getLogger(__name__)


@contextmanager
def get_sftp_session(
    hostname: str,
    username: str,
    password: str | None,
    private_key: RSAKey | None,
    port: int,
    disabled_algorithms: dict[str, Any] | None,
) -> Generator[SFTPClient, None, None]:
    """Get a SFTP server session.

    Parameters
    ----------
    hostname: str
        Hostname of the SFTP server that should be connected to.
    username: str
        Username of the SFTP server that should be connected to.
    password: str | None
        Password of the SFTP server that should be connected to
        If not given, the `private_key` attribute  should be filled at least.
    private_key: RSAKey | None
        Password of the SFTP server that should be connected to.
        If not given, the `password` attribute should be filled at least.
    port: int
        Port of the SFTP server that should be connected to.
    disabled_algorithms: dict[str, Any] | None
        All algorithms that should be disabled when connecting to a SFTP server.
    """
    ssh, sftp = None, None
    if ssh is None:
        ssh = SSHClient()

    # automatically add the server's host key
    ssh.set_missing_host_key_policy(AutoAddPolicy())

    try:
        ssh.connect(
            hostname=hostname,
            username=username,
            password=password,
            pkey=private_key,
            port=port,
            # NOTE: not quite sure why this is needed but it works with this
            # possible explenation: https://stackoverflow.com/a/70567773
            disabled_algorithms=disabled_algorithms,
        )
    except AuthenticationException as error:
        _LOGGER.error("Could not authenticate to server: %s", error)
        raise
    except Exception as error:  # noqa: B902
        _LOGGER.error("Could not connect to server: %s", error)
        raise

    if sftp is None:
        sftp = ssh.open_sftp()

    try:
        yield sftp
    finally:
        _LOGGER.info("Closing SFTP and SSH server connections.")
        sftp.close()
        ssh.close()
        ssh, sftp = None, None
