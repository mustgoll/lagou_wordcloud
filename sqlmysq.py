import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

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


Base.metadata.create_all(engine)
Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
def addinfo(kw):
    try:
        Session = Session_class()  # 该出一定要把实例对象加上去否则写入重复的数据后会导致回滚从而暂停程序
        user_obj = User(id=kw['onlyid'],city=kw['city'],name=kw['name'], company=kw['company'],createTime=kw['createTime'],salary=kw['salary'],fuli=kw['fuli'],workyear=kw['workyear'],edu=kw['edu'],link=kw['link'],fied=kw['fied'],detail=kw['detail']
                        )  # 生成创建的数据对象
        Session.add(user_obj)  # 把要创建的数据对象添加到这个session里， 一会统一创建
        Session.commit()
        print('onlyid:%s已写入数据库' % kw['onlyid'])
    except sqlalchemy.exc.IntegrityError as e:
        print('onlyid:%s已经存在' % kw['onlyid'])
        Session.close()


