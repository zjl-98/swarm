"""
 Created by zjl on 2020/9/28 13:35
"""

__author__ = 'zjl'

from sqlalchemy import Column, Integer, String, Float, Text

from app.models.base import Base, db


class Movie(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    vid = Column(Integer, unique=True, nullable=False)
    name = Column(String(200))  # 名字
    img = Column(String(200))  # 图片链接
    time = Column(Integer)  # 上映年份
    score = Column(Float, default=0)  # 评分
    evaluators_count = Column(Integer, default=0)  # 评价人数
    context = Column(String(50))  # 混合信息
    human = Column(String(200))  # 混合人员信息

    director = Column(String(50))  # 导演
    screenwriter = Column(String(50))  # 编剧
    star = Column(String(100))  # 主演
    type = Column(String(50))  # 类型
    country = Column(String(50))  # 上映国家
    language = Column(String(20))  # 语言
    release_date = Column(String(100))  # 上映具体时间
    length = Column(Integer)  # 片长
    also_called = Column(String(200))  # 又名

    synopsis = Column(Text)  # 剧情简介
    awards = Column(String(300))  # 获奖情况
    video_pictures = Column(String(500))  # 视频图片
    download = Column(String(500))  # 视频下载链接

    @staticmethod
    def get_movie_by_keyword(keyword):
        movie_data = Movie.query.filter(Movie.name.like('%{0}%'.format(keyword))).all()
        return movie_data

    @classmethod
    def has_movie_of_vid(cls, vid):
        movie_data = cls.query.filter(cls.vid == vid).first()
        return movie_data

    # 通过vid访问的说明数据是存在，只是需要通过length项来判断数据是否完整
    @classmethod
    def movie_length_of_vid(cls, vid):
        pass

    # 更新内容
    @staticmethod
    def update_data(vid, detail_data):
        with db.auto_commit():
            movie = Movie.query.filter_by(vid=vid).update(
                dict(director=detail_data['director'],
                     screenwriter=detail_data['screenwriter'],
                     star=detail_data['star'],
                     type=detail_data['type'],
                     country=detail_data['country'],
                     language=detail_data['language'],
                     release_date=detail_data['release_date'],
                     length=detail_data['length'],
                     also_called=detail_data['also_called'],
                     synopsis=detail_data['synopsis'],
                     awards=detail_data['awards'],
                     video_pictures=detail_data['video_pictures']))