#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/10 14:05
@Author     : jzs
@File       : index.py
@Software   : PyCharm
@Description: 主目录路由
"""

from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for
from flask_login import login_required, login_user

# 初始化蓝图命名空间index_bp
from flask_principal import identity_changed, Identity

from app import db
from app.models.cont_gen_element_table import ContGenElementTable
from app.models.contract_gen_table import ContractGenTable
from app.models.user import User

from app.models.contract_ext_table import ContractExtTable

main = Blueprint('main', __name__)


@login_required
@main.route('/')
def index():
    # todo 2019.1.25 修改为跳转到审核主页，并把所以的@login_required注解删除

    # db.create_all()
    return redirect(url_for('main.pagecs'))


@login_required
@main.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_one_user(username, password)
        if username == '':
            flash('请输入用户名')
            return render_template('login.html')
        elif password == '':
            flash('请输入密码')
            return render_template('login.html')
        elif user is not None:
            login_user(user, remember=True)
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.user_id))
            return redirect(url_for('main.pagecs'))
        else:
            flash('用户名或密码不正确')
            return render_template('login.html')


# 日志信息登录
@main.route('/admin_log_first', methods=['POST', 'GET'])
def admin_log_first():
    """
    日志信息登录
    :return:
    """
    pass


@main.route('/pagecs', methods=['POST', 'GET'])
def pagecs():
    """
    合同页面选择
    :return:
    """
    contracts = ContractExtTable.select_all()
    category = ContractExtTable.get_cont_category_all(contracts)
    return render_template('admin_index_test.html', url='admin_exam_docx_v2', categorys=category)


@main.route('/admin_index', methods=['POST', 'GET'])
def admin_index():
    """
    后台首页
    :return:
    """
    return render_template('pagechoose.html')


@main.route('/create_all_db', methods=['POST', 'GET'])
def create_all_db():
    """
    创建数据库表

    :return:
    """
    create_all_db_flag = request.values.get('create_all_db_flag')
    if create_all_db_flag and create_all_db_flag == 'true':
        db.create_all()
        return 'ok!'
    else:
        return 'no!'
