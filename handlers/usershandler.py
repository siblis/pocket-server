from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers, CContacts, CUserStatus
import secrets


# запросы к БД
# Запросы для получение данных пользователя через email
def get_user_data_by_mail(session, user_mail):
    return session.query(CUsers).filter(CUsers.email == user_mail).one_or_none()


def get_user_data_by_nickname(session, username):
    return session.query(CUsers).filter(CUsers.username.like(f"%{username}%")).all()
    # return session.query(CUsers).filter(CUsers.username == username).limit(20)


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
                status = self.db.query(CUserStatus).filter(CUserStatus.status_name == 'not confirm').first()
                user = CUsers(username=user, password=password, email=email, token=token,
                              tokenexp=token_expire, status_id=status.usid)
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
            try:
                user_uid = self.json_data['uid']
                user = self.db.query(CUsers).filter(CUsers.uid == user_uid).one_or_none()  # first or default
                if user is None:
                    self.set_status(404, 'User not found')
                else:

                    status_id = user.status_id
                    user = self.json_data['account_name']
                    password = self.json_data['password']
                    password = self._create_sha(password)
                    email = self.json_data['email']
                    token = secrets.token_hex(8)
                    token_expire = self._token_expiration()
                    user = CUsers(username=user, password=password, email=email, token=token,
                                  tokenexp=token_expire, status_id=status_id)  # это мы создали, а как апдейтить?!

                    self.db.query(CUsers).filter(CUsers.uid == user_uid).update(
                        {'username': user, 'password': password, 'email': email}, synchronize_session='evaluate'
                    )

                    self.db.commit()

                    self.set_status(201, reason='Updated')  # статус какой?

                    self.response['token'] = token
                    self.write_json()
            except Exception as e:
                self.send_error(400, message='Bad JSON, wrong data')


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


class UsersHandlerMail(UsersHandler):
    def get(self, user_mail):
        check_result = self._token_check()
        if check_result:
            try:
                result = get_user_data_by_mail(self.db, user_mail)
            except:
                self.send_error(500, message='Internal Server Error')
            else:
                if result is None:
                    self.set_status(404, 'User not found')
                else:
                    self.response['uid'] = result.uid
                    self.response['account_name'] = result.username
                    self.response['email'] = result.email
                    self.write_json()
                    self.set_status(200)


class UsersHandlerSearchByNickname(UsersHandler):
    def get(self, username):
        check_result = self._token_check()
        if check_result:
            try:
                result = get_user_data_by_nickname(self.db, username)
            except:
                self.send_error(500, message='Internal Server Error')
            else:
                if result is None:
                    self.set_status(404, 'User not found')
                else:
                    for user in result:
                        json_mess = {
                                    'account_name': user.username,
                                    'email': user.email
                        }
                        self.response[user.uid] = json_mess
                    self.write_json()
                    self.set_status(200)
