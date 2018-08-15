import tornado.websocket

# open websocket and retrieve msg
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")
        self.application.webSocketsPool.append(self)

    def on_message(self, message):
        self.write_message(u"You said: " + message)
        print('Come message ' + message)
        # db = self.application.db
        # message_dict = json.loads(message)
        # db.chat.insert(message_dict)
        for key, value in enumerate(self.application.webSocketsPool):
            if value != self:
                value.ws_connection.write_message(message)

    def on_close(self):
        print("WebSocket closed")
        for key, value in enumerate(self.application.webSocketsPool):
            if value == self:
                del self.application.webSocketsPool[key]