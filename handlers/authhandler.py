from handlers.jsonhandler import JsonHandler
import secrets
import hashlib
from salt import salt


class AuthHandler(JsonHandler):
    def get(self):
        self.write('GET - Welcome to the AuthHandler!')

    def create_sha(self, string):
        return hashlib.sha256(string.encode() + salt.encode()).hexdigest()

    def post(self):
        login = self.json_data['user']
        passwd = self.json_data['password']
        passwd = self.create_sha(passwd)
        query = "SELECT COUNT(login) FROM users WHERE login = '" + self.json_data['user'] + "'"
        result = self.db.execute(query)
        result = result.fetchall()
        if len(result) > 0:
            query = "SELECT password FROM users WHERE login = '" + self.json_data['user'] + "'"
            result = self.db.execute(query)
            result = result.fetchone()
            result_sha = result[0]
            
            if passwd == result_sha:
                self.write('You logged success\n')
                token = secrets.token_hex(32)
                # TODO запись token, user, pass в БД
                self.response['token'] = token
                self.response['response'] = '200'
                self.write_json()
            else:
                self.response['response'] = '403'
                self.write_json()
                self.write('Incorrect password')

        else:
            self.write('Login or password incorrect\n')
            self.response['response'] = '403'
            self.write_json()
