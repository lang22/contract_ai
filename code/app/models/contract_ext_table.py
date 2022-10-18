#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/12 17:10
@Author     : jzs
@File       : contract_ext_table.py
@Software   : PyCharm
@Description: ......
"""

from . import db


class ContractExtTable(db.Model):
    """
    合同审核表
    """
    __tablename__ = "contract_ext_table"
    cont_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cont_category = db.Column(db.VARCHAR(500))
    cont_sub_category = db.Column(db.VARCHAR(500))
    cont_info = db.Column(db.TEXT)
    cont_name = db.Column(db.TEXT)
    cont_path = db.Column(db.TEXT)
    backup3 = db.Column(db.TEXT)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def select_one(contid: int) -> 'List[ContractExtTable]':
        """
        得到数据库中一个合同模板
        :param contid: 合同id
        :return:
        """
        return ContractExtTable.query.filter_by(cont_id=contid).one_or_none()

    @staticmethod
    def select_one_by_name(cont_name):
        """
        得到数据库中一个合同模板
        :return:
        """
        return ContractExtTable.query.filter_by(cont_name=cont_name).one_or_none()

    @staticmethod
    def select_all() -> 'List[ContractGenTable]':
        """
        得到数据库中所有合同模板
        :return:
        """
        return list(ContractExtTable.query.all())

    @staticmethod
    def add_one(cont_category: str,
                cont_sub_category: str,
                cont_info: str,
                con_name: str) -> None:
        """
        添加一个合同模板
        :param con_name:
        :param cont_docx_path:
        :param cont_category:
        :param cont_sub_category:
        :param cont_info:
        :return:
        """
        ct = ContractExtTable(
            cont_category=cont_category,
            cont_sub_category=cont_sub_category,
            cont_info=cont_info,
            con_name=con_name
        )
        db.session.add(ct)
        db.session.commit()

    @staticmethod
    def get_cont_category_all(all: 'List[ContractExtTable]') -> 'List[str]':
        """
        得到所有合同模板的大分类

        :param all: 保存在内存中的所有合同模板的list
        :return:
        """
        if all is None:
            all = ContractExtTable.query.all()
        return list(set(a.cont_category for a in all))

    @staticmethod
    def cont_sub_category(all: 'List[ContractExtTable]') -> 'List[str]':
        """
        得到所有合同模板的子分类

        :param all: 保存在内存中的所有合同模板的list
        :return:
        """
        if all is None:
            all = ContractExtTable.query.all()
        print(list(set(a.cont_sub_category for a in all)))
        return list(set(a.cont_sub_category for a in all))
