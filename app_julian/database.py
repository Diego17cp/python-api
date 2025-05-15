from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://api_py_euub_user:MxI7HBiTPsSXRWhcjHqiUs8UrngQMWar@dpg-d0iviaidbo4c738tvaa0-a.oregon-postgres.render.com:5432/api_py_euub"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

