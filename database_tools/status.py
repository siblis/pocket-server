from sqlalchemy import create_engine
from database_tools.db_connect import POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_BASE
from database_tools.alchemy import CUserStatus
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                       POSTGRES_PORT,
                                                       POSTGRES_BASE))

Session = sessionmaker(bind=engine)
session = Session()

session.add_all([CUserStatus(status_name='online'),
                 CUserStatus(status_name='offline'),
                 CUserStatus(status_name='banned'),
                 CUserStatus(status_name='not confirmed'),
                 ])
session.commit()
