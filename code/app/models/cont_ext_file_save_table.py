#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019-03-15 11:12
@Author     : charles
@File       : cont_ext_file_save_table.py
@Software   : PyCharm
@Description: ......
"""

from . import db


class ContExtFileTable(db.Model):
        """
        合同审核文档保存表 此功能一次上传两个文档，两个文档用一条保存下来
        """

        __tablename__ = 'cont_ext_file_save_table'
        elem_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

        cont_name1 = db.Column(db.Text)
        cont_name2 = db.Column(db.Text)

        cont_content1 = db.Column(db.Text)
        cont_content2 = db.Column(db.Text)

        user_id = db.Column(db.Integer)
        upload_time = db.Column(db.DATE)

        backup1 = db.Column(db.Text)
        backup2 = db.Column(db.Text)

        def __init__(self, **kwargs):

            for key, value in kwargs.items():
                setattr(self, key, value)

        @staticmethod
        def add_one(cont_name1: str,
                    cont_name2: str,
                    upload_time: str,
                    cont_content1: str,
                    cont_content2: str,
                    user_id = 1,
                    backup1='',
                    backup2=''
                    ):
            """
            增加一条审核记录 包含两个上传文档的相关信息
            :param cont_name1:
            :param cont_name2:
            :param upload_time:
            :param cont_content1:
            :param cont_content2:
            :param user_id:
            :param backup1:
            :param backup2:
            :return:
            """
            cm = ContExtFileTable(
                cont_name1=cont_name1,
                cont_name2=cont_name2,
                upload_time=upload_time,
                cont_content1=cont_content1,
                cont_content2=cont_content2,
                user_id=user_id,
                backup1=backup1,
                backup2=backup2
            )
            db.session.add(cm)
            db.session.commit()

        @staticmethod
        def get_elements(elem_id):
            """
            得到第elem_id条审核记录，获取两篇文档信息
            :param conid:
            :return:
            """
            return ContExtFileTable.query.filter_by(elem_id=elem_id).all()

        @staticmethod
        def create_table():
            table_name = ContExtFileTable.__tablename__
            structs = [
                {'fieldname': 'elem_id', 'type': 'Integer', 'primary': True, 'default': ''},
                {'fieldname': 'cont_name1', 'type': 'Text', 'default': '', 'isnull': True},
                {'fieldname': 'cont_name2', 'type': 'Text', 'default': '', 'isnull': True},
                {'fieldname': 'cont_content1', 'type': 'Text', 'default': '', 'isnull': True},
                {'fieldname': 'cont_content2', 'type': 'Text', 'default': '', 'isnull': True},
                {'fieldname': 'user_id', 'type': 'Integer', 'default': 0, 'isnull': True},
                {'fieldname': 'upload_time', 'type': 'Date', 'default': '', 'isnull': True},
                {'fieldname': 'backup1', 'type': 'Text', 'default': '', 'isnull': True},
                {'fieldname': 'backup2', 'type': 'Text', 'default': '', 'isnull': True},
            ]
            db.create_table(table_name, structs)


