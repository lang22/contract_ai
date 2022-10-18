#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author     : jzs
@File       : cont_comparison_backup_table.py
@Software   : PyCharm
@Description: ......
"""
from docx import Document

from . import db
from datetime import datetime
from app.tools.aes import Prpcrypt
from config import Config


class ContDocxBackupTable(db.Model):
    """
    合同对比审核存档表
    """
    __tablename__ = "cont_docx_backup_table"
    obj_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime)

    request_ip = db.Column(db.VARCHAR(100))

    docx_content = db.Column(db.TEXT)

    backup1 = db.Column(db.TEXT)
    backup2 = db.Column(db.TEXT)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def add_one(
            request_ip: str,
            docx_path: str
    ):
        """
        添加一个合同存档

        :param request_ip: 请求IP
        :param docx_path:文档的路径
        :return:
        """
        aes = Prpcrypt(Config.DB_STR_AES_KEY)
        document = Document(docx_path)

        content = '\n'.join(para.text for para in list(document.paragraphs))

        cm = ContDocxBackupTable(
            add_time=str(datetime.now()),
            request_ip=aes.encrypt(request_ip),
            docx_content=aes.encrypt(content),
        )
        db.session.add(cm)
        db.session.commit()
