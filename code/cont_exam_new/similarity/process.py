#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/2/28 10:10
@Author     : jzs
@File       : process.py
@Software   : PyCharm
@Description: nlp的预处理
"""
import os

import jieba

from config import BASE_DIR

# 停用词字典路径
STOP_WORD_PATH = os.path.join(BASE_DIR, 'cont_exam_new/data/stop_word.model')

# 停用词字典
STOP_WORD_DICT = dict((e, i) for i, e in enumerate(open(STOP_WORD_PATH, 'r', encoding='UTF-8').read()))

# 标点
punctuation = r"""!"#$%&'()*+-/:;<=>?@[\]^_`{|}~，。、【 】 “”；（）《》‘’{}？！⑦()、%^>℃”“^-——=&#@￥～★―.1234567890
qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM"""
PUNCTUATION_DICT = dict((e, i) for i, e in enumerate(punctuation))


def punctuation_filter(sentence: str) -> str:
    """
    去除标点符号和空格符号

    :param sentence:句子
    :return:
    """
    if not sentence or not isinstance(sentence, str):
        return str()

    sentence = list(filter(lambda x: x not in PUNCTUATION_DICT, sentence))
    sentence = str().join(sentence)
    return str().join(sentence.split())


def process_sentence(sentence: str) -> 'list[str]':
    """
    预处理句子(句子不为空)，去标点、空格、去停用词

    :param sentence:
    :return:
    """
    sentence = punctuation_filter(sentence)
    words = list(jieba.cut(sentence))
    if len(words) > 1:
        words = list(filter(lambda x: x not in STOP_WORD_DICT, words))
    return words


def process_sentences(sentences: 'list[str]') -> 'list[list[str]]':
    """
    将多个句子预处理,预处理句子(句子不为空)，去标点、空格、去停用词

    :param sentences: 句子集合
    :return:
    """
    tmp = list(map(process_sentence, sentences))
    return list(filter(lambda x: len(x) > 0, tmp))
