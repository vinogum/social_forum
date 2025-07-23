from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from posts.models import Post, Image
from posts.utilities import get_file_hash
from rest_framework.test import APIClient
from io import BytesIO
from social_forum import settings
import PIL.Image
import pytest
import base64

MAX_IMAGE_SIZE_MB = int(settings.MAX_IMAGE_SIZE_BYTES / 1024 / 1024)

USERNAME = "testuser"

PASSWORD = "testpassword"


def generate_bmp_image_file(name: str, size_mb: int) -> SimpleUploadedFile:
    if not isinstance(name, str) or len(name) == 0:
        return None

    if not isinstance(size_mb, int) or size_mb <= 0:
        return None

    target_size_bytes = size_mb * 1024 * 1024
    bytes_per_pixel = 3  # RGB = 3 bytes
    side_length = int((target_size_bytes / bytes_per_pixel) ** 0.5)

    image = PIL.Image.new("RGB", (side_length, side_length), color="white")
    img_buffer = BytesIO()
    image.save(img_buffer, format="BMP")

    img_buffer.seek(0)
    content = img_buffer.read()
    content_type = "image/bmp"
    return SimpleUploadedFile(name, content, content_type=content_type)


@pytest.fixture
def invalid_files():
    size_mb = MAX_IMAGE_SIZE_MB + 1
    filename = "invalid__too_large.bmp"

    return [
        (
            "invalid__too_large",
            generate_bmp_image_file(filename, size_mb),
        ),
        (
            "invalid__not_image",
            SimpleUploadedFile(
                "invalid__not_image.pdf",
                b"%PDF-1.4 fake content",
                content_type="application/pdf",
            ),
        ),
        ("invalid__no_file", None),
    ]


@pytest.fixture
def valid_file():
    filename = "valid__file.bmp"
    size_mb = 1
    return generate_bmp_image_file(filename, size_mb)


@pytest.fixture
def user(db):
    return User.objects.create_user(username=USERNAME, password=PASSWORD)


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


@pytest.fixture
def api_client(db, user):
    client = APIClient()

    credentials = f"{USERNAME}:{PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    client.credentials(HTTP_AUTHORIZATION=f"Basic {encoded_credentials}")
    return client
