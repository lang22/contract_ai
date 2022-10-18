import copy

from docx import Document

from cont_check.check_method import get_sims_result_by_paragraphs, sims_result_parse_json, get_sims_result_by_sentence


def sims_result_cast(res):
    """
    相似结果段落转化器
    :param res:
    :return:
    """
    return [{
        "simDocumentID": str(i + 1),
        "simDocumentTitle": r['simple_file'],
        "simDocumentContent": r['content'],
        'simDocumentsName': r['filename'],
        "simValue": r['sims']}
        for i, r in enumerate(res['results'])]


def cont_check_get_sim_paragraphs_by_docx(file_path: str):
    """
    获取是否具有相似的所有段落，并获取第一个相似段落结果
    :param file_path:
    :return:
    """
    f = Document(file_path)
    paragraphs = [p.text for p in f.paragraphs if p.text]
    first_content_result, result = get_sims_result_by_paragraphs(paragraphs)
    tmp = sims_result_parse_json(first_content_result)
    first_content_result = sims_result_cast(tmp)
    return first_content_result, result


def cont_check_get_sim_paragraphs_by_sentence(sentence: str):
    """
    获取相似度的内容
    :param sentence:
    :return:
    """
    result = get_sims_result_by_sentence(sentence)
    if not result:
        return []
    tmp = sims_result_parse_json(result)
    first_content_result = sims_result_cast(tmp)
    return first_content_result
