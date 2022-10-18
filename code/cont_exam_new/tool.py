#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/2/26 17:15
@Author     : jzs
@File       : tool.py
@Software   : PyCharm
@Description: ......
"""
import re

from docx import Document

document = Document("D:/合同机器人项目相关/条款审核测试文档/HR-CK-04-E-债权转让协议（信托公司信托资金信托贷款债权）.docx")
para_list = list(document.paragraphs)

re_str = r'(.{0,3}?|\s*?)第.{1,3}条.{1,30}?$'
indexs = [(i, para.text.strip()) for i, para in enumerate(para_list) if re.match(re_str, para.text)]

for i, s in indexs:
    print(i, s.split())

re_str = r'(.{0,3}?|\s*?)第.{1,3}条.{1,30}?$'


def get_clause_paragraphs_list(para_list: 'List'):
    """
    划分word文档，得到docx文档的条款部分

    :param para_list: 段落(paragraph类型 )list
    :return: 返回首页段落list，非条款list，条款集合list
    """

    indexs = [i for i, para in enumerate(para_list) if re.match(re_str, para.text)]
    # 处理非条款
    not_clause_paragraphs = list(filter(lambda p: len(p.text) > 0, para_list[0:indexs[0]]))

    # 处理条款
    clause_paragraphs_list = list()
    for i, index in enumerate(indexs):
        if i + 1 < len(indexs):
            paras = para_list[index: indexs[i + 1]]
        else:
            paras = para_list[index:]

        clause_paragraphs_list.append(paras)

    clause_paragraphs = []
    for clause_paras in clause_paragraphs_list:
        tmp = list(filter(lambda p: len(p.text) > 0, clause_paras[:-1]))
        clause_paragraphs.append(tmp)
    clause_paragraphs[-1].append(clause_paras[-1].text)

    return not_clause_paragraphs, clause_paragraphs


get_clause_paragraphs_list(para_list)
