#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/12/4 9:55
@Author     : jzs
@File       : element_extracting.py
@Software   : PyCharm
@Description: 合同要素抽取
"""
import re

from .base_regular import PUNCTUATION_DICT, punctuation_filter, FLOAT_NUM, SIMPLE_EQUATION
from .base_regular import SIMPLE_PUNC
from .base_regular import DATE_RE
from .base_regular import LOW_CASE_AMOUNT_RE
from .base_regular import UP_CASE_AMOUNT_RE


def __get_key_sentence(key: str, sentence: str) -> str:
    """
    得到关键词之后的句子

    :param key:关键字
    :param sentence:句子
    :return:
    """
    key = key.split(';')
    key = key[0] if len(key) != 2 else key[1]

    index = [m.start() for m in re.finditer(key, sentence)]
    return sentence[index[0]:] if len(index) > 0 else str()


def get_simple_instructions(key: str, sentence: str) -> str:
    """
    简单的指示，利用分割符号，提取要素内容

    :param key:关键字
    :param sentence:句子
    :return:
    """
    if not sentence or not isinstance(sentence, str):
        return str()
    sentence = __get_key_sentence(key, sentence)
    # elem = sentence.split(SIMPLE_PUNC)
    elem = re.split(SIMPLE_PUNC,sentence )
    return str() if len(elem) != 2 else punctuation_filter(elem[1])


def get_date(key: str, sentence: str) -> str:
    """
    提取日期

    :param key:关键字
    :param sentence:句子
    :return:
    """
    if not sentence or not isinstance(sentence, str):
        return str()

    sentence = __get_key_sentence(key, sentence)
    mat = re.search(DATE_RE, sentence)
    return mat.group(0) if mat else str()


def get_simple_equation(key: str, sentence: str) -> str:
    """
    得到简单计算表达式

    :param key:
    :param sentence:
    :return:
    """
    if not sentence or not isinstance(sentence, str):
        return str()

    sentence = __get_key_sentence(key, sentence)

    mat = re.search(SIMPLE_EQUATION, sentence)
    return mat.group(0) if mat else str()


def get_case_amount(key: str, sentence: str) -> 'tuple[str,str]':
    """
    提取人民币大小写金额

    :param key:关键字
    :param sentence:句子
    :return:
    """
    if not sentence or not isinstance(sentence, str):
        return str()

    sentence = __get_key_sentence(key, sentence)
    mat_low = re.search(LOW_CASE_AMOUNT_RE, sentence)
    amount_low = mat_low.group(0).replace('人民币', '') if mat_low else str()

    mat_up = re.search(UP_CASE_AMOUNT_RE, sentence)
    amount_up = mat_up.group(0).replace('人民币', '') if mat_up else str()

    return [amount_up, amount_low]


def get_up_case_amount(key: str, sentence: str) -> 'str':
    """
    提取大写金额

    :param key:
    :param sentence:
    :return:
    """
    if not sentence or not isinstance(sentence, str):
        return str()
    sentence = __get_key_sentence(key, sentence)
    mat_up = re.search(UP_CASE_AMOUNT_RE, sentence)
    amount_up = mat_up.group(0).replace('人民币', '') if mat_up else str()
    return amount_up


def get_front_instructions(key: str, sentence: str) -> 'tuple[str,str]':
    return sentence


def get_other_instructions(key: str, sentence: str) -> 'tuple[str,str]':
    return '人民币'


def get_float_or_int_number(key: str, sentence: str) -> str:
    """
    提取只有一个浮点数或整数

    :param key:关键字
    :param sentence:句子
    :return:
    """
    if not sentence or not isinstance(sentence, str):
        return str()

    sentence = __get_key_sentence(key, sentence)
    mat = re.search(FLOAT_NUM, sentence)
    return mat.group(0) if mat else str()


if __name__ == '__main__':
    ss = "'2.2截至交易基准日标的债权本息总额为人民币一亿两千万元小写：人民币12333元其中本金余额人民币一亿元元小写：人民币1元欠息人民币两千万元小写：人民币20元'"
    e = get_case_amount('本金余额', ss)
    print(e)
