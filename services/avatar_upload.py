import hashlib

import cloudinary
import cloudinary.uploader
from part_1.conf.config import settings

class UploadService:
    cloudinary.config(
        cloud_name = settings.cloudinary_name,
        api_key = settings.cloudinary_api_key,
        api_secret = settings.cloudinary_api_secret,
        secure = True
    )

    @staticmethod
    def create_avatar_name(email:str, prefix: str):
        pass
        # name = hashlib.sha256(email.encode())