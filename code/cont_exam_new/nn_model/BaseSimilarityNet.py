#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/2/28 11:45
@Author     : jzs
@File       : BaseNLPNet.py
@Software   : PyCharm
@Description: ......
"""
import torch
import torch.nn as nn


class BaseSimilarityNet(nn.Module):
    """
    基础的NLP网络

    """

    def __init__(self, words_size, max_sentences_size):
        """
        初始化网络层

        :param words_size: 词向量大小
        :param max_sentences_size: 最大的句子长度
        """
        super(BaseSimilarityNet, self).__init__()
        self.words_size = words_size
        self.max_sentences_size = max_sentences_size

    def forward(self, *_input):
        pass

    def save(self, path: str):
        """
        保存模型

        :param path: 模型路径
        :return:
        """
        torch.save(self, path)
