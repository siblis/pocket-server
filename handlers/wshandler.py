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
LOG_FILE_NAME = 'websocket.log'
LOG_FULL_PATH = os.path.join(LOG_PATCH, LOG_FILE_NAME)


class UserData(NamedTuple):
    user_id: int
    user_name: str
    ws_object: 'WebSocketHandler'


class WebSocketHandler(tornado.websocket.WebSocketHandler, JsonHandler):
    ws_dict = dict()
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='[%d/%m/%Y %H:%M:%S]', filename=LOG_FULL_PATH,
                        level=logging.INFO)

    def check_origin(self, origin):
        return True

    def _gen_session(self):
        return str(uuid.uuid4())

    def prepare(self):
        if 'Token' in self.request.headers:
            check_result = self._token_check()
            if check_result is None:
                self.send_error(401)
            else:
                self.uid = check_result.uid
                self.username = check_result.username
        else:
            logging.info('Token not found in headers')
            logging.info(self.request.headers)
            self.send_error(401)

    def open(self):
        self.session = self._gen_session()
        logging.info(f'WebSocket opened, {self.session}')
        self.user_tuple = UserData(self.uid, self.username, self)
        self.ws_dict[self.session] = self.user_tuple

    def on_message(self, message):
        logging.info(f'Come message {message} from id {self.uid} and sessid {self.session}')
        json_data = ''
        try:
            json_data = tornado.escape.json_decode(message)
            json_data['senderid'] = self.uid
            json_data['sender_name'] = self.username
            for key in self.ws_dict.keys():
                if key != self.session:
                    if self.ws_dict[key].user_id == int(json_data['receiver']):
                        self.ws_dict[key].ws_object.write_message(json_data)
                        self.write_message({"response":"200"})
                    else:
                        #TODO сделать хранение не дошедших сообщений
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
        logging.info(f'WebSocket closed, {self.session}')
        try:
            self.ws_dict.pop(self.session)
        except:
            logging.info("No session in DICT")
