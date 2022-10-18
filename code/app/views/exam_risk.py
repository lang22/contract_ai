import copy
import json
import os
import re
import traceback

from flask import Blueprint, request, flash, render_template, redirect, url_for, session, send_from_directory

from exam_clause import contract_clause_exam
from ..tools import doc_docx_tools
from ..models.cont_docx_backup_table import ContDocxBackupTable
from ..tools import pre_docx

from app import logger
from app.algorithm.amount_exam import check_amount_difference
from app.models.cont_ext_element_table import ContExtElementTable
from app.models.cont_ext_result import ConExtResult
from app.models.contract_ext_table import ContractExtTable
from app.tools import random_fliename, join_path
from cont_exam_new import get_exam_result_by_html2, get_exam_result_by_html

from config import Config
from elem_extract import extracting

exam_risk = Blueprint('exam_risk', __name__)

SUCCESS = 1

NOT_SUCCESS = 0

OK = 'ok!'

ERROR = "error!"

ERROR_00: str = "error 00:参数1或参数2为空!"

ERROR_01 = "error 00:文档1或文档2不存在！"

ERROR_02 = "error 02:文档1或文档2格式错误！"

ERROR_03 = "error 03:文档1或文档2解析错误！"

DEFAULT_RESULT_JSON = {
    "success": NOT_SUCCESS,
    "msg": ERROR,
}


@exam_risk.route('/get_contract_type_list_by_json', methods=['GET', 'POST'])
def get_contract_type_list_by_json():
    """
    http:// 114.116.74.129:9097/exam_risk/get_contract_type_list_by_json
    http://127.0.0.1:5000/exam_risk/get_contract_type_list_by_json

    {"success": 1, "msg": "ok!", "result": {"type_list": ["XXXX","XXXX","XXXX"] }}
    :return:
    """
    result_json = copy.deepcopy(DEFAULT_RESULT_JSON)
    result = {"typeList": ''}
    try:
        contracts = ContractExtTable.select_all()

        result["typeList"] = [cont.cont_name for cont in contracts]

        result_json["success"] = SUCCESS
        result_json["msg"] = OK
        result_json["result"] = result

    except Exception as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
    finally:
        return json.dumps(result_json)


@exam_risk.route('/exam_model_docx_risk_by_json', methods=['POST', 'GET'])
def exam_model_docx_risk_by_json():
    """
    合同审核后的内容 形式化审核 审核信息 合同流程表
    :param filename:
    :return:
    """

    result_json = copy.deepcopy(DEFAULT_RESULT_JSON)
    result_item = {
        "firstHTMLCode": "",
        "secondHTMLCode": "",
        "downloadFirstDocxID": "",
        "downloadSecondDocxID": "",
        "downloadExcelID": ""}

    try:

        docx_ID = request.values.get("docID")
        model_type_name = request.values.get("type")

        print('doc_ID:', docx_ID,
              '\nmodel_type_name:', model_type_name)
        if not docx_ID or not model_type_name:
            raise ValueError(ERROR_00)

        test_path = join_path(Config.UPLOADED_DIR_PATH, docx_ID)

        # 获取模板的路径
        cont_path = ContractExtTable.select_one_by_name(model_type_name).cont_path
        if not cont_path:
            raise ValueError(ERROR_00)
        model_path = join_path(Config.CONT_GENA_TEMPLATE_DIR_PATH, cont_path + '.docx')

        print('model_path:', model_path,
              "\ntest_path:", test_path)

        if not os.path.exists(model_path) or not os.path.exists(test_path):
            raise FileNotFoundError(ERROR_01)
        #
        # 保存到数据库
        ContDocxBackupTable.add_one(request.remote_addr, test_path)
        ContDocxBackupTable.add_one(request.remote_addr, model_path)

        model_html, test_html, file_path1, file_path2, xlsx_download_path \
            = get_exam_result_by_html(model_path, test_path)

        result_item['firstHTMLCode'] = model_html
        result_item['secondHTMLCode'] = test_html
        result_item['downloadFirstDocxID'] = os.path.basename(file_path1)
        result_item['downloadSecondDocxID'] = os.path.basename(file_path2)
        result_item['downloadExcelID'] = os.path.basename(xlsx_download_path)

        result_json["success"] = SUCCESS
        result_json["msg"] = OK
        result_json['result'] = result_item

    except ValueError as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
    except FileNotFoundError as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
    except Exception as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = ERROR_03
    finally:
        return json.dumps(result_json)


@exam_risk.route('/exam_elem_risk_by_json', methods=['GET', 'POST'])
def exam_elem_risk_by_json():
    """


    :return:
    """
    result_json = copy.deepcopy(DEFAULT_RESULT_JSON)
    result_item = {
        "contractCheckResResult": "",
        "contractClauseTitleExamResult": ""}

    try:
        docx_ID = request.values.get("docID")
        model_type_name = request.values.get("type")

        print('doc_ID:', docx_ID,
              '\nmodel_type_name:', model_type_name)
        if not docx_ID or not model_type_name:
            raise ValueError(ERROR_00)

        test_path = join_path(Config.UPLOADED_DIR_PATH, docx_ID)

        # 获取模板的路径
        cont_path = ContractExtTable.select_one_by_name(model_type_name).cont_path
        if not cont_path:
            raise ValueError(ERROR_00)
        model_path = join_path(Config.CONT_GENA_TEMPLATE_DIR_PATH, cont_path + '.docx')

        print('model_path:', model_path,
              "\ntest_path:", test_path)
        if not os.path.exists(model_path) or not os.path.exists(test_path):
            raise FileNotFoundError(ERROR_01)

        # 保存到数据库
        ContDocxBackupTable.add_one(request.remote_addr, test_path)
        ContDocxBackupTable.add_one(request.remote_addr, model_path)

        # 合同的条款审核
        _, _, clause_title = contract_clause_exam(model_path, test_path)
        # todo

        clause_title_result = [{
            "titleNumber": d[0],
            "titleContent": d[1],
            "examResult": re.findall('<span.*?>(.*?)</span>', d[3])[0],
            "tip": d[4]}
            for d in clause_title]

        print("clause_title_result:", clause_title_result)

        cont_id = ContractExtTable.select_one_by_name(model_type_name).cont_id
        elem_id_dict, elem_key_dict, elem_type_dict = ContExtElementTable.get_elements_dict(cont_id)  # 读取要素列表
        # 要素抽取
        elem_content_dic = extracting(test_path, elem_id_dict, elem_key_dict, elem_type_dict)
        # 加密并保存到数据库
        result_dict = ConExtResult.to_aes_result_dict(elem_id_dict, elem_content_dic)
        ConExtResult.add_all(cont_id, test_path, result_dict)
        # 合同金额审核
        check_res_dict = check_amount_difference(elem_type_dict, elem_content_dic)

        print("check_res_dict:", check_res_dict)
        res_dict = {1: '大小写金额一致', 0: '大小写金额不相等', -1: '大写金额有误'}
        check_res_result = []
        for key in check_res_dict.keys():
            a, b = elem_content_dic.get(key)
            check_res_result.append(
                {"amountName": key,
                 "amountUpValue": a,
                 "amountDownValue": b,
                 "examResult": res_dict[check_res_dict[key]]}
            )

        print("check_res_result:", check_res_result)

        result_item['contractCheckResResult'] = check_res_result
        result_item['contractClauseTitleExamResult'] = clause_title_result
        result_json["msg"] = OK
        result_json['result'] = result_item

    except ValueError as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
    except FileNotFoundError as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
    except Exception as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = ERROR_03
    finally:
        return json.dumps(result_json)
