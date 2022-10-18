#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/20 15:25
@Author     : jzs
@File       : admin_sugg.py
@Software   : PyCharm
@Description: ......
"""

import random
import traceback
from datetime import datetime

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.models.sugg import Sugg
from app.models.user import User
from config import Config
from .. import logger

sugg = Blueprint('sugg', __name__)  # 创建绑定蓝本


@sugg.route('/admin_sugg', methods=['POST', 'GET'])
def admin_sugg():
    """
    意见反馈主页
    :return:
    """
    return render_template('admin_sugg.html')


@sugg.route('/admin_sugg_list', methods=['POST', 'GET'])
def admin_sugg_list():
    """
    查看意见列表
    :return:
    """
    try:
        if request.method == "GET":
            suggest_all = Sugg.get_suggest_all()
            return render_template('admin_sugginfo.html', suggest_all=suggest_all)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
    return render_template("admin_sugg.html")


@sugg.route('/admin_sugg_add', methods=['POST', 'GET'])
def admin_sugg_add():
    """
    添加意见
    :return:
    """
    try:
        if request.method == 'POST':
            suggest_text = request.form.get('demo')
            user_id = User.get_id(current_user)
            now_time = datetime.now().strftime("%Y%m%d%H%M%S")
            str_time = str(now_time)
            str_new = str_time[2:]
            sugg_id = int(str_new) + random.randint(0, 5)
            sugg_id = sugg_id - 180000000000
            new_sugg = Sugg(sugg_id=sugg_id, user_id=user_id, sugg_text=suggest_text)
            Sugg.add_sugg(new_sugg)
            suggest_all = Sugg.get_suggest_all()
            return render_template('admin_sugginfo.html', suggest_all=suggest_all)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
    return render_template('admin_sugg.html')


@sugg.route('/admin_suggdel', methods=['POST', 'GET'])
def admin_suggdel():
    """
    意见反馈删除
    :return:
    """
    try:
        if request.method == "POST":
            sugg_id = request.values.get("sugg_id")
            Sugg.del_sugg_by_sugg_id(sugg_id)
            suggest_all = Sugg.get_suggest_all()
            return render_template('admin_sugginfo.html', suggest_all=suggest_all)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
    return render_template("admin_sugg.html")
