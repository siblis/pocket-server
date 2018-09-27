import tornado.websocket
import tornado.escape
import logging
from handlers.wshandler import UserData, WebSocketHandler


class WebSocketHandlerEcho(WebSocketHandler, UserData):
    def on_message(self, message):
        logging.info(f'Come message {message} from id {self.uid} and sessid {self.session}')
        json_data = ''
        try:
            json_data = tornado.escape.json_decode(message)
            json_data['sender'] = self.session
            json_data['senderid'] = self.uid
            self.write_message(json_data)
        except ValueError:
            message = 'Unable to parse JSON'
            self.write_message({"response": "400", "message": message})
        except Exception as e:
            logging.info(json_data)
            logging.info(e)
            message = 'Bad JSON'
            self.write_message({"response": "400", "message": message})
