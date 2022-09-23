from email.policy import default
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

from config import DATABASE_URL

Base = declarative_base()

def connect_db():
    engine = create_engine(DATABASE_URL, connect_args={})
    session = Session(bind=engine.connect())
    return session


class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.now)


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String)
    translation = Column(String)
    topic_id = Column(Integer, ForeignKey('topics.id'))


class Phrase(Base):
    __tablename__ = 'phrases'

    id = Column(Integer, primary_key=True)
    word = Column(String)
    translation = Column(String)
    topic_id = Column(Integer, ForeignKey('topics.id'))


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    user_tg_id = Column(String)
    chat_tg_id = Column(String)
    interval = Column(String, default='cron 10')
    amount = Column(Integer, default=5)
    topic_id = Column(Integer, ForeignKey('topics.id'), default=2)
