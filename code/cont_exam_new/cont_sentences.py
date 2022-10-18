#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/2/26 10:15
@Author     : jzs
@File       : Sentence.py
@Software   : PyCharm
@Description: Sentence Class 用
"""

from docx.text.paragraph import Paragraph
from numpy import argmax

from app.tools.docx_tools import set_paragraph_text_highlight_by_slice
from .comparetor import get_highlight_dict, get_all_del_highlight_dict, \
    get_all_add_highlight_dict, get_match_dict_by_difflib
from .comparetor.parse_html import parse_html_from_sentence
from .cont_cofig import MAIN_CLAUSES_SIMILARITY_MODEL_PATH, MAIN_CLAUSES_WORD2VEC_MODEL_PATH, \
    SENTENCE_WORD2VEC_MODEL_PATH, SENTENCE_SIMILARITY_MODEL_PATH, SIMILARITY_MAX_VALUE, \
    NO_CLAUSE_SENTENCE_SIMILARITY_MODEL_PATH, SPAN_CSS_CLASS_DOCX_COLOR_DICT

from .similarity import similarity_model_dict, get_pytorch_similarity

# 默认的计算句子相似度的模型
DEFAULT_SENTENCE_SIMILARITY_MODEL = similarity_model_dict['pytorch'](SENTENCE_SIMILARITY_MODEL_PATH)

# 计算非条款短句用的相似度模型
NO_CLAUSE_SENTENCE_SIMILARITY_MODEL = similarity_model_dict['pytorch'](NO_CLAUSE_SENTENCE_SIMILARITY_MODEL_PATH)

# 默认的句子词向量
DEFAULT_SENTENCE_WORD2VEC_MODEL = similarity_model_dict['word2vec'](SENTENCE_WORD2VEC_MODEL_PATH)


class Sentence(object):
    """
    用于合同审核中便于句子操作的各种属性的封装

    """
    # 相似度模型
    similarity_model = DEFAULT_SENTENCE_SIMILARITY_MODEL

    # 词向量模型
    word2vec_model = DEFAULT_SENTENCE_WORD2VEC_MODEL

    def __init__(self, sentence_id: int, clauses_id: int, parent_clauses: "MainClauses",
                 document_id: int, para: 'Paragraph') -> 'Sentence':
        """
        初始化句子类

        :param sentence_id: 该句子的ID
        :param document_id: 该句子所在文档的ID

        :param clauses_id: 该句子的所在的大条款的ID
        :param parent_clauses 该句子所在的大条款的对象
        :param para: 该句子对应的docx包中Paragraph对象
        """
        # 句子ID
        self.__sentence_id = sentence_id

        # 句子所在文档的ID
        self.__document_id = document_id

        # 句子的所在的大条款的ID
        self.__clauses_id = clauses_id

        # 句子所在的子条款号
        self.__sub_clause_no = None

        # 句子所在的大条款的对象
        self.__parent_clauses_obj = parent_clauses

        # 句子对应的docx包中paragraph对象
        self.__paragraph_obj = para

        # 句子内容
        self.__sentence_content = para.text

        # 句子被标高亮的字典
        self.__highlight_dict = None

        # 匹配到的最相似的句子ID, -1 代表没有匹配的句子
        self.__matching_sentence_id = -1

        # 匹配到的最相似的句子对象
        self.__matching_sentence = None

        # 与匹配到的最相似的句子的相似度
        self.__similarity = 0

        # 该转化成的html
        self.__html = ''

        self.__next_sentence = None

    def set_matching_sentence(self, sentence: 'Sentence', max_similarity: float) -> None:
        """
        设置匹配的句子ID和设置匹配的句子对象

        :param sentence: 匹配的主条款对象
        :param max_similarity:  匹配的相似度
        :return:
        """
        self.matching_sentence = sentence
        self.matching_sentence_id = sentence.sentence_id
        self.similarity = max_similarity

    def get_similarity(self, sentence2: 'Sentence') -> float:
        """
        得到与句子2的相似度

        :param sentence2:
        :return:
        """
        if not len(self.content) or not len(sentence2.content):
            return 0
        sim = get_pytorch_similarity(Sentence.word2vec_model,
                                     Sentence.similarity_model,
                                     self.content, sentence2.content)
        return sim

    def set_highlight_dict(self, is_first: bool = True) -> None:
        """
        设置与匹配的句子的差异对比的结果：
        分成4中情况：
        （1）如果该句子是被对比的文档（文档1）的句子，且存在匹配句，
            则使用文档1的句子和文档1的匹配句（文档2的句子）进行差异对比，
            并且，将对比结果依次赋值给文档1的句子和文档1的匹配句（文档2的句子）
        （2）如果该句子是文档1的句子，但是不存在匹配句，则将这个句子表示成“被删除句”
        （3）如果该句子不是文档1的句子而是文档2的句子，且存在匹配句，则什么都不做
        （4）如果该句子不是文档1的句子而是文档2的句子，但是不存在匹配句，则将这个句子表示成“被添加句”

        :param is_first 该句子是不是被对比的文档（文档1），True为文档1的句子，False为文档2的句子
        :return:
        """
        if is_first and self.matching_sentence:
            # 如果该句子是被对比的文档（文档1）的句子，且存在匹配句，
            # 则使用文档1的句子和文档1的匹配句（文档2的句子）进行差异对比
            # 并且，将对比结果依次赋值给文档1的句子和文档1的匹配句（文档2的句子）
            this_dict, match_dict = get_highlight_dict(self.content, self.matching_sentence.content)
            self.__highlight_dict = this_dict
            self.matching_sentence.__highlight_dict = match_dict

        elif is_first and self.matching_sentence is None:
            # 如果该句子是文档1的句子，但是不存在匹配句，则将这个句子表示成“被删除句”
            self.__highlight_dict = get_all_del_highlight_dict(self.content)

        elif not is_first and self.matching_sentence:
            # 如果该句子不是文档1的句子而是文档2的句子，且存在匹配句，则什么都不做
            pass

        elif not is_first and self.matching_sentence is None:
            # 如果该句子不是文档1的句子而是文档2的句子，但是不存在匹配句，则将这个句子表示成“被添加句”
            self.__highlight_dict = get_all_add_highlight_dict(self.content)

    @property
    def sentence_id(self) -> int:
        """
        返回句子ID

        :return:
        """
        return self.__sentence_id

    @property
    def document_id(self) -> int:
        """
        返回句子所在文档的ID

        :return:
        """
        return self.__document_id

    @property
    def parent_clauses_obj(self):
        """
        返回该句子所在的大条款的对象

        :return:
        """
        return self.__parent_clauses_obj

    @property
    def matching_sentence_id(self) -> int:
        """
        返回匹配到的最相似的句子

        :return:
        """
        return self.__matching_sentence_id

    @matching_sentence_id.setter
    def matching_sentence_id(self, _id) -> int:
        """
        设置匹配到的最相似的句子的ID

        :param _id: 最相似的句子的ID
        :return:
        """
        self.__matching_sentence_id = _id

    @property
    def matching_sentence(self) -> 'Sentence':
        """
        返回匹配到的最相似的句子对象

        :return:
        """
        return self.__matching_sentence

    @matching_sentence.setter
    def matching_sentence(self, sentence: 'Sentence'):
        """
        设置匹配到的最相似的句子对象

        :param sentence: 匹配到的最相似的句子对象
        :return:
        """
        self.__matching_sentence = sentence

    @property
    def paragraph_obj(self) -> 'Paragraph':
        """
        返回该句子对应的docx包中paragraph对象

        :return:
        """
        return self.__paragraph_obj

    def highlight_docx_paragraph(self):
        """
        使用高亮字典标注docx文档
        :return:
        """
        if not self.__highlight_dict:
            return
        highlight_dict: dict = self.__highlight_dict
        for key in highlight_dict.keys():
            highlight = highlight_dict[key]
            if highlight:
                color = SPAN_CSS_CLASS_DOCX_COLOR_DICT.get(highlight)
                if color:
                    set_paragraph_text_highlight_by_slice(self.paragraph_obj, key, color)

    @property
    def content(self) -> str:
        """
        返回该句子的内容的符串
        :return:
        """
        return self.__sentence_content

    @property
    def highlight_dict(self):
        """
        得到高亮字典
        :return:
        """
        return self.__highlight_dict

    @property
    def sub_clause_no(self) -> int:
        """
        得到该句子所在的子条款号

        :return:
        """
        return self.__sub_clause_no

    @sub_clause_no.setter
    def sub_clause_no(self, clause_no: int):
        """
        设置该句子所在的子条款号

        :param value:
        :return:
        """
        self.__sub_clause_no = clause_no

    @property
    def html(self) -> str:
        """
        返回该主条款的内容转化成的HTML
        :return:
        """
        if self.matching_sentence:
            # 如果匹配句存在，加入匹配句的相关信息

            parent_clauses = self.matching_sentence.parent_clauses_obj
            self.__html = parse_html_from_sentence(
                docID=self.document_id,
                paraID=self.sentence_id,
                sentence=self.content,
                diff_dict=self.__highlight_dict,
                is_match=True,
                match_main_parasID=parent_clauses.clauses_id,
                match_main_paras_name=parent_clauses.clauses_name,
                match_parasID=self.matching_sentence.sentence_id,
                match_sentence=self.matching_sentence.content
            )
        else:
            self.__html = parse_html_from_sentence(
                docID=self.document_id,
                paraID=self.sentence_id,
                sentence=self.content,
                diff_dict=self.__highlight_dict
            )
        return self.__html

    @property
    def similarity(self) -> float:
        """
        返回与匹配的主条款的主条款的相似度

        :return:
        """
        return self.__similarity

    @similarity.setter
    def similarity(self, sim: float) -> None:
        """
        返回与匹配的主条款的主条款的相似度

        :return:
        """
        self.__similarity = sim

    def __str__(self) -> str:
        """
        对象转化成字符串
        :return:
        """
        return self.__sentence_content

    def __repr__(self) -> str:
        """
        打印输出的字符串
        :return:
        """
        return self.__sentence_content

    def __len__(self) -> int:
        """
        返回句子的长度，句子的长度定义为首尾非空格字符的字符串函数

        :return:
        """
        return len(self.content.strip())


# 默认的计算句子相似度的模型
DEFAULT_MAIN_CLAUSES_SIMILARITY_MODEL = similarity_model_dict['pytorch'](MAIN_CLAUSES_SIMILARITY_MODEL_PATH)

# 默认的计算句子相似度的模型
DEFAULT_MAIN_CLAUSES_WORD2VEC_MODEL = similarity_model_dict['word2vec'](MAIN_CLAUSES_WORD2VEC_MODEL_PATH)


class MainClauses(object):
    """
    大条款类，包括很多个子条款
    """
    # 相似度模型
    similarity_model = DEFAULT_MAIN_CLAUSES_SIMILARITY_MODEL

    # 词向量模型
    word2vec_model = DEFAULT_MAIN_CLAUSES_WORD2VEC_MODEL

    def __init__(self, clauses_id: int, document_id: int,
                 clauses_name: str, sentences: list) -> 'MainClauses':
        """
        初始化大条款类

        :param clauses_id: 大条款ID
        :param document_id: 该句子所在文档的ID
        :param clauses_name: 条款名字
        :param sentences: 条款包含的docx 段落(paragraph类型)的list
        """
        # 主条款的ID

        self.__clauses_id = clauses_id

        # 主条款所在文档的ID
        self.__document_id = document_id

        # 匹配的主条款ID, -1代表没有匹配的句子
        self.__matching_clauses_id = -1

        # 匹配的主条款的主条款对象,none代表没有匹配的
        self.__matching_clauses = None

        # 与匹配的主条款的主条款的相似度
        self.__similarity = 0

        # 主条款的名字
        self.__clauses_name = clauses_name

        # 该主条款的子条款(Sentence类)集合, 初始化clauses中的所有句子类
        if len(sentences) > 1:
            self.__clauses_list = [Sentence(sentence_id=i, clauses_id=clauses_id, parent_clauses=self,
                                            document_id=document_id, para=para)
                                   for i, para in enumerate(sentences)]
        else:
            self.__clauses_list = []

        # 该主条款的子条款字符串
        self.__clauses_content = str().join([para.text for para in sentences])

        # 该转化成的html
        self.__html = ''

    def get_similarity(self, clauses2: 'MainClauses') -> float:
        """
        得到与句子2的相似度

        :param clauses2: 大条款2
        :return:
        """
        if not self.clauses_content or not clauses2.clauses_content:
            return 0

        sim = get_pytorch_similarity(MainClauses.word2vec_model,
                                     MainClauses.similarity_model,
                                     self.clauses_content, clauses2.clauses_content)
        return sim

    def set_matching_clauses(self, clauses: 'MainClauses', max_similarity: float):
        """
        设置匹配的主条款ID和设置匹配的主条款对象

        :param clauses: 匹配的主条款对象
        :param max_similarity: 匹配的相似度
        :return:
        """
        self.matching_clauses = clauses
        self.matching_clauses_id = clauses.clauses_id
        self.similarity = max_similarity

    def set_matching_sentences_by_pytorch(self) -> None:
        """
        设置句子集合中的每一个句子于最匹配的大条款中的最匹配的条款

        设置方式为pytorch的相似度对比
        :return:
        """
        if not self.matching_clauses:
            print('matching_clauses is None!')
            return

        matching_sentences = list(self.matching_clauses.clauses_list)

        for sent1 in self.clauses_list:
            if not len(matching_sentences):
                # 当句子已经匹配完成
                break

            if not len(sent1):
                # 自动跳过空行，空行不计算相似度
                continue

            # 查找相似度最大的
            similarity_list = [sent1.get_similarity(sent2) for sent2 in matching_sentences]
            max_i = argmax(similarity_list)
            match_obj = matching_sentences[max_i]
            max_similarity = similarity_list[max_i]

            if match_obj and max_similarity >= SIMILARITY_MAX_VALUE:
                # 设置最匹配的句子
                sent1.set_matching_sentence(match_obj, max_similarity)
                match_obj.set_matching_sentence(sent1, max_similarity)
                # 去除已经匹配的列表
                matching_sentences.remove(match_obj)
                print("similarity_list:", similarity_list)
                print('sent1:', sent1.content)
                print('match:', match_obj.content)
                print()

    def set_matching_sentences_by_difflib(self) -> None:
        """
        设置句子集合中的每一个句子于最匹配的大条款中的最匹配的条款

        设置方式为difflib的差异对比
        :return:
        """
        if not self.matching_clauses:
            print('matching_clauses is None!')
            return

        # 去除空行的
        this_sentences = list(filter(lambda sent: len(sent), self.clauses_list))
        matching_sentences = list(filter(lambda sent: len(sent), self.matching_clauses.clauses_list))
        # this_sentences = self.clauses_list
        # matching_sentences = self.matching_clauses.clauses_list

        # 得到每个句子的字符串的内容
        this_sentences_content = [sent.content for sent in this_sentences]
        matching_sentences_content = [sent.content for sent in matching_sentences]

        # 得到句子列表1和句子列表2的匹配字典
        match_index_dict = get_match_dict_by_difflib(this_sentences_content, matching_sentences_content)

        # 根据匹配字典设置匹配句
        for i, j in match_index_dict.items():
            sent = this_sentences[i]
            match = matching_sentences[j]
            sent.set_matching_sentence(match, 1.0)
            match.set_matching_sentence(sent, 1.0)

    def set_matching_sentences_by_search(self) -> None:
        """
        设置句子集合中的每一个句子于最匹配的大条款中的最匹配的条款

        设置方式为逐句对比
        :return:
        """
        if not self.matching_clauses:
            print('matching_clauses is None!')
            return

        matching_sentences = list(filter(lambda sent: len(sent), self.matching_clauses.clauses_list))

        for sent1 in self.clauses_list:
            if not len(matching_sentences):
                # 当句子已经匹配完成
                break

            if not len(sent1):
                # 自动跳过空行，空行不计算相似度
                continue
            match = matching_sentences.pop(0)
            sent1.set_matching_sentence(match, 1)
            match.set_matching_sentence(sent1, 1)

    def set_all_sentence_highlight_dict(self, is_first=True):
        """
        将句子集合中所有句子通过表上颜色

        :return:
        """
        for clauses in self.clauses_list:
            clauses.set_highlight_dict(is_first)

    def highlight_docx_paragraphs(self):
        """
        标注所有句子

        :return:
        """
        for clauses in self.clauses_list:
            clauses.highlight_docx_paragraph()

    @property
    def clauses_id(self) -> int:
        """
        返回主条款的ID
        :return:
        """
        return self.__clauses_id

    @property
    def document_id(self) -> int:
        """
        返回主条款所在文档的ID
        :return:
        """
        return self.__document_id

    @property
    def matching_clauses_id(self) -> int:
        """
        返回匹配的主条款ID

        :return:
        """
        return self.__matching_clauses_id

    @matching_clauses_id.setter
    def matching_clauses_id(self, matching_clauses_id: int) -> None:
        """
        设置匹配的主条款ID

        :param matching_clauses_id: 匹配的主条款ID
        :return:
        """
        self.__matching_clauses_id = matching_clauses_id

    @property
    def similarity(self) -> float:
        """
        返回与匹配的主条款的主条款的相似度

        :return:
        """
        return self.__similarity

    @similarity.setter
    def similarity(self, sim: float) -> None:
        """
        返回与匹配的主条款的主条款的相似度

        :return:
        """
        self.__similarity = sim

    @property
    def matching_clauses(self) -> 'MainClauses':
        """
        匹配的主条款对象

        :return:
        """
        return self.__matching_clauses

    @matching_clauses.setter
    def matching_clauses(self, clauses: 'MainClauses'):
        """
        设置匹配的主条款对象

        :param clauses: 匹配的主条款对象
        :return:
        """
        self.__matching_clauses = clauses

    @property
    def clauses_name(self) -> str:
        """
        主条款的名字

        :return:
        """
        return self.__clauses_name

    @property
    def clauses_list(self) -> 'list[Sentence]':
        """
        该主条款的子条款(Sentence类)list集合
        :return:
        """
        return self.__clauses_list

    def __getitem__(self, index: int) -> 'Sentence':
        """
        通过下标获取主条款的子条款(Sentence类)list集合中的某个句子

        :param index:
        :return:
        """
        return self.__clauses_list[index]

    @property
    def clauses_content(self) -> str:
        """
        该主条款的子条款字符串

        :return:
        """
        return self.__clauses_content

    @property
    def html(self) -> str:
        """
        返回该主条款的内容转化成的HTML
        :return:
        """
        return str().join(clauses.html for clauses in self.clauses_list)

    def to_string(self):
        """
        转化成可读的字符串

        :return:
        """
        output = ['clauses_id:', str(self.clauses_id), '\n',
                  'clauses_name:', self.clauses_name, '\n',
                  'document_id:', str(self.document_id), '\n']
        for s in self.clauses_list:
            output.append(s.content)
            output.append('\n')
        # print(output)
        return str().join(output)

    def __len__(self) -> int:
        """
        返回段落的长度，长度规定为句子的个数

        :return:
        """
        return len(self.clauses_list)

    def __str__(self) -> str:
        """
        对象转化成字符串

        :return:
        """
        return self.to_string()

    def __repr__(self) -> str:
        """
        打印输出的字符串

        :return:
        """
        return self.to_string()
