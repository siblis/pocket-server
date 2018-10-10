from server import Application
from tornado.testing import AsyncHTTPTestCase
import json
from database_tools.db_connect import connect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData
from database_tools.alchemy import CUsers


class TestUsersHandler(AsyncHTTPTestCase):
    def setUp(self):
        engine = connect('postgres')
        engine = engine.connect()

        Session = sessionmaker(bind=engine)

        self.session = Session()

        meta = MetaData(bind=engine)

        users = Table('users', meta,
                      Column('uid', Integer, primary_key=True),
                      Column('username', String),
                      Column('password', String),
                      Column('email', String),
                      Column('token', String))

        meta.create_all(engine)

        self.test_user = CUsers(username='test', password='test', email='testemail', token='token')
        self.session.add(self.test_user)
        self.session.commit()

        self.exists_user = CUsers(username='exists_user', password='test123', email='testemail123', token='token2')
        self.session.add(self.exists_user)
        self.session.commit()

        self.db = self.session
        super().setUp()

    def get_app(self):
        return Application(self.db)

    def tearDown(self):
        self.session.execute("commit")
        self.session.execute("drop table users")
        self.session.close()

    def test_userspage_get_unauthorized(self):
        response = self.fetch('/v1/users/')
        self.assertEqual(response.code, 401)

    def test_userspage_get_authorized(self):
        headers = {'Content-Type': 'application/json', 'token': 'token'}
        response = self.fetch('/v1/users/', headers=headers)
        self.assertEqual(response.code, 200)

    def test_userpage_post_conflict(self):
        headers = {'Content-Type': 'application/json'}
        body = {
            "account_name": "exists_user",
            "password": "testpass",
            "email": "testemail"
        }
        response = self.fetch('/v1/users/', headers=headers, method='POST', body=json.dumps(body).encode('utf-8'))
        self.assertEqual(response.code, 409)

    def test_userpage_post_bad_request(self):
        headers = {'Content-Type': 'application/json'}
        body = {
            "login": "new_user",
            "pass": "testpass",
        }
        response = self.fetch('/v1/users/', headers=headers, method='POST', body=json.dumps(body).encode('utf-8'))
        self.assertEqual(response.code, 400)

    def test_userpage_post_success(self):
        headers = {'Content-Type': 'application/json'}
        body = {
            "account_name": "succes_test",
            "password": "newtestpass",
            "email": "newtestemail"
        }
        response = self.fetch('/v1/users/', headers=headers, method='POST', body=json.dumps(body).encode('utf-8'))
        self.assertEqual(response.code, 201)
