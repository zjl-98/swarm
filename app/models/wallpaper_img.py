# """
#  Created by zjl on 2020/10/3 23:25
# """
__author__ = 'zjl'

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class WallpaperImg(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    wallpaper = relationship('Wallpaper')
    wid = Column(Integer, ForeignKey('wallpaper.id'), nullable=False)
    min_url = Column(String(200))
    max_index = Column(String(20))

    @classmethod
    def get_wallpaper_img(cls, wid):
        wallpaper_img_data = cls.query.filter(cls.wid == wid).all()
        return wallpaper_img_data
