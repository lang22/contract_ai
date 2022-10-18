#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/12/19 21:01
@Author     : jzs
@File       : sentence_masked.py
@Software   : PyCharm
@Description: 输出标高亮的html
"""
from exam_clause.exam_process import *


def __get_highlight_string_slices(diff_string: str):
    """
    得到高亮的颜色的切片list
    :param string:
    :param diff_string:
    :return:
    """

    p, color = 0, diff_string[0]
    slices = list()
    for i, s in enumerate(diff_string):
        if s != color:
            slices.append((p, i, color))
            p, color = i, diff_string[i]
    if p != len(diff_string):
        slices.append((p, len(diff_string), color))
    return slices


def __get_highlight_html_string(string: str, diff_string: str) -> str:
    """
    得到string的标高亮的html

    :param string:
    :param diff_string:
    :return:
    """
    if diff_string == COMMON_FLAG:  # 句子完全相同
        return string.replace(' ', '&nbsp;')
    elif diff_string == NOT_COMMON_FLAG:  # 句子完全不同
        s1, s2 = NOT_COMMON
        s1 = s1.replace(SPAN_ID_PLACEHOLDER1, str(0) + '_' + str(len(string)))  # todo 修改
        return str().join((s1, string.replace(' ', '&nbsp;'), s2))

    highlight_list = list()  # 句子有差异

    slices = __get_highlight_string_slices(diff_string)  # todo 对比字符，返回切片

    string = string.replace(' ', '`')
    for i1, i2, lab in slices:
        s1, s2 = SENTENCE_HTML_LAB[lab]
        char = string[i1:i2]

        if s1 and s2:
            s1 = s1.replace(SPAN_ID_PLACEHOLDER1, str(i1) + '_' + str(i2))
            highlight_list.extend((s1, char, s2))
        else:
            highlight_list.append(char)

    return str().join(highlight_list).replace('`', '&nbsp;')


def get_highlight_html(model: str,
                       test: str,
                       model_diff_string: str,
                       test_diff_string: str):
    """
    将model和test标高亮的html

    :param model: 模板的句子
    :param test: 用于测试的句子
    :param model_diff_string: model的差异字符串
    :param test_diff_string: test的差异字符串
    :return:
    """
    model = __get_highlight_html_string(model, model_diff_string)
    model = str().join(('<p>', model, '</p>'))

    test = __get_highlight_html_string(test, test_diff_string)
    test = str().join(('<p>', test, '</p>'))

    return model, test


def get_all_highlight_html(color, strings: 'list[str]') -> str:
    """
    将所有句子都标高亮，输出html
    :param color: 标高亮的颜色
    :param strings: 句子list
    :return:
    """
    s1, s2 = color
    strings = [str().join(('<p>', s1.replace(SPAN_ID_PLACEHOLDER1, str(0) + '_' + str(len(ss))), ss, s2, '</p>'))
               if ss else SPACE_HTML for ss in strings]
    return str().join(strings)


def get_one_highlight_html(color, string: str) -> str:
    """
    将所有句子都标高亮，输出html
    :param color: 标高亮的颜色
    :param string: 句子
    :return:
    """
    s1, s2 = color
    s1 = s1.replace(SPAN_ID_PLACEHOLDER1, str(0) + '_' + str(len(string)))
    return str().join(('<p>', s1, string, s2, '</p>'))


def get_html(strings: 'list[str]') -> str:
    """
    将所有句子，输出html

    :param strings: 句子list
    :return:
    """
    strings = [str().join(('<p>', ss, '</p>')) if ss else '<br>' for ss in strings]
    return str().join(strings)


def add_html_elem_id(string_id, html_string: str) -> 'list[str]':
    """
    html按照<p>标签分割，并给每个<p>和<span>标签添加id，返回html

    :param string_id
    :param html_string: html字符串
    :return:

    """
    html_string = html_string.replace(SPAN_ID_PLACEHOLDER2, string_id)
    p_list = re.findall('<p>.*?</p>', html_string)
    p_list = [p.replace('<p>', '<p id=' + string_id + '_' + str(i) + '">') for i, p in enumerate(p_list)]
    p_list = [p.replace(SPAN_ID_PLACEHOLDER3, str(i)) for i, p in enumerate(p_list)]

    return ''.join(p_list)
