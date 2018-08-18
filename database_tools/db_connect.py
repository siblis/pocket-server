from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_SERVER = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_LOGIN = 'postgres'
POSTGRES_PASS = '123'
POSTGRES_BASE = 'messengerbase'

db_address = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                                POSTGRES_PORT,
                                                                POSTGRES_BASE)
engine = create_engine(db_address)
Session = sessionmaker(bind=engine)

Base = declarative_base()
