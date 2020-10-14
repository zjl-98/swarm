import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree


class DouBanMovieSearchSpider:
    def __init__(self):
        # 设置无界面浏览
        chrome_option = Options()
        # 禁用GPU加速
        chrome_option.add_argument('--disable-gpu')
        # 设置无头浏览
        chrome_option.add_argument('--headless')
        # 日志信息屏蔽
        chrome_option.add_argument('--log-level=3')
        # 禁用自动化栏防检测
        chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # ua
        chrome_option.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; rv:51.0) Gecko/20100101 Firefox/51.0')
        self.webdriver = webdriver.Chrome(chrome_options=chrome_option)
        # 设置最大化屏幕
        self.webdriver.maximize_window()

    def search_data(self, keyword):
        # 发起请求
        self.webdriver.get('https://search.douban.com/movie/subject_search?search_text={0}'.format(keyword))

        # 转化为lxml etree类型
        html_etree = etree.HTML(self.webdriver.page_source)
        html_div = html_etree.xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div')

        # 循环获取数据--默认只获取第一页的
        movie_data = []
        for movie_item in html_div:
            try:
                if movie_item.xpath('./div[1]/div/div[2]/span[3]'):
                    # 获取电影id
                    movie_id_serch = re.compile(r"subject\/(\d+)\/")
                    movie_id = movie_item.xpath('./div[1]/a/@href')[0]
                    vid = re.search(movie_id_serch, movie_id).group(1)

                    # 获取电影图片，
                    movie_img = movie_item.xpath('./div[1]/a/img/@src')[0]

                    # 电影信息
                    movie_title = movie_item.xpath('./div[1]/div/div[1]/a/text()')[0]
                    movie_title_search = re.compile(r'(.*?)\s\((\d+)\)')
                    # 名字、上映时间
                    name = re.search(movie_title_search, movie_title).group(1).replace('\u200e', '')
                    # 上映时间
                    release_time = re.search(movie_title_search, movie_title).group(2)
                    # 评分
                    movie_score = movie_item.xpath('./div[1]/div/div[2]/span[2]/text()')[0]
                    # 评价人数
                    evaluators_count_search = re.compile(r"(\d+)人评价")
                    movie_evaluators_count = movie_item.xpath('./div[1]/div/div[2]/span[3]/text()')[0]
                    evaluators_count = re.search(evaluators_count_search, movie_evaluators_count).group(1)
                    # 相关信息
                    movie_context = movie_item.xpath('./div[1]/div/div[3]/text()')[0]
                    # 人员
                    movie_human = movie_item.xpath('./div[1]/div/div[4]/text()')[0]

                    # 拼接
                    movie = {
                        'vid': int(vid),
                        'img': movie_img,
                        'name': name,
                        'time': int(release_time),
                        'score': float(movie_score),
                        'evaluators_count': int(evaluators_count),
                        'context': movie_context,
                        'human': movie_human
                    }
                    movie_data.append(movie)
            except Exception as e:
                print(e)
                continue
        # 关闭
        self.webdriver.close()
        return movie_data
