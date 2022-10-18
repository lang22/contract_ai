#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/12/20 10:03
@Author     : jzs
@File       : exam_title.py
@Software   : PyCharm
@Description: ......
"""
import re

from exam_clause.exam_process import DIFFERENT_STRING, SIMILAR_STRING, SAME_STRING, SIMILARITY_STRING
from exam_clause.semantic_model import simply_similarity

# 相似度阈值
SIMILARITY_MAX_VALUE = 0.50


def __title_similarity(test, model_title_dict: dict):
    """
    找到在模板字典中最大的
    :param test:
    :param model_title_dict:
    :return:
    """

    sim_table = [(mt, simply_similarity(test, mt)) for mt in model_title_dict.keys()]

    max_key, max_sim = max(sim_table, key=lambda x: x[1])

    return max_key if max_sim >= SIMILARITY_MAX_VALUE else None


def __get_clause_title_different_list(test_title, model_title_dict, test_title_dict):
    """
    通过条款标题字典的对比，判断是否一致，并返回对比结果

    :param test_title: 待审核文档的条款标题
        [['第一条', '定义'], ['第二条', '债权的转让']]
    :param model_title_dict: 模板文档的条款标题字典
        {'定义': 0, '债权的转让': 1}
    :param test_title_dict: 待审核文档的条款标题字典
        {'定义': 0, '债权的转让': 1}
    :return:

    """
    clause_result = list()
    for title in test_title:
        test_title_index = test_title_dict.get(title[1])
        model_title_index = model_title_dict.get(title[1])

        if model_title_index is None:
            # 在模板标题字典中不存在，即不一致，无条款或有极相似条款
            max_key = __title_similarity(title[1], model_title_dict)

            if max_key:
                # 在模板标题字典中不存在，即不一致，有极相似条款
                model_title_index = model_title_dict.get(max_key)
                s2 = SIMILARITY_STRING[2].replace('n', str(model_title_index + 1))
                result = (title[0], title[1], SIMILARITY_STRING[0], SIMILARITY_STRING[1], s2, model_title_index)
                pass
            else:
                # 在模板标题字典中不存在，即不一致，无条款
                result = (title[0], title[1], *DIFFERENT_STRING, -1)

        elif test_title_index != model_title_index:
            # 在模板标题字典中存在但位置不一致，即有此条款，在第n条
            s2 = SIMILAR_STRING[2].replace('n', str(model_title_index + 1))
            result = (title[0], title[1], SIMILAR_STRING[0], SIMILAR_STRING[1], s2, model_title_index)

        elif test_title_index == model_title_index:
            # 在模板标题字典中存在，且位置一致，即一致，通过
            result = (title[0], title[1], *SAME_STRING, model_title_index)

        clause_result.append(result)
    return clause_result


def clause_title_exam(model_clause_paragraphs_list: 'list[list[str]]',
                      test_clause_paragraphs_list: 'list[list[str]]'):
    """
    合同条款的标题的检验, 返回这样的元祖list
    对比结果元祖格式（第几条，条款标题，一致性Flag，是否一致，备注1，备注2）
    其中的 “ 一致性Flag，是否一致，备注1，备注2 ” 分成四类，分别是:
    1.条款一致，输出的字符串: 1, '一致', '通过'
    2.条款不一致，输出的字符串: 0, '不一致', '无该条款'
    3.条款完全相似，输出的字符串 : [2, '不一致', '对应第n条']
    3.条款相似，输出的字符串: [3, '不一致', '与第n条相似']

    :param model_clause_paragraphs_list:
        模板文档的条款集合list
    :param test_clause_paragraphs_list:
        审核文档的条款集合list
    :return:
    """

    # todo 分割成 [['第一条', '定义'], ['第二条', '债权的转让']]
    model_title = [re.split(r'\s+', p[0]) for p in model_clause_paragraphs_list]
    test_title = [re.split(r'\s+', p[0]) for p in test_clause_paragraphs_list]

    model_title_dict = dict((t[1], i) for i, t in enumerate(model_title))
    test_title_dict = dict((t[1], i) for i, t in enumerate(test_title))

    return __get_clause_title_different_list(test_title,
                                             model_title_dict,
                                             test_title_dict)
