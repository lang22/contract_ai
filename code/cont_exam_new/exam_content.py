#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/2/27 15:29
@Author     : jzs
@File       : exam_content.py
@Software   : PyCharm
@Description: ......
"""
import re
from collections import Counter
from functools import reduce

from docx import Document
from numpy import argmax

from .cont_sentences import MainClauses, Sentence, DEFAULT_SENTENCE_SIMILARITY_MODEL, \
    NO_CLAUSE_SENTENCE_SIMILARITY_MODEL

# 条款标题匹配的正则表达式
CLAUSES_TITLE_MATCH_STR = r'(.{0,3}?|\s*?)第.{1,3}条.{1,30}?$'


def __split_clause_paragraphs(document_id: int, para_list: list) -> 'tuple[MainClauses, list[MainClauses]]':
    """
    划分word文档，得到docx文档的非条款部分的大条款MainClauses类，条款部分MainClauses类

    :param document_id 文档ID
    :param para_list: 段落(paragraph类型 )list
    :return:
        分成四种情况：
        （1）tuple[MainClauses, None]：大条款不存在，且非条款存在，返回None和条款集合大条款(MainClauses)的list；
        （2）None：大条款不存在， 且非条款不存在，即para_list为空，返回None
        （3）tuple[None, list[MainClauses]]：大条款存在，且非条款不存在，返回返回非条款的大条款(MainClauses)类的list和None
        （4）tuple[MainClauses, list[MainClauses]]：大条款存在，且非条款存在，返回返回非条款的大条款(MainClauses)类的list和条款集合大条款(MainClauses)的list
    """
    # 获取大条款的下标位置
    indexs = [i for i, para in enumerate(para_list)
              if re.match(CLAUSES_TITLE_MATCH_STR, para.text)]

    # 如果大条款不存在, 且非条款存在
    if not len(indexs) and len(para_list):
        not_clause = MainClauses(clauses_id=0, document_id=document_id,
                                 clauses_name="非条款",
                                 sentences=para_list)
        return not_clause, None
    # 如果大条款不存在, 且非条款不存在
    elif not para_list:
        return None

    # 处理条款
    clause_paragraphs_list = list()
    for i, index in enumerate(indexs):
        if i + 1 < len(indexs):
            paras = para_list[index: indexs[i + 1]]
        else:
            paras = para_list[index:]
        clause_paragraphs_list.append(paras)

    # clause_paragraphs = []
    # for clause_paras in clause_paragraphs_list:
    #     tmp = clause_paras[:-1]
    #     clause_paragraphs.append(tmp)
    # clause_paragraphs[-1].append(clause_paras[-1])

    main_clause_list = []
    for i, clauses in enumerate(clause_paragraphs_list):
        name = clauses[0].text.strip().split()[-1]
        main_clause = MainClauses(clauses_id=i + 1, document_id=document_id,
                                  clauses_name=name,
                                  sentences=clauses)
        main_clause_list.append(main_clause)

    # 处理非条款
    not_clause_paragraphs = para_list[0:indexs[0]]

    # 主条款存在，且非条款不存在
    if not len(not_clause_paragraphs):
        return None, main_clause_list

    # 主条款存在，且非条款存在
    not_clause = MainClauses(clauses_id=0, document_id=document_id,
                             clauses_name="非条款",
                             sentences=not_clause_paragraphs)

    return not_clause, main_clause_list


def get_main_clauses_paragraphs(document, document_id: int) -> 'tuple[MainClauses, list[MainClauses]]':
    """
    读取docx文档，切分文档，封装大条款类和子条款类，
    返回首页非条款的大条款(MainClauses)类的list，条款集合大条款(MainClauses)的list

    :param document: docx文档对象
    :param document_id: 文档ID
    :param path: 文档路径

    :return: 返回非条款的大条款(MainClauses)类的list，条款集合大条款(MainClauses)的list
    """

    para_list = [para for para in list(document.paragraphs)]
    return __split_clause_paragraphs(document_id, para_list)


def __set_clause_sentence_matching(clauses1: 'MainClauses',
                                   clauses2: 'MainClauses',
                                   max_similarity: float) -> None:
    """
    设置大条款1的每一个句子与大条款2的最匹配的句子，
    设置匹配的大条款，并设置大条款中所有匹配的句子，继续向下计算大条款中每个句子的相似度

    :param clauses1: 大条款数组1
    :param clauses2: 大条款数组2
    :param max_similarity: 匹配的相似度
    :return:
    """

    clauses1.set_matching_clauses(clauses2, max_similarity)
    clauses2.set_matching_clauses(clauses1, max_similarity)

    # 设置大条款中所有匹配的句子，继续向下计算大条款中每个句子的相似度
    clauses1.set_matching_sentences_by_difflib()


MAIN_CLAUSE_SIMILARITY_MAX_VALUE = 0.94


def set_clauses_list_matching_clauses(clauses_list1: 'list[MainClauses]',
                                      clauses_list2: 'list[MainClauses]') -> None:
    """
    设置大条款列表1中的每一个大条款与大条款列表1最匹配的条款
    设置匹配的大条款，并设置大条款中所有匹配的句子，继续向下计算大条款中每个句子的相似度
    :param clauses_list1: 大条款数组1
    :param clauses_list2: 大条款数组2
    :return:
    """

    if not clauses_list1 or not clauses_list2:
        return

    Sentence.similarity_model = DEFAULT_SENTENCE_SIMILARITY_MODEL
    clauses_list2_tmp = list(clauses_list2)

    for i, clauses1 in enumerate(clauses_list1):
        if not clauses_list2_tmp:
            # 当句子已经匹配完成
            break

        if len(clauses1) < 1:
            # 自动跳过空行，空行不计算相似度
            continue

        print("clauses1", clauses1.clauses_id, clauses1.clauses_name)

        # 查找相似度最大的
        similarity_list = [clauses1.get_similarity(clauses2) for clauses2 in clauses_list2_tmp]
        max_i = argmax(similarity_list)
        match_obj = clauses_list2_tmp[max_i]
        max_similarity = similarity_list[max_i]

        # 查找相似度最大的
        if match_obj and similarity_list[max_i] >= MAIN_CLAUSE_SIMILARITY_MAX_VALUE:
            # 设置匹配的大条款，并设置大条款中所有匹配的句子，继续向下计算大条款中每个句子的相似度
            print("match:", match_obj.clauses_id, match_obj.clauses_name)

            # 继续向下计算大条款中每个句子的相似度
            __set_clause_sentence_matching(clauses1, match_obj, max_similarity)

            clauses_list2_tmp.remove(match_obj)

            print(max_similarity, '\n')
        else:
            print("match: None", '\n')


def set_no_clauses_sentence_matching(no_clauses1: 'MainClauses',
                                     no_clauses2: 'MainClauses') -> None:
    """
    设置非条款1的每一个句子与非条款2的最匹配的句子
    设置匹配的大条款，并设置大条款中所有匹配的句子，继续向下计算大条款中每个句子的相似度
    :param no_clauses1: 非条款数组1
    :param no_clauses2: 非条款数组2
    :return:
    """
    if not no_clauses1 or not no_clauses2:
        return

    Sentence.similarity_model = NO_CLAUSE_SENTENCE_SIMILARITY_MODEL

    __set_clause_sentence_matching(no_clauses1, no_clauses2, 1.0)


def set_exam_diff_result(first_no_clauses: 'MainClauses',
                         second_no_clauses: 'MainClauses',

                         first_clauses_list: 'list[MainClauses]',
                         second_clauses_list: 'list[MainClauses]', ) -> None:
    """
    通过差异对比得到将审核结果转化成差异字典

    :param first_no_clauses: 文档1的非条款
    :param second_no_clauses: 文档2的非条款
    :param first_clauses_list: 文档1条款列表
    :param second_clauses_list: 文档2条款列表
    :return:
    """
    if first_no_clauses or second_no_clauses:
        # 处理文档1非条款匹配的句子
        first_no_clauses.set_all_sentence_highlight_dict(is_first=True)

        # 处理文档2非条款未匹配的句子
        second_no_clauses.set_all_sentence_highlight_dict(is_first=False)

    if first_clauses_list or second_clauses_list:
        # 处理被对比的文档条款匹配的句子
        for clauses in first_clauses_list:
            clauses.set_all_sentence_highlight_dict(is_first=True)

        # 处理被对比的文档非条款未匹配的句子
        for clauses in second_clauses_list:
            clauses.set_all_sentence_highlight_dict(is_first=False)


def exam_result_to_html(no_clauses: 'MainClauses',
                        clauses_list: 'list[MainClauses]') -> str:
    """
    将审核结果转化成html

    :param no_clauses: 非条款
    :param clauses_list: 条款列表
    :return:
    """
    if not no_clauses:
        return ''.join(clauses.html for clauses in clauses_list)
    elif not clauses_list:
        return no_clauses.html
    else:
        return no_clauses.html + ''.join(clauses.html for clauses in clauses_list)


def exam_result_to_docx(download_document,
                        no_clauses: 'MainClauses',
                        clauses_list: 'list[MainClauses]',
                        download_path: str) -> str:
    """
    将审核结果转化成标注的docx


    :param download_document: docx文档对象
    :param no_clauses: 非条款
    :param clauses_list: 条款列表
    :param download_path: 下载路径
    :return:
    """
    if no_clauses:
        no_clauses.highlight_docx_paragraphs()
    if clauses_list:
        for clause in clauses_list:
            clause.highlight_docx_paragraphs()

    download_document.save(download_path)
    return True


def __split_clauses(not_clauses):
    """
    分割处理非条款，并去除处理空行

    :param not_clauses: 非条款
    :return:
    """
    result_sub_clauses = [[item] for item in not_clauses
                          if len(item.content) > 1]

    # 给sentence添加一个子条款号
    for no, sub_clauses in enumerate(result_sub_clauses):
        for sentence in sub_clauses:
            sentence.sub_clause_no = no

    return result_sub_clauses


def __split_sub_clauses(clauses: 'MainClauses'):
    """
    切分大条款,为若干个子条款，并给每个sentence添加一个子条款号

    :param clauses: 大条款
    :return:
    """
    if not len(clauses.clauses_list):
        return []

    sub_clause = r".{0,5}?\d{1,4}\.\d{1,4}.*?$"
    p, q = 0, 0
    result_sub_clauses = []
    for i, sentence in enumerate(clauses.clauses_list):
        # 查找条款标题
        if re.match(sub_clause, sentence.content.strip()):
            p, q = q, i
            tmp = [item for item in clauses.clauses_list[p:q]
                   if len(item.content) > 1]  # 去除空行
            result_sub_clauses.append(tmp)
    else:
        tmp = [item for item in clauses.clauses_list[q:]
               if len(item.content) > 1]  # 去除空行
        result_sub_clauses.append(tmp)
    # if not result_sub_clauses:
    #     tmp = [item for item in clauses.clauses_list
    #            if len(item.content) > 1]  # 去除空行
    #     result_sub_clauses.append(tmp)

    # 给sentence添加一个子条款号
    for no, sub_clauses in enumerate(result_sub_clauses):

        for sentence in sub_clauses:
            sentence.sub_clause_no = no
            print('__split_sub_clauses:', sentence.sub_clause_no, sentence, sentence.highlight_dict)
    print()
    return result_sub_clauses


def __is_all_space_string(sub_clauses: 'list[Sentence]') -> bool:
    """
    判断子条款是否都是空格/空字符

    :param sub_clauses:
    :return:
    """
    replace_spaces = lambda s: s.strip().replace('\t', '').replace(' ', '')
    return reduce(
        lambda x, y: x or y,
        (len(replace_spaces(sub.content)) < 1 for sub in sub_clauses)
    )


def __is_all_add_del(sub_clauses: 'list[Sentence]') -> bool:
    """
    判断一个子条款是否是整段添加或删除，

    :param sub_clauses: 子条款
    :return:
    """
    return reduce(
        lambda x, y: x and y,
        (sub.matching_sentence is None for sub in sub_clauses)
    )


def __has_highlight_dict(sub_clauses: 'list[Sentence]') -> bool:
    """
    判断一个子条款中的所以句子是否有高亮的字典，

    :param sub_clauses: 子条款
    :return:
    """
    return reduce(
        lambda x, y: x or y,
        (len(sub.highlight_dict) != 0 for sub in sub_clauses)
    )


def __has_diff_item(sub_clauses: 'list[Sentence]') -> 'bool':
    """
    一个子条款是否含有有差异条款

    :param sub_clauses: 子条款
    :return:
    """
    return reduce(
        lambda x, y: x or y,
        (len(sub.highlight_dict) > 0
         for sub in sub_clauses)
    )


def __to_xlsx_result_item(sub_clauses: 'list[Sentence]' = None, clause_no: int = None) -> 'dict':
    """
    返回生成xlsx中的一列的一项，
    如果默认参数或者sub_clauses为空,则返回{'content': [], 'highlight_dict': []}
    否则返回{content:子条款句子list，highlight_dict：子条款句子高亮内容列表}

    :param sub_clauses: 子条款
    :return:
    """
    item = {'content': [], 'highlight_dict': [], 'clause_no': clause_no}
    if sub_clauses:
        item['content'] = [clause.content for clause in sub_clauses]
        item['highlight_dict'] = [clause.highlight_dict for clause in sub_clauses]

    return item


def __get_match_sub_clauses(sub_clauses: 'list[Sentence]') -> int:
    """
    得到非全添加/删除的子条款匹配的子条款
    :param sub_clauses: 子条款
    :return:
    """
    count = Counter(
        sub.matching_sentence.sub_clause_no for sub in sub_clauses
        if sub.matching_sentence
    )
    print('count:', count)
    return max(count.items(), key=lambda a: a[1])[0]


def __get_template_clause_list_exam_result(template_clauses_list: 'list[MainClauses]',
                                           test_clauses_list: 'list[MainClauses]'):
    """
    向左遍历，遍历模板文档的审核结果，如果遇到模板文档的有子条款整段删除的，
    右边则流出一个空值，便于对齐，获取加工后的子条款结果

    :param template_clauses_list:  模板文档原始的审核结果
    :param test_clauses_list:  测试文档原始的审核结果
    :return:
    """
    result_list1 = []  # 暂存模板文档初步加工的审核结果
    result_list2 = []  # 暂存测试文档初步加工的审核结果

    # 遍历左边， 遍历该大条款中的子条款
    for template_clauses_i, main_clause in enumerate(template_clauses_list):  # 开始遍历大条款

        main_clause_result_list1 = []  # 一个文件1大条款生成xlsx的返回的结果值
        main_clause_result_list2 = []  # 一个文件2大条款生成xlsx的返回的结果值
        for main_clause_i, sub_clause in enumerate(main_clause):
            if __is_all_space_string(sub_clause):  # 这个子条款如果都是空行则走下一个循环
                continue
            elif __is_all_add_del(sub_clause):  # 是否全部是删除
                main_clause_result_list1.append(__to_xlsx_result_item(sub_clause, main_clause_i))
                main_clause_result_list2.append(__to_xlsx_result_item())

            elif __has_diff_item(sub_clause):  # 这个子条款含有差异项
                match_sub_clause_no = __get_match_sub_clauses(sub_clause)
                if template_clauses_i >= len(test_clauses_list):
                    continue
                if match_sub_clause_no >= len(test_clauses_list[template_clauses_i]):
                    continue


                match_sub_clauses = test_clauses_list[template_clauses_i][match_sub_clause_no]
                main_clause_result_list1.append(__to_xlsx_result_item(sub_clause, main_clause_i))
                main_clause_result_list2.append(__to_xlsx_result_item(match_sub_clauses, match_sub_clause_no))

        result_list1.append(main_clause_result_list1)
        result_list2.append(main_clause_result_list2)
    return result_list1, result_list2


def __get_test_sub_clause_next_add_sub_clause(test_clauses: 'list[dict]', next_test_clause_no: int):
    """
    获取当前测试文档字体条款的后n个被添加的的子条款

    :param test_clauses:
    :param next_test_clause_no:
    :return:
    """
    next_test_clauses = test_clauses[next_test_clause_no]  #
    result1 = []
    result2 = []
    while __is_all_add_del(next_test_clauses):  # 如果右边的条款为全部删除
        result1.append(__to_xlsx_result_item())
        result2.append(__to_xlsx_result_item(next_test_clauses))
        next_test_clause_no += 1
        if next_test_clause_no >= len(test_clauses):
            break
        next_test_clauses = test_clauses[next_test_clause_no]
    return result1, result2


def __get_test_sub_clause_part_add_sub_clause(test_main_clause: 'list[list[Sentence]]'):
    """
    得到当前测试文档的大条款中仅仅只有部分添加的子条款

    :param test_clauses_list: 测试文档的大条款
    :param clauses_i:
    :return:
    """
    print('test_clauses_list:', test_main_clause)
    result1 = []
    result2 = []
    for test_clauses in test_main_clause:
        if __has_highlight_dict(test_clauses):
            result1.append(__to_xlsx_result_item())
            result2.append(__to_xlsx_result_item(test_clauses))
    return result1, result2


def __continue_get_test_clause_list_exam_result(result_list1: 'list[dict]',
                                                result_list2: 'list[dict]',
                                                test_clauses_list: 'list[list[Sentence]]'):
    """
    继续遍历右边，由于遍历模板文档审核结果后，测试文档的整段添加的子条款无法找到，
    所以继续遍历测试文档的审核结果，通过对应行号的下一个行号查找删除的句子，将整段添加的子条款添加补回，
    并在模板文件的审核结果的对应位置添加一个空值，便于对齐审核结果

    :param result_list1:  模板文档初步加工的审核结果
    :param result_list2: 测试文档初步加工的审核结果
    :param test_clauses_list:  测试文档原始的审核结果
    :return:
    """
    new_result_list1 = []  # 暂存模板文档第二次加工的审核结果
    new_result_list2 = []  # 暂存测试文档第二次加工的审核结果

    for clauses_i, main_clause in enumerate(result_list1):
        test_clause_result = result_list2[clauses_i]
        test_clauses = test_clauses_list[clauses_i]

        main_clause_new_result_list1 = []  # 暂时存储一个大条款的加工结果
        main_clause_new_result_list2 = []  # 暂时存储一个大条款的加工结果
        print('main_clause:', clauses_i, main_clause)
        if not main_clause:  # 如果main_clause为空考虑是否出现测试文档段落部分添加的情况
            result1, result2 = __get_test_sub_clause_part_add_sub_clause(test_clauses_list[clauses_i])
            main_clause_new_result_list1.extend(result1)
            main_clause_new_result_list2.extend(result2)
        for clauses_j, sub_clause in enumerate(main_clause):

            # 通过一一对应，从左边获取右边的编号
            test_result = test_clause_result[clauses_j]
            test_clause_no = test_result.get('clause_no')

            # 添加扫描到的当前左右边句子
            main_clause_new_result_list1.append(sub_clause)
            main_clause_new_result_list2.append(test_result)

            if test_clause_no is None:  # 如果右边为空白, 则不查询右边列表是否有被添加句
                continue

            # 如果右边不为空白, 则查询右边列表是否有被添加句
            # 查找下一个句子，查看是否有删除的情况
            if test_clause_no + 1 < len(test_clauses):
                result1, result2 = __get_test_sub_clause_next_add_sub_clause(test_clauses, test_clause_no + 1)
                main_clause_new_result_list1.extend(result1)
                main_clause_new_result_list2.extend(result2)

        new_result_list1.append(main_clause_new_result_list1)
        new_result_list2.append(main_clause_new_result_list2)
    return new_result_list1, new_result_list2


def exam_result_to_xlsx(
        clause_list1: list,
        clause_list2: list,
        no_clause1: list,
        no_clause2: list):
    """
    主要功能，将模板文档审核结果大条款列表部分、测试文档审核结果大条款列表部分，
    模板文档审核结果非条款部分 、测试文档审核结果非条款部分的审核结果输出成xlsx。

    合同条款审核条款句子以及条款集合的定义:
    非条款的界限：开头是模式为“第一条 **** ”句子之前的句子
    大条款的界限：开头是模式为“第N条 **** ”句子, 结束为但不包含模式为“第N+1条 ****”的句子的若干个子条款集合
    子条款的界限：开头是模式“n.m **** ”句子, 结束为但不包含模式为“n.m+1 ****”的句子的若干个句子（条款句）集合
    条款句子：最基础的句子

    前提条件，模板文档和测试文档的大条款对应位置不会变化，即模板文档和测试文档的大条款数量以及对应位置相同，
    对应的大条款的内容相似且匹配。以下是一个匹配的大条款的内部情况实例图，
    其中“Ⓒ”为有修改（也包括部分删除添加）的子条款，“Ⓒ———————Ⓒ”为匹配的子条款，
    “〇”为没有匹配的句子， “➖”在模板文档被全部删除的子条款, “➕”在测试文档全部添加的子条款
        1        2               1        2
     1 Ⓒ        Ⓒ           1 Ⓒ        Ⓒ
     2 Ⓒ        Ⓒ           2 Ⓒ        Ⓒ
     3 ➖        Ⓒ           3 ➖
     4 Ⓒ        ➕           4 Ⓒ        Ⓒ
     5 Ⓒ        Ⓒ   --->   5           ➕
     6 ➖        〇           6 Ⓒ        Ⓒ
     7 ➖        〇           7 ➖
     8 〇        ➕           8 ➖
     9 Ⓒ        Ⓒ           9 Ⓒ        Ⓒ
    10 〇        ➕           10          ➕
                             11          ➕
    1.首先切分每一个大条款，把它们为若干个子条款，并在该子条款中的每一给sentence都添加一个子条款号。
    2.向左遍历，遍历模板文档的审核结果，如果遇到模板文档的有子条款整段删除的，
    右边则流出一个空值，便于对齐，获取加工后的子条款结果。
    3.继续遍历右边，由于遍历模板文档审核结果后，测试文档的整段添加的子条款无法找到，
    所以继续遍历测试文档的审核结果，通过对应行号的下一个行号查找删除的句子，将整段添加的子条款添加补回，
    并在模板文件的审核结果的对应位置添加一个空值，便于对齐审核结果
    4.遍历对比结果，生成xlsx返回结果

    :param clause_list1: 模板文档审核结果大条款列表部分
    :param clause_list2: 测试文档审核结果大条款列表部分
    :param no_clause1: 模板文档审核结果非条款部分
    :param no_clause2: 测试文档审核结果非条款部分
    :return:
    """
    # 切分大条款

    template_clauses_list = [__split_sub_clauses(clauses) for clauses in clause_list1] if clause_list1 else []

    test_clauses_list = [__split_sub_clauses(clauses) for clauses in clause_list2] if clause_list2 else []

    if no_clause1:
        template_clauses_list.insert(0, __split_clauses(no_clause1))
    if no_clause2:
        test_clauses_list.insert(0, __split_clauses(no_clause2))

    # 遍历右边， 遍历该大条款中的子条款
    result_list1, result_list2 = __get_template_clause_list_exam_result(template_clauses_list, test_clauses_list)

    # 遍历右边， 遍历该大条款中的子条款
    new_result_list1, new_result_list2 = __continue_get_test_clause_list_exam_result(
        result_list1, result_list2, test_clauses_list)

    return new_result_list1, new_result_list2
