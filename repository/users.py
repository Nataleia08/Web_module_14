""""Module of action with DB"""


from datetime import datetime
from libgravatar import Gravatar
from sqlalchemy.orm import Session

from database.models import User
from schemas import UserAuthModel

def birthday_in_this_year(date_birthday: datetime):
    """
    The birthday_in_this_year function takes a datetime object as an argument and returns the date of that person's birthday in 2023.

    :param date_birthday: datetime: Contact's birthday
    :return: The birthday in the year 2023
    """
    new_date = datetime(year=2023, month=date_birthday.month, day=date_birthday.day).date()
    return new_date

async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists,
    it will return None.

    :param email: str: Email of the user
    :param db: Session: Access to database
    :return: A user object if the email exists in the database, or none otherwise
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserAuthModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserAuthModel): The UserAuthModel object containing the data to be used for creating a new user.
            db (Session): The SQLAlchemy Session object that will be used to create and commit the new user record.

    :param body: UserAuthModel: The request body to the function
    :param db: Session: Access to database
    :return: A user object
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Get the user's id
    :param token: str | None: Refresh token
    :param db: Session: Access to database
    :return: None
    """
    user.refresh_token = token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed_email field of the user with that email to True.


    :param email: str: Email of the user
    :param db: Session: Access to database
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed_email = True
    db.commit()

async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.

    :param email: Email of the user
    :param url: str: Url of the avatar
    :param db: Session: Access to database
    :return: The updated user
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user

async def create_new_password(email, password, url: str, db: Session):
    """
    The create_new_password function creates a new password for the user.
        Args:
            email (str): The email of the user to create a new password for.
            password (str): The new password to be created.

    :param email: Email of user
    :param password: Create a new password for the user
    :param url: str: Create a new password for the user
    :param db: Session: Access to database
    :return: A user object
    """
    user = await get_user_by_email(email, db)
    user.password = password
    db.commit()
    return user
