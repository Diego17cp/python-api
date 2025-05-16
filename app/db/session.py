from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlmodel import SQLModel, create_engine, Session

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)