from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers, CContacts
from handlers.wshandler import WebSocketHandler


class ContactsHandler(JsonHandler):
    def prepare(self):
        super().prepare()
        self.check_result = self._token_check()

    def post(self):
        if self.check_result:
            exists_contact = None
            try:
                contact = self.json_data['contact']
                exists_contact = self.db.query(CUsers).filter(CUsers.email == contact).one_or_none()
            except Exception as e:
                print(e)
                self.send_error(400, reason='Bad request body')
            if exists_contact is None:
                self.set_status(404, 'User does not exists')
            else:
                result = self.db.query(CContacts).filter(CContacts.user_id == self.check_result.uid,
                                                         CContacts.contact == exists_contact.uid).first()
                if result is None:
                    new_contact = CContacts(user_id=self.check_result.uid, contact=exists_contact.uid)
                    self.db.add(new_contact)
                    self.db.commit()

                    self.set_response(exists_contact)
                    self.write_json()
                    self.set_status(201, 'Added')
                else:
                    self.set_status(409, 'Contact already in list')

    def delete(self):
        if self.check_result:
            contact = self.json_data['contact']
            result = self.db.query(CUsers).filter(CUsers.email == contact).one_or_none()
            result_db = self.db.query(CContacts).filter(CContacts.user_id == self.check_result.uid,
                                                        CContacts.contact == result.uid).delete()
            if not result_db:
                self.set_status(404, 'Not in your contact list')
            else:
                self.db.commit()
                self.set_status(200)
                self.response['deleted_contact_id'] = result.uid
                self.response['deleted_contact_username'] = result.username
                self.write_json()

    def get(self):
        if self.check_result:
            contacts = self.db.query(CContacts, CUsers).filter(CContacts.user_id == self.check_result.uid)
            query = contacts.join(CUsers, CUsers.uid == CContacts.contact)
            records = query.all()

            ws_dict = WebSocketHandler.ws_dict
            contact_list = []

            for i in range(len(records)):
                status = 'offline'
                for key in ws_dict.keys():
                    if records[i].CUsers.uid == ws_dict[key].user_id:
                        status = 'online'
                    else:
                        status = 'offline'

                contact_list.append({'user_id': records[i].CUsers.uid,
                          'account_name': records[i].CUsers.username,
                          'email': records[i].CUsers.email,
                          'status': status})
            self.response = contact_list
            self.write_json()
