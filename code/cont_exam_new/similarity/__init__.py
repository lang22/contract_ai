#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/2/28 9:38
@Author     : jzs
@File       : __init__.py.py
@Software   : PyCharm
@Description: ......
"""
import torch
from gensim.models import Word2Vec
from sklearn.externals import joblib

from ..nn_model.SimplySimilarityNet import SimplySimilarityNet
from .process import process_sentence
from .word_vec import embedding


def load_word2vec_model(path: str):
    """
    读取word2vec模型

    :param path: 模型路径
    :return:
    """
    return Word2Vec.load(path)


def load_sklearn_model(path: str):
    """
    读取sklearn的模型
    :param path:模型路径
    :return:
    """
    return joblib.load(path)


def load_pytorch_model(path: str):
    """
    读取pytorch的模型

    :param path: 模型路径
    :return:
    """
    model = SimplySimilarityNet(300, 750)
    model.eval()
    return model


# 切换模型
similarity_model_dict = {
    'sklearn': load_sklearn_model,
    'pytorch': load_pytorch_model,
    'word2vec': load_word2vec_model
}


def get_pytorch_similarity(word2vec_model,
                           similarity_model,
                           sent1: str, sent2: str, ) -> float:
    """
    计算句子1和句子2的相似度

    :param word2vec_model: word2vec模型
    :param similarity_model: 该相似度模型
    :param sent1: 句子1
    :param sent2: 句子2
    :return:
    """

    sent1 = process_sentence(sent1)
    sent2 = process_sentence(sent2)

    sent1 = embedding(word2vec_model, similarity_model.words_size, sent1)
    sent2 = embedding(word2vec_model, similarity_model.words_size, sent2)

    return similarity_model(sent1, sent2)


