"""
 Created by zjl on 2020/10/1 22:37
"""
# -*- coding: utf-8 -*-
__author__ = 'zjl'


class MovieViewModel:
    def __init__(self, movie_data, detail_data):
        self.movie_detail = {}
        self.fill(movie_data, detail_data)

    def fill(self, movie_data, detail_data):
        if detail_data:
            data = self.__take_data(detail_data['synopsis'], detail_data['awards'],
                                    detail_data['video_pictures'])
        else:
            data = self.__take_data(movie_data.synopsis, movie_data.awards,
                                    movie_data.video_pictures)
        self.movie_detail = {
            'id': movie_data.id,
            'vid': movie_data.vid,
            'name': movie_data.name,
            'img': movie_data.img,
            'time': movie_data.time,
            'score': movie_data.score,
            'evaluators_count': movie_data.evaluators_count,
            'director': detail_data['director'] if detail_data else movie_data.director,
            'screenwriter': detail_data['screenwriter'] if detail_data else movie_data.screenwriter,
            'star': detail_data['star'] if detail_data else movie_data.star,
            'type': detail_data['type'] if detail_data else movie_data.type,
            'country': detail_data['country'] if detail_data else movie_data.country,
            'language': detail_data['language'] if detail_data else movie_data.language,
            'release_date': detail_data['release_date'] if detail_data else movie_data.release_date,
            'length': detail_data['length'] if detail_data else movie_data.length,
            'also_called': detail_data['also_called'] if detail_data else movie_data.also_called,
            'synopsis': data['synopsis_list'],
            'awards': data['awards_list'],
            'video_pictures': data['video_pictures_list']
        }

    def __take_data(self, synopsis, awards, video_pictures):
        data = {
            'synopsis_list': [],
            'awards_list': [],
            'video_pictures_list': []
        }
        if synopsis:
            data['synopsis_list'] = self.__take_single(synopsis, 1)
        if awards:
            data['awards_list'] = self.__take_single(awards)
        if video_pictures:
            data['video_pictures_list'] = self.__take_single(video_pictures)
        return data

    @staticmethod
    def __take_single(content, ty=0):
        if ty == 1:
            content = content.replace('\u3000', '')
            content_list = content.split('\n')[0:-1]
            return content_list
        else:
            content_list = content.split('\n')
            return content_list
