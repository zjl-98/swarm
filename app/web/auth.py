"""
 Created by zjl on 2020/10/13 13:24
"""

__author__ = 'zjl'

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from app import db
from app.libs.email import send_email
from app.models.user import User
from app.forms.auth import RegisterForm, LoginForm
from app.web import web


@web.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data, status=1).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if not next or next[0] != '/':
                return redirect(url_for('web.index'))
            return redirect(next)
    return render_template('auth/login.html', form=form)


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data, status=0).first()
        if not user:
            with db.auto_commit():
                user = User()
                user.set_attrs(form.data)
                db.session.add(user)
            user = User.query.filter_by(email=form.email.data, status=0).first()
        send_email(form.email.data,
                   '验证您的邮箱',
                   'email/check_email.html', user=user,
                   token=user.generate_token_email(user.id))
        flash('一封新邮件已发送到' + form.email.data + '，请留意查收')
    return render_template('auth/register.html', form=form)


@web.route('/validate/register/<token>')
def validate_register(token):
    user = User()
    success = user.check_token_email(token)
    if not success:
        return '验证失败，请重新验证'
    return redirect(url_for('web.login'))


@web.route('/forget', methods=['GET', 'POST'])
def forget_password_request():
    return ''


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))