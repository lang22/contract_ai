#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/23 15:09
@Author     : jzs
@File       : docxtabel.py
@Software   : PyCharm
@Description: ......
"""
from app.tools.aes import Prpcrypt
from . import db

namelist = [
    "docx_bh", "docx_syy", "docx_xyrq", "docx_xydd", "docx_zrf",
    "docx_srf", "docx_zwf", "docx_zrffzr", "docx_srffzr", "docx_zwffzr",
    "docx_zrfzs", "docx_srfzs", "docx_zwfzs", "docx_zmbjye", "docx_lx",
    "docx_qtzq", "docx_ztzq", "docx_zrjk", "docx_zqje",
    "docx_wyj", "docx_jzr", "docx_bxze", "docx_bjye",
    "docx_qx", "docx_khyh", "docx_hm", "docx_zh", "docx_jybzz"
]


class docx_table(db.Model):
    """
    要素表
    """
    __tablename__ = 'docx_table'
    docx_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    docx_bh = db.Column(db.TEXT)
    docx_syy = db.Column(db.TEXT)
    docx_xyrq = db.Column(db.TEXT)
    docx_xydd = db.Column(db.TEXT)
    docx_zrf = db.Column(db.TEXT)
    docx_srf = db.Column(db.TEXT)
    docx_zwf = db.Column(db.TEXT)
    docx_zrffzr = db.Column(db.TEXT)
    docx_srffzr = db.Column(db.TEXT)
    docx_zwffzr = db.Column(db.TEXT)
    docx_zrfzs = db.Column(db.TEXT)
    docx_srfzs = db.Column(db.TEXT)
    docx_zwfzs = db.Column(db.TEXT)
    docx_zmbjye = db.Column(db.TEXT)
    docx_lx = db.Column(db.TEXT)
    docx_qtzq = db.Column(db.TEXT)
    docx_ztzq = db.Column(db.TEXT)
    docx_zrjk = db.Column(db.TEXT)
    docx_zqje = db.Column(db.TEXT)
    docx_wyj = db.Column(db.TEXT)
    docx_jzr = db.Column(db.TEXT)
    docx_bxze = db.Column(db.TEXT)
    docx_bjye = db.Column(db.TEXT)
    docx_qx = db.Column(db.TEXT)
    docx_khyh = db.Column(db.TEXT)
    docx_hm = db.Column(db.TEXT)
    docx_zh = db.Column(db.TEXT)
    docx_jybzz = db.Column(db.TEXT)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return 'User:%s' % self.name

    # aes加密的密钥
    __aes_key = "jcjjzgzzgsgss"

    @staticmethod
    def __encrypt(text):
        """
        将字符串加密，使用aes加密方式
        :param text:
        :return:
        """

        return Prpcrypt(docx_table.__aes_key).encrypt(text)

    @staticmethod
    def __decrypt(text):
        """
        将aes加密的字符串加密解密
        :return:
        """
        return Prpcrypt(docx_table.__aes_key).decrypt(text)

    @staticmethod
    def add_docx_table(dic):
        """
        将dic转换成字典再通过构造方法提交数据库
        :return:
        """
        try:
            kwd = dict()
            for i in range(len(dic)):
                if isinstance(dic[i], list):
                    kwd[namelist[i]] = docx_table.__encrypt(dic[i][0] + "#" + dic[i][1])
                else:
                    kwd[namelist[i]] = docx_table.__encrypt(dic[i])

            d = docx_table(**kwd)
            db.session.add(d)
            db.session.commit()
        except BaseException as e:
            print(e)
            db.session.rollback()
            print('rollback')
