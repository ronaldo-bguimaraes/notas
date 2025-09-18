import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

local_url = "postgresql://postgresql:postgres@localhost:5432/notas"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", local_url)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
