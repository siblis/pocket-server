from sqlalchemy import Column, Integer, Unicode, UniqueConstraint, ForeignKey, MetaData, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

CBase = declarative_base()


class CUsers(CBase):
    __tablename__ = 'users'

    uid = Column(Integer(), primary_key=True)
    username = Column(Unicode())
    password = Column(Unicode())
    email = Column(Unicode())
    token = Column(Unicode())
    tokenexp = Column(DateTime())
    check_1 = UniqueConstraint('username')
    check_2 = UniqueConstraint('email')
    status_id = Column(Integer(), ForeignKey('status_of_user.usid'))

    def __repr__(self):
        return 'CUsers: uid = %d, account_name = %s, email = %s' % (self.uid, self.username, self.email)


class CUserStatus(CBase):
    __tablename__ = 'status_of_user'

    usid = Column(Integer(), primary_key=True)
    status_name = Column(Unicode())

    def __repr__(self):
        return 'CUserStatus: usid = %d, status = %s' % (self.usid, self.status_name)


class CUserRoles(CBase):
    __tablename__ = 'user_roles'

    roleid = Column(Integer(), primary_key=True)
    role_name = Column(Unicode())

    def __repr__(self):
        return 'CUserStatus: roleid = %d, role_name = %s' % (self.roleid, self.role_name)


class CMessages(CBase):
    __tablename__ = 'messages'

    mid = Column(Integer(), primary_key=True)
    message = Column(Unicode())
    group_id = Column(Integer(), ForeignKey('groups.gid'))
    from_id = Column(Integer(), ForeignKey('users.uid'))
    to_id = Column(Integer(), ForeignKey('users.uid'))
    dtime = Column(Unicode())

    p_group_id = relationship('CGroups', foreign_keys=[group_id])
    p_from_id = relationship('CUsers', foreign_keys=[from_id])
    p_to_id = relationship('CUsers', foreign_keys=[to_id])

    def __repr__(self):
        # return 'CMessages<mid = %d, from_id = %d, to_id = %d, message = %s' % (
        #     self.mid, self.from_id, self.to_id, self.message)
        return f'CMessages<mid = {self.mid}, group_id={self.group_id}, from_id = {self.from_id}, to_id = {self.to_id},' \
               f' message = {self.message}, dtime = {self.dtime}'


class CContacts(CBase):
    __tablename__ = 'contacts'
    cid = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.uid'))
    contact = Column(Integer(), ForeignKey('users.uid'))

    def __repr__(self):
        return 'CContacts<cid = %d, user_id = %d, contact = %d' % (self.cid, self.user_id, self.contact)
    
#------------------------------------------------
class CGroups(CBase):
        __tablename__ = 'groups'
        gid = Column(Integer(), primary_key=True)
        creation_date = Column(DateTime, default=datetime.datetime.utcnow())
        groupname = Column(Unicode())
        creater_user_id = Column(Integer())
        def __repr__(self):
            return 'CGroups<gid = %d, name = %d' % (self.gid, self.group_name)


class CGroupsUsers(CBase):
    __tablename__ = 'user_groups'

    user_id = Column(Integer(), ForeignKey('users.uid'),primary_key=True)
    group_id = Column(Integer(), ForeignKey('groups.gid'), primary_key=True)
    def __repr__(self):
        return f'CGroupsUsers<user_id = {self.user_id}, group_id = {self.group_id}'


# class CMessagesChat(CBase):
#     __tablename__ = 'messages_chat'
#
#     mid = Column(Integer(), primary_key=True)
#     message = Column(Unicode())
#     group_id = Column(Integer(), ForeignKey('groups.gid'))
#     from_id = Column(Integer(), ForeignKey('users.uid'))
#     to_id = Column(Integer(), ForeignKey('users.uid'))
#     dtime = Column(DateTime())
#
#     p_group_id = relationship('CGroups', foreign_keys=[group_id])
#     p_from_id = relationship('CUsers', foreign_keys=[from_id])
#     p_to_id = relationship('CUsers', foreign_keys=[to_id])
#
#     def __repr__(self):
#         return f'CMessages<mid = {self.mid}, group_id={self.group_id}, from_id = {self.from_id}, to_id = {self.to_id}, message = {self.message}, dtime = {self.dtime}'
