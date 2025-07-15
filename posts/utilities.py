import hashlib
from social_forum import settings
from django.core.files import File


def get_file_hash(file_obj: File) -> str:
    if not isinstance(file_obj, File):
        raise TypeError(f"Expected Django File, got {type(file_obj)}!")

    hasher = hashlib.sha256()

    file_obj.seek(0)
    for chunk in file_obj.chunks():
        hasher.update(chunk)

    file_obj.seek(0)

    return hasher.hexdigest()


def upload_to(instance, filename):
    post_id = str(instance.post_id)
    ext = filename.split(".")[-1]
    new_filename = f"{instance.image_hash}.{ext}"

    relative_path = settings.UPLOAD_PATH_TEMPLATE.format(
        post_id=post_id,
        filename=new_filename,
    )
    return relative_path
