import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from database.models import User, Contact
from schemas import ContactModel, ContactResponse, UserAuthModel, UserDb, UserAuthResponse, TokenModel, RequestEmail
from routes.contact import create_contact

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

    async def test_read_contacts(self):
        pass

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
        pass

    async def test_read_contacts_failed(self):
        pass

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




