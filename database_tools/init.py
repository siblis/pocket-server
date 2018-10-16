from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, DateTime
from sqlalchemy import create_engine
from database_tools.db_connect import POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_BASE

engine = create_engine(
    'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                       POSTGRES_PORT,
                                                       POSTGRES_BASE))
meta = MetaData(bind=engine)

users = Table('users', meta,
              Column('uid', Integer, primary_key=True),
              Column('username', String),
              Column('password', String),
              Column('email', String),
              Column('token', String),
              Column('tokenexp', DateTime))

messages = Table('messages', meta,
                 Column('mid', Integer, primary_key=True),
                 Column('to_id', Integer, ForeignKey('users.uid')),
                 Column('from_id', Integer, ForeignKey('users.uid')),
                 Column('message', String),
                 Column('dtime', DateTime))

contacts = Table('contacts', meta,
                 Column('cid', Integer, primary_key=True),
                 Column('user_id', Integer, ForeignKey('users.uid')),
                 Column('contact', Integer, ForeignKey('users.uid')))

#-------------------------------------------------------------------
groups = Table('groups', meta,
              Column('uid', Integer, primary_key=True),
              Column('groupname', String),
              Column('creation_date', DateTime),
              Column('creater_user_id'), Integer)

user_groups = Table('user_groups', meta,
              Column('userid', ForeignKey('users.uid')),
              Column('groupid', ForeignKey('groups.gid')))

#---------------------------------------------------roles
user_roles = Table('user_roles', meta,
              Column('roleid', primary_key=True),
              Column('role_name'))

meta.create_all(engine)
