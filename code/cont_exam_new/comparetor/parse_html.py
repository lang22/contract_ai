#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/3/5 15:21
@Author     : jzs
@File       : parse_html.py
@Software   : PyCharm
@Description: ......
"""

# span标签css class
from typing import Generator

SPAN_CSS_CLASS_ADDED = 'doc_add'

# span标签css class
SPAN_CSS_CLASS_CHANGED = 'doc_change'

# span标签css class
SPAN_CSS_CLASS_DEL = 'doc_delete'

# span标签css class
SPAN_CSS_CLASS_NOT_COMMON = 'doc_diff'

# <p>标签
PARA_HTML_LAB = '<p>', '</p>'

# 序列1仅有的字符的标签（deleted lab）
LAB_SEQ1_UNIQUE = '-'

# 序列2仅有的字符的标签（added lab）
LAB_SEQ2_UNIQUE = '+'

# 序列1和序列2共有的字符的标签(common lab)
LAB_SEQ1_SE2_COMMON = ' '

# 序列1和序列2不共有的字符的标签(changed lab)
LAB_SEQ1_SE2_NOT_COMMON = '^'

# 句子中的标高亮词的标签
SENTENCE_HTML_LAB = {
    LAB_SEQ1_SE2_NOT_COMMON: SPAN_CSS_CLASS_CHANGED,
    LAB_SEQ1_SE2_COMMON: "",
    LAB_SEQ1_UNIQUE: SPAN_CSS_CLASS_DEL,
    LAB_SEQ2_UNIQUE: SPAN_CSS_CLASS_ADDED,
}

# 文本中的空格定义
TEXT_SPACE = ' '

# 句子对比时的占位符号
PLACEHOLDER = '`'

# HTML文本中对空格的定义
HTML_SPACE_CODES = '&nbsp;'

# 有修改的标签,需要替换（格式化）<a>标签的id，<a>标签的title，<span>标签的id，<span>标签的class
ADDED = (
    """<a id="a_%s"  title="%s"  onclick="changeColor(this.id)"><span id="%s" class="%s">""",
    """</span></a>"""
)

# 相同的sqan标签的
SPAN_COMMON = ('<span>', '</span>')

# 空行的标签
SPACE_HTML = '<p><br></p>'

A_LAB_HTML_LAB = {
    LAB_SEQ1_SE2_NOT_COMMON: "修改",
    LAB_SEQ1_SE2_COMMON: "相同",
    LAB_SEQ1_UNIQUE: "删除",
    LAB_SEQ2_UNIQUE: "添加",
}

A_LAB_TITLE_INFO_MATCH = """
操作：源段落部分%s
对应位置：第%s条 %s 第%s段
源段落：%s
"""

A_LAB_TITLE_INFO_NOT_MATCH = """
操作：整段%s
%s的段落：%s
"""


def __batching(sentence: str, batch_size: int) -> str:
    """
    通过生成器批量化match_sentence，使每batch_size个字符一行
    :param sentence 句子
    :param batch_size: 批次数
    :return:
    """
    slice_g = ((x * batch_size, (x + 1) * batch_size)
               for x in range(batch_size * batch_size))
    s, t = next(slice_g)
    match_sentence_list = []
    while t < len(sentence):
        match_sentence_list.append(sentence[s: t])
        s, t = next(slice_g)
    else:
        match_sentence_list.append(sentence[s: len(sentence)])
    return '\n'.join(match_sentence_list)


def __get_a_lab_title_info(is_match: bool, tag: str,
                           match_main_parasID: int = -1,
                           match_main_paras_name: str = '',
                           match_parasID: int = -1, match_sentence: str = '', sentence='') -> str:
    """
    得到句子中的a标签的title信息

    :param is_match: 是否有匹配句，默认值为False
    :param tag: 修改的目标
    :param match_main_parasID: 匹配的大条款号
    :param match_main_paras_name: 匹配的大条款名字
    :param match_parasID:匹配的大条款号段落号
    :param match_sentence 匹配的句子

    :return:
    """
    if is_match:
        ret = A_LAB_TITLE_INFO_MATCH % (
            A_LAB_HTML_LAB[tag],
            match_main_parasID,
            match_main_paras_name,
            match_parasID,
            __batching(match_sentence, 30)
        )
    else:
        ret = A_LAB_TITLE_INFO_NOT_MATCH % (
            A_LAB_HTML_LAB[tag],
            A_LAB_HTML_LAB[tag],
            __batching(sentence, 30)
        )
    return ret


def parse_html_from_sentence(docID: int, paraID: int, sentence: str,
                             diff_dict: 'dict[tuple[int,int], str]',
                             is_match: bool = False,
                             match_main_parasID: int = -1, match_main_paras_name: str = '',
                             match_parasID: int = -1, match_sentence: str = '') -> str:
    """
    将一个句子转换成html代码字符串

    :param docID: 文档ID
    :param paraID: 段落ID
    :param sentence: 句子
    :param diff_dict: 差异字典
    :param is_match: 是否有匹配句，默认值为False
    :param match_main_parasID: 匹配的大条款号
    :param match_main_paras_name: 匹配的大条款名字
    :param match_parasID:匹配的大条款号段落号
    :param match_sentence 匹配的句子

    :return: 句子转换成html代码字符串
    """
    if not len(sentence):
        # 如果是空行
        return SPACE_HTML

    ps, pe = PARA_HTML_LAB
    if not diff_dict:
        # 如果是该句子没有修改
        sentence.replace(TEXT_SPACE, HTML_SPACE_CODES)
        return str().join((ps, sentence, pe))

    # 处理有修改的情况，首先把原句的空格通过占位符替代，之后再还替换成html的代码
    sentence = sentence.replace(TEXT_SPACE, PLACEHOLDER)

    html_string_list = []
    for key in diff_dict.keys():
        lab = diff_dict[key]
        if lab == '#':
            print(sentence)
            continue

        # 生成<span>标签的class
        tag = SENTENCE_HTML_LAB[lab]

        if tag:
            # 如果存在修改，生成<a>标签
            a_lab_start, a_lab_end = ADDED

            # 生成<a>标签的id
            tmp = str(docID), '_', str(paraID), '_', str(key[0]), '_', str(key[1])
            sentenceID = str().join(tmp)

            # 生成<a>标签的title
            title_info = __get_a_lab_title_info(
                is_match, lab,
                match_main_parasID,
                match_main_paras_name,
                match_parasID, match_sentence, sentence
            )

            # 替换（格式化）<a>标签的id，<a>标签的title，<span>标签的id，<span>标签的class
            a_lab_start %= (sentenceID, title_info, sentenceID, tag)
        else:
            # 如果不存在修改，不生成<a>标签，生成空串
            a_lab_start, a_lab_end = "", ""

        # 合并<a>标签和原句
        html_string = str().join((a_lab_start, sentence[slice(*key)], a_lab_end))
        html_string_list.append(html_string)

    # 合并所有
    html_string = str().join(html_string_list)
    return str().join((ps, html_string, pe)).replace(PLACEHOLDER, HTML_SPACE_CODES)


HTML_STYLE_CODE = """
<style>
a { 
    color: black;
    font-weight: Normal; /*CSS字体效果 普通 可以改成bold粗体 如果去除此行那么默认是不显示下划线的*/
    text-decoration: none; /*CSS下划线效果：无下划线*/
}
a:hover { color: black; }
.doc_add {  background-color: #aaffaa}
.doc_change {  background-color: yellow }
.doc_delete {  background-color: #ffaaaa }
.doc_diff {  background-color: lightgrey  }
.doc_confirm {   background-color: #FFF }
.difference {  color: red; }
.no_difference { color: green; }
.cdiv1 {
    border: 2px solid lightgrey;
    width: 50%;
    height: 800px;
    float: left;
    overflow: scroll;
    font-family: '新宋体'
}
.cdiv2 {
    border: 2px solid lightgrey;
    width: 50%;
    height: 800px;
    float: left;
    overflow: scroll;
    font-family: '新宋体';
}
</style>
"""

HTML_JS_CODE = """
/**
 * 修改颜色样式缓存字典
 */
let changeColorTmpDict = new Array()
/**
 * 修改颜色样式
 * @param aID
 */
function changeColor(aID) {
    let a = document.getElementById(aID);
    let spanID = a.firstElementChild.id;
    let span = document.getElementById(spanID);

    // 如果以及被修改，可以取消修改
    if (spanID in changeColorTmpDict) {
        let confirmValue = confirm("是否不接受“" + span.innerText + "”的修改？（点击确定将添加高亮）");
        if (confirmValue) {
            span.className = changeColorTmpDict[spanID];
            delete changeColorTmpDict[spanID];

        }
    } else {
        let confirmValue = confirm("是否接受“" + span.innerText + "”的修改？（点击确定将去除高亮）");
        if (confirmValue) {
            changeColorTmpDict[spanID] = span.className;
            span.className = 'doc_confirm';
        }
    }

    console.log(changeColorTmpDict);
    console.log(changeColorTmpDict.toString());
}
"""
