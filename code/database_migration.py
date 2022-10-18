#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@File       : 远程数据库保存到本地.py
@Software   : PyCharm
@Description: ......
"""

import os

# 缓存迁移前的文件
DATA_NAME = '%s.sql' % id(list())

print("注意：使用该脚本前，请确定本地MySQL数据库中，是否存在空的数据库！")
EXIT_FLAG = input("是否存在空的数据库？不存在则退出脚本 Y/n ?  ")
if EXIT_FLAG != 'Y':
    exit()

print()

# 远程服务器的配置，可以换成下面的控制台输入
# DB_HOST = ""
# DB_PORT = "3306"
# DB_NAME = ""
# DB_USER = ""
# DB_PW = ""

# 可以换成上面的默认输入
DB_HOST = input("输入远程数据库IP地址：")
DB_PORT = "3306"  # 端口号默认为3306
DB_USER = input("输入远程数据库用户名：")
DB_PW = input("输入远程数据库密码：")
DB_NAME = input("输入远程数据库名：")

print("正在保存远程数据库文件...")
DUMP_CMD = "mysqldump -h%s -P%s -u%s -p%s %s > %s" % (DB_HOST, DB_PORT, DB_USER, DB_PW, DB_NAME, DATA_NAME)
os.system(DUMP_CMD)
print("远程数据库文件已保存...\n")

# 本地数据库的配置，可以换成下面的控制台输入
# DB_HOST = '127.0.0.1'
# DB_PORT = "3306"
# DB_NAME = ''
# DB_USER = ''
# DB_PW = ''

# 可以换成上面的默认输入
DB_HOST = "127.0.0.1"
DB_PORT = "3306"  # 端口号默认为3306
DB_USER = input("输入本地数据库用户名：")
DB_PW = input("输入本地数据库密码：")
DB_NAME = input("输入本地已经存在的空的数据库名\n（注意不要输入已经有的数据的数据库名，否则会被覆盖！）：")

print("正在保存到本地数据库文件...")
PUT_CMD = "mysql -h%s -P%s -u%s -p%s -D%s < %s" % (DB_HOST, DB_PORT, DB_USER, DB_PW, DB_NAME, DATA_NAME)
os.system(PUT_CMD)
print("本地数据库文件已保存...\n")

# 删除缓存文件
if os.path.exists(DATA_NAME):
    os.remove(DATA_NAME)
