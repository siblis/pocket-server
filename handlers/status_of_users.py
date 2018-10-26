from sqlalchemy import update
from handlers.json_util import JsonHandler
from database_tools.alchemy import CUserStatus

class StatusOfUsers(JsonHandler):
    """
    Класс для созданию, удалению, изменению статусов которые можно будет присовить пользователям
    """
    pass