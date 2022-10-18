#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/20 15:46
@Author     : jzs
@File       : loguser.py
@Software   : PyCharm
@Description: ......
"""
from flask_login import AnonymousUserMixin
from . import db


class Log_User(db.Model):
    __tablename__ = "log_user"
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
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.user_id
