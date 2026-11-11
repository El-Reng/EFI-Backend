from sqlmodel import Session, create_engine

sqlite_url = "sqlite:///./db_local.db"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


def get_db():
    with Session(engine) as session:
        yield session
