#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/12 16:31
@Author     : jzs
@File       : sugg.py
@Software   : PyCharm
@Description: ......
"""

from . import db


class Sugg(db.Model):
    """
    意见反馈表
    """
    __tablename__ = 'sugg'
    sugg_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    sugg_text = db.Column(db.TEXT)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def add_sugg(sugg):
        """
        添加当前对象意见反馈到数据库
        :return:
        """
        try:
            db.session.add(sugg)
            db.session.commit()
        except BaseException as e:
            print(e)
            db.session.rollback()
            print('rollback')

    @staticmethod
    def del_sugg_by_sugg_id(sugg_id: str):
        """
        删除一个意见反馈，查找方式通过查询sugg_id
        :param sugg_id:
        :return:
        """
        try:
            db.session.query(Sugg).filter_by(sugg_id=sugg_id).delete()
            db.session.commit()
        except BaseException as e:
            print(e)
            db.session.rollback()
            print('rollback')

    @staticmethod
    def get_suggest_all():
        """
        从数据库中得到所有意见反馈
        :return:
        """
        return db.session.query(Sugg).all()
