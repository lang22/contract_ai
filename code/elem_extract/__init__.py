#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/12/4 14:56
@Author     : jzs
@File       : __init__.py.py
@Software   : PyCharm
@Description: ......
"""
from .base_regular import punctuation_filter
from .regular_cls import get_simple_instructions_sentence, get_front_instructions_sentence, \
    get_other_instructions_sentence, get_float_or_int_number_sentence, get_up_case_amount_sentence, \
    get_simple_equation_sentence
from .regular_cls import get_date_sentence
from .regular_cls import get_case_amount_sentence
from .regular_extracting import get_simple_instructions, get_front_instructions, get_other_instructions, \
    get_float_or_int_number, get_up_case_amount, get_simple_equation
from .regular_extracting import get_date
from .regular_extracting import get_case_amount

# 基于规则的分類方法
from elem_pickup.nlp_process import NLPProcess

REGULAR_CLS = {
    'simple_instructions': get_simple_instructions_sentence,
    'date': get_date_sentence,
    'case_amount': get_case_amount_sentence,
    'front_instructions': get_front_instructions_sentence,
    'other_instructions': get_other_instructions_sentence,
    'float_or_int': get_float_or_int_number_sentence,
    'up_case_amount':get_up_case_amount_sentence,
    'simple_equation':get_simple_equation_sentence,
}

# 基于规则的摘取方法
REGULAR_EXTRACTING = {
    'simple_instructions': get_simple_instructions,
    'date': get_date,
    'case_amount': get_case_amount,
    'front_instructions': get_front_instructions,
    'other_instructions': get_other_instructions,
    'float_or_int': get_float_or_int_number,
    'up_case_amount': get_up_case_amount,
    'simple_equation': get_simple_equation,
}


def __cls_by_regular(sentences: 'list[str]',
                     elem_id_dict: 'dict[str, str]',
                     elem_key_dict: 'dict[str, str]',
                     elem_type_dict: 'dict[str, str]') -> 'dict[str, str]':
    """
    通过规则进行句子分类，得到要素-句子字典

    :param sentences:  句子集合
    :param elem_id_dict: 要素-id字典
    :param elem_key_dict: 要素-要素关键字字典
    :param elem_type_dict: 要素-要素类型字典
    :return: 要素-句子字典
    """
    sentences_dict = dict()

    for elem_name in elem_id_dict.keys():
        elem_key = elem_key_dict[elem_name]
        elem_type = elem_type_dict[elem_name]
        cls_func = REGULAR_CLS[elem_type]
        sentences_dict[elem_name] = cls_func(sentences, elem_key)
    return sentences_dict


def __extracting_by_regular(sentences_dict: 'dict',
                            elem_id_dict: 'dict',
                            elem_key_dict: 'dict',
                            elem_type_dict: 'dict') -> 'dict[str, str]':
    """
    通过规则进行句子要素提取，得到要素-要素内容字典

    :param sentences_dict: 要素-句子字典
    :param elem_id_dict: 要素-id字典
    :param elem_key_dict: 要素-要素关键字字典
    :param elem_type_dict: 要素-要素类型字典
    :return:  要素-要素内容字典
    """
    content_dict = dict()
    for elem_name in elem_id_dict.keys():
        sentence = sentences_dict[elem_name]
        elem_key = elem_key_dict[elem_name]
        elem_type = elem_type_dict[elem_name]

        extracting_func = REGULAR_EXTRACTING[elem_type]
        content_dict[elem_name] = extracting_func(elem_key, sentence)
    return content_dict


def extracting(file_path: str,
               elem_id_dict: 'dict',
               elem_key_dict: 'dict',
               elem_type_dict: 'dict') -> 'dict[str, str]':
    """
    通过规则进行句子要素提取，得到要素-要素内容字典

    :param file_path: 文档路径
    :param elem_id_dict: 要素-id字典
    :param elem_key_dict: 要素-要素关键字字典
    :param elem_type_dict: 要素-要素类型字典
    :return:  要素-要素内容字典
    """
    sentences = NLPProcess(file_path, True, '。').sentences
    sentences = [punctuation_filter(ss) for ss in sentences if ss]

    sentences_dict = __cls_by_regular(sentences=sentences,
                                      elem_id_dict=elem_id_dict,
                                      elem_key_dict=elem_key_dict,
                                      elem_type_dict=elem_type_dict)
    # for key in sentences_dict:
    #     print(key, ':', sentences_dict[key])
    content_dict = __extracting_by_regular(sentences_dict=sentences_dict,
                                           elem_id_dict=elem_id_dict,
                                           elem_key_dict=elem_key_dict,
                                           elem_type_dict=elem_type_dict
                                           )
    # print()
    # for key in content_dict:
    #     print(key, ':', content_dict[key])
    return content_dict
