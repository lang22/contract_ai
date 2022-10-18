#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/12/11 10:18
@Author     : jzs
@File       : amount_exam.py
@Software   : PyCharm
@Description: 金额审核模块
当前版本只审核一致性
"""
from app.tools.check_amount import amount_words_to_number

# 大小写金额为空标志
CASE_AMOUNT_NULL_FLAG = -100

# 大小写金额相等标志
CASE_AMOUNT_EQUAL_FLAG = 1

# 大小写金额不相等标志
CASE_AMOUNT_NOT_EQUAL_FLAG = 0

# 大写金额有误标志
CASE_AMOUNT_ERROR_FLAG = -1


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
        return CASE_AMOUNT_NOT_EQUAL_FLAG
    money_X = amount_words_to_number(money_X)
    if money_X == CASE_AMOUNT_ERROR_FLAG:
        return CASE_AMOUNT_ERROR_FLAG
    money_x = money_x.replace('元', '')
    money_x = float(money_x.replace(',', '').strip())
    if money_X == money_x:
        return CASE_AMOUNT_EQUAL_FLAG
    else:
        return CASE_AMOUNT_NOT_EQUAL_FLAG


def __check_one(case_amount: 'list[str,str]'):
    """
    检查一个大小金额是否一致
    返回-2，传入参数有误

    :param case_amount: 大小写金额列表
    :return: 返回-2，或其他
    """

    if case_amount is None:
        return CASE_AMOUNT_NULL_FLAG
    elif not (isinstance(case_amount, list) or isinstance(case_amount, tuple)):
        return CASE_AMOUNT_NULL_FLAG
    elif len(case_amount) != 2:
        return CASE_AMOUNT_NULL_FLAG
    return check(*case_amount)


def check_amount_difference(elem_type_dict: 'dict[str,str]',
                            elem_content_dict: 'dict[str,str]') -> 'dict[str,str]':
    """
    检查合同要素中金额是否一致，返回{金额要素名-金额要素一致性}字典

    :param elem_type_dict:  要素名-要素类型字典
    :param elem_content_dict:   要素名-要素内容字典
    :return:  {金额要素名-金额要素一致性}字典
    """
    amount_list = [key for key in elem_type_dict.keys()
                   if elem_type_dict[key] == 'case_amount']  # 获取金额名字列表
    amount_dict = dict()
    for key in amount_list:
        difference = __check_one(elem_content_dict[key])
        if difference != CASE_AMOUNT_NULL_FLAG:
            amount_dict[key] = difference
    return amount_dict
