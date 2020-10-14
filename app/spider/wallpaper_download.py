"""
 Created by zjl on 2020/10/6 0:47
"""

__author__ = 'zjl'

import requests
from flask import current_app
from lxml import etree

from app.libs.check_dir import take_exists_dir, join_path


class WallpaperDownloadSpider:
    def __init__(self, size, index, url_index):
        self.size = size
        self.index = index
        self.url_index = url_index
        download_url = 'http://desk.zol.com.cn/showpic/' + size + url_index + '.html'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        self.response = requests.get(url=download_url, headers=self.header)

    def download(self):
        # 将请求回来的数据lxml化，方便使用xpath获取数据
        img_take = etree.HTML(self.response.text)
        # 获取到页面中提高的图片下载url
        img_install_url = img_take.xpath("//body/img[1]/@src")[0]
        # 请求图片下载url
        response = requests.get(url=img_install_url, headers=self.header)
        # 判断目录是否存在
        take_exists_dir(current_app.config['UPLOAD_FOLDER'], self.index)

        filename = self.index + '/' + self.size + self.url_index + '.jpg'
        path = join_path(current_app.config['UPLOAD_FOLDER'], filename)

        # 实现图片下载操作，并进行归类
        with open(path, 'wb') as f:
            f.write(response.content)


if __name__ == '__main__':
    wallpaper = WallpaperDownloadSpider('1366x768', '3730_46505_2', '_46505_460')
    wallpaper.download()