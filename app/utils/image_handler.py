# app/utils/image_handler.py
import os
from PIL import Image, ImageOps
from io import BytesIO
import shutil
from fastapi import UploadFile
from app.core.config import settings

def get_upload_path(image_size: str, filename: str, username: str) -> str:
    base_path = os.path.join(str(settings.MEDIA_PATH), str(settings.PERSONAL_IMAGE_PATH))
    path = os.path.join(base_path, username, image_size, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path

def save_image(uploaded_file: UploadFile, upload_path: str) -> str:
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return upload_path

def make_thumbnail(image_path: str, size: tuple[int, int] ) -> str:
    with Image.open(image_path) as img:
        img = ImageOps.exif_transpose(img)
        img.thumbnail(size)

        filename = os.path.basename(image_path)
        username = os.path.basename(os.path.dirname(os.path.dirname(image_path)))  # 사용자의 폴더 이름을 추출

        thumbnail_path = os.path.join(str(settings.MEDIA_PATH), str(settings.PERSONAL_IMAGE_PATH), username, "small",filename)

        os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)
        img.save(thumbnail_path, "JPEG", quality=85)
    return thumbnail_path


def delete_user_folder(username: str) -> None:
    user_folder_path = os.path.join(str(settings.MEDIA_PATH), str(settings.PERSONAL_IMAGE_PATH), username)

    try:
        if os.path.exists(user_folder_path):
            shutil.rmtree(user_folder_path)
    except Exception as e:
        print(f"Error while deleting user folder: {e}")