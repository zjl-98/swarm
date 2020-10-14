"""
 Created by zjl on 2020/9/26 0:00
"""
from flask import current_app
from sqlalchemy import Column, Integer, String, Float, desc, asc
from datetime import datetime
from app.models.base import Base, db

__author__ = 'zjl'


class MovieTop(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    vid = Column(Integer, unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    title = Column(String(50), nullable=False)
    url = Column(String(200), nullable=False)
    img = Column(String(200), nullable=False)
    human_data = Column(String(200), nullable=False)
    release_time = Column(String(100), nullable=False)
    show_country = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    ranking = Column(Integer, nullable=False, default=0)
    score = Column(Float, nullable=False, default=0)
    evaluators_count = Column(Integer, nullable=False, default=0)

    def get_id(self):
        return self.id

    # 判断数据库是否存在数据且数据有效
    @staticmethod
    def is_exists_use():
        """ 判断数据有且有效 """
        movie_data = MovieTop.query.filter_by(status=1).first()
        now_datetime = int(datetime.now().timestamp())
        if movie_data and movie_data.create_time + 604800 > now_datetime:
            return True
        else:
            with db.auto_commit():
                MovieTop.query.filter_by(status=1).delete()
            return False

    # 获取前25条数据
    @staticmethod
    def get_movie_data():
        movie_data = MovieTop.query.filter_by(status=1).order_by(
            asc(MovieTop.ranking)).limit(current_app.config['MOVIE_SEARCH_PAGE_COUNT']).all()
        return movie_data

    # 根据页数获取数据
    @staticmethod
    def get_movie_page(page):
        page = int(page)
        movie_data = MovieTop.query.filter_by(status=1).order_by(
            asc(MovieTop.ranking)).offset(
            current_app.config['MOVIE_SEARCH_PAGE_COUNT'] * page).limit(
            current_app.config['MOVIE_SEARCH_PAGE_COUNT']).all()
        return movie_data

    # 将对象转换为字典数据
    def to_dict(self):
        return {
            'id': self.id,
            'vid': self.vid,
            'name': self.name,
            'title': self.title,
            'url': self.url,
            'img': self.img,
            'human_data': self.human_data,
            'release_time': self.release_time,
            'show_country': self.show_country,
            'type': self.type,
            'ranking': self.ranking,
            'score': self.score,
            'evaluators_count': self.evaluators_count
        }

    @classmethod
    def get_movie_of_vid(cls, vid):
        movie_data = cls.query.filter(cls.vid == vid).first()
        return movie_data