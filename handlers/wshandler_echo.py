import tornado.websocket
import tornado.escape
import logging
from handlers.wshandler import WebSocketHandler


class WebSocketHandlerEcho(WebSocketHandler):
    def on_message(self, message):
        logging.info(f'Come message {message} from id {self.uid} and sessid {self.session}')
        json_data = ''
        try:
            json_data = tornado.escape.json_decode(message)
            json_data['sender'] = self.session
            json_data['senderid'] = self.uid
            self.write_message(json_data)
        except:
            if json_data == '':
                request = message
                self.write_message(f'Bad JSON, your request: {request}')
            else:
                self.write_message(f'Bad JSON, your request: {json_data}')
