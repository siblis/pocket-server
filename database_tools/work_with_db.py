from sqlalchemy.orm import sessionmaker
from database_tools.alchemy import CUsers, CContacts, CMessages
from database_tools.init import engine
from datetime import datetime

dtime = datetime.now()


class ServerStorage:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        self.session = session

    def __commit(self):
        self.session.commit()

    def _get_client_by_username(self, username):
        """ Возвращает клиента с username """
        client = self.session.query(CUsers).filter(CUsers.username == username).first()
        return client

    def add_user(self, username, password, email, token):   # CUsers
        verify = CUsers(username=username, password=password, email=email, token=token)
        result = self.session.query(CUsers).filter((CUsers.Name == username),
                                                   (CUsers.Password == password))
        if result.count() > 0:
            pass
        else:
            self.session.add(verify)
            self.__commit()

    def add_history(self, from_id, to_id, message):    # CMessages
        """ Добавление в историю """
        # client = self._get_client_by_username(username)
        if from_id and to_id:
            history = CMessages(message=message, from_id=from_id, to_id=to_id, dtime=dtime)
            self.session.add(history)
            self.__commit()
        else:
            pass

    def add_contact_list(self, uid, contact):    # CContacts
        """ Добавление в контактный лист"""
        client = self._get_client_by_username(contact)
        if uid and client:
            contact_list = CContacts(user_id=uid, contact=client.uid)
            self.session.add(contact_list)
            self.__commit()
        else:
            pass

    def delete_user(self, username, password):
        pass

    def remove_user_from_contact(self, username):
        pass