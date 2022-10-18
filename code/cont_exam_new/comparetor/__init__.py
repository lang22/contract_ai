#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/3/4 19:43
@Author     : jzs
@File       : __init__.py.py
@Software   : PyCharm
@Description: ......
"""
from ..comparetor.sentence_match import get_match_dict
from ..cont_cofig import LAB_SEQ1_UNIQUE, LAB_SEQ2_UNIQUE
from .sentence_compare import get_compare_sentences_lab, get_different_slices_dict


def get_highlight_dict(string1: str, string2: str) -> 'tuple[dict[tuple[int,int], str],dict[tuple[int,int], str]]':
    """
    得到句子1和句子2的差异字符串切片字典

    输入：apply peans app, apple panse app
    输出：{(4, 5) : '^', (7, 8) : '-' }, {(4, 5) : '^', (11, 12):'+' }

    :param string1: 句子1
    :param string2: 句子2
    :return:string1的差异字符串切片字典和string2的差异字符串切片字典
    """
    d1, d2 = get_compare_sentences_lab(string1, string2)

    slices_dict1 = get_different_slices_dict(d1)
    slices_dict2 = get_different_slices_dict(d2)

    return slices_dict1, slices_dict2


def get_all_del_highlight_dict(string1: str):
    """
    得到句子1，被认为是删除的高亮字典

    :param string1:
    :return:
    """
    return {(0, len(string1)): LAB_SEQ1_UNIQUE}


def get_all_add_highlight_dict(string1: str):
    """
    得到句子1，被认为是增加的高亮字典

    :param string1:
    :return:
    """
    return {(0, len(string1)): LAB_SEQ2_UNIQUE}


def get_match_dict_by_difflib(sentences1: 'list[str]',
                              sentences2: 'list[str]') -> 'dict[int,int]':
    """
    得到句子列表1和句子列表2的匹配字典

    :param sentences1: 不含空行的句子列表2
    :param sentences2: 不含空行的句子列表2
    :return: 匹配字典：句子列表1下标-句子列表2下标
    """
    return get_match_dict(sentences1, sentences2)
