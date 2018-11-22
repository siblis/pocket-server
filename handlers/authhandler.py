from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers, CUserStatus
from sqlalchemy import update
import secrets


class AuthHandler(JsonHandler):
    def get(self):
        self.write('GET - Welcome to the AuthHandler!')

    def put(self):
        login = self.json_data['account_name']
        passwd = self.json_data['password']
        passwd = self._create_sha(passwd)
        exists = self.db.query(CUsers).filter_by(username=login).all()
        if exists:
            result_db = self.db.query(CUsers.password).filter_by(username=login).first()[0]
            if passwd == result_db:
                token = secrets.token_hex(8)
                token_exp = self._token_expiration()
                status = self.db.query(CUserStatus).filter(CUserStatus.status_name == 'online').first()
                query = update(CUsers).where(CUsers.username == login).values(token=token,
                                                                              tokenexp=token_exp,
                                                                              status_id=status.usid)
                self.db.execute(query)
                self.db.commit()
                self.set_status(200)
                self.response['token'] = token
                self.write_json()
            else:
                self.set_status(403, 'Incorrect password')

        else:
            self.set_status(403, reason='Login or password incorrect')
