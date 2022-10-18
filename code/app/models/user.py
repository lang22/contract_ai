#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/10 21:04
@Author     : jzs
@File       : user.py
@Software   : PyCharm
@Description: 用户模型
"""
from flask_login import UserMixin

from . import db
from . import login_manager


class User(UserMixin, db.Model):
    """
    用户类模型
    """
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.VARCHAR(100))
    user_pass = db.Column(db.VARCHAR(100))
    user_email = db.Column(db.VARCHAR(100))
    user_depat = db.Column(db.VARCHAR(100))
    user_auth = db.Column(db.VARCHAR(100))

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def is_authenticated(self):
        if isinstance(self, UserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, UserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.user_id

    @staticmethod
    def get_one_user(user_name: str, user_pass: str):
        """
        查询一个用户

        :param user_name: 用户名
        :param user_pass: 密码
        :return:
        """
        return User.query.filter_by(user_name=user_name, user_pass=user_pass).one_or_none()


@login_manager.user_loader
def load_user(user_id: str):
    """
    加载用户的回调函数

    :param user_id:  用户ID
    :return:
    """
    return User.query.get(int(user_id))
