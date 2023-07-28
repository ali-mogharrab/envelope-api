from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from auth.oauth2 import get_current_user
from db import db_user, db_email
from db.database import get_db

from .schemas import UserAuth, UserBase, UserDisplay

router = APIRouter(
    prefix='/user',
    tags=['user']
)

# Create User
@router.post('', response_model=UserDisplay)
def create_user(request: UserBase, db: Session=Depends(get_db)):
    user = db_user.create_user(db, request)
    db_email.send_last_month_messages(db, user)
    return user

# Read all Users
@router.get('/all', response_model=List[UserDisplay])
def get_all_users(db: Session=Depends(get_db), current_user: UserAuth=Depends(get_current_user)):
    return db_user.get_all_users(db, current_user)

# Read one User
@router.get('/{id}')
def get_user(id: int, db: Session=Depends(get_db), current_user: UserBase=Depends(get_current_user)):
    return db_user.get_user(db, id, current_user)

# Update User
@router.put('/update/{id}')
def update_user(id: int, request: UserBase, db: Session=Depends(get_db), current_user: UserAuth=Depends(get_current_user)):
    return db_user.update_user(db, id, request, current_user)

# Delete User
@router.delete('/delete/{id}')
def delete_user(id: int, db: Session=Depends(get_db), current_user: UserAuth=Depends(get_current_user)):
    return db_user.delete_user(db, id, current_user)
