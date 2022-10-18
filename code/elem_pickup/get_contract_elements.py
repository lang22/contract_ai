#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/9/28 9:14
@Author     : jzs
@File       : get_contract_elements.py
@Software   : PyCharm
@Description: 得到合同要要素，以及给定数量的滑窗
"""

from .nlp_process import NLPProcess

# 滑窗范围
SLIDING_RANGE = (0, 20)


def sliding_range(k: int, mindex: int, length: int) -> 'range':
    """
    得到滑窗下标范围，得到一个range
    :param k: 滑窗大小
    :param mindex: 中点下标
    :param length: 句子列表长度
    :return:
    """
    start = mindex - k if mindex - k > 0 else 0
    end = mindex + k + 1 if mindex + k < length - 1 else length
    return range(start, end)


def get_contract_elements(keyword: str, k: int, nlpp: 'NLPProcess'):
    """
    读取文件,并得到包含合同要要素的句子，以及给定数量的滑窗
    :param keyword:要截取的关键字
    :param k:滑窗大小
    :param nlpp: nlp预处理对象
    :return:
    """
    if not keyword:
        raise ValueError('keyword is null')
    if k > SLIDING_RANGE[1] or k < SLIDING_RANGE[0]:
        raise ValueError('k out of range')
    if not nlpp or not isinstance(nlpp, NLPProcess):
        raise ValueError('nlpp is error')

    sentences = nlpp.sentences


    element_sentences = list()
    element_sentences_index = list()

    for i in range(len(sentences)):
        if sentences[i].find(keyword) < 0:
            continue
        element_sentences.append(sentences[i])
        element_sentences_index.append(i)
    if k == 0:
        return element_sentences, list()
    element_sliding = list()
    for mi in element_sentences_index:
        r = sliding_range(k, mi, len(sentences))
        element_sliding.append([sentences[i] for i in r])
    return element_sentences, element_sliding
