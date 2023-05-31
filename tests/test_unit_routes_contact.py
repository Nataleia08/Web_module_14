import unittest
from unittest.mock import MagicMock
from datetime import datetime

from sqlalchemy.orm import Session

from database.models import User, Contact
from schemas import ContactModel, ContactResponse
from routes.contact import create_contact, read_contact, read_contacts, update_contact, update_contact_part, delete_contact, list_birthdays, search_contacts_all, search_contacts_lastname, search_contacts_firstname, search_contacts_email
from fastapi import HTTPException

from unittest.mock import MagicMock, patch

class TestRoutesContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact = Contact(id = 1, user_id = 1, email= "test888@gamil.com", first_name= "Tester99", last_name= "Testerovich99", phone_number="+380668886600", day_birthday = "2000-11-21")

    async def test_create_contact(self):
        body= ContactModel(email= "test4566@gamil.com", first_name= "Tester", last_name= "Testerovich", phone_number="+380668889900", day_birthday = "2000-11-28")
        self.session.query().filter().first.return_value = None
        result = await create_contact(body= body, current_user = self.user, db=self.session)
        self.assertEqual(result.email, "test4566@gamil.com")
        self.assertEqual(result.first_name, "Tester")
        self.assertEqual(result.last_name, "Testerovich")
        self.assertEqual(result.phone_number, "+380668889900")
        self.assertEqual(result.day_birthday, datetime(year=2000, month=11, day =28).date())
        self.assertTrue(hasattr(result, "id"))



    async def test_read_contacts(self):
        list_contacts = [Contact(user_id = 1), Contact(user_id = 1), Contact(user_id = 1)]
        self.session.query().filter().offset().limit().all.return_value = list_contacts
        result = await read_contacts(skip = 0, limit = 100, current_user = self.user, db=self.session)
        self.assertEqual(result, list_contacts)

    async def test_read_contact(self):
        self.session.query().filter().first.return_value = self.contact
        result = await read_contact(contact_id = 1, current_user = self.user, db=self.session)
        self.assertEqual(result, self.contact)

    async def test_update_contact(self):
        body = ContactModel(email= "test_test@gamil.com", first_name= "Petro02", last_name= "Ivanenko", phone_number="+380668889900", day_birthday = "1999-11-28")
        self.session.query().filter().first.return_value = self.contact
        self.session.commit.return_value = None
        result = await update_contact(body = body, contact_id = 1, current_user = self.user, db=self.session)
        self.assertEqual(result, self.contact)

    async def test_update_contact_part(self):
        self.session.query().filter().first.return_value = self.contact
        self.session.commit.return_value = None
        result = await update_contact_part(first_name="Petro02", day_birthday=datetime(year=2000, month=11, day =28).date(), contact_id=1, current_user=self.user, db=self.session)
        self.assertEqual(result, self.contact)

    async def test_delete_contact(self):
        self.session.query().filter().first.return_value = self.contact
        self.session.commit.return_value = None
        result = await delete_contact(contact_id = 1, current_user = self.user, db=self.session)
        self.assertIsNone(result)

    async def test_list_birthdays(self):
        self.session.query().filter().all.return_value = [Contact()]
        result = await list_birthdays(days = 3, current_user = self.user, db=self.session)
        self.assertEqual(len(result), 3)

    async def test_search_contacts_email(self):
        list_contacts = [Contact(user_id=1, email = "test_test@gamil.com")]
        self.session.query().filter().all.return_value = list_contacts
        result = await search_contacts_email(email = "test_test@gamil.com", current_user=self.user, db=self.session)
        self.assertEqual(len(result), len(list_contacts))

    async def test_search_contacts_firstname(self):
        list_contacts = [Contact(user_id=1, first_name= "Petro02")]
        self.session.query().filter().all.return_value = list_contacts
        result = await search_contacts_firstname(first_name= "Petro02", current_user=self.user, db=self.session)
        self.assertEqual(len(result), len(list_contacts))

    async def test_search_contacts_lastname(self):
        list_contacts = [Contact(user_id=1, last_name="Petro02")]
        self.session.query().filter().all.return_value = list_contacts
        result = await search_contacts_lastname(last_name="Petro02", current_user=self.user, db=self.session)
        self.assertEqual(len(result), len(list_contacts))

    async def test_search_contacts_all(self):
        list_contacts = [Contact(user_id=1, email = "test_test@gamil.com", last_name="Petro02", first_name= "Petro02")]
        self.session.query().filter().all.return_value = list_contacts
        result = await search_contacts_all(email = "test_test@gamil.com", first_name= "Petro02", last_name="Petro02", current_user=self.user, db=self.session)
        self.assertEqual(len(result), len(list_contacts))

    async def test_create_contact_failed(self):
        body = ContactModel(email="test4566@gamil.com", first_name="Tester", last_name="Testerovich",
                            phone_number="+380668889900", day_birthday="2000-05-28")
        with self.assertRaises(HTTPException) as sm:
            await create_contact(body=body, current_user=self.user, db=self.session)

    async def test_read_contacts_not_found(self):
        self.session.query().filter().offset().limit().all.return_value = None
        result = await read_contacts(skip=0, limit=100, current_user=User(id=344), db=self.session)
        self.assertIsNone(result)

    async def test_read_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        with self.assertRaises(HTTPException) as sm:
            await read_contact(contact_id=24587, current_user=self.user, db=self.session)

    async def test_update_contact_failed(self):
        body = ContactModel(email="test_test@gamil.com", first_name="Petro02", last_name="Ivanenko",
                            phone_number="+380668889900", day_birthday="1999-11-28")
        self.session.query().filter().first.return_value = None
        with self.assertRaises(HTTPException) as sm:
            await update_contact(body=body, contact_id=1, current_user=self.user, db=self.session)

    async def test_update_contact_part_failed(self):
        self.session.query().filter().first.return_value = None
        with self.assertRaises(HTTPException) as sm:
            await update_contact_part(first_name="Petro02",
                                           day_birthday=datetime(year=2000, month=11, day=28).date(), contact_id=1,
                                           current_user=self.user, db=self.session)

    async def test_delete_contact_failed(self):
        self.session.query().filter().first.return_value = None
        with self.assertRaises(HTTPException) as sm:
            await delete_contact(contact_id=1, current_user=self.user, db=self.session)

    async def test_list_birthdays_not_found(self):
        self.session.query().filter().all.return_value = []
        result = await list_birthdays(days=3, current_user=self.user, db=self.session)
        self.assertEqual(len(result), 0)

    async def test_search_contacts_email_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await search_contacts_email(email="test_test@gamil.com", current_user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_search_contacts_firstname_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await search_contacts_firstname(first_name="Petro02", current_user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_search_contacts_lastname_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await search_contacts_lastname(last_name="Petro02", current_user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_search_contacts_all_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await search_contacts_all(email="test_test@gamil.com", first_name="Petro02", last_name="Petro02",
                                           current_user=self.user, db=self.session)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()




