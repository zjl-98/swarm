"""
 Created by zjl on 2020/10/13 13:58
"""

__author__ = 'zjl'

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.models.base import Base, db


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(24), nullable=False)
    _password = Column('password', String(128), nullable=False)
    email = Column(String(50), unique=True, nullable=False)

    @property
    def password(self):
        """ 定义方法为属性方法，更改_password的值 """
        return self._password

    @password.setter
    def password(self, raw):
        """ 加密密码 """
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        """ 检测用户输入的密码与数据库保存的密码是否一致 """
        return check_password_hash(self._password, raw)

    def get_id(self):
        return self.id

    @staticmethod
    def generate_token_email(uid, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': uid}).decode('utf-8')

    @staticmethod
    def check_token_email(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.status = 1
        return True

    @staticmethod
    def del_data(value):
        user = User.query.filter_by(nickname=value, status=0).first()
        if user:
            with db.auto_commit():
                db.session.delete(user)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))