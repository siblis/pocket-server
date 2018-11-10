from handlers.json_util import JsonHandler
from database_tools.db_connect import Session
from database_tools.alchemy import CMessages
from database_tools.alchemy import CGroups, CGroupsUsers, CMessagesChat
from datetime import datetime

session = Session()

class ChatsMessagesHandler(JsonHandler):
    def get(self, group_mess_get_name_or_id):
        # получение сообщений из группы(чата)
        if self._token_check():
            pass

    def post(self):
        # создание сообщений для группы(чата)
        if self._token_check():
            pass