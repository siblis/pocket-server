from handlers.json_util import JsonHandler
from database_tools.db_connect import Session
from database_tools.alchemy import CGroups, CGroupsUsers, CMessagesChat
# from sqlalchemy import or_
from handlers.chatshandler import group_get_in_name as group_get_in_name
from datetime import datetime, timedelta

session = Session()

TIME_DELTA = 30


def add_message_in_group(session, group_id, from_id, to_id, message):
    creation_date = datetime.now()
    msg = CMessagesChat(group_id=group_id, from_id=from_id, to_id=to_id, dtime=creation_date, message=message)
    session.add(msg)
    session.commit()


def get_group_in_users_id(session, group_id, user_id):
    return session.query(CGroupsUsers).filter_by(group_id=group_id, user_id=user_id).first()


def get_messages_in_group(session, group_id, start_dtime, end_dtime):
    return session.query(CMessagesChat).filter(CMessagesChat.group_id == group_id,
                                               CMessagesChat.dtime >= start_dtime,
                                               CMessagesChat.dtime <= end_dtime).all()


class ChatsMessagesHandler(JsonHandler):
    # def get(self, url):
    def get(self, url):
        # id-user=[0-9]{1,}&data=[0-9]{2}-[0-9]{2}-[0-9]{4}&time=[0-9]{2}:[0-9]{2}:[0-9]{2}
        # получение последнии сообщения из групыы(чата)
        if self._token_check():
            values = url.split('&')
            print(values)
            result = {}
            for value in values:
                key, itam = value.split('=')
                result[key] = itam
            group_id = int(result['gruop-id'])
            # user_id = int(result['user-id'])
            user_id = self._token_check().uid
            # Проверить входет ли пользователь в группу
            start_dtime = datetime.strptime(f"{result['data']} {result['time']}", '%Y-%m-%d %H:%M:%S')
            end_dtime = start_dtime + timedelta(minutes=TIME_DELTA)
            print(get_messages_in_group(self.db, group_id=group_id, start_dtime=start_dtime, end_dtime=end_dtime))

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
                    add_message_in_group(self.db, group_id=result_group.gid, from_id=from_id, to_id=to_id,
                                         message=message)
                except:
                    self.send_error(500, message='Internal Server Error')
                    return
                self.response['message'] = "Messages add group"
                self.set_status(200)
                self.write_json()
            else:
                self.send_error(404, message='Group not found')
        else:
            self.send_error(400, message='Error token')
