from posts.serializers import ImageWriteSerializer, ReactionSerializer
from posts.models import ReactionType
import pytest  # type: ignore

INVALID_CASES = [
    "invalid__bad_ext",
    "invalid__no_ext",
    "invalid__too_large",
    "invalid__not_image",
]


def test_valid_file(valid_file):
    valid_data = {"image_data": valid_file}
    image_serializer = ImageWriteSerializer(data=valid_data)
    assert image_serializer.is_valid(), image_serializer.errors


@pytest.mark.parametrize("case", INVALID_CASES)
def test_invalid_images(invalid_files, case):
    data = invalid_files[case]
    serializer = ImageWriteSerializer(data=data)
    assert not serializer.is_valid()


def test_react_serializer():
    reacts = [ReactionType.DISLIKE, ReactionType.NONE, ReactionType.DISLIKE]
    datas = [{"type": react} for react in reacts]
    for data in datas:
        react_serializer = ReactionSerializer(data=data)
        assert True == react_serializer.is_valid()
