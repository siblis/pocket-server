from handlers.json_util import JsonHandler
from database_tools.alchemy import CGroups


class GroupHandler(JsonHandler):
    def get(self, *args):
        check_result = self._token_check()
        if check_result:
            result = self.db.query(CGroups).filter(CGroups.gid == check_result.gid).one_or_none()
            self.set_response(result)
            self.set_status(200)
            self.write_json()

    def post(self):
        try:
            result = self.db.query(CGroups.username).filter(
                CGroups.username == self.json_data['group_name']).one_or_none()

            if result is None:
                group_name = self.json_data['group_name']
                creation_time = self.json_data['creation_time']
                creater_user_id = self.json_data['creater_user_id']
                group = CGroups(group_name=group_name, creation_time=creation_time, creater_user_id=creater_user_id)
                self.db.add(group)
                self.db.commit()
                self.set_status(201, reason='Created')
                self.write_json()
            else:
                message = 'Conflict, group exists'
                self.send_error(409, message=message)

        except Exception as e:
            self.send_error(400, message='Bad JSON, need group_name')
