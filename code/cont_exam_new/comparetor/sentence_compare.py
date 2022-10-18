#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/12/18 11:18
@Author     : jzs
@File       : sentence_marked.py
@Software   : PyCharm
@Description: 主要用于句子差异的对比
"""

import difflib

from .configs import *


def __set_placeholder(model: str, test: str):
    """
    预处理句子，得到占位符的个数，向句子加入占位符的

    :param model: 模板的句子
    :param test: 用于测试的句子
    :return: 模板的句子, 用于测试的句子,占位符的个数
    """
    max_len = max(len(model), len(test))
    min_len = min(len(model), len(test))
    if min_len < MIN_SENTENCE_LEN:
        placeholder_num = max_len * MAX_MULTIPLE
    else:
        placeholder_num = max_len * min_MULTIPLE

    model = str().join(PLACEHOLDER for i in range(placeholder_num)) + model
    test = str().join(PLACEHOLDER for i in range(placeholder_num)) + test

    return model, test, placeholder_num


def __del_placeholder(model: str, test: str, placeholder_num: int):
    """
    删除占位符

    :param model: 模板的句子
    :param test: 用于测试的句子
    :param placeholder_num: 占位符的个数
    :return:
    """

    if placeholder_num < len(model) and placeholder_num < len(test):
        return model[placeholder_num:], test[placeholder_num:]
    else:
        return model, test


def __filter_diff_string(line: str,
                         start_index: int,
                         diff_list: 'list[str]'):
    """
    过滤差异字符串

    :param line: 行
    :param start_index: 从占位符开始
    :param diff_list: 行1的差异字符串的list
    :return:
    """
    line_diff_string = diff_list[start_index][2:-1] if start_index > 0 else str()
    num = len(line) - len(line_diff_string)
    space_list = [' '] * num
    return str().join((line_diff_string, *space_list))


def __get_different_list(line1: 'list[str]', line2: 'list[str]') -> 'list[str]':
    """
    通过difflib得到行line1和行line2的差异字符串列表，得到line1和line2的差异对比字符串

    :param line1: 行1
    :param line2: 行2
    :return:
    """

    diff = difflib.ndiff(line1[0].splitlines(keepends=True),
                         line2[0].splitlines(keepends=True))
    diff_list = list(diff)
    diff_key = str().join(d[0] for d in diff_list)
    i1, i2 = DIFF_DICT[diff_key]
    if i1 < 0 and i2 < 0:
        return NOT_COMMON_FLAG, NOT_COMMON_FLAG
    elif i1 > 0 or i2 > 0:
        line1_diff_string = __filter_diff_string(line1[0], i1, diff_list)
        line2_diff_string = __filter_diff_string(line2[0], i2, diff_list)
        return line1_diff_string, line2_diff_string
    else:
        return COMMON_FLAG, COMMON_FLAG


def get_compare_sentences_lab(line1: str, line2: str):
    """
    得到model句子和test句子的对比结果标签集合

    :param line1: 模板的句子
    :param line2: 用于测试的句子
    :return:
    """
    line1, line2, placeholder_num = __set_placeholder(line1, line2)
    line1 = line1.splitlines()
    line2 = line2.splitlines()
    line1_diff_string, line2_diff_string = __get_different_list(line1, line2)
    return __del_placeholder(line1_diff_string,
                             line2_diff_string,
                             placeholder_num)


def get_different_slices_dict(diff_string: str):
    """
    根据差异对比结果，得到的{切片-高亮的颜色}字典

    :param diff_string: 差异对比字符串
    :return:
    """
    if diff_string == COMMON_FLAG:  # 句子完全相同
        return {}
    elif diff_string == NOT_COMMON_FLAG:  # 句子完全不同
        return {(0, len(diff_string)): NOT_COMMON_FLAG}

    # 两个句子稍微不同
    p, color = 0, diff_string[0]
    slices_dict = dict()
    for i, s in enumerate(diff_string):
        if s != color:
            slices_dict[(p, i)] = color
            p, color = i, diff_string[i]
    if p != len(diff_string):
        slices_dict[(p, len(diff_string))] = color
    return slices_dict
