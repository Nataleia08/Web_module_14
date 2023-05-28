""""Module routs.users"""

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from database.db import get_db
from database.models import User
from repository import users as repository_users
from services.auth import auth_service
from configure.config import settings
from schemas import UserDb, UserAuthResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function is a GET request that returns the current user's information.
        It requires authentication, and it uses the auth_service to get the current user.

    :param current_user: User: Pass the current user to the function
    :return: The current user
    """
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The update_avatar_user function takes in a file, the current user and the database session.
    It then uploads the file to cloudinary with a public id of UsersPhoto/username. It overwrites any existing files with that name.
    The function then builds an url for that image using CloudinaryImage and returns it as src_url. The function finally updates
    the avatar field in users table for this user's email address.

    :param file: UploadFile: Upload the file to cloudinary
    :param current_user: User: Get the current user from the database
    :param db: Session: Get the database session
    :return: The user object, which is then sent to the client
    """
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
    """
    The update_password function updates the password of a user.This function will only be available to authenticated users, so we can safely assume that this parameter exists and has a value.
    If not, an HTTPException with status code 401 would have been raised before this function was called anyway!

    :param password: str: Get the password from the request body
    :param current_user: User: Get the current user from the database
    :param db: Session: Get the database session
    :return: A dict with the user and a detail message
    """
    user = await repository_users.create_new_password(current_user.email, password, db)
    return {"user": user, "detail": "Your password was update!"}