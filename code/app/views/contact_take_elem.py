#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019-05-09 10:11
@Author     : charles
@File       : cont_multi_exam.py
@Software   : PyCharm
@Description: ......
"""
import copy
import os
import traceback, json

from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from app import logger
from app.tools import join_path
from app.tools.pre_docx import multi_process
from config import Config
from cont_multi_extract import multi_extracting
from cont_multi_extract.distinct_color import set_color

from ..tools import pre_docx, doc_docx_tools
from ..models.cont_docx_backup_table import ContDocxBackupTable

take_elem = Blueprint('take_elem', __name__)

SUCCESS = 1

NOT_SUCCESS = 0

OK = 'ok!'

ERROR = "error!"

ERROR_00: str = "error 00:参数为空!"

ERROR_01 = "error 00:某个文档不存在！"

ERROR_02 = "error 02:某个文档格式错误！"

ERROR_03 = "error 03:文档解析错误！"

DEFAULT_RESULT_JSON = {
    "success": NOT_SUCCESS,
    "msg": ERROR,
}


@take_elem.route('/contract_multi_solve_by_json', methods=['POST', 'GET'])
def contract_multi_solve_by_json():
    """
    多文档要素抽取以及对比，接口版本
    前端传来的是'["xxxxxx.docx", "xxxxxx.docx",....,"xxxxxx.docx"]' 的json数据
    :return:
    """
    result_json = copy.deepcopy(DEFAULT_RESULT_JSON)
    result_item = {
        "contractNameList": "",
        "contractElementList": ""
    }

    try:

        json_data = request.get_data(as_text=True)
        if not json_data:
            raise ValueError(ERROR_00)

        # 获取前端POST请求传过来的 json 数据
        json_data = json.loads(json_data)
        print(json_data)

        contract_id_list = json_data["contractID"]
        contract_name_list = json_data["fileNameList"]

        # 获取文件路径
        upload_file_path_list = []
        for cid in contract_id_list:
            path = join_path(Config.UPLOADED_DIR_PATH, cid)
            if not os.path.exists(path):
                raise FileNotFoundError(ERROR_01)
            upload_file_path_list.append(path)

        # 将合同保存到数据库
        for file_path in upload_file_path_list:
            ContDocxBackupTable.add_one(request.remote_addr, file_path)
        content_dict_dic, elem_lis = multi_extracting(contract_name_list, upload_file_path_list)
        elem_color_dic = set_color(content_dict_dic, elem_lis)

        # 传入前端的参数，需要有，文件名列表、每个文件对应的要素-内容列表（此处要素数保持一致，不存在写空）

        print("contract_name_list:", contract_name_list)
        print("elem_lis:", elem_lis)
        print("content_dict_dic:", content_dict_dic)
        print("elem_color_dic:", elem_color_dic)

        result_item['contractNameList'] = [filename for filename in contract_name_list]
        result_item['contractElementList'] = [{
            "elementName": element,
            "elements": [
                {"content": str(content_dict_dic[filename][element]),
                 "color": elem_color_dic[element].get(str(content_dict_dic[filename][element]), "none")}
                for filename in contract_name_list]
        } for element in elem_lis]

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
