#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/12/20 10:04
@Author     : jzs
@File       : exam_content.py
@Software   : PyCharm
@Description: ......
"""

from exam_clause.exam_process import SAME_STRING, SIMILAR_STRING, DIFFERENT_STRING, SIMILARITY_STRING, CHANGED, DEL, \
    ADDED
from exam_clause.sentence_compare import get_compare_sentences_lab, SPACE_HTML
from exam_clause.sentence_masked import get_highlight_html, get_all_highlight_html, get_html, get_one_highlight_html


def __get_space_split(paragraphs: 'list[str]'):
    """
    划分处理空行，将空行与非空行分开

    :param paragraphs: docx的段的集合
    :return:
    """
    para_index = [(i, d) for i, d in enumerate(paragraphs) if d]
    para_none_index = [(i, d) for i, d in enumerate(paragraphs) if not d]
    return para_index, para_none_index


def paragraphs_exam(model_paragraphs: 'list[str]',
                    test_paragraphs: 'list[str]') -> str:
    """
    审核多个段落的内容，输出成html

    :param model_paragraphs: 模板文档的首页段的list
    :param test_paragraphs:  待审核文档的首页段的list
    :return:
    """
    model_index, model_none_index = __get_space_split(model_paragraphs)
    test_index, test_none_index = __get_space_split(test_paragraphs)

    model_html = [''] * len(model_paragraphs)
    test_html = [''] * len(test_paragraphs)

    # 处理非空行
    tmp_index = 0
    for i, model in enumerate(model_index):
        tmp_index = i
        if i >= len(test_index):
            break
        model_para_i, model_string = model
        test_para_i, test_string = test_index[i]

        model_string = model_string
        test_string = test_string
        d1, d2 = get_compare_sentences_lab(model_string, test_string)
        h1, h2 = get_highlight_html(model_string, test_string, d1, d2)

        model_html[model_para_i] = h1
        test_html[test_para_i] = h2

    # 处理model句子比test句子多的情况，认为model句子被删除
    if tmp_index >= len(test_index):
        for model in model_index[tmp_index:]:
            model_para_i, model_string = model
            h1 = get_one_highlight_html(DEL, model_string)
            model_html[model_para_i] = h1

    # 处理test句子比model句子多的情况，认为test句子被添加
    elif tmp_index < len(test_index) - 1:
        for test in test_index[tmp_index + 1:]:
            test_para_i, test_string = test
            h2 = get_one_highlight_html(ADDED, test_string)
            test_html[test_para_i] = h2

    # 处理空行
    for model in model_none_index:
        model_para_i, _ = model
        model_html[model_para_i] = SPACE_HTML

    # 处理空行
    for test in test_none_index:
        test_para_i, _ = test
        test_html[test_para_i] = SPACE_HTML

    return str().join(model_html), str().join(test_html)


def clause_paragraphs_exam(model_paragraphs: 'list[str]',
                           test_paragraphs: 'list[str]',
                           clause_title):
    """
    审核多个段落的内容，输出成html

    :param model_paragraphs: 模板文档的首页段的list
    :param test_paragraphs:  待审核文档的首页段的list
    :param clause_title: 标题审核的结果
    :return:
    """
    model_clause_html = [''] * len(model_paragraphs)
    test_clause_html = [''] * len(model_paragraphs)

    # 先标test_paragraphs和一部分的model_paragraphs
    for i, clause in enumerate(clause_title):
        if i >= len(test_clause_html):
            continue
        flag = clause[2]
        line_num = clause[5]
        if flag == SAME_STRING[0]:
            html1, html2 = paragraphs_exam(model_paragraphs[i], test_paragraphs[i])
            model_clause_html[line_num] = html1
            test_clause_html[i] = html2

        elif flag == SIMILAR_STRING[0] and line_num >= 0:
            html1, html2 = paragraphs_exam(model_paragraphs[line_num], test_paragraphs[i])
            model_clause_html[line_num] = html1
            test_clause_html[i] = html2

        elif flag == SIMILARITY_STRING[0] and line_num >= 0:
            html1, html2 = paragraphs_exam(model_paragraphs[line_num], test_paragraphs[i])
            model_clause_html[line_num] = html1
            test_clause_html[i] = html2

        elif flag == DIFFERENT_STRING[0]:
            test_clause_html[i] = get_all_highlight_html(CHANGED, test_paragraphs[i])

    # 在标剩余的部分的model_paragraphs
    for i, html in enumerate(model_clause_html):
        if not html:
            model_clause_html[i] = get_html(model_paragraphs[i])
    return str().join(model_clause_html), str().join(test_clause_html)
