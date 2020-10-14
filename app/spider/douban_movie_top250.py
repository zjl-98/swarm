"""
 Created by zjl on 2020/9/24 9:32
"""
import re

import requests
from lxml import etree

__author__ = 'zjl'


# 爬取豆瓣电影top250的数据
class DouBanMovieTopSpider:
    def __init__(self):
        self.movie_top250 = []
        self.index_url = 'https://movie.douban.com/top250'
        self.page_count = 25
        self.page = int(250 / self.page_count)

        self.movie_top250 = self.__parse()

    def __parse(self):
        """ 获取top250的影片数据 """
        movie_data = []
        for i in range(0, self.page):
            url = self.index_url + '?start=' + str(self.page_count * i)
            header = {
                'Referer': url,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
            }
            response = requests.get(url=url, headers=header)
            movie_lxml = etree.HTML(response.text)
            all_movie = movie_lxml.xpath("//div[@class='article']/ol[@class='grid_view']/li")

            count = 1
            for movie_item in all_movie:
                try:
                    data = self.__take_single_data(movie_item)
                    movie_data.append(data)
                    print("第" + str(i + 1) + "页 第" + str(count) + "条获取成功")
                except Exception as e:
                    print("第" + str(i + 1) + "页 第" + str(count) + "条获取失败")
                    print(e)
                    continue
                count += 1
            #     break
            # break
        return movie_data

    @staticmethod
    def __take_single_data(movie_item):
        """ 获取单影片的数据 """
        # 定义正则匹配表达式
        human_data_search = re.compile(r"\n\s+(.*)")
        movie_data_search = re.compile(r"\n\s+(.*?)\s\/\s([\u4E00-\u9FA5\s]+)\s\/\s(.*)")
        evaluators_count_search = re.compile(r"(\d+)人评价")
        movie_name_search = re.compile(r"\s\/\s(.*)")
        movie_id_search = re.compile(r"subject\/(\d+)\/")
        img_use_search = re.compile(r":\/\/(.*)")

        human_data = movie_item.xpath("./div/div[2]/div[2]/p[1]/text()")[0]
        movie_data = movie_item.xpath("./div/div[2]/div[2]/p[1]/text()")[1]
        evaluators_count = movie_item.xpath("./div/div[2]/div[2]/div/span[4]/text()")[0]
        movie_url = movie_item.xpath("./div/div[1]/a/@href")[0]
        # 原始图片链接
        img_request_url = movie_item.xpath("./div/div[1]/a/img/@src")[0]

        # 再次循环获取全部片名
        movie_name = ''
        count = 0
        for name_item in movie_item.xpath("./div/div[2]/div[1]/a/span"):
            single_name = name_item.xpath("./text()")[0]
            movie_name += single_name.replace('\xa0', ' ')

        # 处理寄语title为空的情况
        try:
            title = movie_item.xpath("./div/div[2]/div[2]/p[2]/span/text()")[0]
        except:
            title = '暂无数据'

        # 发起图片二次请求
        img_request_url = movie_item.xpath("./div/div[1]/a/img/@src")[0]

        try:
            movie_info = {
                'vid': int(re.search(movie_id_search, movie_url).group(1)),
                'name': movie_name,  # 影片名
                'title': str(title),  # 影片宣言
                'url': str(movie_url),  # 访问链接
                # 'img': 'https://images.weserv.nl/?url=' + re.search(img_use_search, img_request_url).group(1),  # 影片标题图片
                'img':  movie_item.xpath("./div/div[1]/a/img/@src")[0],  # 影片标题图片
                'human_data': re.search(human_data_search, human_data)[1].replace('\xa0\xa0\xa0', ' '),  # 人员信息
                'release_time': re.search(movie_data_search, movie_data)[1],  # 上映时间
                'show_country': re.search(movie_data_search, movie_data)[2],  # 上映国家
                'type': re.search(movie_data_search, movie_data)[3],  # 类型
                'ranking': int(movie_item.xpath("./div/div[1]/em/text()")[0]),  # 排名
                'score': float(movie_item.xpath("./div/div[2]/div[2]/div/span[2]/text()")[0]),  # 评分
                'evaluators_count': int(re.search(evaluators_count_search, evaluators_count).group(1)),  # 评价人数
            }
            return movie_info
        except Exception as e:
            print(e)


if __name__ == '__main__':
    douban_movie = DouBanMovieTopSpider()
    print(douban_movie.movie_top250)
    # for data in douban_movie.movie_top250:
    #     print(data)


"""
    try:
        # 创建拥有3个进程数量的进程池
        pool = Pool(3)
        data = pool.map(self.__take_single_data, [all_movie])
        movie_data.append(data)
        pool.close()  # 关闭进程池，不再接受新的进程
        pool.join()  # 主进程阻塞等待子进程的退出
    except Exception as e:
        print(e)
"""