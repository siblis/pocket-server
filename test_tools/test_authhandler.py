from server import Application
from tornado.testing import AsyncHTTPTestCase
import json
from database_tools.db_connect import connect
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from database_tools.alchemy import CUsers



class TestAuthHandler(AsyncHTTPTestCase):
    def setUp(self):
        engine = connect('postgres')
        engine = engine.connect()

        session = sessionmaker(bind=engine)

        self.session = session()

        meta = MetaData(bind=engine)

        users = Table('users', meta,
                      Column('uid', Integer, primary_key=True),
                      Column('username', String),
                      Column('password', String),
                      Column('email', String),
                      Column('token', String))

        meta.create_all(engine)

        self.user = CUsers(username='test', password='test', email='testemail', token='token')
        self.session.add(self.user)
        self.session.commit()
        self.db = self.session
        super().setUp()

    def tearDown(self):
        self.session.execute("commit")
        self.session.execute("drop table users")

        self.session.close()

    def get_app(self):
        return Application(self.db)

    def test_authpage_get(self):
        response = self.fetch('/v1/auth/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'GET - Welcome to the AuthHandler!')

    def test_authpage_put_wrong_password(self):
        headers = {'Content-Type': 'application/json'}
        body = {
            'user': 'test',
            'password': '123TESTtestTEST123',
        }
        response = self.fetch('/v1/auth/', method='PUT', headers=headers, body=json.dumps(body).encode('utf-8'))
        resp_body = json.loads(response.body)

        self.assertEqual(resp_body['response'], '403')
        self.assertEqual(resp_body['message'], 'Incorrect password')

    def test_authpage_put_wrong_cred(self):
        headers = {'Content-Type': 'application/json'}
        body = {
            'user': 'WRONG_USER!',
            'password': 'ANDWRONGPASSTESTtestTEST',
        }
        response = self.fetch('/v1/auth/', method='PUT', headers=headers, body=json.dumps(body).encode('utf-8'))
        resp_body = json.loads(response.body)

        self.assertEqual(resp_body['response'], '403')
        self.assertEqual(resp_body['message'], 'Login or password incorrect')

    def test_authpage_put_good_cred(self):
        headers = {'Content-Type': 'application/json'}
        body = {
            'user': 'test',
            'password': 'test',
        }
        response = self.fetch('/v1/auth/', method='PUT', headers=headers, body=json.dumps(body).encode('utf-8'))
        self.assertEqual(response.code, 200)
