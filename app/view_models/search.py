"""
 Created by zjl on 2020/9/28 15:59
"""
from flask import current_app

from app import db
from app.models.movie import Movie
from app.spider.douban_movie_search import DouBanMovieSearchSpider

__author__ = 'zjl'


def classify(search_type, q):
    if search_type == current_app.config['MOVIE']:
        # 判断数据库中是否能关键字查询
        movie_data = Movie.get_movie_by_keyword(q)
        if not movie_data:
            movie_search = DouBanMovieSearchSpider()
            movie_data = movie_search.search_data(q)
            # 网站爬取数据,保存数据库
            for data in movie_data:
                if not Movie.has_movie_of_vid(data['vid']):
                    movie = Movie()
                    with db.auto_commit():
                        movie.set_attrs(data)
                        db.session.add(movie)
        return movie_data
    if search_type == current_app.config['VIDEO']:
        # 短视频
        pass
    if search_type == current_app.config['JOB']:
        # 招聘
        pass
    if search_type == current_app.config['WALLPAPER']:
        # 壁纸
        pass