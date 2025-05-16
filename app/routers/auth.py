from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.schemas.user import UserCreate, UserRead
from app.schemas.token import Token
from app.models.user import User
from app.controllers.users import get_user_by_email
from app.utils.dependencies import get_db
from app.utils.security import (
    create_access_token,
    verify_password,
    get_password_hash,
)

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED, summary="Register a new user")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_pw=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.post("/login", response_model=Token, summary="Login and get access token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_pw):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(sub=user.email, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}