#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Description: 初始化app包
"""
import logging

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import config, Config

db = SQLAlchemy()

bootstrap = Bootstrap()

login_manager = LoginManager()

logger = None


def config_extensions(app: 'Flask'):
    """
    # 初始化其他
    :param app:
    :return:
    """
    # 初始化数据库
    db.init_app(app)

    # 初始化bootstrap
    bootstrap.init_app(app)

    # 初始化用户安装配置
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    login_manager.login_view = "login"
    login_manager.login_message = "需要先登录"
    login_manager.login_message_category = "info"

    # 初始化日志
    handler = logging.FileHandler(Config.LOG_FILE_PATH, encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    global logger
    logger = app.logger



def create_app(config_name: str):
    """
    创建app实例对象，初始化项目app中的所有配置
    :param config_name:
    :return:
    """
    # 配置蓝本
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config[config_name])
    # 执行额外的初始化
    config.get(config_name).init_app(app)

    # 配置其他
    config_extensions(app)

    # 配置蓝本
    from app.views import config_blueprint
    config_blueprint(app)

    return app
