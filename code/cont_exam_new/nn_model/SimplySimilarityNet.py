#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/2/28 10:29
@Author     : jzs
@File       : SimplySimilarityNet.py
@Software   : PyCharm
@Description: ......
"""

import numpy as np
import torch
import torch.nn as nn

# 默认词向量长度
from ..nn_model.BaseSimilarityNet import BaseSimilarityNet

DEFAULT_WORDS_SIZE = 100

# 默认最大句子长度个数
DEFAULT_MAX_SENTENCES_SIZE = 10


class SimplySimilarityNet(BaseSimilarityNet):
    """
    简单的相似度网络

    网络结构：
    输入1->词嵌入层->平均池化层->
                                余弦相似度层->输出
    输入2->词嵌入层->平均池化层->
    """

    def __init__(self, words_size=DEFAULT_WORDS_SIZE,
                 max_sentences_size=DEFAULT_MAX_SENTENCES_SIZE):
        """
        初始化网络层

        :param words_size: 词向量大小
        :param max_sentences_size: 最大的句子长度
        """
        super(SimplySimilarityNet, self).__init__(words_size, max_sentences_size)
        self.pooling = nn.AvgPool2d(kernel_size=(max_sentences_size, 1))
        self.cos = nn.CosineSimilarity(dim=1, eps=1e-08)

    def forward(self, input1, input2) -> float:
        """
        前向传播，计算句子1和句子2的相似度

        :param input1: 输入句子1的embedding矩阵
        :param input2: 输入句子2的embedding矩阵
        :return:
        """
        input1 = self.padding(input1)
        input2 = self.padding(input2)

        input1 = self.pooling(input1).squeeze(0)
        input2 = self.pooling(input2).squeeze(0)

        ret = self.cos(input1, input2)
        return abs(float(ret.numpy().astype(np.float32)))

    def padding(self, sentence: list):
        """
        句子矩阵补0，并返回句子张量
        :param sentence:  句子矩阵
        :return:
        """
        size = self.max_sentences_size - len(sentence)

        if size > 0:
            zeros = np.zeros(self.words_size)
            sentence.extend([zeros] * size)

        return torch.DoubleTensor(sentence).unsqueeze(0)
