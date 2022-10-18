#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/3/4 19:43
@Author     : jzs
@File       : sentence_match.py
@Software   : PyCharm
@Description: ......
"""

from difflib import Differ

# 占位符数量
DEFAULT_PLACEHOLDERS_NUMBER = 50

# 占位符
PLACEHOLDERS = '`'

# 两个句子相同的符号
COMMEND = ' '

# 句子1的符号
FIRST = '-'

# 句子2的符号
SECOND = '+'

# 有疑问的符号
DIFF = '?'


def add_placeholders(sentence: str) -> str:
    """
    添加占位符

    :param sentence: 句子
    :return: 加入占位符的句子
    """
    size = DEFAULT_PLACEHOLDERS_NUMBER - len(sentence)
    if size <= 0:
        # print(size)
        return sentence
    else:
        return sentence + ''.join((PLACEHOLDERS for x in range(size)))


def get_match_dict(sentences1: 'list[str]',
                   sentences2: 'list[str]') -> 'dict[int,int]':
    """
    得到句子列表1和句子列表2的匹配字典，

    :param sentences1: 不含空行的句子列表2
    :param sentences2: 不含空行的句子列表2
    :return: 匹配字典：句子列表1下标-句子列表1下标2
    """
    # 当句子长度小于50的时候，加入占位符
    sentences1 = [add_placeholders(sent) for sent in sentences1]
    sentences2 = [add_placeholders(sent) for sent in sentences2]

    # 通过差异对比，得到差异结果
    diff_g = Differ().compare(sentences1, sentences2)
    diff_strings: 'list[str]' = [df[0] for df in diff_g if df[0] != DIFF]
    diff_strings.append(COMMEND)

    # 解析对比结果，查找两个句子集合的匹配句
    match_dict = {}
    k, i, j = 0, 0, 0
    while k < len(diff_strings) - 1:

        p = diff_strings[k]
        pr = diff_strings[k + 1]
        if p == COMMEND:
            match_dict[i] = j
            k, i, j = k + 1, i + 1, j + 1
        elif p == FIRST and pr == SECOND:
            match_dict[i] = j
            k, i, j = k + 2, i + 1, j + 1
        elif p == FIRST and pr != SECOND:
            k, i = k + 1, i + 1
        elif p == SECOND:
            k, j = k + 1, j + 1

    print('match_dict:', match_dict)
    return match_dict
