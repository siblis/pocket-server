import tornado.websocket
import uuid
from handlers.json_util import JsonHandler
from database_tools.db_connect import Session

session = Session()


class WebSocketHandler(tornado.websocket.WebSocketHandler, JsonHandler):
    ws_clients = []

    @staticmethod
    def _gen_session():
        return uuid.uuid4()

    def prepare(self):
        if 'Token' in self.request.headers:
            self._token_check(session)
        else:
            self.close(401)

    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket opened")
        self.session = self._gen_session()
        self.application.webSocketsPool.append(self)
        self.ws_clients.append(self.session)
        print(self.ws_clients)

    def on_message(self, message):
        self.write_message(u"You said: " + message)
        print(f'Come message {message} from {self.session}')

        for key, value in enumerate(self.application.webSocketsPool):
            if value != self:
                value.ws_connection.write_message(message)

    def on_close(self):
        print("WebSocket closed")
        self.ws_clients.remove(self.session)
        for key, value in enumerate(self.application.webSocketsPool):
            if value == self:
                del self.application.webSocketsPool[key]
        print(self.ws_clients)
