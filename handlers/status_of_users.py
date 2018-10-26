from sqlalchemy import update
from handlers.json_util import JsonHandler
from database_tools.alchemy import CUserStatus


# запросы к БД
# Запросы к редактированию пользоватлеьких статусов
def get_status_id_users(session, status):
    return session.query(CUserStatus).filter_by(status_name=status).first()


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
