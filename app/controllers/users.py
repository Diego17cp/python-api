from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash

def create_user(session: Session, user_in: UserCreate) -> User:
    hashed = get_password_hash(user_in.password)
    user_data = user_in.model_dump(exclude={"password"})
    user = User(**user_data, hashed_pw=hashed)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
def get_user_by_email(session: Session, email: str) -> User | None:
    return session.exec(
        select(User).where(User.email == email)
    ).first()
def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)
def get_all_users(session: Session) -> list[User]:
    return session.exec(select(User)).all()