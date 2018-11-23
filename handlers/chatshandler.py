from handlers.json_util import JsonHandler
from database_tools.db_connect import Session
from database_tools.alchemy import CMessages
from database_tools.alchemy import CGroups, CGroupsUsers
from datetime import datetime
from handlers.wshandler import WebSocketHandler

session = Session()
logger = WebSocketHandler.logger


# class ChatsHandler(JsonHandler):
#     def get(self):
#         if self._token_check(session):
#             self._get_elements(session, CMessages)
#
#     def post(self):
#         if self._token_check(session):
#             to_id = self.json_data['to_id']
#             from_id = self.json_data['from_id']
#             message = self.json_data['message']
#             dtime = datetime.now()
#             chat = CMessages(to_id=to_id, from_id=from_id, message=message, dtime=dtime)
#             session.add(chat)
#             session.commit()
#             self.set_status(201, reason='Created')

# -------------------------------------ChatsGroupHandler-------------------------------------------------------------
def group_creat(session, id_user, group_name):
    try:
        result = group_get_in_name(session, group_name)
    except Exception as e:
        logger.error("Error message: " + str(e))
        raise ValueError("Error BD")
    if result is None:
        creation_date = datetime.now()
        msg = CGroups(creater_user_id=id_user, group_name=group_name, creation_date=creation_date)
        session.add(msg)
        session.commit()
    else:
        raise ValueError("Group already exists")


def group_user_add(session, id_user, group_id):
    try:
        group = group_get_in_id(session, group_id)
    except:
        raise ValueError("Error BD")
    if group is not None:
        try:
            msg = CGroupsUsers(user_id=id_user, group_id=group_id)
        except:
            raise ValueError("Error BD")
        session.add(msg)
        session.commit()
    else:
        raise ValueError("Group Not Found")


def group_get_in_id(session, group_id):
    # Возврщяет информацию о группе через ID группы
    return session.query(CGroups).filter_by(gid=group_id).first()


def group_get_in_name(session, group_name):
    # Возврщяет информацию о группе через имя группы
    return session.query(CGroups).filter_by(group_name=group_name).first()


def group_users_get_in_id(session, group_id):
    return session.query(CGroupsUsers).filter_by(group_id=group_id).all()

def user_is_in_group(session, id_user, group_id):
    return session.query(CGroupsUsers).filter_by(user_id=id_user, group_id=group_id).first()

def delete_user_is_in_group(session,  id_user, group_id):
    msg = session.query(CGroupsUsers).filter_by(user_id=id_user, group_id=group_id).first()
    session.delete(msg)
    session.commit()

