from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.db.session import SessionLocal
from app.utils.security import verify_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    email = verify_token(token, db)
    if not email:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid token",
        )
    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "User not found",
        )
    return user
