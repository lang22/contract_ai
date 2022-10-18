#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/22 11:29
@Author     : jzs
@File       : admin_flowtable.py
@Software   : PyCharm
@Description: ......
"""
import os
import shutil
import traceback

from docx import Document
from docx.shared import Pt
from flask import Blueprint, render_template, request, send_from_directory
from flask_login import login_required

from app.algorithm.flow_table_dump import dump_flow_table, dump_flow_table2
from .. import logger

flowtab = Blueprint('flowtab', __name__)  # 创建绑定蓝本


@flowtab.route('/admin_choosetable', methods=['POST', 'GET'])
def admin_choose_table():
    """
    选择合同流程表界面
    :return:
    """
    try:
        choose_list = request.values.getlist("cb")
        if not choose_list:
            return render_template("admin_choosetable.html")
        if "cd1" in choose_list and "cd2" in choose_list:
            return render_template("admin_docx.html")
        # 表1 合同面签记录表
        elif "cd1" in choose_list and "cd2" not in choose_list:
            return render_template("admin_docx1.html")
        # 表2 合同审查申请表
        elif "cd1" not in choose_list and "cd2" in choose_list:
            return render_template("admin_docx2.html")
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())

        return render_template("admin_choosetable.html")


@flowtab.route('/admin_docx', methods=['POST', 'GET'])
def admin_docx():
    return render_template("admin_docx.html")


@flowtab.route('/admin_docx4', methods=['POST', 'GET'])
def admin_docx4():
    """
    合同审核后的合同流程表----审查申请表 还包含面签记录表
    :return:
    """
    return render_template('admin_docx4.html')


@flowtab.route('/admin_docx1', methods=['POST', 'GET'])
def admin_docx1():
    """
    合同审核后的合同流程表----面签记录表
    :return:
    """
    return render_template('admin_docx1.html')


@flowtab.route('/admin_docx2', methods=['POST', 'GET'])
def admin_docx2():
    """
    合同审核后的合同流程表----审查申请表
    :return:
    """
    return render_template('admin_docx2.html')


# 保存保存保存保存合同面签记录表
@flowtab.route('/admin_docx1_save', methods=['POST', 'GET'])
def admin_docx1_save():
    """
    保存合同面签记录表
    :return:
    """
    try:
        if request.method == "POST":
            pt_name = request.values.get("pt_name")
            doc_date = request.values.get("doc_date")
            doc_loc = request.values.get("doc_loc")
            rows = list()
            for i in range(1, 7):
                name = request.values.get("name_" + str(i))
                cont = request.values.get("cont_" + str(i))
                othe = request.values.get("othe_" + str(i))
                rows.append((i, name, cont, othe))
            directory, filename = dump_flow_table(pt_name, doc_date, doc_loc, rows)
            return send_from_directory(directory=directory, filename=filename, as_attachment=True)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
    return render_template("admin_index.html")


# 保存保存保存保存合同审查申请表
@flowtab.route('/admin_docx2_save', methods=['POST', 'GET'])
def admin_docx2_save():
    try:
        if request.method == "POST":
            dp_name = request.values.get("dp_name")
            pt_name = request.values.get("pt_name")
            pt_cont = request.values.get("pt_cont")
            its = list()
            for i in range(4):
                it = (request.values.get("xh" + str(i)),
                      request.values.get("mc" + str(i)),
                      request.values.get("tgf" + str(i)),
                      request.values.get("wb" + str(i)),
                      request.values.get("xg" + str(i)),
                      request.values.get("yj" + str(i)),
                      request.values.get("sm" + str(i)),
                      request.values.get("qt" + str(i)))
                its.append(it)
            directory, filename = dump_flow_table2(dp_name, pt_name, pt_cont, its)
            return send_from_directory(directory=directory, filename=filename, as_attachment=True)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
    return render_template("admin_index.html")
