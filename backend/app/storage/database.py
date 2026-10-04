from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker


BASE_DIR=Path(__file__).resolve().parent
DATABASE_PATH=BASE_DIR/"doculens.db"

DATABASE_URL=f"sqlite:///{DATABASE_PATH}"

engine=create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

SessionLocal=sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


class Base(DeclarativeBase):
    pass