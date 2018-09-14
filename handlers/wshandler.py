import tornado.websocket
import uuid
from handlers.json_util import JsonHandler
from typing import NamedTuple
import tornado.escape


class UserData(NamedTuple):
    user_id: int
    ws_object: 'WebSocketHandler'


class WebSocketHandler(tornado.websocket.WebSocketHandler, JsonHandler):
    ws_dict = dict()

    def check_origin(self, origin):
        return True

    def _gen_session(self):
        return uuid.uuid4()

    def prepare(self):
        if 'Token' in self.request.headers:
            self.uid = self._token_check()
        else:
            self.close(401)

    def open(self):
        # TODO в лог
        # print("WebSocket opened")
        self.session = self._gen_session()
        self.user_tuple = UserData(self.uid, self)

        self.ws_dict[self.session] = self.user_tuple

    def on_message(self, message):
        #TODO в лог и этот принт
        # print(f'Come message {message} from id {self.uid} and sessid {self.session}')
        json_data = ''
        try:
            json_data = tornado.escape.json_decode(message)
            json_data['sender'] = self.session
            for key in self.ws_dict.keys():
                if key != self.session:
                    if self.ws_dict[key].user_id == int(json_data['receiver']):
                        self.ws_dict[key].ws_object.write_message(json_data['message'])
                        self.write_message({"response": "200"})
                    else:
                        self.write_message({"response": "404", "message": "Client not found or not online"})
                else:
                    if len(self.ws_dict) == 1:
                        self.write_message({"response": "404", "message": "Not found receiver"})
        except ValueError:
            message = 'Unable to parse JSON'
            self.write_message({"response": "400", "message": message})
        except Exception as e:
            message = 'Bad JSON'
            self.write_message({"response": "400", "message": message})


    def on_close(self):
        # print("WebSocket closed")
        self.ws_dict.pop(self.session)