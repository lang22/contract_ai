#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/9/28 11:37
@Author     : jzs
@File       : get_sentences_label.py
@Software   : PyCharm
@Description: ......
"""
import os
from typing import *

from .get_highlight_paragraphs import get_highlight_paragraphs
from .nlp_process import NLPProcess


def load_highlight_paragraphs_dict(path: str, punc: str, isfile: bool) -> 'Dict[str,int]':
    """
    从文件夹或docx文档中读取，并处里获得被标注的句子
    :param punc:
    :param path: 文件路径
    :param isfile: 是否是单个文件
    :return:
    """
    try:
        if isfile:
            list1 = get_highlight_paragraphs(path)
            list1 = NLPProcess.paragraphs_to_sentences(punc, list1)
            list2 = [i for i in range(len(list1))]
        else:
            file_path_set = os.listdir(path)
            list1 = list()
            for file_path in file_path_set:
                list1.extend(get_highlight_paragraphs(path + '/' + file_path))
                list1 = NLPProcess.paragraphs_to_sentences(punc, list1)
                list2 = [i for i in range(len(list1))]
        return dict(zip(list1, list2))
    except BaseException as e:
        print(e)
        return dict()


def get_sentences_label(h_dic: 'Dict[str,int]', sentences: 'List[str]') -> 'List[list[str]], List[int]':
    """
    读取高亮句子字典和一个要素句子列表, 将句子标注后，再将句子分词
    :param h_dic:高亮句子字典
    :param sentences:一个要素句子列表
    :return:要素句子列表, 要素句子的标签
    """
    y = list(map(lambda x: 1 if h_dic.get(x) else 0, sentences))

    sentences = NLPProcess.sentences_to_words(sentences)

    return sentences, y


def get_sliding_label(h_dic: 'Dict[str,int]', slidings: 'List[List[str]]') -> 'Tuple':
    """
    读取高亮句子字典和一个要素句子滑窗列表，将句子标注后，再将句子分词
    :param h_dic:高亮句子字典
    :param slidings:一个要素句子滑窗
    :return:
    """

    # 判断一个滑窗中是否包含高亮句子
    def contain(x):
        table = sum([1 if h_dic.get(e) else 0 for e in x])
        return 1 if table > 0 else 0

    y = list(map(contain, slidings))

    tmp = list()
    for sl in slidings:
        words = list()
        sl = NLPProcess.sentences_to_words(sl)
        for w in sl:
            words.extend(w)
        tmp.append(words)

    return tmp, y
