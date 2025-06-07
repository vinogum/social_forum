from social_forum import settings
import os


def upload_to(instance, filename):
    # Path where the file will be uploaded
    # Example: user_<user_id>/post_<post_id>/<filename>
    return f"user_{instance.user.id}/post_{instance.id}/{filename}"
