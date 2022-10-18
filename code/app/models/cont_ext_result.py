#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/12 17:22
@Author     : jzs
@File       : cont_ext_result.py
@Software   : PyCharm
@Description: ......
"""
from datetime import datetime
from app.tools.aes import Prpcrypt
from config import Config
from . import db


class ConExtResult(db.Model):
    """
    合同抽取结果
    """
    __tablename__ = "cont_ext_result"
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime)
    elem_id = db.Column(db.Integer)
    con_id = db.Column(db.Integer)
    context = db.Column(db.TEXT)
    doc_name = db.Column(db.TEXT)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def add_all(con_id: int, doc_name: str, result_dict: 'dict[int ,str]'):
        """
        添加多个合同的抽取结果

        :param con_id: 合同ID
        :param doc_name:  合同文档名字
        :param result_dict: 加密后的抽取结果
        :return:
        """
        try:
            now = str(datetime.now())
            all = [ConExtResult(elem_id=key,
                                add_time=now,
                                doc_name=doc_name,
                                con_id=con_id,
                                context=result_dict[key])
                   for key in result_dict.keys()]
            db.session.add_all(all)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    @staticmethod
    def to_aes_result_dict(elem_id_dict: 'dict[str,int]',
                           elem_content_dic: 'dict[str,str]') -> 'dict[int ,str]':
        """
        将要素-要素id字典转换成要素-要素内容字典，并将要素内容使用AES加密

        :param elem_id_dict:  要素-要素id字典
        :param elem_content_dic:  要素-要素内容字典
        :return: 要素id-要素内容字典
        """
        ase = Prpcrypt(Config.DB_STR_AES_KEY)
        result_dict = dict()
        for key in elem_id_dict.keys():
            content = elem_content_dic[key]
            eid = elem_id_dict[key]
            if not content:
                continue
            elif isinstance(content, list) or isinstance(content, tuple):
                content = ase.encrypt(content[0] + content[1])
            result_dict[eid] = ase.encrypt(content)

        return result_dict
