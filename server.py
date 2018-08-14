import tornado.web
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import json
from sqlalchemy import create_engine
import hashlib, secrets
from tornado.options import define, options

define("port", default=8888, help="start on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        self.webSocketsPool = []
        handlers = [
            (r'/v1', MainHandler),
            (r'/v1/auth', AuthHandler),
            (r'/v1/users', UsersHandler),
            (r'/v1/users/add', UserAddHandler),
            (r'/v1/wsocket/', WebSocketHandler),
            (r'/v1/chats/', ChatsHandler),
            (r'/v1/test/', TestHandler)

        ]
        settings = dict()
        tornado.web.Application.__init__(self, handlers, **settings)

        # bd connection
        self.db = create_engine('postgresql://postgres:123@localhost:5432/messengerbase')
        # self.db = "connection to db"


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class MainHandler(BaseHandler):
    def get(self):
        result = "Welcome to server"

        self.write(str(result))


class JsonHandler(BaseHandler):
    def prepare(self):
        if self.request.body:
            try:
                # print(self.request.body)
                arg = self.request.body
                arg = arg.decode()
                arg = arg.replace("'", '"')
                self.json_data = tornado.escape.json_decode(arg)
            except ValueError:
                message = 'Unable to parse JSON.'
                self.send_error(400, message=message)  # Bad Request

        self.response = dict()

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405:
                kwargs['message'] = 'Invalid HTTP method.'
            else:
                kwargs['message'] = 'Unknown error.'

        self.response = kwargs
        self.write_json()

    def write_json(self):
        output = json.dumps(self.response)
        self.write(output)


class TestHandler(JsonHandler):
    def get(self):
        incoming_arg_1 = self.json_data['token']
        incoming_arg_2 = self.json_data['name']

        print(incoming_arg_1)
        print(incoming_arg_2)

        self.response['response'] = 'OK'
        self.response['func'] = '12345'

        self.write_json()


class AuthHandler(JsonHandler):
    def get(self):
        self.write('GET - Welcome to the AuthHandler!')

    def post(self):
        login = self.json_data['user']
        passwd = self.json_data['password']

        credpass = hashlib.md5(passwd.encode('utf8')).hexdigest()
        if login == 'admin' and credpass == hashlib.md5('admin'.encode('utf8')).hexdigest():
            self.write('You logged success\n')
            token = secrets.token_hex(32)
            # запись tkn, user, pass в БД
            # отправка клиенту
            self.response['token'] = token
            self.response['response'] = '200'
            self.write_json()
        else:
            self.write('Login or password incorrect\n')
            self.response['response'] = '403'
            self.write_json()


class UsersHandler(JsonHandler):
    def get(self):
        # token сверить с БД
        # если токен есть вывести список всех юзеров
        result_set = self.db.execute("SELECT * FROM users")
        for r in result_set:
            self.write(str(r) + "\n")
        # self.write(str(result_set))
        # print(result_set)


class UserAddHandler(JsonHandler):
    def post(self):
        # add user to db
        # token сверить
        # если токен верный проверить данные
        # если данных нет в БД, записать, иначе выдать ошибку

        if self.json_data:
            query = "SELECT * FROM users WHERE token = '" + self.json_data['token'] + "'"
            result = self.db.execute(query)
            result_len = len(result.fetchall())
            # print(result_len)
            if result_len > 0:
                print('token ok')
                print('next check data')
                query = "SELECT * FROM users WHERE login = '" + self.json_data['user'] + "'"
                result = self.db.execute(query)

                result_len = len(result.fetchall())
                if result_len > 0:
                    print('error add, write exists')
                else:
                    print('create new str in bd')
                    self.response['response'] = '200'
                    self.write_json()
            else:
                # to log
                print('token wrong')
                self.response['message'] = 'token is wrong'
                self.response['response'] = '403'
                self.write_json()


class ChatsHandler(BaseHandler):
    def get(self):
        # token сверить с БД
        # если токен есть вывести список всех чатов
        # result_set = self.db.execute("SELECT * FROM chats")
        # self.write(str(result_set))
        pass

    def post(self):
        # create new chat
        # token сверить
        # если токен верный проверить данные
        # если данных нет в БД, записать, иначе выдать ошибку
        pass


# open websocket and retrieve msg
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")
        self.application.webSocketsPool.append(self)

    def on_message(self, message):
        self.write_message(u"You said: " + message)
        print('Come message ' + message)
        # db = self.application.db
        # message_dict = json.loads(message)
        # db.chat.insert(message_dict)
        for key, value in enumerate(self.application.webSocketsPool):
            if value != self:
                value.ws_connection.write_message(message)

    def on_close(self):
        print("WebSocket closed")
        # print(self.application.webSocketsPool)
        for key, value in enumerate(self.application.webSocketsPool):
            if value == self:
                del self.application.webSocketsPool[key]


def main():
    print('Start server')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
