#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/9/29 11:22
@Author     : jzs
@File       : get_sentences_vector.py
@Software   : PyCharm
@Description: 主要将句子集合转化成句子向量
"""
import math
import numpy as np
from collections import Counter
from functools import reduce

from sklearn import preprocessing

from .get_contract_elements import sliding_range
from .nlp_process import NLPProcess


def tf(word: str, word_bag: "Counter", words_sum: int) -> 'float':
    """
    计算一个词的tf值
    :param word: 词
    :param word_bag: 该词所在的句子词袋，数据结构为：dict（词：词频）
    :param words_sum: 句子所有词的词频之和
    :return:
    """
    if not word_bag.get(word) or not words_sum:
        return 0
    return word_bag[word] / words_sum


def idf(word: str, word_bag_list: "List[Counter]") -> 'float':
    """
    计算一个词的idf值
    :param word: 词
    :param word_bag_list: 句子词袋集合
    :return:
    """
    nw = sum(1 for word_bag in word_bag_list if word_bag.get(word))
    if not nw or not len(word_bag_list):
        return 0
    N = len(word_bag_list)
    return math.log(N / (nw + 1))


def tf_idf(word: 'str', word_bag: "Counter", word_bag_list: "List[Counter]") -> 'float':
    """
    计算一个词的tfidf
    :param word: 词
    :param word_bag: 该句子的词袋
    :param word_bag_list: 所有句子的词袋
    :return:
    """
    words_sum = sum(word_bag.values())
    return tf(word, word_bag, words_sum) * idf(word, word_bag_list)


def to_vector(index_dict: 'Dict[str,int]',
              sentence: 'list[str]',
              word_bag: "Counter",
              word_bag_list: "List[Counter]") -> 'List[float]':
    """
    计算一个句子中的每一个词的tf-idf值，并将一个句子转化成n位向量集合
    :param index_dict: 语料库特征向量字典
    :param sentence: 句子
    :param word_bag: 该句子的词袋
    :param word_bag_list: 所有句子的词袋
    :return:
    """
    vector = [0] * len(index_dict)
    words_sum = sum(word_bag.values())
    for word in sentence:
        index = index_dict.get(word)
        if not index:
            continue
        tf_idf = tf(word, word_bag, words_sum) * idf(word, word_bag_list)

        vector[index] = tf_idf
    return vector


def get_vector_set(nlpp: 'NLPProcess', sentences: 'List[list[str]]') -> 'list[List[int]]':
    """
    将句子集合传化成n维特征向量集合
    :param nlpp: 语料库
    :param sentences: 句子集合
    :return:
    """
    word_bag_list = [Counter(sen) for sen in sentences]
    index_dict = nlpp.eigenvector_dict
    return [to_vector(index_dict,
                      sentences[i],
                      word_bag_list[i],
                      word_bag_list)
            for i in range(len(sentences))]


def get_word_vector_set(nlpp: 'NLPProcess', sentences: 'List[list[str]]', calculator):
    """
    将句子集合传化成词向量向量集合

    :param nlpp:语料库
    :param sentences:句子集合
    :param calculator:计算器
    :return:二维numpy.ndarray
    """
    vectors = list()
    word_dict = nlpp.word2vec_dict

    tf_idf_flag = False
    if not calculator:
        word_bag_list = [Counter(sen) for sen in sentences]
        calculator = lambda x, y: x + y
        tf_idf_flag = True

    for i, sentence in enumerate(sentences):
        if not tf_idf_flag:
            vector = [word_dict[word] for word in sentence if word in word_dict]
        else:
            vector = [
                tf_idf(word, word_bag_list[i], word_bag_list) * word_dict[word]
                for word in sentences[i]
                if word in word_dict]
        vector = reduce(calculator, vector)
        vectors.append(vector)

    return vectors


def get_co_occurrence_matrix(nlpp: 'NLPProcess', sli_num: 'int'):
    """
    得到词库的共现矩阵
    词库的共现矩阵,如：
       w1,  w2,...,  wn
    w1 c11,c12,..., c1n
    w2 c11,c12,..., c1n
    ...    .....
    wn c11,c12,..., c1n
    :param nlpp: 语料库
    :param sli_num: 滑窗数
    :return:
    """
    word_dict: dict = nlpp.eigenvector_dict
    coo_mat = np.zeros(shape=(len(word_dict), len(word_dict)))
    for sentence in nlpp.words_sentences:
        for si in range(len(sentence)):
            mi = word_dict.get(sentence[si])
            for i in sliding_range(sli_num, si, len(sentence)):
                if i != si:
                    mj = word_dict.get(sentence[i])
                    coo_mat[mi, mj] += 1
    # 共现矩阵标准化
    x_scaled = preprocessing.scale(coo_mat)
    return x_scaled


def co_occurrence_matrix_dist(word, nlpp, matrix):
    """
    得到共现的一个词的array向量
    :param word:词
    :param nlpp:语料库
    :param matrix:共现矩阵
    :return:
    """
    index_dict = nlpp.eigenvector_dict
    i = index_dict.get(word, -1)
    return matrix[i] if i else np.zeros(shape=len(matrix))


def get_co_occurrence_matrix_set(nlpp: 'NLPProcess',
                                 sli_num: 'int',
                                 sentences: 'List[list[str]]',
                                 calculator):
    """
    通过共现矩阵转化成句子向量
    :param nlpp: 语料库
    :param sli_num: 共现矩阵滑窗
    :param sentences: 句子集合
    :param calculator: 合并向量的计算器
    :return:
    """

    matrix = get_co_occurrence_matrix(nlpp, sli_num)
    vectors = list()
    word_dict = co_occurrence_matrix_dist

    tf_idf_flag = False
    if not calculator:
        word_bag_list = [Counter(sen) for sen in sentences]
        calculator = lambda x, y: x + y
        tf_idf_flag = True

    for i, sentence in enumerate(sentences):
        if not tf_idf_flag:
            vector = [word_dict(word, nlpp, matrix) for word in sentence]
        else:
            vector = [tf_idf(word, word_bag_list[i], word_bag_list) * word_dict(word, nlpp, matrix)
                      for word in sentences[i]]
        vector = reduce(calculator, vector)

        vectors.append(vector)
    return vectors
