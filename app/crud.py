from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from app.models import ActionLog

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user_by_email_or_username(db: Session, email_or_username: str):
    return db.query(models.User).filter(
        (models.User.email == email_or_username) | (models.User.username == email_or_username)
    ).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None

    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()

def create_log(db: Session, user_id: int, action: str):
    log = ActionLog(user_id=user_id, action=action)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_logs(db: Session):
    return db.query(ActionLog).all()

def log_action(db: Session, user_id: int, action: str):
    log_entry = models.ActionLog(user_id=user_id, action=action)
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry

def cteate_user_if_not_exists(db: Session, user: schemas.UserCreate):
    existing_user = db.query(models.User).filter_by(username=user.username).filter()
    if existing_user:
        return existing_user
    return create_user(db, user)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()