#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/12 16:07
@Author     : jzs
@File       : log.py
@Software   : PyCharm
@Description: ......
"""
from . import db


class Log(db.Model):
    """
    登陆日志
    """
    __tablename__ = 'log'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    log_time = db.Column(db.DateTime)
    log_loc = db.Column(db.VARCHAR(500))
    log_ip = db.Column(db.VARCHAR(500))
    log_brow = db.Column(db.VARCHAR(500))

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def add_Log(user_id, log_time, log_ip, log_loc, log_brow):
        try:
            d = Log(user_id=user_id, log_time=log_time,
                    log_ip=log_ip,
                    log_loc=log_loc, log_brow=log_brow)
            db.session.add(d)
            db.session.commit()
        except BaseException as e:
            print(e)
            db.session.rollback()
            print('rollback')

    @staticmethod
    def get_all():
        sql = 'select * from log;'
        log = db.session.execute(sql)
        log_list = []
        for l in log:
            log_list.append(l)
        return log_list
