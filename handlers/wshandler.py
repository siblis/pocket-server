import tornado.websocket
import uuid
from handlers.json_util import JsonHandler
from database_tools.db_connect import Session


class WebSocketHandler(tornado.websocket.WebSocketHandler, JsonHandler):
    ws_dict = dict()

    @staticmethod
    def _gen_session():
        return uuid.uuid4()

    def prepare(self):
        if 'Token' in self.request.headers:
            self.uid = self._token_check(self.db)
        else:
            self.close(401)

    def open(self):
        temp_list = []
        print("WebSocket opened")
        # ген сессии
        self.session = self._gen_session()
        temp_list.append(self.uid)
        temp_list.append(self)
        # обьект ws
        self.application.webSocketsPool.append(self)
        # словарь ключ сессия, объект ws
        self.ws_dict[self.session] = temp_list

    def on_message(self, message):
        print(self.ws_dict)
        self.write_message(u"You said: " + message)
        print(f'Come message {message} from id {self.uid} and sessid {self.session}')

        for key in self.ws_dict.keys():
            if key != self.session:
                self.ws_dict[key][1].write_message(message)

    def on_close(self):
        print("WebSocket closed")
        self.ws_dict.pop(self.session)
