from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers, CContacts
from database_tools.db_connect import Session
import secrets

session = Session()


class UsersHandler(JsonHandler):
    def get(self):
        uid = self._token_check(session)
        if uid:
            # пока убрал запросы ко всей бд, потому как сейчас отсутствует реализация пользователя-админа
            # self._get_elements(session, CUsers)
            self._get_filtered(session, CUsers, uid)
            # TODO реализовать получение статуса пользователей из списка контактов
            self.response['users_status'] = users_status
            self.response['response'] = '200'
            self.write_json()

    def post(self):
        if self._token_check(session):
            try:
                result = session.query(CUsers.username).filter(
                    CUsers.username == self.json_data['account_name']).one_or_none()
                if result is None:
                    user = self.json_data['account_name']
                    password = self.json_data['password']
                    email = self.json_data['email']
                    token = secrets.token_hex(8)
                    user = CUsers(username=user, password=password, email=email, token=token)
                    session.add(user)
                    session.commit()
                    self.set_status(201, reason='Created')
                else:
                    message = 'Conflict'
                    self.send_error(409, message=message)

            except:
                self.send_error(400)

    def put(self):
        uid = self._token_check(session)
        if uid:
            contact = self.json_data['contact']
            contact = session.query(CUsers).filter(CUsers.email == contact).one_or_none()
            new_contact = CContacts(user_id=uid, contact=contact.uid)
            session.add(new_contact)
            session.commit()
            self.response['contact_uid'] = contact.uid
            self.response['response'] = '201'
            self.write_json()

