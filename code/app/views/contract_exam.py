#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/23 11:30
@Author     : jzs
@File       : contract_exam.py
@Software   : PyCharm
@Description: ......
"""
import json
import traceback

from flask import Blueprint, request, flash, render_template, redirect, url_for, session, send_from_directory

from ..tools import doc_docx_tools
from ..models.cont_docx_backup_table import ContDocxBackupTable
from ..tools import pre_docx

from app import logger
from app.algorithm.amount_exam import check_amount_difference
from app.models.cont_ext_element_table import ContExtElementTable
from app.models.cont_ext_result import ConExtResult
from app.models.contract_ext_table import ContractExtTable
from app.tools import random_fliename, join_path
from cont_exam_new import get_exam_result_by_html2

from config import Config
from elem_extract import extracting

# 创建绑定蓝本gen
from exam_clause import contract_clause_exam, get_test_html_highlight_dict, highlight_docx
from flask_login import login_required

exam = Blueprint('exam', __name__)

# 合同要素抽取后的字典（list)的session的键
SESSION_KEY_OUTPUT_ELEMENTS = "SESSION_KEY_OUTPUT_ELEMENTS"
SESSION_KEY_CONT_ID = 'SESSION_KEY_CONT_ID'

# 待审核文档路径
SESSION_KEY_TEST_DOCX_PATH = "SESSION_KEY_TEST_DOCX_PATH"

# 模板文档路径
SESSION_KEY_MODEL_DOCX_PATH = 'SESSION_KEY_MODEL_DOCX_PATH'

# 待审核文档span的id-标注颜色
SESSION_KEY_TEST_HIGHLIGHT_DICT = 'SESSION_KEY_TEST_HIGHLIGHT_DICT'

# 模板文档span的id-标注颜色
SESSION_KEY_MODEL_HIGHLIGHT_DICT = 'SESSION_KEY_MODEL_HIGHLIGHT_DICT'

# 合同标题审核结果
SESSION_KEY_CLAUSE_TITLE = "SESSION_KEY_CLAUSE_TITLE"

# 合同金额审核结果
SESSION_KEY_CHECK_RES_DICT = "SESSION_KEY_CHECK_RES_DICT"

SESSION_KEY_EXAM_RESULT_FILE_PATH1 = 'SESSION_KEY_EXAM_RESULT_FILE_PATH1'

SESSION_KEY_EXAM_RESULT_FILE_PATH2 = 'SESSION_KEY_EXAM_RESULT_FILE_PATH2'


@exam.route('/', methods=['POST', 'GET'])
def admin_exam_index():
    contracts = ContractExtTable.select_all()
    category = ContractExtTable.get_cont_category_all(contracts)
    return render_template('admin_index.html', categorys=category)


@exam.route('/choose_contract', methods=['POST', 'GET'])
def choose_contract():
    """
    根据参数，选择合同模板，返回合同模板json字符串
    :return:
    """
    try:
        all_contracts = ContractExtTable.select_all()
        value = request.values.get('value')
        contracts = list(filter(lambda x: x.cont_category == value, all_contracts))
        if value:
            result = dict()
            result['conLen'] = len(contracts)
            result['conPid'] = [cont.cont_id for cont in contracts]
            result['conNames'] = [cont.cont_name for cont in contracts]
            result['conContent'] = dict((cont.cont_id, cont.cont_info) for cont in contracts)

            return json.dumps(result)
        else:
            return ''
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return ''


@exam.route('/admin_exam', methods=['POST', 'GET'])
def admin_exam():
    """
    合同审核，上传合同文档，将文档保存到 static/kuploads 文件夹下
    :return:
    """
    try:
        if request.method == 'POST':
            up_file = request.files['file']
            cont_id = request.values.get('xz_ejfl')

            # 暂存合同模板ID
            session[SESSION_KEY_CONT_ID] = int(cont_id)

            # filename = random_fliename()
            # upload_path = join_path(Config.UPLOADED_DIR_PATH, filename)
            # up_file.save(upload_path)

            upload_path = doc_docx_tools.save_docx(up_file, Config.UPLOADED_DIR_PATH)

            return redirect(url_for('exam.admin_examdoc', filename=upload_path.split('/')[-1]))
    except Exception as e:
        flash("请上传后缀为.docx的文件”")
        print(e)
        logger.warning(traceback.format_exc())
        return redirect(url_for('exam.admin_exam_index'))


@exam.route('/admin_exam/<string:filename>', methods=['POST', 'GET'])
def admin_examdoc(filename):
    """
    合同审核后的内容 形式化审核 审核信息 合同流程表
    :param filename:
    :return:
    """
    try:
        # 读取上传后的docx文档，并保存文档的路径
        upload_path_userup = join_path(Config.UPLOADED_DIR_PATH, filename)

        # 处理存在批注的情况
        pre_docx.multi_process([upload_path_userup], Config.UPLOADED_DIR_PATH)

        # 保存到数据库
        ContDocxBackupTable.add_one(request.remote_addr, upload_path_userup)

        session[SESSION_KEY_TEST_DOCX_PATH] = upload_path_userup

        cont_id = session[SESSION_KEY_CONT_ID]  # 获取合同ID
        elem_id_dict, elem_key_dict, elem_type_dict = ContExtElementTable.get_elements_dict(cont_id)  # 读取要素列表

        # 要素抽取
        elem_content_dic = extracting(upload_path_userup, elem_id_dict, elem_key_dict, elem_type_dict)
        session[SESSION_KEY_OUTPUT_ELEMENTS] = elem_content_dic  # 保存session

        # 加密并保存到数据库
        result_dict = ConExtResult.to_aes_result_dict(elem_id_dict, elem_content_dic)
        ConExtResult.add_all(cont_id, filename, result_dict)

        # 合同金额审核
        check_res_dict = check_amount_difference(elem_type_dict, elem_content_dic)
        session[SESSION_KEY_CHECK_RES_DICT] = check_res_dict

        # 合同模板的路径，并保存
        model_path = join_path(Config.CONT_GENA_TEMPLATE_DIR_PATH,
                               ContractExtTable.select_one(cont_id).cont_path + '.docx')
        session[SESSION_KEY_MODEL_DOCX_PATH] = model_path

        # 合同的条款审核
        _, _, clause_title = contract_clause_exam(model_path, upload_path_userup)

        # 合同的条款审核
        # model_html, test_html, clause_title = contract_clause_exam(model_path, upload_path_userup)
        model_html, test_html, file_path1, file_path2 \
            = get_exam_result_by_html2(model_path, upload_path_userup)

        session[SESSION_KEY_EXAM_RESULT_FILE_PATH1] = file_path1
        session[SESSION_KEY_EXAM_RESULT_FILE_PATH2] = file_path2

        # 保持合同标题审核结果
        session[SESSION_KEY_CLAUSE_TITLE] = clause_title

        # 保存模板文档的id-标注颜色字典
        highlight_dict = get_test_html_highlight_dict(model_html)
        session[SESSION_KEY_TEST_HIGHLIGHT_DICT] = highlight_dict

        # 保存待审核文档的id-标注颜色字典
        highlight_dict = get_test_html_highlight_dict(test_html)
        session[SESSION_KEY_MODEL_HIGHLIGHT_DICT] = highlight_dict

        # if os.path.exists(upload_path_userup):
        #     os.remove(u;pload_path_userup)

        return render_template('admin_exam.html',
                               model_html=model_html,
                               test_html=test_html,
                               )
    except Exception as e:
        print(e)
        flash("服务器计算错误!")
        logger.warning(traceback.format_exc())
        return redirect(url_for('exam.admin_exam_index'))


@exam.route('/download_exam_result_docx', methods=['POST', 'GET'])
def download_exam_result_docx():
    """
    下载审核的文件
    :return:
    """
    try:

        is_first = request.values.get('download_input')
        if is_first == 'is_first':
            file_path = session[SESSION_KEY_EXAM_RESULT_FILE_PATH1]
        else:
            file_path = session[SESSION_KEY_EXAM_RESULT_FILE_PATH2]

        import os
        (download_directory_path, fill_docx_name) = os.path.split(file_path)

        # args = file_path.split('/')
        # download_directory_path = "/" + '/'.join(args[:-1])
        # fill_docx_name = args[-1]

        print('download_directory_path', download_directory_path)
        print('fill_docx_name', fill_docx_name)

        return send_from_directory(directory=download_directory_path,
                                   filename=fill_docx_name,
                                   as_attachment=True)
    except Exception as e:
        print(e)
        flash("服务器计算错误!")
        logger.warning(traceback.format_exc())
        return redirect(url_for('exam.admin_exam_index'))


@exam.route('/admin_examdocx_next', methods=['POST', 'GET'])
def admin_examdocx_next():
    """
    合同审核后的要素表
    :return:
    """
    try:

        clause_title = session[SESSION_KEY_CLAUSE_TITLE]

        check_res_dict = session[SESSION_KEY_CHECK_RES_DICT]

        elem_content_dic = session[SESSION_KEY_OUTPUT_ELEMENTS]

        print("clause_title:", clause_title)
        print("check_res_dict:", check_res_dict)
        print("elem_content_dic:", elem_content_dic)

        clause_title = [('第一条', '定义', 1, '<span class="no_difference">一致</span>', '通过', 0),
                        ('第二条', '债权的转让', 1, '<span class="no_difference">一致</span>', '通过', 1),
                        ('第三条', '双方的陈述', 3, '<span class="difference">不一致</span>', '与第3条相似', 2),
                        ('第四条', '债权文件的交割', 1, '<span class="no_difference">一致</span>', '通过', 3),
                        ('第五条', '过渡期安排', 1, '<span class="no_difference">一致</span>', '通过', 4),
                        ('第六条', '合作', 1, '<span class="no_difference">一致</span>', '通过', 5),
                        ('第七条', '通知与送达', 1, '<span class="no_difference">一致</span>', '通过', 6),
                        ('第八条', '声明和保证', 3, '<span class="difference">不一致</span>', '与第3条相似', 2),
                        ('★第九条', '合作不是', 3, '<span class="difference">不一致</span>', '与第6条相似', 5),
                        ('第九条', '其他规定', 2, '<span class="difference">不一致</span>', '对应第8条', 7)]

        return render_template('admin_examdocx_next.html',
                               clause_title=clause_title,
                               elem_content_dic=elem_content_dic,
                               check_res_dict=check_res_dict)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return render_template("admin_index.html")


@exam.route('/admin_examdocx_ys', methods=['POST', 'GET'])
def admin_examdocx_ys():
    """
    合同审核后的要素表
    :return:
    """
    try:
        cont_id = session[SESSION_KEY_CONT_ID]
        elem_content_dic = session[SESSION_KEY_OUTPUT_ELEMENTS]

        elem_id_dict, elem_key_dict, elem_type_dict = ContExtElementTable.get_elements_dict(cont_id)  # 读取要素列表

        # 按要素ID排序，得到tuple列表
        elem_id_list = sorted(elem_id_dict.items(), key=lambda d: d[1], reverse=False)
        return render_template('admin_exam_ys.html',
                               elem_id_list=elem_id_list,
                               elem_type_dict=elem_type_dict,
                               elem_content_dic=elem_content_dic)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return render_template("admin_index.html")


@exam.route('/admin_download', methods=['POST', 'GET'])
def admin_download():
    """
    下载确认后的待审核合同

    :return:
    """
    try:
        span_del_list: str = request.values.get('download_input')
        span_del_list = [d for d in span_del_list.split(' ') if d]

        # 读取合同标题审核结果
        clause_title = session[SESSION_KEY_CLAUSE_TITLE]

        # 读取模板文档的id-标注颜色字典
        model_highlight_dict = session[SESSION_KEY_TEST_HIGHLIGHT_DICT]

        # 读取待审核文档的id-标注颜色字典
        test_highlight_dict = session[SESSION_KEY_MODEL_HIGHLIGHT_DICT]

        model_docx_path = session[SESSION_KEY_MODEL_DOCX_PATH]
        test_docx_pat = session[SESSION_KEY_TEST_DOCX_PATH]

        template_path, fill_docx_name = highlight_docx(
            model_docx_path=model_docx_path,
            test_docx_path=test_docx_pat,
            model_span_dict=model_highlight_dict,
            test_span_dict=test_highlight_dict,
            span_del_list=span_del_list,
            clause_title=clause_title
        )

        return send_from_directory(directory=template_path,
                                   filename=fill_docx_name,
                                   as_attachment=True)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return render_template("admin_index.html")


@exam.route('/elem_extract', methods=['POST', 'GET'])
def admin_elem_extract_index():
    contracts = ContractExtTable.select_all()
    category = ContractExtTable.get_cont_category_all(contracts)
    return render_template('admin_index_elem_extrac.html', categorys=category)


@exam.route('/elem_extracting_run', methods=['POST', 'GET'])
def admin_elem_extracting():
    """
    运行要素抽取，并输出到HTML中的table中
    :return:
    """
    try:
        # 读取上传后的docx文档，并保存文档的路径
        up_file = request.files['file']
        cont_id = request.values.get('xz_ejfl')

        filename = random_fliename()
        upload_path_userup = join_path(Config.UPLOADED_DIR_PATH, filename + ".docx")
        up_file.save(upload_path_userup)

        # 处理存在批注的情况
        pre_docx.multi_process([upload_path_userup], Config.UPLOADED_DIR_PATH)

        # 保存到数据库
        ContDocxBackupTable.add_one(request.remote_addr, upload_path_userup)

        elem_id_dict, elem_key_dict, elem_type_dict = ContExtElementTable.get_elements_dict(cont_id)  # 读取要素列表

        # 要素抽取
        elem_content_dic = extracting(upload_path_userup, elem_id_dict, elem_key_dict, elem_type_dict)
        session[SESSION_KEY_OUTPUT_ELEMENTS] = elem_content_dic  # 保存session

        # 加密并保存到数据库
        result_dict = ConExtResult.to_aes_result_dict(elem_id_dict, elem_content_dic)
        ConExtResult.add_all(cont_id, filename, result_dict)

        # 按要素ID排序，得到tuple列表
        elem_id_list = sorted(elem_id_dict.items(), key=lambda d: d[1], reverse=False)
        return render_template('admin_exam_ys.html',
                               elem_id_list=elem_id_list,
                               elem_type_dict=elem_type_dict,
                               elem_content_dic=elem_content_dic)
    except Exception as e:
        flash("服务器计算错误!")
        print(e)
        logger.warning(traceback.format_exc())
        return redirect(url_for('exam.admin_elem_extract_index'))
