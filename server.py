import tornado.web
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
from tornado.options import define, options
from handlers.json_util import BaseHandler
from handlers.authhandler import AuthHandler
from handlers.usershandler import UsersHandler
from handlers.usershandler import UsersHandlerId
from handlers.chatshandler import ChatsHandler
from handlers.contactshandler import ContactsHandler
from handlers.contactshandler import ContactsByIdHandler
from handlers.wshandler import WebSocketHandler
from handlers.wshandler import WebSocketStatusHandler
from handlers.wshandler_echo import WebSocketHandlerEcho
from database_tools.db_connect import Session

define("port", default=8888, help="start on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self, db=None):
        if db == None:
            db = Session()
        self.webSocketsPool = []
        handlers = [
            (r'/v1', MainHandler),
            (r'/v1/auth/', AuthHandler),
            (r'/v1/users/', UsersHandler),
            (r'/v1/users/([0-9]+)', UsersHandlerId),
            (r'/v1/users/contacts/', ContactsHandler),
            (r'/v1/users/contacts_by_id/', ContactsByIdHandler),
            (r'/v1/ws/', WebSocketHandler),
            (r'/v1/ws/status/([0-9]+)', WebSocketStatusHandler),
            (r'/v1/ws_echo/', WebSocketHandlerEcho),
            (r'/v1/chats/', ChatsHandler),
            (r'/v1/chats/add', ChatsHandler),
        ]

        # если понадобится cookie_secret(для подписания cookie),
        # login_url(декоратор для перенаправления на страницу авторизации не зарегистрированного пользователя
        settings = dict()
        # websocket_ping_interval=1 (для включения пинга) для отключение неактивных клиентов
        tornado.web.Application.__init__(self, handlers, **settings, websocket_ping_interval=10,
                                         websocket_ping_timeout=5 * 60)

        self.db = db


class MainHandler(BaseHandler):
    def get(self):
        result = "Welcome to server"
        self.write(str(result))


def main():
    print('Start server')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(), ssl_options={
        "certfile": "/var/www/ca/fullchain.pem",
        "keyfile": "/var/www/ca/privkey.pem",
    })
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
