#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/2/27 15:42
@Author     : jzs
@File       : train_vec.py
@Software   : PyCharm
@Description: ......
"""
import os

import jieba
from gensim.models import Word2Vec

from config import BASE_DIR
from exam_clause.exam_process import punctuation_filter

# 停用词字典路径
STOP_WORD_PATH = os.path.join(BASE_DIR, 'exam_clause/stop_word.model')

# 词向量字典路径
WORD2VEC_MODEL = os.path.join(BASE_DIR, 'exam_clause/word2vec.model')

# 停用词字典
STOP_WORD_DICT = dict((e, i) for i, e in enumerate(open(STOP_WORD_PATH, 'r', encoding='UTF-8').read()))

# 词向量长度
WORDS_SIZE = 100

# 最大句子长度个数
MAX_SENTENCES_SIZE = 10


def train_word2vec_model(sentences: 'list[list[str]]',
                         words_size=WORDS_SIZE,
                         words_window=2,
                         min_count=1):
    """
    训练词向量的模型
    :param min_count:
    :param words_window:
    :param words_size:
    :param sentences: 分词后的句子集合
    :return:
    """
    model = Word2Vec(sentences, window=words_window,
                     size=words_size, min_count=min_count,
                     workers=10, sg=1)
    model.save(WORD2VEC_MODEL)
    print('训练成功...')
    return model


def load_word2vec_model():
    """
    读取word2vec模型
    :return:
    """
    return Word2Vec.load(WORD2VEC_MODEL)


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
    将多个句子预处理

    :param sentences: 句子集合
    :return:
    """
    tmp = list(map(process_sentence, sentences))
    return list(filter(lambda x: len(x) > 0, tmp))
