#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/10 11:04
@Author     : jzs
@File       : mange.py
@Software   : PyCharm
@Description: 运行主程序
"""
import os

from app import create_app
from flask_script import Manager

# 从环境变量中获取启动配置
config_name = os.environ.get('FLASK_CONFIG') or 'default'
#test
# 初始化，并生成app
app = create_app(config_name)

# 绑定数据库


# 绑定管理工具
manager = Manager(app)
#test
if __name__ == '__main__':
    manager.run()
