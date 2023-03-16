import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,DateTime,Float,Boolean
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///database.db', echo=False,connect_args={'check_same_thread': False})


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False,unique=True)
    password = Column(String(100), nullable=False)

class Images(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    image = Column(String(100), nullable=False)
    


Base.metadata.create_all(engine)