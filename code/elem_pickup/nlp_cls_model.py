#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/10/18 10:23
@Author     : jzs
@File       : nlp_model.py
@Software   : PyCharm
@Description: ......
"""
import csv
import os
import pickle

import numpy as np
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression

from .get_contract_elements import get_contract_elements
from .get_sentences_label import load_highlight_paragraphs_dict, get_sliding_label, get_sentences_label
from .get_sentences_vector import get_co_occurrence_matrix_set, get_word_vector_set, get_vector_set
from .nlp_process import NLPProcess


class NLPCLSModel(object):
    """
    通过规定的sklearn分类模型，指定的语料库，抽取的关键字构建语言分类模型。
    可以在这个分类模型的上进行训练、预测、评估，还可以对预测结果进行评价
    """

    # 使用共现矩阵作为计算方式
    CO_OCCURRENCE_MATRIX = 'CO_OCCURRENCE_MATRIX'

    # 使用word2vec作为计算方式
    WORD2VEC = 'WORD2VEC'

    # 只是用TF-IDF作为计算方式
    PURE_TF_IDF = 'PURE_TF_IDF'

    # 训练模型使用的方法的函数指针
    FIT_METHOD = {
        'CO_OCCURRENCE_MATRIX': get_co_occurrence_matrix_set,
        'WORD2VEC': get_word_vector_set,
        'PURE_TF_IDF': get_vector_set,
    }

    def __init__(self,
                 path: str,
                 punc: 'List[str]',
                 keyword,
                 sliding_num,
                 nlpp=None,
                 model=LogisticRegression()):
        """
        初始化这次的分类模型，建立语料库，为训练准备
        :param path: 文档文件或文档文件夹路径
        :param punc: 分割标点符号列表，如('、','。','，')
        :param keyword: 选择的关键字
        :param sliding_num: 句子的滑窗数
        :param model: sklearn二分类的分类器模型，如SVC()、LogisticRegression()等，默认为SVC()
        """
        self.__cls_args = {  # 保存这次初始化函数的参数的参数
            'path': path,
            'punc': punc,
            'keyword': keyword,
            'sliding_num': sliding_num
        }
        self.__fit_error_flag = False  # 是否训练失败
        self.__fit_args = None  # 初始化这次训练函数的参数，参数格式(函数名，参数)
        self.__mode = model

        if nlpp:
            self.__nlpp = nlpp
        else:
            self.__nlpp = NLPProcess(path, os.path.isfile(path), *punc)

        self.__predict_result = {}
        self.__sentences = None
        self.__sentences_y = None
        sent, sli = get_contract_elements(keyword, sliding_num, self.__nlpp)
        hp_dic = load_highlight_paragraphs_dict(path, self.__cls_args['punc'], False)

        if sliding_num > 0:
            self.__sentences, self.__sentences_y = get_sliding_label(hp_dic, sli)
        else:
            self.__sentences, self.__sentences_y = get_sentences_label(hp_dic, sent)

    def __pre_X(self, sentences_: 'List[List[str]]', method: str, **method_args) -> 'list':
        """
        由self.fit()函数调用，为训练前做准备数据计算做准备
        :param sentences_:用于处理的分词后的句子句子
        :param method:输入字符串，若输入错误抛出异常
        :param method_args:该方法的参数，若参数错误抛出异常
        :return:返回X矩阵
        """

        fit_func = NLPCLSModel.FIT_METHOD.get(method)
        if not fit_func:
            raise ValueError('method的计算方式不在字典中')
        elif fit_func is get_co_occurrence_matrix_set:

            X = fit_func(nlpp=self.nlpp, sli_num=method_args['matric_sliding_num'],
                         sentences=sentences_,
                         calculator=NLPCLSModel.__calculator(method_args['calculator']))
        elif fit_func is get_word_vector_set:
            X = fit_func(nlpp=self.nlpp, sentences=sentences_,
                         calculator=NLPCLSModel.__calculator(method_args['calculator']))
        elif fit_func is get_vector_set:
            X = fit_func(nlpp=self.nlpp, sentences=sentences_)
        return X

    @staticmethod
    def __calculator(calculator_name: str):
        """
        将计算方式转化成lambda表达式
        :param calculator_name:
        :return:
        """
        if not calculator_name:
            return None
        if calculator_name == '+':
            return lambda x, y: x + y
        if calculator_name == '*':
            return lambda x, y: x * y

    def fit(self, method: str, **method_args) -> 'NLPCLSModel':
        """
        训练模型，能判断是那种方法，并能保存方法的参数，训练方法有三种
        1.CO_OCCURRENCE_MATRIX：使用共现矩阵作为计算方式
        （1）调用函数 get_co_occurrence_matrix_set(nlpp,sli_num,sentences,calculator)
        （2）method_args的参数，matric_sliding_num: 共现矩阵滑窗，calculator: 合并向量的计算器
        2.WORD2VEC：使用word2vec作为计算方式
        （1）你调用函数 get_word_vector_set(nlpp,sentences,calculator)
        （2）则**method_args为：calculator:合并向量的计算器
        3.PURE_TF_IDF：只是用TF-IDF作为计算方式
        （1）调用函数 get_vector_set()
        （2）则**method_args为：nlpp:语料库，sentences:句子集合
        4.参数calculator为合并向量的迭代方式，有三种，
        （1）calculator=None ：词向量*tfidf求和
        （2）calculator='+' ：求和
        （3）calculator='*' ：求积
        :param method: 输入字符串，若输入错误抛出异常
        :param method_args:该方法的参数，若参数错误抛出异常
        :return:该类本身对象self
        """

        self.__fit_args = (method, method_args)
        X = self.__pre_X(self.__sentences, method, **method_args)
        X = np.array(X)
        y = np.array(self.__sentences_y)
        try:
            self.mode.fit(X, y)
        except ValueError as e:
            self.__fit_error_flag = True
            print(e)
        finally:
            return self

    def refit(self, model, keyword, sliding_num, method, **method_args) -> 'NLPCLSModel':
        """
        更换分类模型和抽取的关键字，重新训练模型
        :param model:
        :param keyword:
        :param sliding_num:
        :param method:
        :param method_args:
        :return:
        """
        self.__mode = model
        self.__cls_args['keyword'] = keyword
        self.__cls_args['sliding_num'] = sliding_num
        self.fit(method, **method_args)

    def __load_sentences_X(self, doc_path: str) -> 'List[List[str]]':
        """
        读取新文档
        :param doc_path:
        :return:
        """
        if not os.path.isfile(doc_path):
            raise ValueError(doc_path + '路径错误!')
        new_doc = NLPProcess(doc_path, True, *self.__cls_args['punc'])

        # 得到要素包含要素的句子和该句子的滑窗
        sentences, sli = get_contract_elements(keyword=self.__cls_args['keyword'],
                                               k=0, nlpp=new_doc)

        return sentences, NLPProcess.sentences_to_words(sentences)

    def predict(self, doc_path) -> None:
        """
        进行预测，输入一篇新文章，通过已经记录的方法转化成词向量，进行预测，对于预测结果的TopN排序
        :param doc_path:
        :return:
        """
        # 加载新文章句子
        sentences, sentences_words = self.__load_sentences_X(doc_path)
        # 转化成相应的向量
        X = self.__pre_X(sentences_words, self.__fit_args[0], **self.__fit_args[1])
        X = np.array(X)

        if self.__fit_error_flag or not len(X):
            self.__predict_result = {
                'fit_error_flag': self.__fit_error_flag,
                'sentences': sentences}
        else:
            y_predict_lab = self.__mode.predict(X)
            y_predict_Pr = self.__mode.predict_proba(X)
            self.__predict_result = {
                'fit_error_flag': self.__fit_error_flag,
                'sentences': sentences,
                'y_predict_lab': y_predict_lab,
                'y_predict_Pr': y_predict_Pr,
                'topN_index': list(reversed(np.argsort(y_predict_Pr[:, -1])))
            }
        return self.__predict_result

    def topN(self, n: int, print_flag=False) -> str:
        """
        返回和打印预测结果的TopN
        :return:
        """
        try:
            sentences = self.__predict_result['sentences']
            y_predict_lab = self.__predict_result['y_predict_lab']
            y_predict_Pr = self.__predict_result['y_predict_Pr']
            topN_index = self.__predict_result['topN_index']
            if n > len(topN_index):
                n = len(topN_index)
            if print_flag:
                for i in topN_index[0:n]:
                    print('类别：', y_predict_lab[i], '，概率：', y_predict_Pr[i, 1], '，句子：', sentences[i])
            return [(i + 1, y_predict_lab[index], y_predict_Pr[index, 1], sentences[index])
                    for i, index in enumerate(topN_index[0:n])]
        except Exception as e:
            print(e)
            return []

    def evaluation(self) -> 'str':
        pass

    @staticmethod
    def write_predict_result(file_name, datas):
        """
        将数据写入csv文件
        :param file_name:
        :param datas:
        :return:
        """
        headline = ['序号', '类别', '类别1的概率', '句子']

        with open(file_name, 'w', newline='', encoding='GBK') as file:
            writer = csv.writer(file)
            writer.writerow(headline)
            for i in range(len(datas)):
                writer.writerow(datas[i])

    @property
    def mode(self):
        """
        sklearn二分类的分类器模型
        :return: sklearn中的
        """
        return self.__mode

    @mode.setter
    def mode(self, value):
        """
        更换klearn二分类的分类器模型
        :param value:
        :return:
        """
        self.__mode = value

    @property
    def nlpp(self):
        """
        经过预处理的语料库
        :return:
        """
        return self.__nlpp

    @property
    def predict_result(self):
        """
        一次预测的结果
        predict_result['sentences']: 预测的句子
        predict_result['y_predict_lab']: 被预测的句子标签
        predict_result['y_predict_Pr']: 被预测句子的概率
        predict_result['topN_index']: 预测的句子的topN排序
        :return:
        """
        return self.__predict_result

    @property
    def cls_args(self):
        """
        这次初始化函数的参数的参数字典
        :return:
        """
        return self.__cls_args

    @property
    def y_train(self):
        """
        得到训练集的y集合

        :return:
        """
        return self.__sentences_y

    @property
    def X_train(self):
        """
        得到训练集的X集合

        :return:
        """
        return self.__sentences

    def dump_cls_model(self, file_name: str) -> None:
        """
        将分类器模型保存
        :param file_name:文件路径
        :return:
        """

        joblib.dump(self.mode, file_name)

    @staticmethod
    def load_cls_model(file_name: str):
        """
        读取分类器模型
        :param file_name: 文件路径
        :return:
        """
        return joblib.load(file_name)

    @staticmethod
    def dump(file_path_obj: str, file_name_model: str, nlpcls: 'NLPCLSModel'):
        """
        将NLPCLSModel对象持久化存储，并保存分类器模型

        :param file_path_obj:
        :param file_name_model:
        :return:
        """
        nlpcls.dump_cls_model(file_name_model)
        with open(file_path_obj, 'wb') as f:
            pickle.dump(nlpcls, f)

    @staticmethod
    def load(file_path_obj: str, file_name_model: str):
        """
        将NLPCLSModel对象从文件中读取

        :param file_path_obj:
        :param file_name_model:
        :return:
        """
        mode = NLPCLSModel.load_cls_model(file_name_model)
        with open(file_path_obj, 'rb') as f:
            obj = pickle.load(f)
            obj.mode = mode
            return obj

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()
