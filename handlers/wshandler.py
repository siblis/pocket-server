import tornado.websocket
import uuid
from handlers.json_util import JsonHandler
from typing import NamedTuple


class UserData(NamedTuple):
    user_id: int
    ws_object: 'WebSocketHandler'


class WebSocketHandler(tornado.websocket.WebSocketHandler, JsonHandler):
    ws_dict = dict()

    def _gen_session(self):
        return uuid.uuid4()

    def prepare(self):
        if 'Token' in self.request.headers:
            self.uid = self._token_check()
        else:
            self.close(401)

    def open(self):
        print("WebSocket opened")
        # ген сессии
        self.session = self._gen_session()
        self.user_tuple = UserData(self.uid, self)
        # обьект ws
        self.application.webSocketsPool.append(self)
        # словарь ключ сессия, объект ws
        self.ws_dict[self.session] = self.user_tuple

    def on_message(self, message):
        self.write_message(u"You said: " + message)
        # print(f'Come message {message} from {self.session}')
        print(f'Come message {message} from id {self.uid} and sessid {self.session}')
        for key in self.ws_dict.keys():
            if key != self.session:
                self.ws_dict[key].ws_object.write_message(message)

    def on_close(self):
        print("WebSocket closed")
        self.ws_dict.pop(self.session)


