#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/10/29 15:27
@Author     : jzs
@File       : __init__.py.py
@Software   : PyCharm
@Description: ......
"""
import os


from .nlp_cls_model import NLPCLSModel

# 缓存模型的字典
MODEL_CACHE = {}


def pikeup(obj_file_path: str,
           model_file_path: str,
           predict_doc_path: str,
           number: int):
    """
    合同要素抽取
    输入：相应的合同要素的模型和分类器路径，以及需要抽取的文件的路径。
    输出：得到对应合同要素的topN排序

    :param obj_file_path: 合同要素的分类器模型，类NLPCLSModel的持久化对象的路径
    :param model_file_path: 对应的合同要素的sklearn模型的持久化对象的路径
    :param predict_doc_path: 需要预测的文档的路径
    :param number: topN数
    :return:
    """

    if not isinstance(obj_file_path, str) or not os.path.exists(obj_file_path):
        raise ValueError('is not str or not exists :', obj_file_path)
    if not isinstance(model_file_path, str) or not os.path.exists(model_file_path):
        raise ValueError('is not str or not exists :', model_file_path)
    if not isinstance(predict_doc_path, str) or not os.path.exists(predict_doc_path):
        raise ValueError('is not str or not exists :', predict_doc_path)
    if not isinstance(number, int) or number <= 0:
        raise ValueError('is not int or <= 0 :', number)

    model = NLPCLSModel.load(obj_file_path, model_file_path)
    model.predict(predict_doc_path)
    return model.topN(number, True)

