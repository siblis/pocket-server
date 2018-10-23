from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers, CContacts
import secrets


class UsersHandler(JsonHandler):
    def get(self, *args):
        check_result = self._token_check()
        if check_result:
            # пока убрал запросы ко всей бд, потому как сейчас отсутствует реализация пользователя-админа
            # self._get_elements(session, CUsers)
            # self._get_filtered(self.db, CUsers, uid)
            result = self.db.query(CUsers).filter(CUsers.uid == check_result.uid).one_or_none()
            self.set_response(result)
            self.set_status(200)
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
                token_expire = self._token_expiration()
                user = CUsers(username=user, password=password, email=email, token=token, tokenexp=token_expire)
                self.db.add(user)
                self.db.commit()
                self.set_status(201, reason='Created')
                self.response['token'] = token
                self.write_json()
            else:
                message = 'Conflict, user exists'
                self.send_error(409, message=message)

        except Exception as e:
            self.send_error(400, message='Bad JSON, need account_name')

    def put(self):
        check_result = self._token_check()
        if check_result:
            contact = self.json_data['contact']
            contact = self.db.query(CUsers).filter(CUsers.email == contact).one_or_none()
            if contact is None:
                self.set_status(404, 'Contact not found')
            else:
                new_contact = CContacts(user_id=check_result.uid, contact=contact.uid)
                self.db.add(new_contact)
                self.db.commit()
                self.set_status(201, 'Created')


class UsersHandlerId(UsersHandler):
    def get(self, user_id):
        check_result = self._token_check()
        if check_result:
            result = self.db.query(CUsers).filter(CUsers.uid == user_id).one_or_none()
            if result is None:
                self.set_status(404, 'User not found')
            else:
                self.set_response(result)
                self.write_json()
                self.set_status(200)
