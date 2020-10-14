"""
 Created by zjl on 2020/10/3 23:09
"""

__author__ = 'zjl'
from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Wallpaper(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    index = Column(String(20))
    title = Column(String(100))  # 名字
    count = Column(Integer)  # 图片页数
    resolving = Column(String(200))  # 标签集

    @classmethod
    def has_wallpaper_of_index(cls, wid):
        wallpaper_data = cls.query.filter(cls.index == wid).first()
        return wallpaper_data