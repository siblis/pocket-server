from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers
from sqlalchemy import update
import secrets


class AuthHandler(JsonHandler):
    def get(self):
        self.write('GET - Welcome to the AuthHandler!')


class AuthHandlerLogin(AuthHandler):
    def post(self):
        try:
            login = str(self.json_data['account_name'])
            passwd = str(self.json_data['password'])
        except Exception as e:
            self.send_error(400, reason='Invalid fields, need login and password')
            return
        passwd = self._create_sha(passwd)
        exists = self.db.query(CUsers).filter_by(username=login).all()
        if exists:
            result_db = self.db.query(CUsers.password).filter_by(username=login).first()[0]
            if passwd == result_db:
                token = secrets.token_hex(8)
                token_exp = self._token_expiration()
                query = update(CUsers).where(CUsers.username == login).values(token=token,
                                                                              tokenexp=token_exp)
                self.db.execute(query)
                self.db.commit()
                self.set_status(200)
                self.response['token'] = token
                self.write_json()
            else:
                self.set_status(403, 'Login or password incorrect')

        else:
            self.set_status(403, reason='Login or password incorrect')


class AuthHandlerRegister(AuthHandler):
    def post(self):
        try:
            result_email = self.db.query(CUsers.email).filter(CUsers.email == str(self.json_data['email'])).all()
            if len(result_email) > 0:
                message = 'Conflict, mail exist'
                self.send_error(409, message=message)
                return
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
                user = CUsers(username=user, password=password, email=email, token=token,
                              tokenexp=token_expire)
                self.db.add(user)
                self.db.commit()
                self.set_status(201, reason='Created')
                self.response['token'] = token
                self.response['user_id'] = user.uid
                self.write_json()
            else:
                message = 'Conflict, user exists'
                self.send_error(409, message=message)

        except Exception as e:
            print(e)
            self.send_error(400, message='Bad JSON, need account_name')
