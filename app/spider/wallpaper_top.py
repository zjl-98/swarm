"""
 Created by zjl on 2020/10/5 11:04
"""

__author__ = 'zjl'

import re

import requests
from lxml import etree


class WallpaperTopSpider:
    def __init__(self):
        self.wallpaper_top = []
        # 主页url
        index_url = 'http://desk.zol.com.cn'
        # 主页请求头
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        # 发起主页请求
        response = requests.get(url=index_url + '/', headers=header)
        self.wallpaper_top = self.spider(response.text)

    @staticmethod
    def spider(text):
        # 将请求回来的数据lxml化，方便使用xpath获取数据
        response_lxml = etree.HTML(text)
        # 通过xpath获取定位到所有壁纸类型下载排行版
        side_response = response_lxml.xpath("//div[@class='side']/div[@class='model mt15']")

        # 通过循环操作每个壁纸类型下载排行版
        info = []
        for side_item in side_response:
            type_info = {}
            # 壁纸类型
            side_title = side_item.xpath("./div[@class='mod-header']/text()")[0]
            # 该类型下所有的壁纸专题
            li_response = side_item.xpath("./ul/li")
            # 通过循环操作每个壁纸专题
            special_info = []
            for li_item in li_response:
                index_url_search = re.compile(r'\/bizhi\/(.*?)\.html')
                # 专题标题
                special = {
                    'title': li_item.xpath("./a/text()")[0],
                    'count': li_item.xpath("./span/text()")[0],
                    'index': re.search(index_url_search, li_item.xpath("./a/@href")[0]).group(1)
                }
                special_info.append(special)
            type_info['type'] = side_title
            type_info['special'] = special_info
            info.append(type_info)
        return info


if __name__ == '__main__':
    wallpaper = WallpaperTopSpider()
    print(wallpaper.wallpaper_top)