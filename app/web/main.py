"""
 Created by zjl on 2020/9/24 23:02
"""
import json
import re
import time

from flask import render_template, request, jsonify

from app import db
from app.models.movie import Movie
from app.models.movie_top import MovieTop
from app.spider.douban_movie_detail import DouBanMovieDetailSpider
from app.spider.douban_movie_top250 import DouBanMovieTopSpider
from app.view_models.movie import MovieViewModel
from app.view_models.movie_top import MovieTopCollection, MovieTopViewModel
from app.web import web

__author__ = 'zjl'


@web.route('/')
def index():
    recent = []
    if not MovieTop.is_exists_use():
        # 网站爬取数据,保存数据库
        movie_data = DouBanMovieTopSpider()
        for data in movie_data.movie_top250:
            movie_top = MovieTop()
            with db.auto_commit():
                movie_top.set_attrs(data)
                db.session.add(movie_top)

    # 数据库获取数据
    recent = MovieTop.get_movie_data()
    return render_template('index.html', recent=recent)


@web.route('/movie/<vid>/detail')
def movie_detail(vid):
    detail_data = {}
    movie = Movie()
    movie_data = movie.has_movie_of_vid(vid)
    if not movie_data:
        # 表示该片子是top250
        movie_top_data = MovieTop.get_movie_of_vid(vid)
        search = re.compile(r'(.*?)\s+\/')
        name = re.search(search, movie_top_data.name).group(1)
        with db.auto_commit():
            movie = Movie()
            movie.vid = movie_top_data.vid
            movie.name = name
            movie.img = movie_top_data.img
            movie.time = movie_top_data.release_time
            movie.score = movie_top_data.score
            movie.evaluators_count = movie_top_data.evaluators_count
            db.session.add(movie)
            movie_data = movie
        detail = DouBanMovieDetailSpider(vid)
        detail_data = detail.movie_detail()
        movie = Movie()
        movie.update_data(vid, detail_data)
    else:
        if not movie_data.length:
            detail = DouBanMovieDetailSpider(vid)
            detail_data = detail.movie_detail()
            movie = Movie()
            movie.update_data(vid, detail_data)
    movie = MovieViewModel(movie_data, detail_data)

    return render_template('movie_detail.html', movie=movie.movie_detail)


@web.route('/movie/top250', methods=['POST'])
def movie_top():
    page = request.form.get('page')
    # 通过数据库获取的数据是模型类型，传回模型内部，转化成dict类型
    movie_data = MovieTop.get_movie_page(page)
    if movie_data:
        recent = [movie.to_dict() for movie in movie_data]
        # 无法返回list，使用jsonify返回元组
        return jsonify(recent), 200
    else:
        return jsonify({})