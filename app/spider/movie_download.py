# """
#  Created by zjl on 2020/10/2 22:37
# """
import re
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

__author__ = 'zjl'


class MovieDownload:
    def __init__(self):
        # 设置无界面浏览
        chrome_option = Options()
        # 禁用GPU加速
        # chrome_option.add_argument('--disable-gpu')
        # 设置无头浏览
        chrome_option.add_argument('--headless')
        # 日志信息屏蔽
        # chrome_option.add_argument('--log-level=3')
        # 禁用自动化栏防检测
        # chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # ua
        # chrome_option.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; rv:51.0) Gecko/20100101 Firefox/51.0')
        self.webdriver = webdriver.Chrome(chrome_options=chrome_option)
        # 设置最大化屏幕
        self.webdriver.maximize_window()

    def movie_download(self, search_name):
        # 发起请求
        self.webdriver.get('https://www.dy2018.com/e/search/result/?searchid=629020')
        # print(self.webdriver.page_source)
        name_search = re.compile(r'\《(.*)\》')
        # # 转化为lxml etree类型
        html_etree = etree.HTML(self.webdriver.page_source)
        html_div = html_etree.xpath('//*[@id="header"]/div/div[3]/div[1]/div[1]/div[5]/div[2]/ul/table')
        for movie_item in html_div:
            name = movie_item.xpath('/tbody/tr[2]/td[2]/b/a/text()')[0]
            movie_name = re.search(name_search, name).group(1)


if __name__ == '__main__':
    movie_download = MovieDownload()
    movie_download.movie_download()