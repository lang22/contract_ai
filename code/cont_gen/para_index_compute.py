import re

from .base_tools import REGEX_EXPRESSION


def __get_key_index(sentences: list, keywords: str):
    """
    获取关键词所在的以及以后的起始段落号
    :param sentences: 段落集合
    :param keywords: 关键字
    :return: 关键字  段落号
    """

    index = -1
    elem_keys = keywords.split(';')

    if len(elem_keys) == 2:  # 存在后缀的情况
        restr = []
        key_first = elem_keys[0].split('|')

        if len(key_first) > 1:  # 有同义词存在

            for j in range(len(key_first)):  # 考虑每一个同义词集合中的key关键字

                restr.append(REGEX_EXPRESSION['base'] % key_first[j])
        else:
            restr.append(REGEX_EXPRESSION['base'] % key_first[0])

        for re_temp in restr:
            flag = 0  # 用于判断是否结束
            for i, s in enumerate(sentences):  # 针对这个关键字进行匹配
                text = s.text.replace(' ', '')
                if re.match(re_temp, text):
                    index = i
                    flag = 1
                    break

            if flag == 1:
                break

        key = elem_keys[1]

    else:
        key = elem_keys[0]

    return key, index


def __get_key_location(sentences: list, mark: int, key: str, type: str) -> int:  # 获取关键词的准确替换位置
    """

    :param sentences: 段落集合
    :param mark: 应该开始处理的段落号
    :param key: 关键词
    :param type: 操作指令类型
    :return: 段落号
    """
    index = -1
    final_key = ''

    key_list = key.split('|')
    restr = {}

    if len(key_list) > 1:  # 存在同义词

        # print('__get_key_location存在同义词')
        for i, key in enumerate(key_list):
            restr[key] = REGEX_EXPRESSION[type] % key

    else:
        restr[key_list[0]] = REGEX_EXPRESSION[type] % key_list[0]

    for i, item in enumerate(sentences):

        if i <= mark:
            continue

        flag = 0  # 用于判断是否已经匹配成功
        for key_item in restr:
            re_str = restr[key_item]
            text = item.text.replace(' ', '')
            # print('开始匹配', re_str, text)
            if re.match(re_str, text):
                index = i
                final_key = key_item
                flag = 1
                # print('匹配成功')
                break

        if flag == 1:
            break

        # print('匹配失败')

    return index, final_key


def get_para_index(para_list: list, keywords: str, type: str):
    """
    得到需要的段落号

    :param para_list:
    :param keywords:
    :param type:
    :return:
    """
    key, mark_index = __get_key_index(para_list, keywords)
    # print("keywords, key, mark_index", keywords, key, mark_index)
    para_index, final_key = __get_key_location(para_list, mark_index, key, type)
    # print('para_index, final_key', para_index, final_key)
    # print('key, para_index', key, para_index)
    return para_index, final_key
