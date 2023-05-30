import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from database.models import User, Contact
from schemas import ContactModel, ContactResponse, UserAuthModel, UserDb, UserAuthResponse, TokenModel, RequestEmail
from services.email import send_email


class TestServicesEmail(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, email = "test@gmail.com", username = "tester01")
        self.contact = Contact(id=1)

    async def test_send_email_failed(self):
        self.assertIsNone(await send_email(self.user.email, self.user.username, 465))



if __name__ == '__main__':
    unittest.main()