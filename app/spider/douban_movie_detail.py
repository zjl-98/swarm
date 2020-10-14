"""
 Created by zjl on 2020/9/26 22:23
"""
import re

import requests
from lxml import etree

__author__ = 'zjl'


class DouBanMovieDetailSpider:
    def __init__(self, vid):
        self.detail_url = 'https://movie.douban.com/subject/' + vid + '/'
        self.header = {
            'Referer': self.detail_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }

    def movie_detail(self):
        response = requests.get(url=self.detail_url, headers=self.header)
        html_etree = etree.HTML(response.text)

        director_div = html_etree.xpath('//*[@id="info"]/span[1]/span[2]/a')
        director = self.__get_list(director_div)

        screenwriter = ''
        if html_etree.xpath('//*[@id="info"]/span[2]/span[1]/text()'):
            screenwriter_div = html_etree.xpath('//*[@id="info"]/span[2]/span[2]/a')
            screenwriter = self.__get_list(screenwriter_div)

        star = ''
        if html_etree.xpath('//*[@id="info"]/span[3]/span[1]/text()'):
            star_div = html_etree.xpath('//*[@id="info"]/span[3]/span[2]/a')
            star = self.__get_list(star_div)

        type_search = re.compile(r'<span property="v:genre">(.*?)</span>')
        type = self.__get_str(type_search, response.text)

        country_search = re.compile(r'<span class="pl">制片国家/地区:</span>\s(.*?)<br/>')
        country = self.__get_str(country_search, response.text)

        language_search = re.compile(r'<span class="pl">语言:</span>\s(.*?)<br/>')
        language = self.__get_str(language_search, response.text)

        release_date_search = re.compile(r'<span property="v:initialReleaseDate" content="(.*?)">')
        release_date = self.__get_str(release_date_search, response.text)

        length_search = re.compile(r'<span property="v:runtime" content="(.*?)">')
        length = self.__get_str(length_search, response.text)

        also_called_search = re.compile(r'<span class="pl">又名:</span>\s(.*?)<br/>')
        also_called = self.__get_str(also_called_search, response.text)

        synopsis = ''
        synopsis_list = html_etree.xpath("//div[@id='link-report']/span[1]/text()")
        for item in synopsis_list:
            synopsis += item.replace(' ', '').replace('\n', '') + '\n'

        awards = self.__get_awards(html_etree)
        video_pictures = self.__get_video_pictures(html_etree)

        return {
            'director': director,  # 导演
            'screenwriter': screenwriter,  # 编剧
            'star': star,  # 主演
            'type': type,  # 类型
            'country': country, # 上映国家
            'language': language,  # 语言
            'release_date': release_date,  # 上映具体时间
            'length': length,  # 片长
            'also_called': also_called,  # 又名
            'synopsis': synopsis or '',  # 剧情简介
            'awards': awards,  # 获奖情况
            'video_pictures': video_pictures  # 视频图片
        }

    @staticmethod
    def __get_list(div):
        result = ''
        try:
            count = len(div)
            for item, index in zip(div, range(0, count)):
                if index < count - 1:
                    result += item.xpath('./text()')[0] + ' / '
                else:
                    result += item.xpath('./text()')[0]
        except Exception as e:
            print(e)
        return result

    @staticmethod
    def __get_str(search, response_text):
        data = ''
        try:
            result = re.findall(search, response_text)
            data = ' / '.join(result)
        except Exception as e:
            print(e)
        return data

    @staticmethod
    def __get_awards(html_etree):
        awards = ''
        try:
            if html_etree.xpath("//div[@class='mod']/ul"):
                awards_list = html_etree.xpath("//div[@class='mod']/ul")
                awards_count = len(awards_list)
                for item, index in zip(awards_list, range(0, awards_count)):
                    one = item.xpath('./li[1]/a/text()')[0]
                    two = item.xpath('./li[2]/text()')[0]
                    if index < awards_count - 1:
                        awards += one + ': ' + two + '\n'
                    else:
                        awards += one + ': ' + two
        except Exception as e:
            print(e)
        return awards

    @staticmethod
    def __get_video_pictures(html_etree):
        video_pictures = ''
        try:
            if html_etree.xpath("//div[@id='related-pic']/ul"):
                video_pictures_list = html_etree.xpath("//div[@id='related-pic']/ul/li")
                video_pictures_count = len(video_pictures_list)
                for item, index in zip(video_pictures_list, range(0, video_pictures_count)):
                    if item.xpath('./a/@title'):
                        url_con = item.xpath('./a/@style')[0]
                        url_search = re.compile(r'background-image:url\((.*?)\?\)')
                        url = re.search(url_search, url_con).group(1)
                        video_pictures += url
                    else:
                        url = item.xpath('./a/img/@src')[0]
                        video_pictures += '\n' + url
        except Exception as e:
            print(e)
        return video_pictures


if __name__ == '__main__':
    print(DouBanMovieDetail(vid='30331149').movie_detail())