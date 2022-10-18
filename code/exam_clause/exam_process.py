#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/12/20 10:10
@Author     : jzs
@File       : exam_process.py
@Software   : PyCharm
@Description: ......
"""

import re

from docx import Document

# 条款一致，输出的字符串
SAME_STRING = 1, '<span class="no_difference">一致</span>', '通过'

# 条款不一致，输出的字符串
DIFFERENT_STRING = 0, '<span class="difference">不一致</span>', '无该条款'

# 条款完全相似，输出的字符串
SIMILAR_STRING = [2, '<span class="difference">不一致</span>', '对应第n条']

# 条款相似，输出的字符串
SIMILARITY_STRING = [3, '<span class="difference">不一致</span>', '与第n条相似']

# 标题审核结果差异字典
TITLE_DIFFERENT_RESULT_DICT = {
    'SAME_STRING': SAME_STRING,
    'DIFFERENT_STRING': DIFFERENT_STRING,
    'SIMILAR_STRING': SIMILAR_STRING,
    'SIMILARITY_STRING': SIMILARITY_STRING
}

# 序列1仅有的字符的标签（deleted lab）
LAB_SEQ1_UNIQUE = '-'

# 序列2仅有的字符的标签（added lab）
LAB_SEQ2_UNIQUE = '+'

# 序列1和序列2共有的字符的标签(common lab)
LAB_SEQ1_SE2_COMMON = ' '

# 序列1和序列2不共有的字符的标签(changed lab)
LAB_SEQ1_SE2_NOT_COMMON = '^'

# 句子对比时的占位符号
PLACEHOLDER = '`'

# 差异类型字典
DIFF_DICT = {
    ' ': (0, 0),
    '-+': (-1, -1),
    '-+?': (-1, 2),
    '-?+': (1, -1),
    '-?+?': (1, 3)
}

# span标签ID1
SPAN_ID_PLACEHOLDER1 = '~'

# span标签ID2
SPAN_ID_PLACEHOLDER2 = '^'

# span标签ID3
SPAN_ID_PLACEHOLDER3 = '【·】'

# span标签ID
SPAN_ID = SPAN_ID_PLACEHOLDER2 + "_" + SPAN_ID_PLACEHOLDER1 + "_" + SPAN_ID_PLACEHOLDER3

# span标签css class
SPAN_CSS_CLASS_ADDED = 'doc_add'

# span标签css class
SPAN_CSS_CLASS_CHANGED = 'doc_change'

# span标签css class
SPAN_CSS_CLASS_DEL = 'doc_delete'

# span标签css class
SPAN_CSS_CLASS_NOT_COMMON = 'doc_diff'

# 增加的标签
ADDED = (
    '<a id="a%s" onclick="changeColor(this.id)"><span id="%s" class="%s">'
    % (SPAN_ID, SPAN_ID, SPAN_CSS_CLASS_ADDED),
    '</span></a>'
)

# 修改的标签
CHANGED = (
    '<a id="a%s" onclick="changeColor(this.id)"><span id="%s" class="%s">'
    % (SPAN_ID, SPAN_ID, SPAN_CSS_CLASS_CHANGED),
    '</span></a>'
)

# 删除的标签
DEL = (
    '<a id="a%s" onclick="changeColor(this.id)"><span id="%s" class="%s">'
    % (SPAN_ID, SPAN_ID, SPAN_CSS_CLASS_DEL),
    '</span></a>'
)

# 句子完全不同时候的标签
NOT_COMMON = (
    '<a id="a%s" onclick="changeColor(this.id)"><span id="%s" class="%s">'
    % (SPAN_ID, SPAN_ID, SPAN_CSS_CLASS_NOT_COMMON),
    '</span></a>'
)

# 相同的标签
COMMON = '', ''

# 空行的标签
SPACE_HTML = '<p><br></p>'

# 句子中的字的标签
SENTENCE_HTML_LAB = {
    LAB_SEQ1_SE2_NOT_COMMON: CHANGED,
    LAB_SEQ1_SE2_COMMON: COMMON,
    LAB_SEQ1_UNIQUE: DEL,
    LAB_SEQ2_UNIQUE: ADDED,
}

# 两个句子无差异的标志
COMMON_FLAG = '*'

# 句子完全不同的标志
NOT_COMMON_FLAG = '#'

# 标点
punctuation = r"""!"#$%&'()*+-/:;<=>?@[\]^_`{|}~，。、【 】 “”；（）《》‘’{}？！⑦()、%^>℃”“^-——=&#@￥～★―.1234567890
qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM"""
PUNCTUATION_DICT = dict((e, i) for i, e in enumerate(punctuation))

# span标签css class-docx文档颜色字典
SPAN_CSS_CLASS_DOCX_COLOR_DICT = {
    SPAN_CSS_CLASS_ADDED: 'BRIGHT_GREEN',
    SPAN_CSS_CLASS_CHANGED: 'YELLOW',
    SPAN_CSS_CLASS_DEL: 'PINK',
    SPAN_CSS_CLASS_NOT_COMMON: 'GRAY_25'
}


def __split_doc_string(para_list: 'list[str]'):
    """
    划分word文档

    :param para_list: 段落list
    :return: 返回首页段落list，非条款list，条款集合list
    """
    index1 = 0
    for i, para in enumerate(para_list):
        if re.match('.*分公司$', para):
            index1 = i
            break
    first_paragraphs = para_list[0:index1 + 1]

    index2 = 0
    for i, para in enumerate(para_list):
        if re.match('★?第一条.*$', para):
            index2 = i
            break
    un_clause_paragraphs = [cl.replace('\n', '') for cl in para_list[index1 + 1:index2]]

    clause_paragraphs_list = list()
    indexs = [i for i, para in enumerate(para_list) if re.match('★?第.{1,3}条.*$', para)]
    for i, index in enumerate(indexs):
        if i + 1 < len(indexs):
            paras = para_list[index: indexs[i + 1]]
        else:
            paras = para_list[index:]
        paras = [p.replace('\n', '') for p in paras]
        clause_paragraphs_list.append(paras)

    return first_paragraphs, un_clause_paragraphs, clause_paragraphs_list


def get_clause_paragraphs_list(para_list: 'list'):
    """
    划分word文档，得到docx文档的条款部分

    :param para_list: 段落list
    :return: 返回首页段落list，非条款list，条款集合list
    """

    clause_paragraphs_list = list()
    indexs = [i for i, para in enumerate(para_list) if re.match('★?第.{1,3}条.*$', para.text)]
    for i, index in enumerate(indexs):
        if i + 1 < len(indexs):
            paras = para_list[index: indexs[i + 1]]
        else:
            paras = para_list[index:]

        clause_paragraphs_list.append(paras)
    clause_paragraphs = []
    for clause_paras in clause_paragraphs_list:
        clause_paragraphs.append([para for para in clause_paras[:-1] if len(para.text) > 1])
    clause_paragraphs.append(clause_paras[-1])
    return clause_paragraphs


def load_document(path):
    """
    读取docx文档，返回first_paragraphs, un_clause_paragraphs, clause_paragraphs_list

    :param path:
    :return: 返回首页段落list，非条款list，条款集合list
    """
    document = Document(path)
    para_list = [para.text for para in list(document.paragraphs)]
    return __split_doc_string(para_list)


def punctuation_filter(sentence: str) -> str:
    """
    去除标点符号和空格符号

    :param sentence:句子
    :return:
    """
    if not sentence or not isinstance(sentence, str):
        return str()

    sentence = list(filter(lambda x: x not in PUNCTUATION_DICT, sentence))
    sentence = str().join(sentence)
    return str().join(sentence.split())
