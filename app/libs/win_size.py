"""
 Created by zjl on 2020/10/5 21:47
"""

import win32api, win32con

__author__ = 'zjl'


def get_size():
    # 获得屏幕分辨率X轴
    win_x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)

    # 获得屏幕分辨率Y轴
    win_y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    size = str(win_x) + 'x' + str(win_y)
    return size


if __name__ == '__main__':
    get_size()
