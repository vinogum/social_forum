from posts.models import User, Post, Image, Reaction
from social_forum import settings
import pytest  # type: ignore
from django.core.files import File
from pathlib import Path
import io
from posts.utilities import get_file_hash

TEST_FILES_DIR = settings.BASE_DIR / "tests" / "files"


def wrap_file(file_path: Path) -> File:
    return File(open(file_path, "rb"), name=file_path.name)


# Serializer fixtures
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


# Model fixtures
@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def post(db, user):
    post = Post.objects.create(user=user, title="title", text="text")
    try:
        yield post
    finally:
        if Post.objects.filter(id=post.id):
            post.delete()


@pytest.fixture
def image(db, post, valid_file):
    image_hash = get_file_hash(valid_file)
    image = Image.objects.create(
        post=post, image_data=valid_file, image_hash=image_hash
    )
    try:
        yield image
    finally:
        if Image.objects.filter(id=image.id).exists():
            image.delete()
