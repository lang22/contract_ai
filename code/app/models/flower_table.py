#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/3/15 11:11
@Author     : lsy
@File       : flower_table .py
@Software   : PyCharm
@Description: ......
"""

from . import db


class Flower(db.Model):
    """
    送花点击功能
    """
    __tablename__ = 'flower'
    elem_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cont_name = db.Column(db.Text)
    para_content = db.Column(db.Text)
    sim_cont_name = db.Column(db.Text)
    user_id = db.Column(db.Integer)
    upload_time = db.Column(db.Date)
    sims_content = db.Column(db.TEXT)
    backup1 = db.Column(db.TEXT)
    backup2 = db.Column(db.TEXT)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def add(cont_name: str, para_content: str, sim_cont_name: str, user_id: int, upload_time: str, sims_content: str):
        """

        :param elem_id:
        :param cont_name:
        :param sim_cont_name:
        :param user_id:
        :param upload_time:
        :param sims_content:
        :return:
        """
        try:
            flo = Flower(cont_name=cont_name, para_content=para_content, sim_cont_name=sim_cont_name,
                         user_id=user_id, upload_time=upload_time, sims_content=
                         sims_content)
            db.session.add(flo)
            db.session.commit()
        except BaseException as e:
            print(e)
            db.session.rollback()
            print('rollback')

    @staticmethod
    def get_item_by_para_content(para_content: str):
        """
        返回para_content被点赞的相似信息
        :param para_content:
        :return:
        """

        return Flower.query.filter_by(para_content=para_content).all()