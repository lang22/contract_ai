#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/10/22 11:22
@Author     : jzs
@File       : checkeeee.py
@Software   : PyCharm
@Description: ......
"""


def operation_func0(tmp_stack: list, result_stack: list, num: int):
    """
    数字位，将数字入tmp_stack栈
    """
    tmp_stack.append(num)


def operation_func1(tmp_stack: list, result_stack: list, num: int):
    """
    万结算位，将tmp_stack的求和，清空，乘以10000，入tmp_stack栈
    """
    s = sum(tmp_stack) * num
    tmp_stack.clear()
    tmp_stack.append(s)


def operation_func2(tmp_stack: list, result_stack: list, num: int):
    """
    亿、元结算位，将tmp_stack的求和，清空，乘以一亿或一，入result_stack栈
    """
    s = sum(tmp_stack) * num
    tmp_stack.clear()
    result_stack.append(s)


def operation_func3(tmp_stack: list, result_stack: list, num: int):
    """
    普通计算位，将tmp_stack弹出，使用num计算，入tmp_stack栈
    :param tmp_stack:
    :param result_stack:
    :param num:
    :return:
    """
    n = tmp_stack.pop()
    tmp_stack.append(num * n)


def operation_func4(tmp_stack: list, result_stack: list, num: int):
    """
    越过位，什么也不做
    """
    pass


number_dict = {
    '壹': (1, operation_func0),
    '贰': (2, operation_func0),
    '叁': (3, operation_func0),
    '肆': (4, operation_func0),
    '伍': (5, operation_func0),
    '陆': (6, operation_func0),
    '陸': (6, operation_func0),
    '柒': (7, operation_func0),
    '捌': (8, operation_func0),
    '玖': (9, operation_func0),

    '万': (1e4, operation_func1),

    '圆': (1, operation_func2),
    '元': (1, operation_func2),
    '亿': (1e8, operation_func2),

    '仟': (1e3, operation_func3),
    '佰': (100, operation_func3),
    '拾': (10, operation_func3),
    '角': (1e-1, operation_func3),
    '分': (1e-2, operation_func3),
    '厘': (1e-3, operation_func3),

    '整': (1, operation_func4),
    '零': (0, operation_func4)
}


def amount_words_to_number(money: str) -> float:
    """
    将中文大写金额字符串转换成数学
    :param money:大写金额字符串
    :return:
    """
    try:
        money = money.strip()
        tmp_stack = list()
        result_stack = list()
        for m in money:
            number, func = number_dict.get(m, (-1, -1))
            if number == -1:
                return number
            func(tmp_stack, result_stack, number)
        return sum(tmp_stack) + sum(result_stack)

    except IndexError as e:
        print(e)
        return -1


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


if __name__ == '__main__':
    a = amount_words_to_number('陆亿陆仟陆佰零陆万陆仟陆佰陆拾陆圆陆角陆分  ')
    print(a)