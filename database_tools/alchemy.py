from sqlalchemy import Column, Integer, Unicode, UniqueConstraint, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

CBase = declarative_base()


class CUsers(CBase):
    __tablename__ = 'users'

    uid = Column(Integer(), primary_key=True)
    username = Column(Unicode())
    password = Column(Unicode())
    email = Column(Unicode())
    token = Column(Unicode())
    check_1 = UniqueConstraint('username')
    check_2 = UniqueConstraint('email')

    def __repr__(self):
        return 'CUsers<uid = %d, login = %s' % (self.uid, self.username)


class CMessages(CBase):
    __tablename__ = 'messages'

    mid = Column(Integer(), primary_key=True)
    message = Column(Unicode())
    from_id = Column(Integer(), ForeignKey('users.uid'))
    to_id = Column(Integer(), ForeignKey('users.uid'))
    dtime = Column(Unicode())

    p_from_id = relationship('CUsers', foreign_keys=[from_id])
    p_to_id = relationship('CUsers', foreign_keys=[to_id])

    def __repr__(self):
        return 'CMessages<mid = %d, from_id = %d, to_id = %d, message = %s' % (
            self.mid, self.from_id, self.to_id, self.message)


class CContacts(CBase):
    __tablename__ = 'contacts'
    cid = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.uid'))
    contact = Column(Integer(), ForeignKey('users.uid'))

    def __repr__(self):
        return 'CContacts<cid = %d, user_id = %d, contact = %d' % (self.cid, self.user_id, self.contact)
