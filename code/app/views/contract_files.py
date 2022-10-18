import copy
import json
import os
import traceback

from flask import Blueprint, request, render_template, send_from_directory
from flask_cors import cross_origin

from ..tools import doc_docx_tools, pre_docx
from config import Config
from ..tools import join_path
from ..tools.doc_docx_tools import snowflake, get_word_file_ext_name
from .. import logger

contract_files = Blueprint('contract_files', __name__)

SUCCESS = 1

NOT_SUCCESS = 0

OK = 'ok!'

ERROR = "error!"
ERROR_00: str = "error 00:Arg is None!"
ERROR_01 = "error 01:File Not Found ! "

DEFAULT_RESULT_JSON = {
    "success": NOT_SUCCESS,
    "msg": ERROR,
}


@contract_files.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
    return render_template("uploads_file_test.html")


@contract_files.route('/put_one_file', methods=['GET', 'POST'])
@cross_origin()
def put_one_file():
    """
    文件上传，并把合同转化成docx，去除

    测试命令
    curl -F "file=@test1.docx" -X POST "http://127.0.0.1:5000/contract_files/put_one_file"

    :return:
    """
    result_json = copy.deepcopy(DEFAULT_RESULT_JSON)
    docx_id = {'docxID': ''}
    try:

        # 这里改动以存储多份文件
        doc_file = request.files.getlist('file')[0]

        # 保存文件
        snowflake_filename, upload_path = doc_docx_tools.save_docx_return_path_and_name(
            doc_file, Config.UPLOADED_DIR_PATH)

        # 处理存在批注的情况
        pre_docx.multi_process([upload_path, ], Config.UPLOADED_DIR_PATH)

        print("上传的文件：", doc_file.filename, '\n',
              "保存的名字：", snowflake_filename, '\n',
              "保存的路径：", upload_path)

        docx_id['docxID'] = snowflake_filename

        result_json["success"] = SUCCESS
        result_json["msg"] = OK
        result_json["result"] = docx_id

    except Exception as e:
        logger.warning(traceback.format_exc())
        print(e, '\n', traceback.format_exc())
        result_json["msg"] = str(e)
    finally:
        return json.dumps(result_json)


@contract_files.route('/download_file_by_json1', methods=['POST', 'GET'])
def download_exam_result_docx_by_json1():
    """
    下载审核的文件，参数title，返回下载的文件流，
    http://127.0.0.1:5000/contract_files/download_file_by_json?title=合同文档1-50052325841581586742041.docx
    :return:
    """
    result_json = copy.deepcopy(DEFAULT_RESULT_JSON)

    try:
        # result = {"fileName": '', "binData": ''}

        docx_filename = request.values.get("title")

        if not docx_filename:
            raise ValueError(ERROR_00)

        fill_docx_name = join_path(Config.OTHER_DOWNLOAD_PATH, docx_filename)

        print('fill_docx_name:', fill_docx_name)

        if not os.path.exists(fill_docx_name):
            raise FileNotFoundError(ERROR_01 + docx_filename)

        print('download_directory_path：', Config.OTHER_DOWNLOAD_PATH)
        print('fill_docx_name：', fill_docx_name)

        with open(fill_docx_name, 'rb') as f:
            file_bin_data = f.read()
        return file_bin_data
        # result["fileName"] = docx_filename
        # result["binData"] = file_bin_data
        # result_json['msg'] = OK
        # result_json['result'] = result

    except Exception as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
        return json.dumps(result_json)


@contract_files.route('/download_file_by_json2', methods=['POST', 'GET'])
def download_exam_result_docx_by_json2():
    """
    下载审核的文件，参数title，返回下载的文件流，
    http://127.0.0.1:5000/contract_files/download_file_by_json?title=合同文档1-50052325841581586742041.docx
    :return:
    """
    result_json = copy.deepcopy(DEFAULT_RESULT_JSON)

    try:
        result = {"fileName": '', "binData": ''}

        docx_filename = request.values.get("title")

        if not docx_filename:
            raise ValueError(ERROR_00)

        fill_docx_name = join_path(Config.OTHER_DOWNLOAD_PATH, docx_filename)

        if not os.path.exists(fill_docx_name):
            raise FileNotFoundError(ERROR_01 + docx_filename)

        print('download_directory_path：', Config.OTHER_DOWNLOAD_PATH)
        print('fill_docx_name：', fill_docx_name)

        with open(fill_docx_name, 'rb') as f:
            file_bin_data = f.read()

        result["fileName"] = docx_filename
        result["binData"] = str(file_bin_data)
        result_json["success"] = SUCCESS
        result_json["msg"] = OK
        result_json['result'] = result

    except Exception as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
    finally:
        return json.dumps(result_json)
