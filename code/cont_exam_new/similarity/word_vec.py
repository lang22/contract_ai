#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/2/27 15:42
@Author     : jzs
@File       : train_vec.py
@Software   : PyCharm
@Description: word2vec有关
"""
import os
import numpy as np
from gensim.models import Word2Vec

from config import BASE_DIR

# 词向量字典路径
WORD2VEC_MODEL = os.path.join(BASE_DIR, 'exam_clause/data/word2vec.model')

# 词向量长度
WORDS_SIZE = 100


def train_word2vec_model(sentences: 'list[list[str]]',
                         words_size=WORDS_SIZE,
                         words_window=2,
                         min_count=1, **other):
    """
    训练词向量的模型

    :param min_count: 最小出现次数
    :param words_window: 词滑窗
    :param words_size: 词向量长度
    :param sentences: 分词后的句子集合
    :return:
    """
    print('开始训练word2vec...')
    model = Word2Vec(sentences, window=words_window,
                     size=words_size, min_count=min_count,
                     workers=10, sg=1, **other)
    model.save(WORD2VEC_MODEL)
    print('训练成功...')
    return model


def load_word2vec_model():
    """
    读取word2vec模型
    :return:
    """
    return Word2Vec.load(WORD2VEC_MODEL)


def embedding(word2vec_model, words_size, sentence: list):
    """
    将句子转换成词向量矩阵

    :param word2vec_model: word2vec模型
    :param words_size: 词向量长度
    :param sentence: 句子
    :return:
    """
    zeros = np.zeros(words_size)
    return [word2vec_model[word] if word in word2vec_model else zeros for word in sentence]
