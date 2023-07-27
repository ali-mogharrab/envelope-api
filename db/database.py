import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./envelope.db'
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{os.environ['DATABASE_PASSWORD']}@localhost/{os.environ['DATABASE_NAME']}"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True, connect_args={"check_same_thread": False})
engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
