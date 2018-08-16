from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy import create_engine


POSTGRES_SERVER = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_LOGIN = 'postgres'
POSTGRES_PASS = '123'
POSTGRES_BASE = 'messengerbase'

engine = create_engine('postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                               POSTGRES_PORT,
                                                               POSTGRES_BASE))
meta = MetaData(bind=engine)

users = Table('users', meta,
              Column('uid', Integer, primary_key=True),
              Column('username', String),
              Column('password', String),
              Column('token', String))

messages = Table('messages', meta,
                 Column('mid', Integer, primary_key=True),
                 Column('to_id', Integer, ForeignKey('users.uid')),
                 Column('from_id', Integer, ForeignKey('users.uid')),
                 Column('content', String),
                 Column('dtime', Integer))

meta.create_all(engine)

