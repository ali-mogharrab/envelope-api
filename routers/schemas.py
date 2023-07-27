from datetime import datetime

from pydantic import BaseModel


# -----------------User------------------

class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        orm_mode = True


# ----------------Message-----------------

class MessageBase(BaseModel):
    subject: str
    body: str


class MessageDisplay(BaseModel):
    id: int
    subject: str
    body: str
    timestamp: datetime
    class Config:
        orm_mode = True


# -----------------Email------------------

class EmailBase(BaseModel):
    message_id: int
    user_id: int


class EmailDisplay(BaseModel):
    message_subject: str
    username: str
    class Config:
        orm_mode = True


class EmailAllBase(BaseModel):
    message_id: int


class EmailAllDisplay(BaseModel):
    message_subject: str
    message_body: str
    class Config:
        orm_mode = True


# -----------------Auth------------------

class UserAuth(BaseModel):
    id: int
    username: str
    email: str
