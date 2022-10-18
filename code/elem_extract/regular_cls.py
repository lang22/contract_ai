#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/12/7 10:07
@Author     : jzs
@File       : regular_cls.py
@Software   : PyCharm
@Description: ......
"""
import re

from .base_regular import DATE_RE, UP_CASE_AMOUNT_RE, LOW_CASE_AMOUNT_RE, punctuation_filter, FLOAT_NUM, SIMPLE_EQUATION


def __get_key_index(sentences: 'List[str]', elem_keys: str):
    """
    得到正确位置的句子集合，和关键字
    :param sentences:
    :param elem_keys:
    :return:
    """
    index = 0
    elem_keys = elem_keys.split(';')

    if len(elem_keys) == 2:
        restr = r'.*(%s).*' % elem_keys[0]
        for i, s in enumerate(sentences):
            if re.match(restr, s):
                index = i
                key = elem_keys[1]
                break;
        else:
            return None, []
    else:
        key = elem_keys[0]

    return key, sentences[index:]


def __get_sentence(key, sentences):
    """
    得到句子
    :param path:
    :return:
    """
    for ss in sentences:
        if re.match(key, ss):
            # print('key:', key, 'sent:', ss)
            return ss
    return str()


def get_simple_instructions_sentence(sentences: 'list[str]', elem_keys: str) -> str:
    """
    得到简单指示的关键字的句子
    :param sentences:
    :param elem_keys:
    :return:
    """
    key, sentences = __get_key_index(sentences, elem_keys)
    key = r'.{0,10}(%s).{0,10}(：|:).{1,50}$' % key
    return __get_sentence(key, sentences)


def get_date_sentence(sentences: 'list[str]', elem_keys: str) -> str:
    """
    得到日期的句子
    :return:
    """
    key, sentences = __get_key_index(sentences, elem_keys)
    key = r'.*(%s).{0,50}(%s).{0,50}$' % (key, DATE_RE)
    return __get_sentence(key, sentences)


def get_case_amount_sentence(sentences: 'list[str]', elem_keys: str) -> str:
    """
    得到含有大小写金额的句子
    :param sentences:
    :param elem_keys:
    :return:
    """
    key, sentences = __get_key_index(sentences, elem_keys)
    key = r'.*%s.{0,50}%s.{0,50}%s.*$' % (key, UP_CASE_AMOUNT_RE, LOW_CASE_AMOUNT_RE)
    return __get_sentence(key, sentences)


def get_up_case_amount_sentence(sentences: 'list[str]', elem_keys: str) -> str:
    """
    得到含有大写金额的句子
    :param sentences:
    :param elem_keys:
    :return:
    """
    key, sentences = __get_key_index(sentences, elem_keys)
    key = r'.*?%s.{0,50}?%s.*?$' % (key, UP_CASE_AMOUNT_RE)
    return __get_sentence(key, sentences)


def get_front_instructions_sentence(sentences: 'list[str]', elem_keys: str) -> str:
    """
    得到前指示的句子
    :param sentences:
    :param elem_keys:
    :return:
    """
    key, sentences = __get_key_index(sentences, elem_keys)
    key = r'.{0,50}%s$' % key
    return __get_sentence(key, sentences)


def get_float_or_int_number_sentence(sentences: 'list[str]', elem_keys: str) -> str:
    """
    得到只有一个浮点数和整数的句子
    :return:
    """
    key, sentences = __get_key_index(sentences, elem_keys)
    key = r'.*(%s).{0,50}?(%s)?.{0,50}?$' % (key, FLOAT_NUM)
    return __get_sentence(key, sentences)


def get_simple_equation_sentence(sentences: 'list[str]', elem_keys: str) -> str:
    """
    得到一个简单的计算表达式
    :return:
    """
    key, sentences = __get_key_index(sentences, elem_keys)
    key = r'.*(%s).{0,50}?(%s)?.{0,50}?$' % (key, SIMPLE_EQUATION)
    return __get_sentence(key, sentences)


def get_other_instructions_sentence(sentences: 'list[str]', elem_keys: str) -> str:
    return ''


# 基于规则的分類方法
REGULAR_CLS = {
    'simple_instructions': get_simple_instructions_sentence,
    'date': get_date_sentence,
    'case_amount': get_case_amount_sentence
}

if __name__ == '__main__':
    sentences = [
        '合同编号：   45678  号',
        '债 权 转 让 协 议',
        '(适用于我司债权打包/单户对外转让项目)'
        '备注：标注有“★”的条款为合同底线条款，正式使用时请将“★”符号删除，附件内容分公司可以根据实际情况调整使用。',
        'xxxx资产管理股份有限公司',
        '[我的]分公司',
        '债权转让协议',
        '2.2  截至交易基准日，标的债权本息总额为人民币 [  一亿两千万  ]元（小写：人民币[   12333   ]元），其中本金余额人民币[      一亿元    ]元（小写：人民币[       1     ]元），欠息人民币[       两千万     ]元（小写：人民币[    20    ]元）。'
    ]
    sentences = [punctuation_filter(ss) for ss in sentences if ss]
    print(sentences)

    elem_keys = '协议'
    ss = get_front_instructions_sentence(sentences, elem_keys)
    print('结果：', ss)
