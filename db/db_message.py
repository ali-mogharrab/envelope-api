import datetime

from sqlalchemy.orm.session import Session

from routers.schemas import MessageBase
from fastapi import HTTPException, status
from .models import DbMessage


def create_message(db: Session, request: MessageBase, current_user):
    # we consider that the user with id 1 is admin
    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Only admin can update a message.'
        )

    new_message = DbMessage(
        subject=request.subject,
        body=request.body,
        timestamp=datetime.datetime.now()
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


def get_all_messages(db: Session):
    return db.query(DbMessage).all()


def get_message(db: Session, id: int):
    message = db.query(DbMessage).filter(DbMessage.id==id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Message with id {id} not found!'
        )
    return message


def update_message(db: Session, id: int, request: MessageBase, current_user):
    # we consider that the user with id 1 is admin
    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Only admin can update a message.'
        )

    message = db.query(DbMessage).filter(DbMessage.id==id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Message with id {id} not found!'
        )

    message.update({
        DbMessage.subject: request.subject,
        DbMessage.body: request.body
    })
    db.commit()
    return 'Message updated.'


def delete_message(db: Session, id: int, current_user):
    # we consider that the user with id 1 is admin
    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Only admin can update a message.'
        )

    message = db.query(DbMessage).filter(DbMessage.id==id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Message with id {id} not found!'
        )

    db.delete(message)
    db.commit()
    return 'message deleted!'
