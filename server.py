import tornado.web
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
from sqlalchemy import create_engine
from tornado.options import define, options
from handlers.jsonhandler import BaseHandler
from handlers.authhandler import AuthHandler
from handlers.usershandler import UsersHandler
from handlers.chatshandler import ChatsHandler
from handlers.wshandler import WebSocketHandler

define("port", default=8888, help="start on the given port", type=int)
POSTGRES_SERVER = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_LOGIN = 'postgres'
POSTGRES_PASS = '123'
POSTGRES_BASE = 'messengerbase'


class Application(tornado.web.Application):
    def __init__(self):
        self.webSocketsPool = []
        handlers = [
            (r'/v1', MainHandler),
            (r'/v1/auth', AuthHandler),
            (r'/v1/users', UsersHandler),
            (r'/v1/users/add', UsersHandler),
            (r'/v1/ws/', WebSocketHandler),
            (r'/v1/chats/', ChatsHandler),
        ]

        # если понадобится cookie_secret(для подписания cookie),
        # login_url(декоратор для перенаправления на страницу авторизации не зарегистрированного пользователя
        settings = dict()
        tornado.web.Application.__init__(self, handlers, **settings)

        # bd connection
        db_address = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                               POSTGRES_PORT,
                                                               POSTGRES_BASE)
        self.db = create_engine(db_address)


class MainHandler(BaseHandler):
    def get(self):
        result = "Welcome to server"
        self.write(str(result))


def main():
    print('Start server')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
