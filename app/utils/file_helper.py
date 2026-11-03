from fastapi import UploadFile

from app.exceptions import UnsupportedFilesException


def _check_files(files: list[UploadFile], expected_file_extension: str):
    for file in files:
        if not file.filename.lower().endswith(expected_file_extension.lower()):
            # TODO: replace with dependency (magic lib shall do the job)
            raise UnsupportedFilesException(
                expected_file_extension=expected_file_extension
            )
        yield file


def check_files(files: list[UploadFile], expected_file_extension: str):
    return [file for file in _check_files(files, expected_file_extension)]


async def get_file_contents(files: list[UploadFile], expected_file_extension: str):
    return [await file.read() for file in _check_files(files, expected_file_extension)]
