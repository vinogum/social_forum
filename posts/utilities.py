from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
import hashlib
import os
import uuid


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


# posts/post_id/images/...
# file1 file2 file3
def upload_to(instance, filename):
    post_dir = os.path.join("posts", str(instance.post_id))

    ex = filename.split(".")[-1]
    new_filename = f"{uuid.uuid1()}.{ex}"
    image_dir = os.path.join("images", new_filename)
    
    return os.path.join(post_dir, image_dir)
