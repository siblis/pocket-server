from handlers.jsonhandler import JsonHandler


class UsersHandler(JsonHandler):
    def get(self):
        # TODO token сверить с БД
        # TODO если токен есть вывести список всех юзеров
        result_set = self.db.execute("SELECT id, login, is_admin, last_login FROM users")
        for r in result_set:
            self.write(str(r) + "\n")

    def post(self):
        # add user to db
        # token сверить
        # если токен верный проверить данные
        # если данных нет в БД, записать, иначе выдать ошибку

        if self.json_data:
            query = "SELECT id FROM users WHERE token = '" + self.json_data['token'] + "'"
            result = self.db.execute(query)
            result_len = len(result.fetchall())
            # print(result_len)
            if result_len > 0:
                print('token ok')
                print('next check data')
                query = "SELECT id FROM users WHERE login = '" + self.json_data['adduser'] + "'"
                result = self.db.execute(query)

                result_len = len(result.fetchall())
                if result_len > 0:
                    print('error add, write exists')
                else:
                    print('create new str in bd')
                    self.response['response'] = '200'
                    self.write_json()
            else:
                self.response['message'] = 'token is wrong'
                self.response['response'] = '403'
                self.write_json()
