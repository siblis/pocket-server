from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database_tools.db_config import POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_BASE

db_address = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                                POSTGRES_PORT,
                                                                POSTGRES_BASE)
engine = create_engine(db_address)
Session = sessionmaker(bind=engine)

Base = declarative_base()


def connect(dbname):
    db_address = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                                    POSTGRES_PORT,
                                                                    dbname)
    engine = create_engine(db_address)
    return engine
