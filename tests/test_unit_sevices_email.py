import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from database.models import User, Contact
from schemas import ContactModel, ContactResponse, UserAuthModel, UserDb, UserAuthResponse, TokenModel, RequestEmail


class TestServicesEmail(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact = Contact(id=1)

    async def test_send_email(self):
        pass

    async def test_send_email_failed(self):
        pass



if __name__ == '__main__':
    unittest.main()