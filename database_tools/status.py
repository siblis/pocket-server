from database_tools.alchemy import CUserStatus
from sqlalchemy.orm import sessionmaker


def add_status(engine):

    Session = sessionmaker(bind=engine)
    session = Session()

    session.add_all([CUserStatus(status_name='online'),
                     CUserStatus(status_name='offline'),
                     CUserStatus(status_name='banned'),
                     CUserStatus(status_name='not confirmed'),
                     ])
    session.commit()
