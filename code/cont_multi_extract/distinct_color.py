#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019-05-14 15:04
@Author     : charles
@File       : distinct_color.py
@Software   : PyCharm
@Description: ......
"""
from collections import Counter


def set_color(content_dict_dic: dict, elem_lis: list):
    """
    将所有文件同种要素的生成内容排序，出现次数最多的为黑色，其余分别赋予其他颜色
    规定颜色对 0：黑色（不进行改变，使用默认色） 1：红色 2：蓝色 3：绿色 4：黄色 5：blueviolet 6. purple
    :param content_dict_dic: 每个文件对应的 要素-内容字典
    :param elem_lis: 所有文件的所有要素的并集
    :return: {
              element: {'content1': 'color1', 'content2': 'color2'},
              element2: {'content1': 'color1', 'content2': 'color2'}
             }
    """
    color_dic = {
        '0': 'none',
        '1': 'red',
        '2': 'blue',
        '3': 'green',
        '4': 'yellow',
        '5': 'blueviolet',
        '6': 'purple'
    }

    element_color = {}

    for element in elem_lis:

        elem_count = []

        for file in content_dict_dic:
            value = content_dict_dic[file][element]
            if value != '--':
                if type(value) == list:
                    value = str(value)
                elem_count.append(value)

        result = Counter(elem_count)

        d = sorted(result.items(), key=lambda x: x[1], reverse=True)
        # d 示例： [('content1', 3), ('content2', 2), ('content1', 1)]

        # 单个要素的要素-颜色代码字典
        elem_color_dic = {content_item[0]: color_dic[str(index)] for index, content_item in enumerate(d)}

        element_color[element] = elem_color_dic

    return element_color
