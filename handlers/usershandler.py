from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers
from database_tools.db_connect import Session

session = Session()


class UsersHandler(JsonHandler):
    def get(self):
        if self._token_check(session, CUsers):
            users_set = session.query(CUsers).all()

            for user in users_set:
                self.write(str(user) + "\n")

    def post(self):
        if self._token_check(session, CUsers):
            try:
                result = session.query(CUsers.username).filter(
                    CUsers.username == self.json_data['account_name']).one_or_none()
                if result is None:
                    user = self.json_data['account_name']
                    password = self.json_data['password']
                    email = self.json_data['email']
                    user = CUsers(username=user, password=password, email=email, token='')
                    session.add(user)
                    session.commit()
                    self.set_status(201, reason='Created')
                else:
                    message = 'Conflict'
                    self.send_error(409, message=message)

            except:
                self.send_error(400)
