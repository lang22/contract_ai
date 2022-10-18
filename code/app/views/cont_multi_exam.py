#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019-05-09 10:11
@Author     : charles
@File       : cont_multi_exam.py
@Software   : PyCharm
@Description: ......
"""
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

multi_exam = Blueprint('multi_exam', __name__)


# FILE_NAME_LIST = 'FILE_NAME_LIST'
# FILE_PATH_LIST = 'FILE_PATH_LIST'


@multi_exam.route('/', methods=['POST', 'GET'])
def admin_index():
    """
        基础路由，直接返回上传文件页面
        :return:
        """

    return render_template('admin_multi_exam_index.html')


@multi_exam.route('/admin_multi_upload', methods=['POST', 'GET'])
def upload_file():
    """
    获取上传的多个文件，将文件名称保存下来并传参，上传的文档保存下来进行要素抽取
    :return:
    """
    try:
        if request.method == 'POST':
            upload_files = request.files.getlist('file')

            file_path_list = []
            for file in upload_files:
                upload_path = doc_docx_tools.save_docx(file, Config.UPLOADED_DIR_PATH)
                file_path_list.append(upload_path)

            # # 多文件雪花路径list
            # session[FILE_NAME_LIST] = [item.filename for item in upload_files]
            #
            # # 多文件名list
            # session[FILE_PATH_LIST] = file_path_list
        # 多文件雪花路径list
        contract_name_list = [item.filename for item in upload_files]

        # 多文件名list
        upload_file_path_list = file_path_list

        print(upload_file_path_list)
        print(contract_name_list)

        # 将文档预处理，将可能存在的批注内容变成正常文本
        multi_process(upload_file_path_list, Config.UPLOADED_DIR_PATH)

        # upload_paths = [join_path(Config.CONT_MULTI_EXAM_PATH, file) for file in filenames]

        # 将合同保存到数据库
        for file_path in upload_file_path_list:
            ContDocxBackupTable.add_one(request.remote_addr, file_path)

        content_dict_dic, elem_lis = multi_extracting(contract_name_list, upload_file_path_list)

        elem_color_dic = set_color(content_dict_dic, elem_lis)

        # 传入前端的参数，需要有，文件名列表、每个文件对应的要素-内容列表（此处要素数保持一致，不存在写空）

        return render_template('admin_multi_exam_result.html',
                               filenames=contract_name_list,
                               elem_lis=elem_lis,
                               content_dict_dic=content_dict_dic,
                               elem_color_dic=elem_color_dic)
    except Exception as e:
        flash("服务器可能不支持该文档内容！")
        print(e)
        logger.warning(traceback.format_exc())
        return redirect(url_for('multi_exam.admin_index'))
