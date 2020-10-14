"""
 Created by zjl on 2020/10/5 10:36
"""

__author__ = 'zjl'

import os

from flask import request, render_template, send_from_directory, current_app

from app import db
from app.libs.check_dir import is_exists_file
from app.libs.win_size import get_size
from app.models.wallpaper import Wallpaper
from app.models.wallpaper_img import WallpaperImg
from app.spider.wallpaper_detail import WallpaperDetail
from app.spider.wallpaper_download import WallpaperDownloadSpider
from app.spider.wallpaper_top import WallpaperTopSpider
from app.web import web


@web.route('/wallpaper/top', methods=['GET'])
def wallpaper_top():
    wallpaper = WallpaperTopSpider()
    wallpapers = wallpaper.wallpaper_top
    return render_template('wallpaper.html', wallpapers=wallpapers)


@web.route('/wallpaper/<wid>/detail', methods=['GET'])
def wallpaper_detail(wid):
    wallpaper = Wallpaper()
    wallpaper_data = wallpaper.has_wallpaper_of_index(wid)
    if wallpaper_data:
        wallpaper_img = WallpaperImg()
        wallpaper_img_data = wallpaper_img.get_wallpaper_img(wallpaper_data.id)
        size_list = take_size(wallpaper_data.resolving)
    else:
        wallpaper_spider = WallpaperDetail(wid=wid)
        wallpaper_data = wallpaper_spider.detail
        size_list = take_size(wallpaper_data['resolving'])
        wallpaper = Wallpaper()
        with db.auto_commit():
            wallpaper.set_attrs(wallpaper_data)
            db.session.add(wallpaper)

        wallpaper_img_data = wallpaper_spider.img_spider(wallpaper.id)
        for data in wallpaper_img_data:
            wallpaper_img = WallpaperImg()
            with db.auto_commit():
                wallpaper_img.set_attrs(data)
                db.session.add(wallpaper_img)

    win_size = get_size()
    return render_template('wallpaper_detail.html', wallpaper=wallpaper_data,
                           size_list=size_list, wallpaper_img=wallpaper_img_data,
                           win_size=win_size)


@web.route('/wallpaper/download', methods=['GET'])
def download_file():
    size, index, url_index = request.args.get('size'), \
                             request.args.get('index'), request.args.get('url_index')
    filename = index + '/' + size + url_index + '.jpg'
    if not is_exists_file(current_app.config['UPLOAD_FOLDER'], filename):
        wallpaper = WallpaperDownloadSpider(size, index, url_index)
        wallpaper.download()
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)


def take_size(size_str):
    size_list = size_str.split(',')[0:-1]
    return size_list