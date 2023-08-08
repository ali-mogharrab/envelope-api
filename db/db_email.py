import datetime
import os
import smtplib
from email.message import EmailMessage
from smtplib import SMTPRecipientsRefused
import dateutil.relativedelta
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from routers.schemas import EmailAllBase, EmailBase

from .models import DbMessage, DbUser


def send_email(message, user):
    email_address = os.environ['EMAIL_HOST_USER']
    email_password = os.environ['EMAIL_HOST_PASSWORD']

    # create email
    msg = EmailMessage()
    msg['Subject'] = message.subject
    msg['From'] = email_address
    msg['To'] = user.email
    msg.set_content(
       f"""\
        Hi Dear {user.username}
        You've got a new message.
        Message : {message.body}
        """
    )

    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        try:
            smtp.send_message(msg)
        except SMTPRecipientsRefused:
            raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'{user.email} is not a valid email address.'
        )

    return "Email successfully sent."


def send_message(db: Session, request: EmailBase, current_user):
    # we consider that the user with id 1 is admin
    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Only admin can send a message.'
        )

    user = db.query(DbUser).filter(DbUser.id==request.user_id).first()
    message = db.query(DbMessage).filter(DbMessage.id==request.message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Message with id {id} not found!'
        )

    condition = send_email(message, user)

    message.users.append(user)
    db.commit()

    return{
        'message_subject': message.subject,
        'message_body': message.body,
        'username': user.username,
        'Condition': condition,
    }


def send_message_to_all(db: Session, request: EmailAllBase, current_user):
    # we consider that the user with id 1 is admin
    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Only admin can send a message.'
        )

    users = db.query(DbUser).all()
    message = db.query(DbMessage).filter(DbMessage.id==request.message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Message with id {id} not found!'
        )

    for user in users:
        send_email(message, user)
        message.users.append(user)
    db.commit()

    return{
        'message_subject': message.subject,
        'message_body': message.body,
        'Condition': "Emails successfully sent."
    }


def send_last_month_messages(db: Session, user: DbUser):
    now = datetime.datetime.now()
    last_month = now + dateutil.relativedelta.relativedelta(months=-1)
    messages = db.query(DbMessage).filter(DbMessage.timestamp>=last_month).all()
    for message in messages:
        try:
            send_email(message, user)
        except:
            pass
        message.users.append(user)
    db.commit()
