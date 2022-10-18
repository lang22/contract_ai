import re

#  基于类型的正则表达式字典
REGEX_EXPRESSION = {
    'simple_instructions' : r'.*%s.*(\[.*?\])?',
    'date' : r'.*%s.*(\[\])?年.*(\[\])?月.*(\[\])?日',
    'base' : r'.*%s.*',
    'case_amount' : r'.*(%s.*?(人民币)?\[\]元?（小写：(人民币)?\[\]元?）)',
}


def trans_date(date):
    """
    将 2018年11月12日这种类型提取出数字来
    :param date:
    :return:
    """

    result = re.findall('(\d{1,4})', date)
    return result

