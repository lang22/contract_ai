#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/2/28 15:52
@Author     : jzs
@File       : cont_cofig.py
@Software   : PyCharm
@Description: ......
"""
import os

from config import BASE_DIR

# 用于句子的词向量模型路径
SENTENCE_WORD2VEC_MODEL_PATH = os.path.join(BASE_DIR, 'cont_exam_new/data/word2vec_paras.model')

# 用于句子的相似度模型路径
SENTENCE_SIMILARITY_MODEL_PATH = os.path.join(BASE_DIR, 'cont_exam_new/data/SimilarityNet_sent.pth')

# 用于句子的相似度模型的词向量维度
SENTENCE_SIMILARITY_MODEL_WORDS_SIZE = 300

# 用于句子的相似度模型的最大句子长度（单词的数量）
SENTENCE_SIMILARITY_MODEL_MAX_SENTENCES_SIZE = 150

# 用于句子的相似度模型路径
NO_CLAUSE_SENTENCE_SIMILARITY_MODEL_PATH = os.path.join(BASE_DIR, 'cont_exam_new/data/SimilarityNet_no_clause.pth')

# 用于句子的相似度模型的词向量维度
NO_CLAUSE_SENTENCE_SIMILARITY_MODEL_WORDS_SIZE = 300

# 用于句子的相似度模型的最大句子长度（单词的数量）
NO_CLAUSE_SENTENCE_SIMILARITY_MODEL_MAX_SENTENCES_SIZE = 2

# 用于大条款的词向量模型路径
MAIN_CLAUSES_WORD2VEC_MODEL_PATH = os.path.join(BASE_DIR, 'cont_exam_new/data/word2vec_paras.model')

# 用于大条款的相似度模型路径
MAIN_CLAUSES_SIMILARITY_MODEL_PATH = os.path.join(BASE_DIR, 'cont_exam_new/data/SimilarityNet_paras.pth')

# 用于大条款的相似度模型的词向量维度
MAIN_CLAUSES_SIMILARITY_MODEL_WORDS_SIZE = 300

# 用于大条款的相似度模型的最大句子长度（单词的数量）
MAIN_CLAUSES_SIMILARITY_MODEL_MAX_SENTENCES_SIZE = 750

# 用于条款标题的词向量模型路径
CLAUSES_TITLE_WORD2VEC_MODEL_PATH = os.path.join(BASE_DIR, 'cont_exam_new/data/word2vec.model')

# 用于条款标题的相似度模型路径
CLAUSES_TITLE_SIMILARITY_MODEL_PATH = os.path.join(BASE_DIR, 'cont_exam_new/data/SimilarityNet.pth')

# 相似度阈值
SIMILARITY_MAX_VALUE = 0.50

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

#  class-docx文档颜色字典
SPAN_CSS_CLASS_DOCX_COLOR_DICT = {
    LAB_SEQ2_UNIQUE: 'BRIGHT_GREEN',
    LAB_SEQ1_SE2_NOT_COMMON: 'YELLOW',
    LAB_SEQ1_UNIQUE: 'PINK',
    SPAN_CSS_CLASS_NOT_COMMON: 'GRAY_25'
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
    LAB_SEQ2_UNIQUE: 'BRIGHT_GREEN',
    LAB_SEQ1_SE2_NOT_COMMON: 'YELLOW',
    LAB_SEQ1_UNIQUE: 'PINK',
    LAB_SEQ1_SE2_COMMON: None
}

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
