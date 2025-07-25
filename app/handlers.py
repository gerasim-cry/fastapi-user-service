from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app import schemas, crud, models
from app.models import ActionLog, User as DBUser
from app.dependencies import require_admin
from app.crud import get_user_by_email_or_username, get_logs
from typing import List
from app.schemas import LogRead

router = APIRouter()

@router.get("/users", response_model=list[schemas.UserRead])
def get_users(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(DBUser).all()

@router.get("/")
def root():
    return {"message": "Hello from FastAPI!"}

@router.post("/users", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email_or_username(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = crud.create_user(db, user)

    crud.log_action(db, new_user.id, "created user")

    created_user = crud.create_user(db, user)
    crud.create_log(db, create_user.id, "User registred")
    return crud.create_user(db, user)

@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserRead)
def read_current_user(current_user: schemas.UserRead = Depends(get_current_user)):
    return current_user

@router.get("/admin-data")
def get_admin_data(current_user: schemas.UserRead = Depends(require_admin)):
    return {"message": f"Welcome admin {current_user.username}!"}

@router.patch("/users/{user_id}", response_model=schemas.UserRead)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):

    updated_user = crud.update_user(db, user_id, user_update)

    cred.log_action(db, current_user.id, f"updated user {user_id}")

    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user = crud.update_user(db, user_id, user_update)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    crud.delete_user(db, user_id)

    crud.log_action(db, current_user.id, f"deleted user {user_id}")

    return {"message": "User deleted"}

@router.get("/logs", response_model=List[schemas.LogRead])
def read_logs(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.get_logs(db)