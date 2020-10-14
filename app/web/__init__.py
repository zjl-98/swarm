"""
 Created by zjl on 2020/9/24 0:20
"""
# 只是注册到web蓝图，需要在app的init文件中最终写入
from flask import Blueprint

__author__ = 'zjl'


web = Blueprint('web', __name__)

from app.web import main
from app.web import search
from app.web import wallpaper
from app.web import auth