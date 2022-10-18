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
from exam_clause.exam_process import *


def __set_placeholder(model: str, test: str):
    """
    预处理句子，得到占位符的个数，向句子加入占位符的

    :param model: 模板的句子
    :param test: 用于测试的句子
    :return: 模板的句子, 用于测试的句子,占位符的个数
    """
    max_len = max(len(model), len(test))
    min_len = min(len(model), len(test))
    if min_len < 30:
        placeholder_num = max_len * 4
    else:
        placeholder_num = max_len * 2

    model = str().join('`' for i in range(placeholder_num)) + model
    test = str().join('`' for i in range(placeholder_num)) + test

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
    print(diff_list)
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


def get_compare_sentences_lab(model: str, test: str):
    """
    得到model句子和test句子的对比结果标签集合

    :param model: 模板的句子
    :param test: 用于测试的句子
    :return:
    """
    line1, line2, placeholder_num = __set_placeholder(model, test)
    line1 = line1.splitlines()
    line2 = line2.splitlines()
    line1_diff_string, line2_diff_string = __get_different_list(line1, line2)
    return __del_placeholder(line1_diff_string,
                             line2_diff_string,
                             placeholder_num)


def make_different_html(line1, line2):
    """
    将line1和line2的对比结果写成HTML的形式

    :param line1: 字符串1分行后的list
    :param line2: 字符串2分行后的list
    :return:
    """
    line1 = line1.splitlines()
    line2 = line2.splitlines()
    d = difflib.HtmlDiff()
    q = d.make_file(line1, line2)
    with open('diff.html', 'w', encoding='UTF-8') as f_new:
        f_new.write(q)


if __name__ == '__main__':
    s1 = '''债权转让协议 转让方： [ ] 法定代表人：[ ] 住所：[] 受让方： [ ] 负责人：[ ] 地址：[ ] 协议签订地点：[ ] 协议签订日期：[ ]年[ ]月[ ]日'''
    s2 = '''债权转让协议 转让方： [XXX ] 法定代表人：[XXX ] 住所：[XXX] 受让方： [XXX ] 负责人：[XXX ] 地址：[ XXX] 协议签订地点：[XXX ] 协议签订日期：[X ]年[X ]月[X ]日'''
    # s1 = '合同编号：'
    # s2 = '编号：合同机器人测试合同3号'
    # d1, d2 = get_compare_sentences_lab(s1, s2)
    line1 = s1.splitlines()
    line2 = s2.splitlines()
    diff = difflib.ndiff(line1[0].splitlines(keepends=True),
                         line2[0].splitlines(keepends=True))
    for i in list(diff):
        print(i)
