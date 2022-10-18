#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/10 17:11
@Author     : jzs
@File       : __init__.py.py
@Software   : PyCharm
@Description: 常用工具类
"""
import os
import time


def random_fliename() -> str:
    """
    得到随机数字文件名字:
    随机方式为当前毫秒级时间戳与随机的一个python对象的id值的拼接

    :return: 得到随机数字文件名字
    """
    return str(id(list())) + str(round(time.time() * 1000))


def join_path(*paths) -> str:
    """
    路径拼接

    :return: 路径
    """
    return os.path.join(*paths)
