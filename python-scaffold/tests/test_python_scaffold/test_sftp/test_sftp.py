from typing import Any, Callable
from uuid import uuid4

from paramiko import SFTPClient


def test_get_sftp_session_successful(
    sftp_session: SFTPClient, upload_data_to_sftp: Callable[[SFTPClient, list[dict[str, Any]]], list[dict[str, Any]]]
) -> None:

    test_data = upload_data_to_sftp(
        sftp_session,
        [
            {"filename": "invalid.file", "filedata": "Id;Name\n1;Tommy Iommi "},
            {"filename": "invalid.csv", "filedata": "Id;Name\n1;Thomas Mausbach"},
            {"filename": "test.csv", "filedata": "Id;Name\n1;John Dong"},
            {"filename": "test1.csv", "filedata": "Id;Name\n2;Sepp Meier"},
            {"filename": "test_1.csv", "filedata": "Id;Name\n2;Kuschrim Depp"},
            {"filename": "test-1.csv", "filedata": "Id;Name\n2;Norbert Bert"},
            {"filename": f"test_{uuid4()}.csv", "filedata": "Id;Name\n2;Rick Sanchez"},
            {"filename": "1test.csv", "filedata": "Id;Name\n2;Al Cisneros"},
            {"filename": "1_test.csv", "filedata": "Id;Name\n2;Matt Pike"},
            {"filename": "1-test.csv", "filedata": "Id;Name\n2;Johnny Sins"},
            {"filename": f"{uuid4()}_test.csv", "filedata": "Id;Name\n2;Nick Gurr"},
        ],
    )
    assert len(sftp_session.listdir()) == len(test_data)
