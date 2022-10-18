#!/bin/bash

export LANG=C.UTF-8
export contract_home=/home/Contract_AI


# 启动nginx和uwsgi服务器

nginx -c /home/Contract_AI/nginx.conf

uwsgi -d  --ini /home/Contract_AI/uwsgi.ini

