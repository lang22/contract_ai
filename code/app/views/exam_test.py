#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/3/7 10:50
@Author     : jzs
@File       : exam_test.py
@Software   : PyCharm
@Description: ......
"""
import copy
import json
import os
import traceback

from flask import Blueprint, render_template, request, flash, session, send_from_directory
from flask_login import login_required

from ..models.cont_docx_backup_table import ContDocxBackupTable
from ..tools import pre_docx, doc_docx_tools

from cont_exam_new import download_result_docx
from .. import logger
from ..tools import join_path, random_fliename
from config import Config
from cont_exam_new import get_exam_result_by_html
from exam_clause import contract_clause_exam

exam_test = Blueprint('exam_test', __name__)

SESSION_KEY_OTHER_RESULT_DICT_KEY = "SESSION_KEY_OTHER_RESULT_DICT_KEY"
EXAM_RESULT_FILE_PATH1 = 'EXAM_RESULT_FILE_PATH1'
EXAM_RESULT_FILE_PATH2 = 'EXAM_RESULT_FILE_PATH2'
EXAM_RESULT_XLSX_FILE_PATH = 'EXAM_RESULT_XLSX_FILE_PATH'


@login_required
@exam_test.route('/', methods=['POST', 'GET'])
def index():
    return render_template('admin_index_test.html', url='admin_exam_docx_v2')


@exam_test.route('/admin_exam_docx_v2', methods=['POST', 'GET'])
def admin_exam_docx_v2():
    try:

        if request.method == 'GET':
            return render_template('admin_index_test.html', url='admin_exam_docx_v2')
        doc1 = request.files['file1']
        doc2 = request.files['file2']

        # 将flask request的文件数据流保存指指定目录，如果是doc文件则转换成docx文件。并返回保存后的路径
        upload_path1 = doc_docx_tools.save_docx(doc1, Config.UPLOADED_DIR_PATH)
        upload_path2 = doc_docx_tools.save_docx(doc2, Config.UPLOADED_DIR_PATH)

        # 处理存在批注的情况
        pre_docx.multi_process([upload_path1, upload_path2], Config.UPLOADED_DIR_PATH)

        # 保存到数据库
        ContDocxBackupTable.add_one(request.remote_addr, upload_path1)

        # 保存到数据库
        ContDocxBackupTable.add_one(request.remote_addr, upload_path2)

        model_html, test_html, file_path1, file_path2, xlsx_download_path \
            = get_exam_result_by_html(upload_path1, upload_path2)

        session[EXAM_RESULT_FILE_PATH1] = file_path1
        session[EXAM_RESULT_FILE_PATH2] = file_path2
        session[EXAM_RESULT_XLSX_FILE_PATH] = xlsx_download_path

        return render_template('admin_exam_test.html', model_html=model_html, test_html=test_html)
    except Exception as e:
        print(e)
        flash("服务器计算错误!")
        logger.warning(traceback.format_exc())
        return render_template('admin_index_test.html', url='admin_exam_docx_v2')


@exam_test.route('/download_exam_result_docx', methods=['POST', 'GET'])
def download_exam_result_docx():
    """
    下载审核的文件
    :return:
    """
    try:

        is_first = request.values.get('is_first')
        if is_first == 'is_first':
            file_path = session[EXAM_RESULT_FILE_PATH1]
        else:
            file_path = session[EXAM_RESULT_FILE_PATH2]

        args = file_path.split('/')
        download_directory_path = "/" + '/'.join(args[:-1])
        fill_docx_name = args[-1]

        print('download_directory_path', download_directory_path)
        print('fill_docx_name', fill_docx_name)

        return send_from_directory(directory=download_directory_path,
                                   filename=fill_docx_name,
                                   as_attachment=True)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return render_template('admin_index_test.html', url='admin_exam_docx_v2')


@exam_test.route('/download_exam_result_xlsx', methods=['POST', 'GET'])
def download_exam_result_xlsx():
    """
    下载审核后的xlsx的文件
    :return:
    """
    try:

        xlsx_download_path = session[EXAM_RESULT_XLSX_FILE_PATH]

        args = xlsx_download_path.split('/')
        download_directory_path = "/" + '/'.join(args[:-1])
        fill_docx_name = args[-1]

        print('download_directory_path', download_directory_path)
        print('fill_docx_name', fill_docx_name)

        return send_from_directory(directory=download_directory_path,
                                   filename=fill_docx_name,
                                   as_attachment=True)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return render_template('admin_index_test.html', url='admin_exam_docx_v2')


@exam_test.route('/admin_exam_docx_v1', methods=['POST', 'GET'])
def admin_exam_docx_v1():
    try:
        if request.method == 'GET':
            return render_template('admin_index_test.html', url='admin_exam_docx_v1')

        doc1 = request.files['file1']
        doc2 = request.files['file2']

        filename = random_fliename()
        upload_path1 = join_path(Config.UPLOADED_DIR_PATH, filename + '.docx')
        doc1.save(upload_path1)

        filename = random_fliename()
        upload_path2 = join_path(Config.UPLOADED_DIR_PATH, filename + '.docx')
        doc2.save(upload_path2)

        model_html, test_html, _ = contract_clause_exam(upload_path1, upload_path2)

        return render_template('admin_exam_test.html', model_html=model_html, test_html=test_html)
    except Exception as e:
        print(e)
        flash("服务器计算错误!")
        logger.warning(traceback.format_exc())
        return render_template('admin_index_test.html', url='admin_exam_docx_v1')


# ----------------------------------------------------------------------------------------------------------------------
# 接口化代码

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


@exam_test.route('/admin_exam_docx_by_json', methods=['POST', 'GET'])
def admin_exam_docx_by_json():
    """
    用于前后端分离的对比审核接口

    访问参数
    参数名字	                中文名	                            不可为空	    类型	长度	备注
    firstDocxID	    版本v1文档的id	        Y	        String	不限制	——
    secondDocxID	版本v2文档的id	        Y	        String	不限制	——

    返回字段	        字段类型	    说明
    success	        boolean	    成功/失败标志
                                    1：成功
                                    0：失败
    msg	            String	    错误信息：
                                    OK：文档是否成功接收并处理
                                    Error00：参数1或参数2为空
                                    Error01：文档1或文档2不存在
                                    Error02：文档1或文档2格式错误
                                    Error03：文档1或文档2解析错误
    result：        dict       包括如下
        firstHTMLCode	       String	      模板文档标注的html代码的字符串
        secondHTMLCode	       String	      待审核文档标注html代码的字符串
        downloadFirstDocxID    String         模板文档标注docx文件的ID
        downloadSecondDocxID   String         待审核文档标注docx文件的ID
        downloadExcelID        String         差异的Excel表的ID

    测试命令：curl \
        -F "firstDocxID=51939370961581583211687.docx" \
        -F "secondDocxID=51940220241581583219041.docx" \
        -X POST "http://127.0.0.1:5000/exam_test/admin_exam_docx_by_json" > data.json
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

        # 前端传来的是'["xxxxxx.docx", "xxxxxx.docx"]'
        print(request.get_data(as_text=True))

        # 获取前端POST请求传过来的 json 数据
        data = json.loads(request.get_data(as_text=True))
        print(data)
        if not data:
            raise ValueError(ERROR_00)

        firstDocxID = data[0]  # firstDocxID = request.values.get('firstDocxID')
        secondDocxID = data[1]  # secondDocxID = request.values.get('secondDocxID')

        print('firstDocxID:', firstDocxID, "secondDocxID:", secondDocxID)

        if not firstDocxID or not secondDocxID:
            raise ValueError(ERROR_01)

        upload_path1 = join_path(Config.UPLOADED_DIR_PATH, firstDocxID)
        upload_path2 = join_path(Config.UPLOADED_DIR_PATH, secondDocxID)

        print("upload_path1:", upload_path1)
        print("upload_path2:", upload_path1)

        if not os.path.exists(upload_path1) or not os.path.exists(upload_path2):
            raise FileNotFoundError(ERROR_01)

        # 保存到数据库
        ContDocxBackupTable.add_one(request.remote_addr, upload_path1)
        ContDocxBackupTable.add_one(request.remote_addr, upload_path2)

        model_html, test_html, file_path1, file_path2, xlsx_download_path \
            = get_exam_result_by_html(upload_path1, upload_path2)

        # session[EXAM_RESULT_FILE_PATH1] = file_path1
        # session[EXAM_RESULT_FILE_PATH2] = file_path2
        # session[EXAM_RESULT_XLSX_FILE_PATH] = xlsx_download_path

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
