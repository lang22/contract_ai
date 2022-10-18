import datetime
import time
import traceback
import json

from docx import Document
from flask import Blueprint, request, session, redirect, url_for, flash, render_template, send_from_directory
from flask_login import current_user

from app import logger, db
from app.json_models.admin_check_search_json_result import parse_json
from app.models.cont_ext_element_table import ContExtElementTable
from app.models.user import User
from app.tools import random_fliename, join_path
from app.tools.aes import Prpcrypt
from config import Config
from cont_check.check_download_method import get_content_by_filename
from cont_check.check_method import get_check_results, save_to_mysql, get_sims_result_by_sentence
from app.models.flower_table import Flower
from cont_check.solve_html import solve_method
from ..tools import doc_docx_tools

from ..models.cont_docx_backup_table import ContDocxBackupTable
from ..tools import pre_docx

check = Blueprint('check', __name__)

# CONT_NAME 存储读入的文件名称
CONT_NAME = 'CONT_NAME'
UP_FILE_NAME = 'UP_FILE_NAME'
SIMS_LIST = 'sims_list'


@check.route('/', methods=['POST', 'GET'])
def admin_check_index():
    """
    基础路由，直接返回上传文件页面
    :return:
    """
    return render_template('admin_check_index.html')


@check.route('/admin_check', methods=['POST', 'GET'])
def admin_check():
    """
    合规性审查，上传合同文档，将文档保存到 static/uploads 文件夹下
    :return:
    """
    try:
        if request.method == 'POST':
            up_file = request.files['file']
            up_file_name = up_file.filename

            session[UP_FILE_NAME] = up_file_name
            #
            # filename = random_fliename()
            # upload_path = join_path(Config.UPLOADED_DIR_PATH, filename)
            # up_file.save(upload_path + '.docx')
            upload_path = doc_docx_tools.save_docx(up_file, Config.UPLOADED_DIR_PATH)

            filename = upload_path.split('/')[-1].replace('.docx', '')

            return redirect(url_for('check.admin_check_solve', filename=filename, up_file_name=up_file_name))
        else:
            return render_template('admin_check_index.html')
    except Exception as e:
        # flash("请上传后缀为.docx的文件，如“BUPT合同.docx”")
        print(e)
        logger.warning(traceback.format_exc())
        return redirect(url_for('check.admin_check'))


@check.route('/admin_check_detail/<string:filename>/<string:up_file_name>', methods=['POST', 'GET'])
def admin_check_solve(filename, up_file_name):
    """
    合规性审查，生成审查文档，按段落存储
    :param filename:读入的文件路径名称
    :return:
    """
    try:
        upload_path_userup = join_path(Config.UPLOADED_DIR_PATH, filename + '.docx')

        # 处理存在批注的情况
        pre_docx.multi_process([upload_path_userup], Config.UPLOADED_DIR_PATH)

        # 将合同保存到数据库
        ContDocxBackupTable.add_one(request.remote_addr, upload_path_userup)

        body, style, first_sims, first_para_content = solve_method(upload_path_userup)

        if len(first_sims) == 0:
            flash("本合同未查找到任何相似信息")
            return render_template('admin_check_index.html')

        para_temp = Document(upload_path_userup)
        results = list()
        for item in para_temp.paragraphs:
            text = item.text
            if text:
                results.append(text)

        save_to_mysql(up_file_name, results)

        session[CONT_NAME] = upload_path_userup

        print("body：", body, '\n')
        print("style:", style, '\n')
        print("first_sims:", first_sims)
        print("first_para_content:", first_para_content)

        return render_template('admin_check_show.html',
                               body=body,
                               style=style,
                               first_sims=[(i + 1, e) for i, e in enumerate(first_sims)],
                               first_para_content=first_para_content)

    except Exception as e:
        print(e)
        flash("服务器计算错误!")
        logger.warning(traceback.format_exc())
        return redirect(url_for('check.admin_check'))


@check.route('/admin_check_search/', methods=['POST', 'GET'])
def admin_check_search():
    """
    合规性审查，生成审查信息
    :param filename:读入的文件路径名称
    :return:
    """
    try:

        content = request.values.get('content')

        print("content:", content)
        res = get_sims_result_by_sentence(content)
        res_json = json.dumps(parse_json(res))
        print("res_json:", res_json)
        return json.dumps(parse_json(res))

    except Exception as e:
        print(e)
        flash("服务器计算错误!")
        logger.warning(traceback.format_exc())
        return redirect(url_for('check.admin_check'))


@check.route('/admin_check_download/', methods=['POST', 'GET'])
def admin_check_download():
    """
    下载相似性的文档
    :return:
    """
    try:
        dic_str = request.values.get('download_input')
        # print('dic_str:', dic_str)
        dic = json.loads(dic_str)
        filename = dic['filename']
        content = dic['content']
        filename = filename + '.docx'
        get_content_by_filename(filename, content)
        return send_from_directory(directory=Config.DOWNLOAD_PATH,
                                   filename=filename,
                                   as_attachment=True)

    except Exception as e:
        print(e)
        # logger.warning(traceback.format_exc())
        # return render_template("admin_check_index.html")


@check.route('/admin_check_flower/', methods=['POST', 'GET'])
def admin_check_flower():
    """
    flower 送花表示点击此篇文档，并将点击数据存入数据库
    :return:
    """
    try:

        # user_id = User.get_id(current_user)
        user_id = 123456  # admin 没有登录功能，统一使用admin  id

        cont_name = session.get(UP_FILE_NAME)[:-5]
        sim_cont_name = request.values.get("filename")
        upload_time = time.strftime('%Y.%m.%d', time.localtime(time.time()))
        sims_content = request.values.get("sims_content")
        para_content = request.values.get('para_content')

        print("sim_cont_name:", sim_cont_name)
        print("sims_content:", sims_content)
        print("para_content:", para_content)

        aes = Prpcrypt(Config.DB_STR_AES_KEY)
        aes_cont_name = aes.encrypt(cont_name)
        aes_sim_cont_name = aes.encrypt(sim_cont_name)
        aes_sims_content = aes.encrypt(sims_content)
        aes_para_content = aes.encrypt(para_content)

        Flower.add(aes_cont_name, aes_para_content, aes_sim_cont_name, user_id, upload_time, aes_sims_content)
        return json.dumps({"succeed": 1})

    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return json.dumps({"succeed": 0})
