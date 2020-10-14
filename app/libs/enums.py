"""
 Created by zjl on 2020/9/26 21:01
"""
from enum import Enum

__author__ = 'zjl'


def pending_str(key):
    key_map = ['影视', '短视频', '招聘', '壁纸']
    return key_map[key]