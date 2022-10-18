#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/10/25 11:06
@Author     : jzs
@File       : test_elem_statistics.py
@Software   : PyCharm
@Description: 统计合同要素
"""
import csv
import os
from collections import Counter

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from . import NLPCLSModel
from .nlp_process import NLPProcess

ELEMENT_NAME_KEY_LIST_FILE = 'element_list/element.csv'

ELEMENT_VALID_NAME_KEY_LIST_FILE = 'element_list/element_valid.csv'


def predict(path, punc, keyword, nlpp):
    """
    得到预测的标签
    """
    print('# 开始处理合同关键字：', keyword)
    print('# 正在预处理...')
    nlp_cls_model = NLPCLSModel(
        path=path,
        punc=punc,
        keyword=keyword,
        nlpp=nlpp,
        sliding_num=0,
        model=LogisticRegression()
    )
    print('# 正在训练...')
    nlp_cls_model.fit(NLPCLSModel.CO_OCCURRENCE_MATRIX,
                      matric_sliding_num=2,
                      calculator=lambda x, y: x + y)
    print('# 正在预测...')
    nlp_cls_model.predict('test_data/test6.docx')
    return nlp_cls_model.predict_result


# 代替lambda表达式的函数
def plus(x, y): return x + y


def dump_cls_model(path,
                   punc,
                   keyword,
                   sliding_num,
                   file_path_obj: str,
                   file_name_model: str):
    """
    保存预测的模型
    :param sliding_num:
    :param path:
    :param punc:
    :param keyword:
    :param file_path_obj:
    :param file_name_model:
    :return:
    """
    print('# 开始处理合同关键字：', keyword)
    nlp_cls_model = NLPCLSModel(
        path=path,
        punc=punc,
        keyword=keyword,
        sliding_num=sliding_num,
        model=LogisticRegression()
    )

    nlp_cls_model.fit(NLPCLSModel.CO_OCCURRENCE_MATRIX,
                      matric_sliding_num=2,
                      calculator=plus)
    print('# 正在保存...')
    nlp_cls_model.dump_cls_model(file_name_model)
    NLPCLSModel.dump(file_path_obj, file_name_model, nlp_cls_model)

    # print(nlp_cls_model)
    # a = NLPCLSModel.load(file_path_obj, file_name_model)
    # a.predict('test_data/test6.docx')
    # top5 = nlp_cls_model.topN(5, False)


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
    return model.topN(number)


# if __name__ == "__main__":
#     pikeup('model_data/受让方_NLPCLSModel.obj',
#            'model_data/受让方_LR_CO_OCCURRENCE_MATRIX_plus_0.model',
#            'test_data/test6.docx',
#            5)

if __name__ == "__main__":
    dump_cls_model(path='../source_data/',
                   punc=['。', '，'],
                   keyword='转让方',
                   sliding_num=0,
                   file_path_obj='model_data/转让方_NLPCLSModel.obj',
                   file_name_model='model_data/转让方_LR_CO_OCCURRENCE_MATRIX_plus_0.model')

    dump_cls_model(path='../source_data/',
                   punc=['。', '，'],
                   keyword='受让方',
                   sliding_num=0,
                   file_path_obj='../model_data/受让方_NLPCLSModel.obj',
                   file_name_model='../model_data/受让方_LR_CO_OCCURRENCE_MATRIX_plus_0.model')

    # a = NLPCLSModel.load('model_data/受让方_NLPCLSModel.obj',
    #                      'model_data/受让方_LR_CO_OCCURRENCE_MATRIX_plus_0.model')
    # a.predict('test_data/test6.docx')
    # top5 = a.topN(5, True)
