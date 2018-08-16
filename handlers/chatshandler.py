from handlers.jsonhandler import BaseHandler

class ChatsHandler(BaseHandler):
    def get(self):
        # token сверить с БД
        # если токен есть вывести список всех чатов
        # result_set = self.db.execute("SELECT * FROM chats")
        # self.write(str(result_set))
        pass

    def post(self):
        # create new chat
        # token сверить
        # если токен верный проверить данные
        # если данных нет в БД, записать, иначе выдать ошибку
        pass