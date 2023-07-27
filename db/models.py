from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .database import Base

user_messages = Table('user_messages', Base.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('message_id', ForeignKey('message.id'), primary_key=True),
    Column('send_time', DateTime)
)


class DbUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    messages = relationship('DbMessage', secondary='user_messages', back_populates='users')


class DbMessage(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String)
    body = Column(String)
    timestamp = Column(DateTime)
    users = relationship('DbUser', secondary='user_messages', back_populates='messages')
