from posts.serializers import ImageWriteSerializer, ReactionSerializer
from posts.models import ReactionType, Image, Post
from posts.utilities import get_file_hash, upload_to
import pytest  # type: ignore
import os


def test_image_write_serializer(image_data):
    data = {"image_data": image_data}
    image_serializer = ImageWriteSerializer(data=data)
    assert image_serializer.is_valid(), image_serializer.errors


def test_react_serializer():
    reacts = [ReactionType.DISLIKE, ReactionType.NONE, ReactionType.DISLIKE]
    datas = [{"type": react} for react in reacts]
    for data in datas:
        react_serializer = ReactionSerializer(data=data)
        assert True == react_serializer.is_valid()


def test_get_file_hash(image_data):
    file_hash = get_file_hash(image_data)
    assert None != file_hash


@pytest.mark.django_db
def test_upload_to(image_obj, cleanup):
    filename = image_obj.image_hash + ".jpg"
    result_file_path = upload_to(image_obj, filename)
    post_id = f"{image_obj.post_id}"
    expected_file_path = os.path.join("posts", post_id, "images", filename)
    assert result_file_path == expected_file_path
