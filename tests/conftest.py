from social_forum import settings
import pytest  # type: ignore
from django.core.files import File
from pathlib import Path
import io

TEST_FILES_DIR = settings.BASE_DIR / "tests" / "files"


def wrap_file(file_path: Path) -> File:
    with open(file_path, "rb") as f:
        content = f.read()
    return File(io.BytesIO(content), name=file_path.name)


@pytest.fixture
def valid_file():
    file_path = TEST_FILES_DIR / "valid__file.jpg"
    file = wrap_file(file_path)
    return file


@pytest.fixture
def invalid_files():
    file_paths = TEST_FILES_DIR.iterdir()
    files_dict = {}

    for file_path in file_paths:
        if file_path.is_file():
            key = file_path.stem

            if key.startswith("invalid__"):
                files_dict[key] = {"image_data": wrap_file(file_path)}

    files_dict["invalid__not_image"] = {"image_data": None}
    return files_dict
