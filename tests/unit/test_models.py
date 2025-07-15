import pytest  # type: ignore
from pathlib import Path


@pytest.mark.django_db
def test_post_delete_custom_logic(post, image):
    file_path = Path(image.image_data.path)
    assert file_path.parent.is_dir()

    post.delete()
    assert not file_path.parent.is_dir()


@pytest.mark.django_db
def test_image_delete_custom_logic(image):
    file_path = Path(image.image_data.path)
    assert file_path.is_file()

    image.delete()
    assert not file_path.is_file()
