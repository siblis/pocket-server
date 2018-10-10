from handlers.json_util import JsonHandler
from database_tools.db_connect import Session
from database_tools.alchemy import CMessages
from datetime import datetime

from database_tools.work_with_db import ServerStorage   # Добавил класс из work_with_db.py

session = Session()


class ChatsHandler(JsonHandler):
    def get(self):
        if self._token_check(session):
            self._get_elements(session, CMessages)

    def post(self):
        if self._token_check(session):
            to_id = self.json_data['to_id']
            from_id = self.json_data['from_id']
            message = self.json_data['message']
            # dtime = datetime.now()
            # chat = CMessages(to_id=to_id, from_id=from_id, message=message, dtime=dtime)
            # session.add(chat)
            # session.commit()
            ServerStorage().add_history(from_id=from_id,
                                        to_id=to_id,
                                        message=message)    # Добавление сообщений в db через work_with_db.py
            self.set_status(201, reason='Created')
