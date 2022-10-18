#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019-03-15 09:12
@Author     : charles
@File       : cont_check_table.py
@Software   : PyCharm
@Description: ......
"""
import time
from docx import Document

from app.tools.aes import Prpcrypt
from config import Config
from . import db


class ContCheckTable(db.Model):
    """
    合同合规性审核合同保存表
    """

    __tablename__ = 'cont_check_table'
    elem_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cont_name = db.Column(db.Text)
    user_id = db.Column(db.Integer)
    upload_time = db.Column(db.DATE)
    cont_content = db.Column(db.Text)
    backup = db.Column(db.Text)

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def add_one(cont_name: str,
                upload_time: str,
                cont_content: str,
                user_id=1,
                backup=''):
        """
        添加一个上传合同记录
        :param elem_id:
        :param cont_name:
        :param user_id: 默认为1 即admin用户
        :param upload_time:
        :param cont_content:
        :param backup: 备注选项，默认为空
        :return:
        """
        cm = ContCheckTable(
            cont_name=cont_name,
            upload_time=upload_time,
            cont_content=cont_content,
            user_id=user_id,
            backup=backup
        )
        db.session.add(cm)
        db.session.commit()

    @staticmethod
    def get_elements(cont_name):
        """
        得到合同名为cont_name为conid的合同记录
        :param conid:
        :return:
        """
        return ContCheckTable.query.filter_by(cont_name=cont_name).all()

    @staticmethod
    def create_table():
        table_name = ContCheckTable.__tablename__
        structs = [
            {'fieldname': 'elem_id', 'type': 'Integer', 'primary': True, 'default': ''},
            {'fieldname': 'cont_name', 'type': 'Text', 'default': '', 'isnull': True},
            {'fieldname': 'user_id', 'type': 'Integer', 'default': 0, 'isnull': True},
            {'fieldname': 'upload_time', 'type': 'Date', 'default': '', 'isnull': True},
            {'fieldname': 'cont_content', 'type': 'Text', 'default': '', 'isnull': True},
            {'fieldname': 'backup', 'type': 'Text', 'default': '', 'isnull': True},
        ]
        db.create_table(table_name, structs)
