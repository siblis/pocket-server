from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers, CContacts
from tornado.web import RequestHandler
import secrets

from database_tools.work_with_db import ServerStorage   # Добавил класс из work_with_db.py


class UsersHandler(JsonHandler):

    def get(self, *args):
        uid = self._token_check()
        if uid:
            # пока убрал запросы ко всей бд, потому как сейчас отсутствует реализация пользователя-админа
            # self._get_elements(session, CUsers)
            self._get_filtered(self.db, CUsers, uid)
            self.response['response'] = '200'
            self.write_json()

    def post(self):
        try:
            result_email = self.db.query(CUsers.email).filter(CUsers.email == self.json_data['email']).all()
            if len(result_email) > 0:
                message = 'Conflict, mail exist'
                self.send_error(409, message=message)
        except KeyError:
            self.send_error(400, message='Bad JSON, email need')

        try:
            result = self.db.query(CUsers.username).filter(
                CUsers.username == self.json_data['account_name']).one_or_none()

            if result is None:
                user = self.json_data['account_name']
                password = self.json_data['password']
                password = self._create_sha(password)
                email = self.json_data['email']
                token = secrets.token_hex(8)
                # user = CUsers(username=user, password=password, email=email, token=token)
                # self.db.add(user)
                # self.db.commit()
                ServerStorage().add_user(username=user,
                                         password=password,
                                         email=email,
                                         token=token)   # Добавление нового юзера через work_with_db.py
                self.set_status(201, reason='Created')
                self.response['token'] = token
                self.write_json()
            else:
                message = 'Conflict, user exists'
                self.send_error(409, message=message)

        except:
            self.send_error(400, message='Bad JSON, need account_name')

    def put(self):
        uid = self._token_check()
        if uid:
            contact = self.json_data['contact']
            # contact = self.db.query(CUsers).filter(CUsers.email == contact).one_or_none()
            # new_contact = CContacts(user_id=uid, contact=contact.uid)
            # self.db.add(new_contact)
            # self.db.commit()
            ServerStorage().add_contact_list(uid=uid,
                                             contact=contact)  # Добавление в список конактов через work_with_db.py
            self.response['contact_uid'] = contact.uid
            self.response['response'] = '201'
            self.write_json()


class UsersHandlerId(UsersHandler):
    def get(self, user_id):
        uid = self._token_check()
        if uid:
            result = self.db.query(CUsers).filter(CUsers.uid == user_id).one_or_none()
            if result is None:
                self.set_status(404, 'User not found')
            else:
                self.response['uid'] = result.uid
                self.response['account_name'] = result.username
                self.response['email'] = result.email
                self.write_json()
                self.set_status(200)
