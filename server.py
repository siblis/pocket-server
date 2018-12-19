import tornado.web
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
from tornado.options import define, options
from handlers.json_util import BaseHandler
from handlers.authhandler import AuthHandler
from handlers.authhandler import AuthHandlerLogin
from handlers.authhandler import AuthHandlerRegister
from handlers.usershandler import UsersHandler
from handlers.usershandler import UsersHandlerId, UsersHandlerMail, UsersHandlerSearchByNickname
from handlers.chatshandler import ChatsHandler
from handlers.chatsmessageshandler import ChatsMessagesHandler
from handlers.contactshandler import ContactsHandler
from handlers.wshandler import WebSocketHandler
from handlers.grouphandler import GroupHandler
from database_tools.db_connect import Session

define("port", default=8888, help="start on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self, db=None):
        if db == None:
            db = Session()
        self.webSocketsPool = []
        handlers = [
            (r'/v1', MainHandler),
            (r'/v1/auth/?', AuthHandler),
            (r'/v1/auth/login/?', AuthHandlerLogin),
            (r'/v1/auth/register/?', AuthHandlerRegister),
            (r'/v1/account/?', UsersHandler),
            (r'/v1/account/contacts/?', ContactsHandler),
            (r'/v1/users/([0-9]+)', UsersHandlerId),

            (r'/v1/users/([a-zA-Z][a-zA-Z0-9]{2,})', UsersHandlerSearchByNickname),
            (r'/v1/users/([a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)', UsersHandlerMail),
            (r'/v1/users/groups/', GroupHandler),

            (r'/v1/ws/?', WebSocketHandler),

            (r'/v1/chats/?', ChatsHandler),
            (r'/v1/chats/([0-9]+)', ChatsHandler),
            (r'/v1/chats/([a-zA-Z0-9]{3,})', ChatsHandler),
            (r'/v1/chats/messages/', ChatsMessagesHandler),
            (r'/v1/chats/messages/(gruop-id=[0-9]{1,}&data=[0-9]{4}-[0-9]{2}-[0-9]{2}&time=[0-9]{2}:[0-9]{2}:[0-9]{2})', ChatsMessagesHandler),
            # (r'/v1/chats/add', ChatsHandler),
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
