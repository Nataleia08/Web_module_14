""""Module routs.contact"""


from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from repository.users import birthday_in_this_year
from fastapi import FastAPI, Path, Query, Depends, HTTPException, status
from schemas import ContactResponse, ContactModel
from database.db import get_db
from database.models import User, Contact
from datetime import datetime, timedelta, date
from typing import List
from sqlalchemy import and_
from services.auth import auth_service
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body:ContactModel, current_user: User = Depends(auth_service.get_current_user), db:Session = Depends(get_db)):
    """
    The create_user function creates a new user in the database.
        It takes in a ContactModel object, which is validated by pydantic.
        The function then checks if the email address already exists, and if it does not,
        adds it to the database and returns an HTTP 201 status code with the newly created contact.

    :param body:ContactModel: Get the data from the request body
    :param current_user: User: Get the current user
    :param db:Session: Access the database
    :return: The newly created contact object
    """
    new_contact = db.query(Contact).filter(and_(Contact.email == body.email, Contact.user_id == current_user.id)).first()
    if new_contact:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "This email is exists!")
    new_contact = Contact(**body.dict(), user_id = current_user.id)
    new_contact.birthday_now = birthday_in_this_year(new_contact.day_birthday)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


@router.get("/", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = Query(default=10, le=100, ge=10), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The read_users function returns a list of users.

    :param skip: int: Skip a number of records from the database
    :param limit: int: Limit the number of results returned
    :param le: Limit the number of results returned to 100
    :param ge: Set a minimum value for the limit parameter
    :param current_user: User: Get the current user from the database
    :param db: Session: Access the database
    :return: A list of contacts
    """
    list_contacts = db.query(Contact).filter(Contact.user_id == current_user.id).offset(skip).limit(limit).all()
    return list_contacts


@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contact(contact_id: int = Path(description="The ID of the contact", ge=1), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The read_user function will return a contact with the given ID.
    If the user does not exist, it will raise an HTTP 404 error.

    :param contact_id: int: Get the id of the contact
    :param ge: Specify that the contact_id must be greater than or equal to 1
    :param current_user: User: Get the current user from the database
    :param db: Session: Access the database
    :return: A contact object, which is defined in the models
    """
    search_contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == current_user.id)).first()
    if search_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return search_contact

@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body:ContactModel, contact_id: int = Path(description="The ID of the user", ge=1), current_user: User = Depends(auth_service.get_current_user),  db: Session = Depends(get_db)):
    """
    The update_user function updates a user in the database.

    :param body:ContactModel: Get the data from the request body
    :param contact_id: int: Get the id of the contact that we want to delete
    :param ge: Specify the minimum value of the parameter
    :param current_user: User: Get the current user
    :param db: Session: Get the database session
    :return: The updated user
    """
    new_contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == current_user.id)).first()
    if new_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    new_contact.email = body.email
    new_contact.first_name = body.first_name
    new_contact.last_name = body.last_name
    new_contact.day_birthday = body.day_birthday
    new_contact.phone_number = body.phone_number
    new_contact.birthday_now = birthday_in_this_year(new_contact.day_birthday)
    db.commit()
    db.refresh(new_contact)
    return new_contact

@router.patch("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact_part(email: str = None, first_name: str = None, last_name: str = None, day_birthday: date = None, phone_number: str = None, contact_id: int = Path(description="The ID of the user", ge=1), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The update_user function updates a user in the database.

    :param email: str: Set the email of a contact
    :param first_name: str: Get the first name of the user
    :param last_name: str: Update the last name of a user
    :param day_birthday: date: Receive the date of birth from the user
    :param phone_number: str: Update the phone number of a contact
    :param contact_id: int: Find the contact in the database
    :param ge: Specify that the parameter must be greater than or equal to a given value
    :param current_user: User: Get the user that is currently logged in
    :param db: Session: Get access to the database
    :return: The updated contact
    """
    new_contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == current_user.id)).first()
    if new_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    if email:
        new_contact.email = email
    if first_name:
        new_contact.first_name = first_name
    if last_name:
        new_contact.last_name = last_name
    if day_birthday:
        new_contact.day_birthday = day_birthday
        new_contact.birthday_now = birthday_in_this_year(day_birthday)
    if phone_number:
        new_contact.phone_number = phone_number
    db.commit()
    db.refresh(new_contact)
    return new_contact


@router.delete("/{contact_id}", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def delete_contact(contact_id: int = Path(description="The ID of the user", ge=1), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The delete_user function deletes a user from the database.
        The function takes in an ID of a user and returns nothing.
        If the ID is not found, it will return 404 Not Found.

    :param contact_id: int: Get the id of the contact to be deleted
    :param ge: Make sure that the contact_id is greater than or equal to 1
    :param current_user: User: Get the current user from the auth_service
    :param db: Session: Get the database session
    :return: A 204 status code, which means that the request was successful and there is no content to return
    """
    delete_contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == current_user.id)).first()
    if delete_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    db.delete(delete_contact)
    db.commit()


