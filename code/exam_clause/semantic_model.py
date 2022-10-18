#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/12/28 9:53
@Author     : jzs
@File       : semantic_model.py
@Software   : PyCharm
@Description: ......
"""
import os
import jieba
import numpy as np
import torch.nn as nn
import torch
from gensim.models import Word2Vec
from torch import Tensor

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


class SimplySimilarityNet(nn.Module):
    """
    简单的相似度网络

    网络结构：
    输入1->词嵌入层->平均池化层->
                                余弦相似度层->输出
    输入2->词嵌入层->平均池化层->
    """

    def __init__(self):
        super(SimplySimilarityNet, self).__init__()
        self.model = load_word2vec_model()
        self.pooling = nn.AvgPool2d(kernel_size=(MAX_SENTENCES_SIZE, 1))
        self.cos = nn.CosineSimilarity(dim=1, eps=1e-6)

    def embedding(self, sentence: list):
        """
        将句子转换成词向量矩阵
        :param model:
        :param sentence:
        :return:
        """
        zeros = np.zeros(WORDS_SIZE)
        return [self.model[word] if word in self.model else zeros for word in sentence]

    def forward(self, input1, input2) -> float:
        """
        前向传播，计算句子1和句子2的相似度

        :param input1: 输入句子1矩阵
        :param input2: 输入句子2矩阵
        :return:
        """

        input1 = self.embedding(input1)
        input2 = self.embedding(input2)

        input1 = SimplySimilarityNet.padding(input1)
        input2 = SimplySimilarityNet.padding(input2)

        input1 = self.pooling(input1).squeeze(0)
        input2 = self.pooling(input2).squeeze(0)

        ret = self.cos(input1, input2)
        return float(ret.numpy().astype(np.float32))

    @staticmethod
    def padding(sentence: list):
        """
        句子矩阵补0，并返回句子张量
        :param sentence:  句子矩阵
        :return:
        """
        size = MAX_SENTENCES_SIZE - len(sentence)

        if size > 0:
            zeros = np.zeros(WORDS_SIZE)
            sentence.extend([zeros] * size)

        return torch.DoubleTensor(sentence).unsqueeze(0)


def simply_similarity(sent1: str, sent2: str) -> float:
    """
    计算简单相似度
    :param sent1: 句子1
    :param sent2: 句子2
    :return:
    """
    similarity = SimplySimilarityNet()
    sent1 = process_sentence(sent1)
    sent2 = process_sentence(sent2)
    return similarity(sent1, sent2)


if __name__ == '__main__':
    t = simply_similarity("定义与解释", "定义与解释 ")
    print(t)
