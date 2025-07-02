from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
import hashlib
from social_forum import settings


def get_file_hash(file):
    if isinstance(file, InMemoryUploadedFile):
        file.seek(0)
        content = file.read()
        file.seek(0)
        return hashlib.sha256(content).hexdigest()

    elif isinstance(file, TemporaryUploadedFile):
        hash_obj = hashlib.sha256()
        file.seek(0)
        for chunk in file.chunks():
            hash_obj.update(chunk)
        file.seek(0)
        return hash_obj.hexdigest()

    return None


def upload_to(instance, filename):
    post_id = str(instance.post_id)
    ext = filename.split(".")[-1]
    new_filename = f"{instance.image_hash}.{ext}"

    relative_path = settings.UPLOAD_PATH_TEMPLATE.format(
        post_id=post_id,
        filename=new_filename,
    )
    return relative_path
