from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from core.security import hash_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email== email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user_data: UserCreate):
    # check for existing
    if get_user_by_email(db, user_data.email):
        return None

    # hash & save
    hashed_pw = hash_password(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pw,
        role="customer"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
