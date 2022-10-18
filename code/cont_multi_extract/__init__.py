#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019-05-07 13:48
@Author     : charles
@File       : __init__.py.py
@Software   : PyCharm
@Description: ......
"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-
from app.tools import join_path
from config import Config

"""
@Time       : 2019-05-07 13:48
@Author     : charles
@File       : process_test.py
@Software   : PyCharm
@Description: ......
"""
import os

from app.models.cont_ext_element_table import ContExtElementTable
from elem_extract import REGULAR_CLS, REGULAR_EXTRACTING
from elem_extract.base_regular import punctuation_filter
from elem_pickup.nlp_process import NLPProcess


def get_content_dict(file_path, elem_lis: list):
    """
    传入一个文件，以及全部的要素，在文件中抽取所有的可能存在的要素-要素内容
    :param file_path:文件路径
    :param elem_lis:
    :return:
    """
    # file_path = join_path(Config.CONT_MULTI_EXAM_PATH, file)

    # 获得文档经过处理之后的句子集合
    sentences = NLPProcess(file_path, True, '。').sentences
    sentences = [punctuation_filter(ss) for ss in sentences if ss]

    result_dic = {}

    for elem_name in elem_lis:

        cur_content = ''

        temp_sentences = sentences

        key_type_dic = ContExtElementTable.get_elements_key_type_dic(elem_name)

        for key in key_type_dic.keys():
            # 现在elem_name, elem_key, elem_type都已经有了
            # 先查找到要素所在的句子，然后在句子中提取要素内容，当提取到一个内容之后，就结束匹配，进行下一个要素的匹配
            type = key_type_dic[key]
            cls_func = REGULAR_CLS[type]
            sent = cls_func(temp_sentences, key)  # 要素所在的句子

            if not sent and key != '币种':  # 这个key-type规则没有匹配到句子
                continue

            extracting_func = REGULAR_EXTRACTING[type]
            cur_content = extracting_func(key, sent)

            # if elem_name == '受托方代表人':
            #     print(key, type)
            #     print(sent)

            break

        if not cur_content:
            cur_content = '--'

        result_dic[elem_name] = cur_content

    return result_dic


def multi_extracting(contract_name_list: list, file_path_list: list):
    """
    多文档要素识别主函数
    遍历file_lis中的每个文件，获得每个文件的要素-内容字典
    :param file_path_list: 文件路径列表
    :param contract_name_list: 合同文件名列表
    :return: 每个文件对应的要素-内容字典 的 字典
    """
    elem_lis = ContExtElementTable.get_column_element('elem_name')

    content_dict_dic = {}  # 存储每个文件对应的要素内容字典

    for i, file_name in enumerate(contract_name_list):
        content_dict = get_content_dict(file_path_list[i], elem_lis)
        content_dict_dic[file_name] = content_dict

    not_ex = []  # 记录下所有文档中都没有的要素

    for element in elem_lis:
        flag = 0
        for file in content_dict_dic:
            if content_dict_dic[file][element] != '--':
                flag = 1
                break
        if flag == 0:  # 所有文档都没有这个要素，就把这个要素删掉
            not_ex.append(element)

    for item in not_ex:
        elem_lis.remove(item)

    return content_dict_dic, elem_lis

#
# if __name__ == '__main__':
#     file_lis = ['债权转让协议_一般企业债权.docx', '债权转让协议_保证协议（法人保证）.docx', '债权转让协议_保证协议（自然人保证）.docx',
#                 '债权转让协议_信托公司信托资金信托贷款债权.docx', '债权转让协议_信托公司自有资金信托贷款债权.docx']
#
#     ext_res_dic = multi_extracting(file_lis)
