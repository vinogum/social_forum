from posts.serializers.image import ImageWriteSerializer


def test_valid_file(valid_file):
    image_serializer = ImageWriteSerializer(data={"image_data": valid_file})
    assert image_serializer.is_valid(), image_serializer.errors


def test_invalid_images(invalid_files):
    for error, invalid_file in invalid_files:
        image_serializer = ImageWriteSerializer(data={"image_data": invalid_file})
        assert (
            not image_serializer.is_valid()
        ), f"Failed case: {error}. Serializer error: {image_serializer.errors}"
