from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from posts.models import Image, Post
from social_forum import settings
from posts.utilities import get_file_hash
import pytest  # type: ignore
import io
import os

FILENAME = "image_to_test.jpg"

IMAGE_DIR = "test"

IMAGE_PATH = os.path.join(settings.MEDIA_ROOT, IMAGE_DIR, FILENAME)


@pytest.fixture
def image_data():
    if not os.path.exists(IMAGE_PATH):
        return None

    with open(IMAGE_PATH, "rb") as f:
        file_content = f.read()

    file_obj = io.BytesIO(file_content)
    file_obj.name = FILENAME

    return InMemoryUploadedFile(
        file=file_obj,
        field_name="image",
        name=FILENAME,
        content_type="image/jpeg",
        size=file_obj.getbuffer().nbytes,
        charset=None,
    )


@pytest.fixture
def user_obj(db):
    return User.objects.create_user(username="testuser", password="testuser")


@pytest.fixture
def post_obj(db, user_obj):
    return Post.objects.create(user=user_obj, title="title", text="text")


@pytest.fixture
def image_obj(db, post_obj, image_data):
    image_hash = get_file_hash(image_data)
    return Image.objects.create(
        post=post_obj, image_data=image_data, image_hash=image_hash
    )


@pytest.fixture
def cleanup(post_obj):
    yield
    post_obj.delete()
