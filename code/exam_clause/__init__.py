#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/12/18 11:15
@Author     : jzs
@File       : __init__.py.py
@Software   : PyCharm
@Description: ......
"""
from docx import Document

from app.tools import join_path
from config import Config
from exam_clause.exam_content import paragraphs_exam, clause_paragraphs_exam
from exam_clause.exam_process import load_document, SPAN_ID_PLACEHOLDER2
from exam_clause.exam_title import clause_title_exam
from exam_clause.highlight_docx import remove_html_highlight_item, html_highlight_dict, to_highlight_dict, \
    highlight_test_docx_for_change, highlight_test_docx_for_delete

from exam_clause.sentence_masked import add_html_elem_id


def contract_clause_exam(model_path: str, test_path: str):
    """
    合同条款审核，包括合同条款的标题审核和合同的内容审核
    返回合同的标题审核结果，合同的条款内容审核的差异对比结果（使用html形式展示）

    1. 合同条款的标题的检验, 返回这样的元祖list
    对比结果元祖格式（第几条，条款标题，一致性Flag，是否一致，备注1，备注2）
    其中的 “ 一致性Flag，是否一致，备注1，备注2 ” 分成四类，分别是:
    a.条款一致，输出的字符串: 1, '一致', '通过'
    b.条款不一致，输出的字符串: 0, '不一致', '无该条款'
    c.条款完全相似，输出的字符串 : [2, '不一致', '对应第n条']
    d.条款相似，输出的字符串: [3, '不一致', '与第n条相似']

    2.合同的条款内容审核的差异对比结果，返回两个HTML文档字符串，分别是
    a.模板文档审核结果html文档字符串
    b.待审核文档审核结果html文档字符串

    :param model_path: 模板文档的路径
    :param test_path: 审核文档的路径
    :return: 模板文档对比结果html，审核文档对比结果html, 条款标记审核结果
    """

    # 读取文档并分段，分成首页、非条款、条款
    first_paragraphs1, un_clause_paragraphs1, clause_paragraphs_list1 = load_document(model_path)

    first_paragraphs2, un_clause_paragraphs2, clause_paragraphs_list2 = load_document(test_path)

    # print(clause_paragraphs_list1)
    # 条款的标题审核
    clause_title = clause_title_exam(clause_paragraphs_list1, clause_paragraphs_list2)

    # 首页审核
    first1_html, first2_html = paragraphs_exam(first_paragraphs1,
                                               first_paragraphs2)

    # 非条款审核
    un_clause1_html, un_clause2_html = paragraphs_exam(un_clause_paragraphs1,
                                                       un_clause_paragraphs2)

    # 条款内容审核
    clause1_html, clause2_html = clause_paragraphs_exam(clause_paragraphs_list1,
                                                        clause_paragraphs_list2,
                                                        clause_title)

    # 合并
    model_html = str().join((first1_html, un_clause1_html, clause1_html))
    test_html = str().join((first2_html, un_clause2_html, clause2_html))

    # 微处理
    model_html = add_html_elem_id('model', model_html)
    test_html = add_html_elem_id('test', test_html)

    return model_html, test_html, clause_title


def get_test_html_highlight_dict(html_string: str) -> dict:
    """
    提取待审核文档html中所有span标签的id，并构建span的id-标注颜色字典

    :param html_string: html字符串
    :return: span的id-标注颜色字典
    """
    return html_highlight_dict(html_string)


def highlight_docx(model_docx_path: str,
                   test_docx_path: str,
                   model_span_dict: dict,
                   test_span_dict: dict,
                   span_del_list: list,
                   clause_title: list):
    """
    高亮标注待审核合同文档

    1. 首先，删除模板文档和测试文档中已经被确认的标签，并删除模板文档中除了“删除”标签之外的标签;
    2. 将span标签-id字典转化成方便标注docx文档的字典：高亮语句下标组-颜色字典;
    3. 使用待审核文档的高亮语句下标组-颜色字典，来标注待审核文档的修改和增加的部分;
    4. 使用模板文档的高亮语句下标组-颜色字典和模板文档，来添加并标注待审核文档的删除的部分
    5. 保存待审核文档，并返回 待审核文档所在文件夹 和 待审核文档名字

    :param model_docx_path: 模板文档的路径
    :param test_docx_path: 测试文档的路径
    :param model_span_dict: 模板文档的span标签id-标注颜色字典
    :param test_span_dict: 测试文档的span标签id-标注颜色字典
    :param span_del_list: 需要删除的span标签id列表
    :param clause_title: 条款审核结果
    :return: 待审核文档所在文件夹 和 待审核文档名字
    """

    model_span_dict, test_span_dict = remove_html_highlight_item(model_span_dict, test_span_dict, span_del_list)

    model_highlight_dict = to_highlight_dict(model_span_dict)
    test_highlight_dict = to_highlight_dict(test_span_dict)

    model_docx = Document(model_docx_path)
    test_docx = Document(test_docx_path)

    first_paragraphs1, un_clause_paragraphs1, clause_paragraphs_list1 = load_document(model_docx_path)
    first_paragraphs2, un_clause_paragraphs2, clause_paragraphs_list2 = load_document(test_docx_path)

    # for i, c in enumerate(clause_paragraphs_list1):
    #     print(i, ":", c)

    highlight_test_docx_for_change(test_docx, test_highlight_dict)

    highlight_test_docx_for_delete(test_docx,
                                   model_docx,
                                   first_paragraphs2,
                                   un_clause_paragraphs2,
                                   clause_paragraphs_list1,
                                   clause_title,
                                   model_highlight_dict)

    template_path = Config.CONT_GENA_DIR_PATH
    save_name = '标注结果.docx'
    test_docx.save(join_path(template_path, save_name))
    return template_path, save_name
