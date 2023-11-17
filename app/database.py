import os
from datetime import datetime as dt
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, DeclarativeBase


SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:postgres@localhost:5432/tric-itpc-db'


engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class Service(Base):
    """Таблица service"""
    __tablename__ = "service"

   # id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, primary_key=True, unique=True)
    state = Column(String)
    description = Column(Text)
    saved_at = Column(DateTime, default=dt.now())


class StateHistory(Base):
    """Таблица state_history"""
    __tablename__ = "state_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String, ForeignKey('service.name', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    state = Column(String)
    updated_at = Column(DateTime, default=dt.now())
    downtime = Column(DateTime)
    uptime = Column(DateTime)





Base.metadata.create_all(bind=engine)