#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@File       : Config.py
@Software   : PyCharm
@Description: 项目配置文件
"""
import os
import configparser
# 项目的基础路径
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

config_load = configparser.ConfigParser()
config_load.read(os.path.join(BASE_DIR, "config.ini"))


class Config:
    """
    定义配置基类
    """
    BOOTSTRAP_SERVE_LOCAL = True

    # 设置session的保存时间为7天
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # 秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'root'

    # 数据库AES加密密钥
    DB_STR_AES_KEY = "jcjjzgzzgsgss"

    # 数据库公用配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_POOL_RECYCLE = 2

    # 上传文件路径
    UPLOADED_DIR_PATH = os.path.join(BASE_DIR, 'app/static/uploads')

    # # 其他上传文件路径
    # OTHER_UPLOADED_DIR_PATH = os.path.join(BASE_DIR, 'app/static/uploads')

    # LSI模型文件路径
    LSI_MODEL_PATH = os.path.join(BASE_DIR, 'cont_check/model')

    # 合规库json_data文件路径
    LAW_LIBRARY_DATA_PATH = os.path.join(BASE_DIR, 'cont_check/law_library_data.json')

    # 合规性审核下载文件路径
    DOWNLOAD_PATH = os.path.join(BASE_DIR, 'app/static/check_download')

    # 其他文件下载文件路径
    OTHER_DOWNLOAD_PATH = os.path.join(BASE_DIR, 'app/static/downloads')

    # 合同模板生成的路径
    CONT_GENA_TEMPLATE_DIR_PATH = os.path.join(BASE_DIR, 'app/static/docx/template')

    # 合同流转单目录模板路径
    CONT_FLOW_TABLE_DIR_PATH = os.path.join(BASE_DIR, 'app/static/docx/docx_ft')

    # 合同生成结构的目录路径
    CONT_GENA_DIR_PATH = os.path.join(BASE_DIR, 'app/static/docx/docx_repo')

    # 多文档要素识别的目录路径
    CONT_MULTI_EXAM_PATH = os.path.join(BASE_DIR, 'app/static/multi_exam_upload')

    # 带批注docx文档预处理压缩与解压路径
    CONT_PRE_DOCX_PATH = os.path.join(BASE_DIR, 'app/static/pre_process_docx')
    # 日志文件路径
    LOG_FILE_PATH = os.path.join(BASE_DIR, 'flask_log.log')

    # 机器学习和深度学习模型文件的路径
    STATIC_ELEM_MODEL = os.path.join(BASE_DIR, 'app/static/elem_model')

    # 仿真环境doc2docx服务url
    # DOC2DOCX_SERVICE_URL = 'http://10.64.141.43:9099/doc2docx'
    DOC2DOCX_SERVICE_URL = 'http://%s:%s/%s' % (
        config_load['DOC2DOCX_SERVICE']['host'], config_load['DOC2DOCX_SERVICE']['port'],
        config_load['DOC2DOCX_SERVICE']['action']
    )

    # 仿真环境doc2docx服务的相应时间
    DOC2DOCX_SERVICE_URL_TIMEOUT = 10

    # 额外的初始化操作
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """开发环境配置

    """
    DEBUG = True
 
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/css2?charset=utf8mb4&autocommit=true'  # 本地数据库


class TestingConfig(Config):
    """
    测试环境配置
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@xx.xx.xx.xx/css3?charset=utf8mb4&autocommit=true'


"""
[DATABASE]
host = xx.xx.xx.xx
port = 3306
user = root
password = root
database = css2
"""


class ProductionConfig(Config):
    """
    生产环境配置
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4&autocommit=true' % (
        config_load['DATABASE']['user'], config_load['DATABASE']['password'], config_load['DATABASE']['host'],
        config_load['DATABASE']['port'], config_load['DATABASE']['database']
    )


# 生成一个字典，用来根据字符串找到对应的配置类
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
