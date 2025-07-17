from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from posts.models import User, Post, Image
from posts.utilities import get_file_hash
from rest_framework.test import APIClient
from io import BytesIO
import PIL.Image
import pytest
import base64

USERNAME = "testuser"

PASSWORD = "testpassword"


def generate_image_file(
    name="image.jpg", size=(100, 100), color="white", format="JPEG"
):
    img_io = BytesIO()
    image = PIL.Image.new("RGB", size, color=color)
    image.save(img_io, format=format)
    img_io.seek(0)
    return SimpleUploadedFile(name, img_io.read(), content_type="image/jpeg")


def generate_large_image_file(name="large_image.jpg", min_size_mb=3):
    img_io = BytesIO()
    size = 1000
    while True:
        img_io.seek(0)
        img_io.truncate(0)
        image = PIL.Image.new("RGB", (size, size), color="white")
        image.save(img_io, format="JPEG", quality=95)
        if img_io.tell() >= min_size_mb * 1024 * 1024:
            break
        size += 200
    img_io.seek(0)
    return SimpleUploadedFile(name, img_io.read(), content_type="image/jpeg")


@pytest.fixture
def invalid_files():
    return [
        (
            "invalid__too_large",
            generate_large_image_file("invalid__too_large.jpg", min_size_mb=3),
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
    return generate_image_file("valid__file.jpg", size=(10, 10))


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