class ChatsHandler(JsonHandler):
    def get(self, group_or_name_or_id):
        # Если только цифры, то выдать инофрмацию о группе по id
        # Если не только цыфры, то значит это имя группы, выдать информацию о группе
        if self._token_check():
            if group_or_name_or_id.isdigit() == True:
                # Цифры
                try:
                    result_group = group_get_in_id(self.db, group_or_name_or_id)
                except Exception as e:
                    logger.error("Error message: " + str(e))
                    self.send_error(500, message='Internal Server Error')
                    return
            else:
                # строка
                try:
                    result_group = group_get_in_name(self.db, group_or_name_or_id)
                except Exception as e:
                    logger.error("Error message: " + str(e))
                    self.send_error(500, message='Internal Server Error')
                    return
            if result_group is not None:
                self.response['gid'] = result_group.gid
                self.response['group_name'] = result_group.group_name
                self.response['users'] = []
                try:
                    result_users_group = group_users_get_in_id(self.db, result_group.gid)
                except Exception as e:
                    logger.error("Error message: " + str(e))
                    self.send_error(500, message='Internal Server Error')
                    return
                for user in result_users_group:
                    self.response['users'].append(user.user_id)
                self.set_status(200)
                self.write_json()
            else:
                self.send_error(404, message='Group not found')
        else:
            self.send_error(400, message='Error token')

    def post(self):
        # создать группу, добавить пользователя в группу
        if self._token_check():
            # Если группа(чат) не существует, создаем ее
            try:
                group_name = self.json_data['group_name']
                creater_user_id = self._token_check().uid
            except Exception as e:
                logger.error("Error message: " + str(e))
                self.send_error(400, message='Bad JSON')
                return
            try:
                result = group_get_in_name(self.db, group_name)
            except Exception as e:
                logger.error("Error message: " + str(e))
                self.send_error(500, message='Internal Server Error')
                return
            if result is None:
                # Группа не создана, создать
                try:
                    group_creat(self.db, creater_user_id, group_name)
                    group_id = group_get_in_name(self.db, group_name).gid
                    group_user_add(self.db, creater_user_id, group_id)
                except ValueError as err:
                    logger.error("Error message: " + str(err))
                    self.send_error(500, message=err)
                    return
                except Exception as e:
                    logger.error("Error message: " + str(e))
                    self.send_error(500, message='Internal Server Error')
                    return
                self.response['message'] = "Group creat"
                self.set_status(200)
                self.write_json()
            else:
                # Группа уже есть
                self.send_error(404, message='Group with that name already exists')
        else:
            self.send_error(400, message='Error token')

    def put(self):
        # добавление пользователя в группу(чат)
        if self._token_check():
            try:
                group_id = self.json_data['group_id']
                new_user_id = self.json_data['new_user_id']
            except Exception as e:
                logger.error("Error message: " + str(e))
                self.send_error(400, message='Bad JSON')
                return
            try:
                result = group_get_in_id(self.db, group_id)
            except Exception as e:
                logger.error("Error message: " + str(e))
                self.send_error(500, message='Internal Server Error')
                return
            if result is not None:
                group_id = result.gid
                # група существует, проверяем не ли там уже этого пользователя
                try:
                    result_user_is_in_group = user_is_in_group(self.db, new_user_id, group_id)
                except Exception as e:
                    logger.error("Error message: " + str(e))
                    self.send_error(500, message='Internal Server Error')
                    return
                if result_user_is_in_group is None:
                    # пользователь отсутсвует добовляем опльзователя
                    try:
                        group_user_add(self.db, new_user_id, group_id)
                    except ValueError as err:
                        logger.error("Error message: " + str(err))
                        self.send_error(500, message=err)
                        return
                    except Exception as e:
                        logger.error("Error message: " + str(e))
                        self.send_error(500, message='Internal Server Error')
                        return
                    self.response['message'] = "User add group"
                    self.set_status(200)
                    self.write_json()
                else:
                    self.send_error(404, message='User already in group')
            else:
                # группа с таким именем не существует
                self.send_error(404, message='Group not found')
        else:
            self.send_error(400, message='Error token')

    def delete(self):
        # удаление пользователя в группу(чат)
        if self._token_check():
            try:
                group_name = self.json_data['group_name']
                user_id = self.json_data['user_id']
            except Exception as e:
                logger.error("Error message: " + str(e))
                self.send_error(400, message='Bad JSON')
                return
            try:
                result = group_get_in_name(self.db, group_name)
            except Exception as e:
                logger.error("Error message: " + str(e))
                self.send_error(500, message='Internal Server Error')
                return
            if result is not None:
                group_id = result.gid
                # Проверяем пользователь находится ли в группе
                try:
                    result_user_ia_in_group = user_is_in_group(self.db, id_user=user_id, group_id=group_id)
                except Exception as e:
                    logger.error("Error message: " + str(e))
                    self.send_error(500, message='Internal Server Error')
                    return
                if result_user_ia_in_group is not None:
                    # група существует, удалить пользователя
                    try:
                        delete_user_is_in_group(self.db, id_user=user_id, group_id=group_id)
                    except Exception as e:
                        logger.error("Error message: " + str(e))
                        self.send_error(500, message='Internal Server Error')
                        return
                    self.response['message'] = "User delete group"
                    self.set_status(200)
                    self.write_json()
                else:
                    self.send_error(404, message='User not found in group')
            else:
                self.send_error(404, message='Group not found')
        else:
            self.send_error(400, message='Error token')


if __name__ == '__main__':
    pass
    # group_creat(session, id_user, group_name)
    # group_user_add(session, id_user, group_id)
