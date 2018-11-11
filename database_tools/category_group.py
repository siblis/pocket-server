from database_tools.alchemy import CCategoryGroup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_tools.db_config import POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_BASE

db_address = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                                POSTGRES_PORT,
                                                                POSTGRES_BASE)

engine = create_engine(db_address)
Session = sessionmaker(bind=engine)
session = Session()

session.add_all([CCategoryGroup(category_name='Single'),
                 CCategoryGroup(category_name='Multi')])
