#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/20 15:36
@Author     : jzs
@File       : loginlog.py
@Software   : PyCharm
@Description: ......
"""
import datetime
import random
import traceback

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.models.log import Log
from app.models.loguser import Log_User
from app.models.sugg import Sugg
from app.models.user import User
from config import Config
from .. import logger

log = Blueprint('log', __name__)  # 创建绑定蓝本gen


# 日志信息登录
@log.route('/admin_log_first', methods=['POST', 'GET'])
def admin_log_first():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            log_user = Log_User.query.filter_by(user_name=username, user_pass=password).one_or_none()
            if username == '':
                flash('请输入用户名')
                return render_template('admin_log_first.html')
            elif password == '':
                flash('请输入密码')
                return render_template('admin_log_first.html')
            elif log_user is not None:
                # login_user(log_user, remember=True)
                # identity_changed.send(current_app._get_current_object(), identity=Identity(log_user.user_id))
                # print('admin_log_first(): log_user is not None')
                return redirect(url_for('log.admin_loginlog'))
            else:
                flash('用户名或密码不正确')
                return render_template('admin_log_first.html')
    except Exception as e:
        logger.warning(traceback.format_exc())
        return render_template('login.html')

    return render_template('admin_log_first.html')


@log.route('/admin_mage', methods=['POST', 'GET'])
def admin_mage():
    """
    系统管理，账户设置
    :return:
    """
    return render_template('admin_mage.html')


@log.route('/admin_info', methods=['POST', 'GET'])
def admin_info():
    """
    系统信息
    :return:
    """
    return render_template('admin_info.html')


@log.route('/admin_loginlog', methods=['POST', 'GET'])
def admin_loginlog():
    """
    登录日志
    :return:

    """
    try:
        log_list = Log.get_all()
        length = len(log_list)
        return render_template('admin_loginlog.html', log_list=log_list, length=length)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return None
