import tornado.websocket
import uuid
from handlers.json_util import JsonHandler
from typing import NamedTuple
import tornado.escape
import logging
import os

'''
Пример для Windows: 
LOG_PATCH = r'C:\\' 
'''
LOG_PATCH = '/var/log/pocket/'
LOG_FILE_NAME = 'websocket_echo.log'
LOG_FULL_PATH = os.path.join(LOG_PATCH, LOG_FILE_NAME)


class UserData(NamedTuple):
    user_id: int
    ws_object: 'WebSocketHandlerEcho'


class WebSocketHandlerEcho(tornado.websocket.WebSocketHandler, JsonHandler):
    ws_dict = dict()
    logging.basicConfig(filename=LOG_FULL_PATH, level=logging.INFO)

    def check_origin(self, origin):
        return True

    def _gen_session(self):
        return str(uuid.uuid4())

    def prepare(self):
        if 'Token' in self.request.headers:
            self.uid = self._token_check()
        else:
            logging.info('Token not found in headers')
            logging.info(self.request.headers)
            self.send_error(401)

    def open(self):
        self.session = self._gen_session()
        logging.info(f'WebSocket opened, {self.session}')
        self.user_tuple = UserData(self.uid, self)
        self.ws_dict[self.session] = self.user_tuple

    def on_message(self, message):
        logging.info(f'Come message {message} from id {self.uid} and sessid {self.session}')
        json_data = ''
        try:
            json_data = tornado.escape.json_decode(message)
            json_data['sender'] = self.session
            json_data['senderid'] = self.uid
            for key in self.ws_dict.keys():
                self.write_message(json_data)
        except ValueError:
            message = 'Unable to parse JSON'
            self.write_message({"response": "400", "message": message})
        except Exception as e:
            logging.info(json_data)
            logging.info(e)
            message = 'Bad JSON'
            self.write_message({"response": "400", "message": message})

    def on_close(self):
        logging.info(f'WebSocket closed, {self.session}')
        try:
            self.ws_dict.pop(self.session)
        except:
            logging.info("No session in DICT")
