#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/12/7 14:18
@Author     : jzs
@File       : base_re.py
@Software   : PyCharm
@Description: ......
"""

# 构建标点符号字典
punctuation = r"""!"#$%&'();<=>?@[\]^_`{|}~，。、【 】 “”；（）《》‘’{}？！⑦()、%^>℃”“^-——=&#@￥～★"""
PUNCTUATION_DICT = dict((e, i) for i, e in enumerate(punctuation))

# 大写金额数字正则式
Dd = '(零|壹|贰|叁|肆|伍|陆|柒|捌|玖|拾|佰|仟|万|亿|〇|一|二|三|四|五|六|七|八|九|十|两|百|千)'
UP_CASE_AMOUNT_RE = r'(零|(人民币)?%s{1,50}.*?元)' % Dd
# Dd = '.'
# UP_CASE_AMOUNT_RE = r'(零|人民币?(%s{1,50}元){1})' % Dd

# 小写金额数字正则式
df1 = '(([0-9]+|[0-9]{1,3}(,[0-9]{3})*)(.[0-9]{1,2})?)'
df2 = '(^(([1-9]\d*)|0)(\.\d{1-2})?)'
LOW_CASE_AMOUNT_RE = r"((%s|%s)元)" % (df1, df2)

# 日期正则式
DATE_RE = r"(\d{4}年\d{1,2}月\d{1,2}日)"

# 简单指代分隔符
SIMPLE_PUNC = '：|:'

# 浮点数
FLOAT_NUM = r"(%s|%s)" % (df1, df2)

# 简单公式表述类型1
EQUATION1 = r"(%s%s%s)" % (".{1,3}?", "(\*|/|\+|-)", FLOAT_NUM)
EQUATION2 = r"(%s%s%s)" % (FLOAT_NUM, "(\+|-|\*|/)", ".{0,10}?")
SIMPLE_EQUATION = r"(%s|%s)" % (EQUATION1, EQUATION2)


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
