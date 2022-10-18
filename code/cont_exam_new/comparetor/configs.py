#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/3/5 8:55
@Author     : jzs
@File       : configs.py
@Software   : PyCharm
@Description: ......
"""
MIN_SENTENCE_LEN = 30

MAX_MULTIPLE = 4

min_MULTIPLE = 2

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

# 两个句子无差异的标志
COMMON_FLAG = '*'

# 句子完全不同的标志
NOT_COMMON_FLAG = '#'
