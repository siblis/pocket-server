from handlers.json_util import JsonHandler
from database_tools.alchemy import CGroups


class GroupHandler(JsonHandler):
    def prepare(self):
        super().prepare()
        self.check_result = self._token_check()

    def get(self, *args):
        if self.check_result:
            try:
                result = self.db.query(CGroups).filter(CGroups.gid == self.check_result.gid).one_or_none()
                self.set_response(result)
                self.set_status(200)
                self.write_json()
            except:
                self.send_error(400, message='Please check gid')

    def post(self):
        if self.check_result:
            exists_group = None
            try:
                exists_group = self.db.query(CGroups.group_name).filter(
                    CGroups.group_name == self.json_data['group_name']).one_or_none()
            except:
                self.send_error(400, message='Please check group_name')

            if exists_group is None:
                group_name = self.json_data['group_name']
                creation_time = self.json_data['creation_time']
                creater_user_id = self.json_data['creater_user_id']
                group = CGroups(group_name=group_name, creation_time=creation_time, creater_user_id=creater_user_id)
                self.db.add(group)
                self.db.commit()
                self.set_status(201, reason='Created')
                self.write_json()
            else:
                message = 'Group already exists'
                self.send_error(409, message=message)

    def delete(self):
        if self.check_result:
            group_name = self.json_data['group_name']
            result = self.db.query(CGroups).filter(CGroups.group_name == group_name).one_or_none()
            result_gid = self.db.query(CGroups).filter(CGroups.gid == result.gid).delete()
            if not result_gid:
                self.set_status(404, 'Group does not exists')
            else:
                self.db.commit()
                self.set_status(200)
                self.response['deleted_group_id'] = result.gid
                self.response['deleted_group_name'] = result.group_name
                self.write_json()
        else:
            self.send_error(400)
