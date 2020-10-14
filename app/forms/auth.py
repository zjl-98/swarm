"""
 Created by zjl on 2020/10/13 16:06
"""

__author__ = 'zjl'

from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError

from app import db
from app.models.user import User


class RegisterForm(Form):
    """ 注册信息项验证 """
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空， 请输入你的密码'),
                                         Length(6, 32)])
    nickname = StringField(validators=[DataRequired(),
                                       Length(2, 10, message='昵称至少两个字符，最多10个字符')])

    # 自定义邮箱邮箱验证器
    def validate_email(self, field):
        if User.query.filter_by(email=field.data, status=1).first():
            raise ValidationError('该邮箱已被注册')

    # 自定义邮箱邮箱验证器
    def validate_nickname(self, field):
        user = User()
        user.del_data(value=field.data)
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('该昵称已被注册')


class EmailForm(Form):
    """ 邮箱验证 """
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])


class LoginForm(EmailForm):
    """ 登录信息项验证 """
    password = PasswordField(validators=[DataRequired(message='密码不能为空， 请输入你的密码'),
                                         Length(6, 32)])