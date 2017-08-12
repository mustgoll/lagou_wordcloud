from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re
engine = create_engine("mysql+pymysql://root:abcd1234@localhost/lagou?charset=utf8",encoding='utf-8', echo=False)

Base = declarative_base()  # 生成orm基类


class User(Base):
    __tablename__ = 'info'  # 表名
    id = Column(Integer, primary_key=True)
    city=Column(String(32))
    name = Column(String(32))
    createTime = Column(String(64))
    company = Column(String(64))
    salary = Column(String(64))
    fuli = Column(String(64))
    workyear = Column(String(64))
    edu = Column(String(64))
    link = Column(String(64))
    fied = Column(String(64))
    detail=Column(String(4000))



Session_class=sessionmaker(bind=engine)
Session=Session_class()
def totle_str():
    info=Session.query(User)
    str=''
    for x in info:
        if x.detail:
            str+=x.detail
    return str
if __name__=='__main__':
    print(totle_str())