from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from db import db_message
from db.database import get_db
from typing import List
from .schemas import MessageBase, MessageDisplay, UserAuth
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/message',
    tags=['message']
)

# Create Message
@router.post('', response_model=MessageDisplay)
def create_message(request: MessageBase, db: Session=Depends(get_db), current_user: UserAuth=Depends(get_current_user)):
    return db_message.create_message(db, request, current_user)

# Read all Messages
@router.get('/all', response_model=List[MessageDisplay])
def get_all_messages(db: Session=Depends(get_db), current_user: UserAuth=Depends(get_current_user)):
    return db_message.get_all_messages(db)

# Read one Message
@router.get('/{id}')
def get_message(id: int, db: Session=Depends(get_db), current_user: UserAuth=Depends(get_current_user)):
    return db_message.get_message(db, id)

# Update Message
@router.put('/update/{id}')
def update_message(id: int, request: MessageBase, db: Session=Depends(get_db), current_user: UserAuth=Depends(get_current_user)):
    return db_message.update_message(db, id, request, current_user)

# Delete Message
@router.delete('/delete/{id}')
def delete_message(id: int, db: Session=Depends(get_db), current_user: UserAuth=Depends(get_current_user)):
    return db_message.delete_message(db, id, current_user)