@router.get("/birthdays", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def list_birthdays(days:int = 7, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The read_users function returns a list of contacts that have birthdays in the next 7 days.
        The function takes an optional parameter, days, which is set to 7 by default.
        The current_user parameter is used to get the user id from the JWT token and then filter out only those contacts that belong to this user.

    :param days:int: Set the number of days to search for contacts
    :param current_user: User: Get the current user
    :param db: Session: Create a connection to the database
    :return: A list of lists
    """
    list_contacts = []
    for i in range(days):
        new_days = (datetime.now() + timedelta(days=i)).date()
        contacts = db.query(Contact).filter(and_(Contact.birthday_now == new_days, Contact.user_id == current_user.id)).all()
        list_contacts.extend(contacts)
    return list_contacts


@router.get("/search/email", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def search_contacts_email(email: str, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The search_users function searches for a user's contacts by email.

    :param email: str: Get the email of the user we want to search for
    :param current_user: User: Get the current user
    :param db: Session: Access the database
    :return: A list of contacts
    """
    list_contacts = db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == current_user.id)).all()
    return list_contacts

@router.get("/search/first_name", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def search_contacts_firstname(first_name: str, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The search_users function searches for contacts in the database that match a given first name.

    :param first_name: str: Get the first name of the contact
    :param current_user: User: Get the current user
    :param db: Session: Connect to the database
    :return: A list of contacts that match the first name provided
    """
    list_contacts = db.query(Contact).filter(and_(Contact.first_name == first_name, Contact.user_id == current_user.id)).all()
    return list_contacts

@router.get("/search/last_name", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def search_contacts_lastname(last_name: str, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The search_users function searches for contacts by last name.
        The function takes a string as an argument and returns a list of contacts.

    :param last_name: str: Specify the last name of the contact we want to search for
    :param current_user: User: Get the current user
    :param db: Session: Get the database session
    :return: A list of contacts
    """
    list_contacts = db.query(Contact).filter(and_(Contact.last_name == last_name, Contact.user_id == current_user.id)).all()
    return list_contacts

@router.get("/search", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def search_contacts_all(email: str = None, first_name: str = None, last_name: str = None, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    """
    The search_users function searches for contacts in the database.
        It takes three optional parameters: email, first_name and last_name.
        If all three are provided, it will search for a contact with that exact combination of values.
        If only one or two are provided, it will search for any contact with those values regardless of the other(s).


    :param email: str: Search for a contact by email
    :param first_name: str: Search for a contact by first name
    :param last_name: str: Specify the last name of a contact
    :param current_user: User: Get the user who is currently logged in
    :param db: Session: Get the database session
    :return: A list of contacts
    """
    if email and first_name and last_name:
        list_contacts = db.query(Contact).filter(and_(Contact.email == email, Contact.last_name == last_name, Contact.first_name == first_name, Contact.user_id == current_user.id)).all()
    elif not email:
        if first_name and last_name:
            list_contacts = db.query(Contact).filter(and_(Contact.last_name == last_name, Contact.first_name == first_name, Contact.user_id == current_user.id)).all()
        elif first_name:
            list_contacts = db.query(Contact).filter(and_(Contact.first_name == first_name, Contact.user_id == current_user.id)).all()
        elif last_name:
            list_contacts = db.query(Contact).filter(and_(Contact.last_name == last_name, Contact.user_id == current_user.id)).all()
    else:
        if first_name:
            list_contacts = db.query(Contact).filter(and_(Contact.email == email,Contact.first_name == first_name, Contact.user_id == current_user.id)).all()
        elif last_name:
            list_contacts = db.query(Contact).filter(and_(Contact.email == email, Contact.last_name == last_name, Contact.user_id == current_user.id)).all()
        else:
            list_contacts = db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == current_user.id)).all()
    if (email is None) and (first_name is None) and (last_name is None):
        list_contacts = db.query(Contact).all()
    return list_contacts

