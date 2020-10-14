"""
 Created by zjl on 2020/10/13 21:58
"""

__author__ = 'zjl'

from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from app import mail


# 异步发送邮件
def send_async_mail(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(e)


def send_email(to, subject, template, **kwargs):
    # 邮件头，获取mail对象
    msg = Message('[虫聚]' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    # 邮件body
    msg.html = render_template(template, **kwargs)

    # 异步发送
    app = current_app._get_current_object()
    tr = Thread(target=send_async_mail, args=[app, msg])
    tr.start()