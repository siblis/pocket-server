from handlers.json_util import JsonHandler
from database_tools.db_connect import Session
from database_tools.alchemy import CGroups, CGroupsUsers, CMessagesChat
from handlers.chatshandler import group_get_in_name as group_get_in_name
from datetime import datetime

session = Session()

def add_message_in_group(session, group_id, from_id, to_id, message)
    creation_date = datetime.now()
    msg = CMessagesChat(id_group=group_id, from_id=from_id, to_id=to_id, dtime=creation_date, message=message)
    session.add(msg)
    session.commit()

def get_group_in_users_id(session, group_id, user_id):
    return session.query(CGroupsUsers).filter_by(group_id=group_id, user_id=user_id).first()

class ChatsMessagesHandler(JsonHandler):
    def get(self, group_mess_get_name_or_id):
        # получение сообщений из группы(чата)
        if self._token_check():
            pass

    def post(self):
        # создание сообщений для группы(чата)
        if self._token_check():
            try:
                group_name = self.json_data['group_name']
                from_id = self._token_check().uid
                to_id = self.json_data['to_id']
                message = self.json_data['message']
            except:
                self.send_error(400, message='Bad JSON')
                return
            try:
                result_group = group_get_in_name(self.db, group_name)
            except:
                self.send_error(500, message='Internal Server Error')
                return
            if result_group is not None:
                # Группа с таким названием существует
                # Проверить есть ли пользователь в чате
                try:
                    # От кого
                    from_user_in_group = get_group_in_users_id(self.db, group_id=result_group.gid, user_id=from_id)
                except:
                    self.send_error(500, message='Internal Server Error')
                    return
                try:
                    # От для кого
                    to_user_in_group = get_group_in_users_id(self.db, group_id=result_group.gid, user_id=to_id)
                except:
                    self.send_error(500, message='Internal Server Error')
                    return

                if from_user_in_group is None:
                    self.send_error(405, message='User_from not found in group')
                    return
                if to_user_in_group is None:
                    self.send_error(405, message='User_to not found in group')
                    return
                # Все проверики прошли успешно
                # Добовляем сообщение в группу
                try:
                    add_message_in_group(self.db, group_id=result_group.gid, from_id=from_id, to_id=to_id, message=message)
                except:
                    self.send_error(500, message='Internal Server Error')
                    return
                else:
                    self.send_error(404, message='Only admin groups can add users to chat')
            else:
                self.send_error(404, message='Group not found')
        else:
            self.send_error(400, message='Error token')