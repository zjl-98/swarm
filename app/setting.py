# """
#  Created by zjl on 2020/9/24 8:21
# """
import os

__author__ = 'zjl'


MOVIE_SEARCH_PAGE_COUNT = 25

# 豆瓣影视
MOVIE = 0
# 抖音短视频
VIDEO = 1
# 招聘信息
JOB = 2
# 桌面壁纸
WALLPAPER = 3

# 下载路径
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/wallpaper')