#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/12 17:17
@Author     : jzs
@File       : cont_ext_element_table.py
@Software   : PyCharm
@Description: ......
"""

from . import db


class ContExtElementTable(db.Model):
    """
    合同审核要素表
    """
    __tablename__ = "cont_ext_element_table"
    elem_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    con_id = db.Column(db.Integer)
    elem_name = db.Column(db.VARCHAR(500))
    elem_key = db.Column(db.VARCHAR(500))
    elem_type = db.Column(db.VARCHAR(255))
    elem_check_re = db.Column(db.VARCHAR(500))
    elem_info = db.Column(db.TEXT)
    backup1 = db.Column(db.TEXT)
    backup2 = db.Column(db.TEXT)
    backup3 = db.Column(db.TEXT)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def add_one(con_id: int,
                elem_name: str,
                elem_key: str,
                elem_type: str,
                elem_check_re: str,
                elem_info: str):
        """
        添加一个合同要素

        :param con_id:
        :param elem_name:
        :param elem_key:
        :param elem_type:
        :param elem_check_re:
        :param elem_info:
        :return:
        """
        cm = ContExtElementTable(
            con_id=con_id,
            elem_name=elem_name,
            elem_key=elem_key,
            elem_type=elem_type,
            elem_check_re=elem_check_re,
            elem_info=elem_info
        )
        db.session.add(cm)
        db.session.commit()

    @staticmethod
    def get_elements(conid):
        """
        得到合同id为conid的合同要素
        :param conid:
        :return:
        """
        return ContExtElementTable.query.filter_by(con_id=conid).all()

    @staticmethod
    def get_elements_dict(conid):
        """
        得到三个字典，分别是要素-id字典，要素-要素关键字字典，要素-要素类型字典
        :param conid:
        :return:
        """
        elements = ContExtElementTable.get_elements(conid)
        elem_id_dict = dict((elem.elem_name, elem.elem_id) for elem in elements)
        elem_key_dict = dict((elem.elem_name, elem.elem_key) for elem in elements)
        elem_type_dict = dict((elem.elem_name, elem.elem_type) for elem in elements)

        return elem_id_dict, elem_key_dict, elem_type_dict

    @staticmethod
    def get_elements_key_type_dic(elem_name):
        """
        得到要素名为elem_name的合同要素，然后获取要素关键字-要素类型字典，由于elem_name一致，直接返回一个字典就行了
        :param elem_name: 合同要素名称
        :return:
        """
        elements = ContExtElementTable.query.filter_by(elem_name=elem_name).all()
        elem_key_type = {elem.elem_key: elem.elem_type for elem in elements}

        return elem_key_type

    @staticmethod
    def get_column_element(column_name):
        """
        得到column_name 这一列所有的内容
        :param column_name:n 所取的列名
        :return: 返回去重之后的要素列表
        """
        elements = ContExtElementTable.query.with_entities(getattr(ContExtElementTable, column_name)).distinct().all()
        elements = [item[0] for item in elements]

        return elements


