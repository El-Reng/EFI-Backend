import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql+psycopg://",
            1,
        )
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

else:
    sqlite_url = "sqlite:///./db_local.db"

    engine = create_engine(
        sqlite_url,
        connect_args={"check_same_thread": False},
    )


def get_db():
    with Session(engine) as session:
        yield session
