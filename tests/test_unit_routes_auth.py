import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, status, Security, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from database.models import User, Contact
from schemas import ContactModel, ContactResponse, UserAuthModel, UserDb, UserAuthResponse, TokenModel, RequestEmail
from routes.auth import signup, login, confirmed_email, refresh_token, request_email

class TestRoutsAuth(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.contact = Contact(id = 1)

    async def test_signup(self):
        body = UserAuthModel(username = "tester", email= "test9@gmail.com", password= "1234567")
        background_tasks = MagicMock(spec = BackgroundTasks)
        requset = MagicMock(spec = Request)
        self.session.query().filter().first.return_value = None
        result = await signup(body = body, background_tasks = background_tasks, request = requset, db=self.session)
        self.assertTrue(hasattr(result["user"], "id"))
        self.assertEqual(result["user"].username, body.username)
        self.assertEqual(result["user"].email, body.email)
        self.assertEqual(result["user"].password, body.password)

    async def test_signup_failed(self):
        body = UserAuthModel(username="tester", email="test9@gmail.com", password="1234567")
        background_tasks = MagicMock(spec=BackgroundTasks)
        requset = MagicMock(spec=Request)
        with self.assertRaises(HTTPException) as cm:
            await signup(body=body, background_tasks=background_tasks, request=requset, db=self.session)

    async def test_login_failed(self):
        body_oauth = MagicMock(spec=OAuth2PasswordRequestForm)
        body_oauth.username = "tester"
        body_oauth.password = "1234567"
        new_user = User(username="tester", email="test9@gmail.com", password="1234567")
        self.session.query().filter().first.return_value = new_user
        with self.assertRaises(HTTPException) as cm:
            await login(body=body_oauth, db=self.session)


    async def test_refresh_token(self):
        pass

    async def test_refresh_token_failed(self):
        pass

    async def test_request_email(self):
        body = RequestEmail(email="test9@gmail.com")
        background_tasks = MagicMock(spec=BackgroundTasks)
        requset = MagicMock(spec=Request)
        new_user = User(email="test9@gmail.com")
        self.session.query().filter().first.return_value = new_user
        result = await request_email(body = body, background_tasks = background_tasks, request = requset, db=self.session)
        self.assertEqual(result["message"], "Check your email for confirmation.")


    async def test_request_email_failed(self):
        body = RequestEmail(email="test9@gmail.com")
        background_tasks = MagicMock(spec=BackgroundTasks)
        requset = MagicMock(spec=Request)
        new_user = User(email="test9@gmail.com", confirmed_email = True)
        self.session.query().filter().first.return_value = new_user
        result = await request_email(body=body, background_tasks=background_tasks, request=requset, db=self.session)
        self.assertEqual(result["message"], "Your email is already confirmed")



if __name__ == '__main__':
    unittest.main()