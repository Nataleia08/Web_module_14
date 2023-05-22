from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from part_1.database.db import get_db
from part_1.database.models import User
from part_1.repository import users as repository_users
from part_1.services.auth import auth_service
from part_1.conf.config import settings
from part_1.schemas import UserDb, UserAuthResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'UsersPhoto/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'UsersPhoto/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user

@router.post("/update_password", response_model=UserAuthResponse)
async def update_password(password: str, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    user = await repository_users.create_new_password(current_user.email, password, db)
    return {"user": user, "detail": "Your password was update!"}