from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from auth.oauth2 import get_current_user
from db import db_email
from db.database import get_db
from routers.schemas import UserAuth

from .schemas import EmailAllBase, EmailAllDisplay, EmailBase, EmailDisplay

router = APIRouter(
    prefix='/email',
    tags=['email']
)


@router.post('', response_model=EmailDisplay)
def send_email(request: EmailBase, db: Session=Depends(get_db), current_user: UserAuth=Depends(get_current_user)):
    return db_email.send_message(db, request, current_user)


@router.post('/all', response_model=EmailAllDisplay)
def send_email_to_all(request: EmailAllBase, db: Session=Depends(get_db), current_user: UserAuth=Depends(get_current_user)):
    return db_email.send_message_to_all(db, request, current_user)
