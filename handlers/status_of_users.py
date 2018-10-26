from sqlalchemy import update
from handlers.json_util import JsonHandler
from database_tools.alchemy import CUserStatus


# запросы к БД
# Запросы к редактированию пользоватлеьких статусов
def get_status_id_users(session, status):
    return session.query(CUserStatus).filter_by(status_name=status).first()


def add_status_users(session, status):
    msg = CUserStatus(status_name=status)
    session.add(msg)
    session.commit()


def change_status_name_users(session, old_status, new_status):
    query = update(CUserStatus).where(CUserStatus.status_name == old_status).values(status_name=new_status)
    session.execute(query)
    session.commit()


class StatusOfUsers(JsonHandler):
    """
    Класс для созданию, удалению, изменению статусов которые можно будет присовить пользователям
    """

    def get(self, status):
        # Необходимо ограничить доступ к команде (сделать только для админов сервера)
        check_result = self._token_check()
        if check_result:
            try:
                result = get_status_id_users(self.db, status)
            except:
                self.send_error(500, message='Internal Server Error')
            else:
                if result is not None:
                    self.response['users_status_id'] = result.usid
                    self.set_status(200)
                    self.write_json()
                else:
                    self.send_error(404, message='Status does not exists')
        else:
            self.send_error(400, message='Error token')

    def post(self):
        # Необходимо ограничить доступ к команде (сделать только для админов сервера)
        check_result = self._token_check()
        if check_result:
            try:
                status = self.json_data['status_name']
            except:
                self.send_error(400, message='Bad JSON')
                return
            if get_status_id_users(self.db, status) is None:
                try:
                    add_status_users(self.db, status)
                except:
                    self.send_error(500, message='Internal Server Error')
                else:
                    self.response['message'] = "Status created"
                    self.set_status(200)
                    self.write_json()
            else:
                self.send_error(409, message='Status already in list')
        else:
            self.send_error(400, message='Error token')

    def put(self):
        # Необходимо ограничить доступ к команде (сделать только для админов сервера)
        check_result = self._token_check()
        if check_result:
            try:
                old_status_name = self.json_data['old_status_name']
                new_status_name = self.json_data['new_status_name']
            except:
                self.send_error(400, message='Bad JSON')
                return
            if get_status_id_users(self.db, old_status_name) is not None:
                if get_status_id_users(self.db, new_status_name) is None:
                    try:
                        change_status_name_users(self.db, self.json_data['old_status_name'],
                                                 self.json_data['new_status_name'])
                    except:
                        self.send_error(500, message='Internal Server Error')
                    else:
                        self.response['message'] = "Status change"
                        self.set_status(200)
                        self.write_json()
                else:
                    self.send_error(409, message='New status already in list')
            else:
                self.send_error(409, message='Old status does not exists')
        else:
            self.send_error(400, message='Error token')
