import copy
import json
import os
import traceback

from cont_check import cont_check_get_sim_paragraphs_by_docx, cont_check_get_sim_paragraphs_by_sentence
from flask import Blueprint, request

from app.tools import join_path
from config import Config
from app import logger
from cont_check.check_download_method import get_content_by_filename

from ..models.cont_docx_backup_table import ContDocxBackupTable

cont_check_new = Blueprint('cont_check', __name__)

SUCCESS = 1

NOT_SUCCESS = 0

OK = 'ok!'

ERROR = "error!"

ERROR_00: str = "error 00:参数为空!"

ERROR_01 = "error 00:文档不存在！"

ERROR_02 = "error 02:文档格式错误！"

ERROR_03 = "error 03:文档解析错误！"

DEFAULT_RESULT_JSON = {
    "success": NOT_SUCCESS,
    "msg": ERROR,
}


@cont_check_new.route('/contract_check_detail', methods=['POST', 'GET'])
def contract_check_detail():
    """
    合规性审查，生成审查文档，按段落存储
    :param filename:读入的文件路径名称
    :return:
    """
    result_json = copy.deepcopy(DEFAULT_RESULT_JSON)

    try:
        filename = request.values.get("docID")

        if not filename:
            raise ValueError(ERROR_00)

        upload_path_userup = join_path(Config.UPLOADED_DIR_PATH, filename)
        if not os.path.exists(upload_path_userup):
            raise FileNotFoundError(ERROR_01)

        first_para_content, document_content = cont_check_get_sim_paragraphs_by_docx(upload_path_userup)

        print("data1：", first_para_content)
        print("data2：", document_content)

        # 将合同保存到数据库
        ContDocxBackupTable.add_one(request.remote_addr, upload_path_userup)

        # body, style, first_sims, first_para_content = solve_method(upload_path_userup)

        if len(first_para_content) == 0:
            result_json['result'] = "本合同未查找到任何相似信息"

        else:
            result_item = {'documentContent': document_content,
                           'firstSimsList': first_para_content}
            result_json['result'] = result_item
        print("first_para_content:", first_para_content)

        result_json["success"] = SUCCESS
        result_json["msg"] = OK

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


@cont_check_new.route('/contract_check_detail_one', methods=['POST', 'GET'])
def admin_check_search():
    """
    合规性审查，生成审查信息
    :param filename:读入的文件路径名称
    :return:
    """
    result_json = copy.deepcopy(DEFAULT_RESULT_JSON)

    try:

        content = request.values.get('content')
        if not content:
            raise ValueError(ERROR_00)

        result_json["result"] = cont_check_get_sim_paragraphs_by_sentence(content)
        print("content:", result_json["result"])

        result_json["success"] = SUCCESS
        result_json["msg"] = OK

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


@cont_check_new.route('/download', methods=['POST', 'GET'])
def admin_check_download():
    """
    下载相似性的文档
    :return:
    """
    result_json = copy.deepcopy(DEFAULT_RESULT_JSON)
    try:
        filename = request.values.get('simDocumentsName')
        content = request.values.get('simDocumentContent')

        filename = filename + '.docx'

        get_content_by_filename(filename, content)

        fill_docx_name = join_path(Config.DOWNLOAD_PATH, filename)
        with open(fill_docx_name, 'rb') as f:
            file_bin_data = f.read()
        return file_bin_data

    except Exception as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
        return json.dumps(result_json)
