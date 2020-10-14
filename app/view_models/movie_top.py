"""
 Created by zjl on 2020/9/27 12:22
"""

__author__ = 'zjl'


class MovieTopViewModel:
    def __init__(self, book):
        self.vid = book['vid']
        self.name = book['name']
        self.title = book['title']
        self.url = book['url']
        self.img = book['img']
        self.human_data = book['human_data']
        self.release_time = book['release_time']
        self.show_country = book['show_country']
        self.type = book['type']
        self.ranking = book['ranking']
        self.score = book['score']
        self.evaluators_count = book['evaluators_count']

    # 数据表示特征  方法表示行为  因为此方法只是提取数据，所以定义为特征函数
    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.release_time, self.show_country, self.type])
        return ' / '.join(intros)


class MovieTopCollection:
    def __init__(self):
        self.movies = []

    def fill(self, movie_data):
        self.movies = [MovieTopViewModel(movie) for movie in movie_data]