"""
 Created by zjl on 2020/9/24 0:20
"""
from flask import Flask
from flask_login import LoginManager
from app.models.base import db
from flask_mail import Mail

__author__ = 'zjl'

# from app.models.user import User

login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)

    # 配置文件写入app
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    # 将web蓝图最终注册到flask中
    register_blueprint(app)

    # 初始化flask_sqlalchemy
    db.init_app(app)
    db.create_all(app=app)

    # 初始化login
    login_manager.init_app(app=app)
    # 定义无权访问的重定向
    login_manager.login_view = 'web.login'
    # 定义重定向说明
    login_manager.login_message = '请先注册或登录'

    # 初始化mail对象
    mail.init_app(app=app)

    return app


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)