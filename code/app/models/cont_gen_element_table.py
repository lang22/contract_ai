#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/12 17:20
@Author     : jzs
@File       : cont_gen_element_table.py
@Software   : PyCharm
@Description: ......
"""

from . import db


class ContGenElementTable(db.Model):
    """
    合同生成要素表
    """
    __tablename__ = "cont_gen_element_table"
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
        cm = ContGenElementTable(
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
        return ContGenElementTable.query.filter_by(con_id=conid).all()

    @staticmethod
    def get_gene_elements_dict(conid):
        """
        得到三个字典，分别是要素-id字典，要素-要素关键字字典，要素-要素类型字典

        :param conid:
        :return:
        """
        elements = ContGenElementTable.get_elements(conid)
        elem_id_dict = dict((elem.elem_name, elem.elem_id) for elem in elements)  #  得到elem.elem_name

        elem_key_dict = dict((elem.elem_name, elem.elem_key) for elem in elements)  # 通过name查找到elem_key
        elem_type_dict = dict((elem.elem_name, elem.elem_type) for elem in elements)  # 这个type是  汉子 地址 之类的
        elem_elem_info_dict = dict((elem.elem_name, elem.elem_info) for elem in elements)  # 示例输入
        elem_gena_type_dict = dict((elem.elem_name, elem.backup1) for elem in elements)  # instruction 类型

        return elem_id_dict, elem_key_dict, elem_type_dict, elem_elem_info_dict, elem_gena_type_dict

    @staticmethod
    def get_elements_name_dict(conid: int):
        """
        得到要素-name字典

        :param conid:
        :return:
        """
        elements = ContGenElementTable.get_elements(conid)
        elem_name_dict = dict((elem.elem_name, elem.elem_id) for elem in elements)  # 得到elem.elem_name

        return elem_name_dict

    @staticmethod
    def get_id_key_gena_type_dic(con_id: int):
        """
        得到合同的要素-要素ID字典、要素-关键字字典和要素-生成类型字典

        :param con_id: 合同id
        :return:  要素-要素ID字典、要素-关键字字典和要素-生成类型字典
        """
        elem_id_dict, elem_key_dict, elem_type_dict, elem_elem_info_dict, elem_gena_type_dict \
            = ContGenElementTable.get_gene_elements_dict(con_id)

        return elem_id_dict, elem_key_dict, elem_gena_type_dict

