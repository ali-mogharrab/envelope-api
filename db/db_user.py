from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from routers.schemas import UserBase

from .hashing import Hash
from .models import DbUser


def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session, current_user):
    # we consider that the user with id 1 is admin
    if current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Only admin can get all users.'
        )

    return db.query(DbUser).all()


def get_user(db: Session, id: int, current_user):
    user = db.query(DbUser).filter(DbUser.id==id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {id} not found!'
    )
    # we consider that the user with id 1 is admin
    if current_user.id != user.id and current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Only user owner can get the user.'
        )

    return user


# For authentication
def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username==username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with username {username} not found!'
        )
    return user


def update_user(db: Session, id: int, request: UserBase, current_user):
    user = db.query(DbUser).filter(DbUser.id==id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {id} not found!'
        )

    # we consider that the user with id 1 is admin
    if current_user.id != user.first().id and current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Only user owner can update the user.'
        )

    user.update({
        DbUser.username: request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password)
    })
    db.commit()
    return 'User updated.'


def delete_user(db: Session, id: int, current_user):
    user = db.query(DbUser).filter(DbUser.id==id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {id} not found!'
        )

    # we consider that the user with id 1 is admin
    if current_user.id != user.id and current_user.id != 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Only user owner can delete the user.'
        )

    db.delete(user)
    db.commit()
    return 'User deleted.'
