#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/10 11:03
@Author     : jzs
@File       : __init__.py.py
@Software   : PyCharm
@Description: 初始化蓝图
"""
from flask import Flask, session

from .contract_gen_json import cont_gen
from .errors import main_error
from .cont_multi_exam import multi_exam
from .index import main
from .contract_gen import gen
from .contract_exam import exam
from .admin_sugg import sugg
from .admin_flowtable import flowtab
from .loginlog import log
from .cont_check import check
from .exam_test import exam_test
from .contract_files import contract_files
from .exam_risk import exam_risk
from .contact_take_elem import take_elem
from .contact_ckeck import cont_check_new

# 配置蓝图的对象以及蓝图的VIEWS的访问路径
DEFAULT_BLUEPRINT = (
    (main, ''),
    (gen, '/gen'),
    (sugg, '/sugg'),
    (log, '/log'),
    (flowtab, '/flowtab'),
    (exam, '/exam'),
    (check, '/check'),
    (exam_test, '/exam_test'),
    (multi_exam, '/multi_exam'),
    (main_error, '/main_error'),
    (contract_files, '/contract_files'),
    (exam_risk, '/exam_risk'),
    (take_elem, '/take_elem'),
    (cont_gen, '/cont_gen'),
    (cont_check_new, '/cont_check')
)


def config_blueprint(app: 'Flask'):
    """
    封装配置蓝本的函数，循环读取元组中的蓝本，注册蓝本对象
    :param app: Flask app对象
    :return:
    """
    for blueprint, prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=prefix)


def set_session(key: 'str', values: 'object'):
    """
    设置session中的值

    :param key:  键
    :param values: 值
    :return:
    """
    session[key] = values


def get_session(key: 'str') -> 'object':
    """
    得到session中的值

    :param key: 键
    :return:
    """
    return session.get(key, None)
