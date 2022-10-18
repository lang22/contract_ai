#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/1/17 10:02
@Author     : jzs
@File       : highlight_docx.py
@Software   : PyCharm
@Description: ......
"""
import re

from app.tools.docx_tools import set_paragraph_text_highlight_by_slice, insert_paragraph_text_highlight_by_slice, \
    add_paragraph_text_highlight_before
from exam_clause.exam_process import SPAN_CSS_CLASS_DOCX_COLOR_DICT, SPAN_CSS_CLASS_DEL, get_clause_paragraphs_list


def html_highlight_dict(html_string: str) -> dict:
    """
    提取html中所有span标签的id，并构建span的id-标注颜色字典

    :param html_string: html字符串
    :return: span的id-标注颜色字典
    """
    span_list = re.findall('<span id="(.*?)" class="(.*?)">.*?</span>', html_string)
    return dict(span_list)


def remove_html_highlight_item(model_span_dict: dict,
                               test_span_dict: dict,
                               span_del_list: list):
    """
    删除模板文档和测试文档中已经被确认的标签，并删除模板文档中除了“删除”标签之外的标签

    :param model_span_dict: 模板文档的span标签id-标注颜色字典
    :param test_span_dict: 测试文档的span标签id-标注颜色字典
    :param span_del_list: 需要删除的span标签id列表
    :return:
    """
    for span_id in span_del_list:
        if span_id in model_span_dict:
            model_span_dict.pop(span_id)
        elif span_id in test_span_dict:
            test_span_dict.pop(span_id)

    model_span_dict = dict(filter(lambda k: k[1] == SPAN_CSS_CLASS_DEL, model_span_dict.items()))
    return model_span_dict, test_span_dict


def to_highlight_dict(span_dict: dict) -> dict:
    """
    将span标签-id字典转化成方便标注docx文档的字典：高亮语句下标组-颜色字典

    高亮语句下标组为这样的元祖（文件类型，需标高亮的字符串下标开始，需标高亮的字符串下标结束，段落号）
    颜色为{'BRIGHT_GREEN','YELLOW','PINK','GRAY_25'}
    :param span_dict:  span标签id-颜色字典
    :return: 高亮语句下标组-颜色字典
    """
    highlight_dict = dict()
    for key, value in span_dict.items():
        # print("key, value:", key, value)

        tmp = key.split('_')

        key = (tmp[0], int(tmp[1]), int(tmp[2]), int(tmp[3]))
        value = SPAN_CSS_CLASS_DOCX_COLOR_DICT[value]
        highlight_dict[key] = value
    return highlight_dict


def highlight_test_docx_for_change(test_docx,
                                   test_highlight_dict: dict):
    """
    使用待审核文档的高亮语句下标组-颜色字典，来标注待审核文档的修改和增加的部分

    :param test_docx: 待审核文档
    :param test_highlight_dict: 高亮语句下标组-颜色字典
    :return:
    """
    paragraphs = test_docx.paragraphs
    for key, color in test_highlight_dict.items():
        _, slice1, slice2, para_num = key
        set_paragraph_text_highlight_by_slice(paragraphs[para_num], (slice1, slice2), color)


# 非条款的相对段号为 -1
UN_CLAUSE_RELATIVE_PARA_NUM = -1


def __get_space_para_clauses_map(clauses: 'list[list[str]]') -> 'list[dict]':
    """
    得到条款文档中非空行之间的映射

    :param clauses:
    :return:
    """
    clauses_map_list = list()
    for clause in clauses:
        clause_map = [i for i, para in enumerate(clause) if para]
        dic = dict((j, i) for i, j in enumerate(clause_map))
        dic[len(clause) - 1] = len(dic)

        clauses_map_list.append(dic)

    return clauses_map_list


def __get_model_paragraph_map(test_first_para: 'list[str]',
                              test_un_clause_para: 'list[str]',
                              model_clause_paras: 'list[list[str]]') -> dict:
    """
    通过条款标题审核结果和分段结果，得到模板的“绝对段号”映射成模板的“相对段号”的字典

    模板的绝对段号为当前语句的段号，
    模板的相对段号为（条款段号，条款内部号），
    其中若是非条款的相对段号，则“条款段号”为“UN_CLAUSE_RELATIVE_PARA_NUM”，“条款内部号”为绝对段号

    :param test_first_para:  测试文档首页
    :param test_un_clause_para: 测试文档非条款
    :param model_clause_paras: 模板文档条款
    :return:
    """

    len1 = len(test_first_para)
    len2 = len(test_un_clause_para)

    # print(len1, test_first_para)
    # print(len2, test_un_clause_para)

    clauses_map = __get_space_para_clauses_map(model_clause_paras)
    # print('clauses_map:', clauses_map)
    paragraph_map = [(i, (UN_CLAUSE_RELATIVE_PARA_NUM, i)) for i in range(len1)]
    paragraph_map.extend((i + len1, (UN_CLAUSE_RELATIVE_PARA_NUM, i + len1)) for i in range(len2))
    # print('paragraph_map:', paragraph_map)
    base = len1 + len2
    count = 0
    for i, clause in enumerate(model_clause_paras):
        for j, para in enumerate(clause):
            paragraph_map.append((base + count, (i, clauses_map[i].get(j, -20))))
            count += 1
    return dict(paragraph_map)


def __to_test_para_relative_number(model_paragraph_map: dict,
                                   clause_title: list,
                                   absolute_number: int):
    """
    查模板的“绝对段号”映射成模板的“相对段号”的字典，将模板文档绝对段号映射成测试文档的“相对段号”
    :param model_paragraph_map: “绝对段号”映射成模板的“相对段号”的字典
    :param clause_title: 条款审核结果
    :param absolute_number: 模板文档绝对段号
    :return: 测试文档的“相对段号”
    """
    a1, a2 = model_paragraph_map.get(absolute_number, (UN_CLAUSE_RELATIVE_PARA_NUM, UN_CLAUSE_RELATIVE_PARA_NUM))
    if a1 != UN_CLAUSE_RELATIVE_PARA_NUM:
        a1 = clause_title[a1][-1]
    else:
        pass
    return a1, a2


def highlight_test_docx_for_delete(test_docx,
                                   model_docx,
                                   test_first_para: 'list[str]',
                                   test_un_clause_para: 'list[str]',
                                   model_clause_paras: 'list[list[str]]',
                                   clause_title: list,
                                   model_highlight_dict: dict):
    """
    使用模板文档的高亮语句下标组-颜色字典和模板文档，来添加并标注待审核文档的删除的部分

    :param test_docx: 待审核文档
    :param model_docx: 模板文档
    :param test_first_para:  测试文档首页
    :param test_un_clause_para: 测试文档非条款
    :param model_clause_paras: 模板文档条款
    :param clause_title: 条款审核结果
    :param model_highlight_dict: 高亮语句下标组-颜色字典
    :return:
    """
    model_paragraph_map = __get_model_paragraph_map(test_first_para,
                                                    test_un_clause_para,
                                                    model_clause_paras)
    test_para = list(test_docx.paragraphs)

    model_para = model_docx.paragraphs
    clauses = get_clause_paragraphs_list(test_docx.paragraphs)
    model_highlight_dict_items = sorted(model_highlight_dict.items(), key=lambda i: i[0][3])

    for key, color in model_highlight_dict_items:
        _, slice1, slice2, para_num = key
        rela_index1, rela_index2 = __to_test_para_relative_number(model_paragraph_map, clause_title, para_num)

        # 如果删除位置在条款位置上
        if rela_index1 != UN_CLAUSE_RELATIVE_PARA_NUM:
            test_clause = clauses[rela_index1]

            # todo 如果是末尾删除
            if rela_index2 >= len(test_clause) - 2:
                add_paragraph_text_highlight_before(clauses[rela_index1][-1],
                                                    model_para[para_num],
                                                    model_para[para_num].text)
            else:
                insert_paragraph_text_highlight_by_slice(test_clause[rela_index2],
                                                         model_para[para_num],
                                                         (slice1, slice2))
        else:
            insert_paragraph_text_highlight_by_slice(test_para[rela_index2],
                                                     model_para[para_num],
                                                     (slice1, slice2))
