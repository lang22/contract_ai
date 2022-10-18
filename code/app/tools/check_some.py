#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/13 9:43
@Author     : jzs
@File       : check_some.py
@Software   : PyCharm
@Description: 输入检查
"""
import re
import time

from app.tools.check_amount import amount_words_to_number

# 缓存字典
tag_dict = dict()


def check(money_X: str, money_x: str) -> int:
    """
    检查大小写金额是否相等
    :param money_X: 大写金额字符串
    :param money_x: 小写金额字符串
    :return: 返回-1,0,1
    -1：大写金额有误
    0：大小写金额不相等
    1：大小写金额一致
    """
    if not money_X or not money_x:
        return 0
    # print(money_X, money_x)
    money_X = amount_words_to_number(money_X)
    if money_X == -1:
        return -1
    money_x = money_x.replace('元', '')
    money_x = float(money_x.replace(',', '').strip())
    if money_X == money_x:
        return 1
    else:
        return 0


def check_tag_dict_equals(tag: str, tmp: str) -> int:
    """
    判断目标串和缓存串是否相等
    :param tag: 目标串
    :param tmp: 缓存串
    :return:
    """
    return 1 if tag == tmp else 0


def check_address(word: str) -> int:
    """
    检查地址，地址不为空返回1，否则返回0
    :return: 暂时返回1
    """

    if not word or word.isdigit():
        return 0
    re_srt = r'([\u4e00-\u9fa5]|[a-zA-Z]|[0-9])*$'
    return 1 if re.match(re_srt, word) else 0


def check_chinese_characters(word: str) -> int:
    """
    检查是否是中文串
    :param word: 中文串
    :return: 正确返回1，错误返回0
    """
    if not word:
        return 0
    re_srt = r'([\u4e00-\u9fa5])*$'
    return 1 if re.match(re_srt, word) else 0


def check_date(date: str) -> int:
    """
    检查日期格式是否正确
    :param date: 日期串
    :return: 正确返回1，错误返回0
    """
    try:
        time.strptime(date, "%Y年%m月%d日")
        return 1
    except ValueError:
        return 0


def check_bank_name(word: str) -> int:
    """
    必须要以‘行’字结尾
    :param word: 中文串
    :return: 正确返回1，错误返回0
    """
    if not word:
        return 0
    re_srt = r'([\u4e00-\u9fa5])*行$'
    return 1 if re.match(re_srt, word) else 0


def check_acount(word: str):
    """
    检查是否是银行账户，必须为数字，且为14位以上
    :param word: 数字串
    :return:  正确返回1，错误返回0
    """

    if not word:
        return 0
    re_srt = r'[0-9]{14,30}$'
    return 1 if re.match(re_srt, word) else 0


def check_number(num: str):
    """
    检查是否是数字
    :param num: 输入数字
    :param word: 数字串
    :return:  正确返回1，错误返回0
    """

    if not num:
        return 0
    re_srt = r'[0-9]{0,30}$'
    return 1 if re.match(re_srt, num) else 0


def check_money(money: str) -> int:
    """
    检查大小写金额是否
    :param money: 大写小写金额字符串
    :return: 返回-2,-1,0,1
    -2：大小写金额格式有误
    -1：大写金额有误
    0：大小写金额不相等
    1：大小写金额一致
    """
    if not money:
        return -2
    money = re.split(r',|，', money)
    if len(money) != 2:
        return -2
    return check(money[0], money[1])


def check_mix(content: str) -> int:
    """
    :param content: 表述类型
    :return: 返回1
    """
    return 1


def check_float(fl_num: str) -> int:
    """
    :param fl_num: 可能是小数
    :return: 返回1 0
    """
    if not fl_num:
        return 0

    re_srt = r'[0-9]{0,30}.?[0-9]{0,30}$'
    return 1 if re.match(re_srt, fl_num) else 0


def check_table4(string: str) -> int:
    """
    判断是否符合表格填写规范，此函数适用于一行需要填写三个内容的表格情况
    :param string: 输入
    :return: 1 or 0
    """
    tt = string.split('，')
    if len(tt) == 3:
        return 1
    return 0


check_dict = {
    '地址': check_address,
    '汉字': check_chinese_characters,
    '日期': check_date,
    '银行名': check_bank_name,
    '账户号': check_acount,
    '大小写金额': check_money,
    '数字': check_number,
    '表述类型': check_mix,
    '小数': check_float,
    '表格4': check_table4
}

result_dict = {
    '地址': {1: '输入正确！', 0: '输入有误！'},
    '汉字': {1: '输入正确！', 0: '输入有误，请输入汉字！'},
    '大小写金额': {1: '输入正确！', 0: '大小写金额不相等！', -1: '大写金额有误!', -2: '大小写金额格式有误!'},
    '日期': {1: '输入正确！', 0: '输入有误，请输入正确日期！'},
    '银行名': {1: '输入正确！', 0: '输入有误，请输入正确银行名！'},
    '账户号': {1: '输入正确！', 0: '输入有误，请输入大于14位的数字！'},
    '数字': {1: '输入正确！', 0: '输入有误，请输入数字！'},
    '表述类型': {1: '输入正确！', 0: '输入有误，请输入正确内容！'},
    '小数': {1: '输入正确！', 0: '输入有误，请输入小数或者整数！'},
    '表格4': {1: '输入正确！', 0: '输入有误，表格内容一行有三项内容！'},
}
