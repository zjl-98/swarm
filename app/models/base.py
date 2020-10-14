"""
 Created by zjl on 2020/9/26 0:27
"""
from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger

__author__ = 'zjl'


# contextmanager模拟管理器拼接代码
class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


db = SQLAlchemy()


class Base(db.Model):
    # 生成数据库时不生成它
    __abstract__ = True

    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=0)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        # 动态语言，如果key在其中，就将其对应值赋值过去
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)