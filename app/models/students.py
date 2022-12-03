from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from tornado_sqlalchemy import declarative_base
from sqlalchemy import Column, Integer, String
from ..config import config as c
from time import sleep

Base = declarative_base()
login = f'{c.MYSQL_USER}:{c.MYSQL_PASSWORD}'
socket = f'{c.MYSQL_HOSTNAME}:{c.MYSQL_PORT}'
engine = create_engine(f'mysql+pymysql://{login}@{socket}/{c.MYSQL_DATABASE}') # pip install PyMySQL


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    fullname = Column(String(100))
    nickname = Column(String(100))

    def __repr__(self):
        return f"<User(fullname='{self.fullname}', nickname='{self.nickname}')>"


def init_db():
    loop = True
    while loop:
        try:
            Base.metadata.create_all(engine)
            loop = False
        except OperationalError as e:
            print(e)
            sleep(2)
