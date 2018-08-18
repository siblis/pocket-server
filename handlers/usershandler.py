from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers
from database_tools.db_connect import Session
import secrets

session = Session()


class UsersHandler(JsonHandler):
    def get(self):
        if self._token_check(session):
            self._get_elements(session, CUsers)

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
