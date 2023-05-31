import unittest
from unittest.mock import MagicMock
from datetime import datetime

from sqlalchemy.orm import Session

from database.models import User, Contact
from schemas import ContactModel, ContactResponse, UserAuthModel, UserDb, UserAuthResponse, TokenModel, RequestEmail
from routes.contact import create_contact, read_contact, read_contacts
from fastapi import HTTPException

from unittest.mock import MagicMock, patch

class TestRoutesContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact = Contact(id = 1, user_id = 1)

    async def test_create_contact(self):
        body= ContactModel(email= "test4566@gamil.com", first_name= "Tester", last_name= "Testerovich", phone_number="+380668889900", day_birthday = "2000-05-28")
        self.session.query().filter().first.return_value = None
        result = await create_contact(body= body, current_user = self.user, db=self.session)
        self.assertEqual(result.email, "test4566@gamil.com")
        self.assertEqual(result.first_name, "Tester")
        self.assertEqual(result.last_name, "Testerovich")
        self.assertEqual(result.phone_number, "+380668889900")
        self.assertEqual(result.day_birthday, datetime(year=2000, month=5, day =28).date())
        self.assertTrue(hasattr(result, "id"))



    async def test_read_contacts(self):
        list_contacts = [Contact(user_id = 1), Contact(user_id = 1), Contact(user_id = 1)]
        self.session.query().filter().offset().limit().all.return_value = list_contacts
        result = await read_contacts(skip = 0, limit = 100, current_user = self.user, db=self.session)
        self.assertEqual(result, list_contacts)

    async def test_read_contact(self):
        pass

    async def test_update_contact(self):
        pass

    async def test_update_contact_part(self):
        pass

    async def test_delete_contact(self):
        pass

    async def test_list_birthdays(self):
        pass

    async def test_search_contacts_email(self):
        pass

    async def test_search_contacts_firstname(self):
        pass

    async def test_search_contacts_lastname(self):
        pass

    async def test_search_contacts_all(self):
        pass

    async def test_create_contact_failed(self):
        body = ContactModel(email="test4566@gamil.com", first_name="Tester", last_name="Testerovich",
                            phone_number="+380668889900", day_birthday="2000-05-28")
        with self.assertRaises(HTTPException) as sm:
            await create_contact(body=body, current_user=self.user, db=self.session)

    async def test_read_contacts_not_found(self):
        self.session.query().filter().offset().limit().all.return_value = None
        result = await read_contacts(skip=0, limit=100, current_user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_read_contact_failed(self):
        pass

    async def test_update_contact_failed(self):
        pass

    async def test_update_contact_part_failed(self):
        pass

    async def test_delete_contact_failed(self):
        pass

    async def test_list_birthdays_failed(self):
        pass

    async def test_search_contacts_email_failed(self):
        pass

    async def test_search_contacts_firstname_failed(self):
        pass

    async def test_search_contacts_lastname_failed(self):
        pass

    async def test_search_contacts_all_failed(self):
        pass


if __name__ == '__main__':
    unittest.main()




