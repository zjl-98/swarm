"""
 Created by zjl on 2020/9/26 20:39
"""
from flask import render_template, request

from app import db
from app.forms.search import SearchForm
from app.libs.enums import pending_str
from app.view_models.search import classify
from app.web import web

__author__ = 'zjl'


@web.route('/search')
def search():
    form = SearchForm(request.args)
    keyword, status = request.args.get('q').strip(), request.args.get('type')
    movie_data = []
    if form.validate():
        search_type = form.type.data
        q = form.q.data.strip()
        # 根据search_type的类型区分定位查询
        movie_data = classify(search_type, q)

    return render_template('search_result.html', movies=movie_data,
                           keyword=keyword, total=len(movie_data) or 0,
                           type=pending_str(int(status)))