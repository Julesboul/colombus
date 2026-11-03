import pytest
from fastapi import UploadFile

from app.exceptions import UnsupportedFilesException
from app.utils.file_helper import check_files, get_file_contents


def test_check_files():
    list_of_file_names = [
        UploadFile("", filename="example1.txt"),
        UploadFile("", filename="example2.txt"),
        UploadFile("", filename="example3.txt"),
    ]

    assert check_files(list_of_file_names, "txt")


def test_check_files_fails():
    list_of_file_names = [
        UploadFile("", filename="example1.txt"),
        UploadFile("", filename="example1.json"),
        UploadFile("", filename="example1.txt"),
        UploadFile("", filename="example1.yaml"),
    ]

    with pytest.raises(UnsupportedFilesException):
        check_files(list_of_file_names, "txt")


@pytest.mark.asyncio
async def test_get_file_contents():
    with open("tests/ressources/test_file_1.txt") as file1, open(
        "tests/ressources/test_file_2.txt"
    ) as file2:
        list_of_files = [
            UploadFile(file1, filename="test_file_1.txt"),
            UploadFile(file2, filename="test_file_2.txt"),
        ]
        result = await get_file_contents(list_of_files, "txt")

    assert result == [
        "I am a testing file\n\nLine 3\n\nLast line\n",
        "Another testing file\n",
    ]


@pytest.mark.asyncio
async def test_get_file_contents_fails():
    with pytest.raises(UnsupportedFilesException):
        with open("tests/ressources/test_file_1.txt") as file1, open(
            "tests/ressources/test_file_2.txt"
        ) as file2, open("tests/ressources/test_file_3.py") as file3:
            list_of_files = [
                UploadFile(file1, filename="test_file_1.txt"),
                UploadFile(file2, filename="test_file_2.txt"),
                UploadFile(file3, filename="test_file_3.py"),
            ]
            result = await get_file_contents(list_of_files, "txt")
