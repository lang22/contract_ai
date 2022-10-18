#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2018/11/19 11:34
@Author     : jzs
@File       : contract_gen.py
@Software   : PyCharm
@Description: ......
"""
import traceback
import json

from flask import Blueprint, render_template, session, request, send_from_directory
from flask_login import login_required

from app.algorithm.contract_generation_v3 import contract_generation
from app.models.cont_gen_element_table import ContGenElementTable
from app.models.contract_gen_table import ContractGenTable
from app.tools import check_some
from app.tools.list_tools import strings_to_list, list_to_dict, list_to_dict_by_name
from config import Config
from cont_gen import contract_generate_func
from .. import logger

gen = Blueprint('gen', __name__)  # 创建绑定蓝本gen

SESSION_KEY_GEN_TABLE = 'ContractGenTable'  # 合同生成表的session key

SESSION_KEY_ELEMENT_LIST = 'element_list'

SESSION_KEY_TEMPLATE_DOCX_PATH = 'cont_docx_path'

SESSION_KEY_ELEMENT_CONTEXT = 'element_context'


@gen.route('/', methods=['POST', 'GET'])
def admin_gena_index():
    """
    返回合同生成的合同类型选择页面
    :return:
    """
    try:
        contracts = ContractGenTable.select_all()
        category = ContractGenTable.get_cont_category_all(contracts)
        return render_template('admin_gena.html', categorys=category)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return render_template('admin_gena.html')


@gen.route('/admin_gena', methods=['POST', 'GET'])
def admin_gena():
    """
    返回合同生成的合同类型选择页面
    :return:
    """
    try:
        contracts = ContractGenTable.select_all()
        category = ContractGenTable.get_cont_category_all(contracts)
        return render_template('admin_gena.html', categorys=category)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return render_template('admin_gena.html')


@gen.route('/admin_gena2', methods=['POST', 'GET'])
def admin_gena2():
    """
    合同信息填写,返回合同信息的网站
    :return:
    """
    try:
        template_id = request.values.get("xz_ejfl")
        contracts = ContractGenTable.select_one(int(template_id))
        element_list = ContGenElementTable.get_elements(template_id)
        element_list = [(e.elem_id, e.elem_name, e.elem_type, e.elem_check_re)
                        for e in element_list]

        # 缓存合同模板的路径和合同要素列表
        session[SESSION_KEY_ELEMENT_LIST] = element_list
        session[SESSION_KEY_GEN_TABLE] = template_id
        session[SESSION_KEY_TEMPLATE_DOCX_PATH] = contracts.cont_docx_path

        print(element_list)
        return render_template('admin_gena2.html', element_list=element_list)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return ''


@gen.route('/admin_gena3/<go_back_flag>', methods=['POST', 'GET'])
def admin_gena3(go_back_flag):
    """
    合同生成的个性化条款生成
    :return:
    """
    try:
        if go_back_flag == '0':
            element_list = session.get(SESSION_KEY_ELEMENT_LIST)
            element_context_list = list()
            for e in element_list:
                if e[2] == '大小写金额':
                    element_context_list.append(strings_to_list(request.values.get('elem_' + str(e[0]))))
                else:
                    element_context_list.append(request.values.get('elem_' + str(e[0])))
            session[SESSION_KEY_ELEMENT_CONTEXT] = element_context_list
        return render_template('admin_gena3.html')
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return ''


@gen.route('/goback', methods=['POST', 'GET'])
def goback():
    """
    合同生成的个性化条款生成
    :return:
    """
    try:
        element_list = session.get(SESSION_KEY_ELEMENT_LIST)
        element_context_list = session.get(SESSION_KEY_ELEMENT_CONTEXT)
        new_list = list()
        for index, item in enumerate(element_list):
            if element_context_list[index] == ['', '']:
                str_tuple = item
            elif type(element_context_list[index]) != str:
                str_tuple = item + tuple([element_context_list[index][0] + ',' + element_context_list[index][1]])
            else:
                str_tuple = item + tuple([element_context_list[index]])
            new_list.append(str_tuple)
        return render_template('admin_gena2.html', element_list=new_list)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return ''


@gen.route('/admin_gena4/<go_back_flag>', methods=['POST', 'GET'])
def admin_gena4(go_back_flag):
    """
    合同生成，个性化条款生成，合同一键生成
    :return:
    """
    try:
        if go_back_flag == '0':
            element_list = session.get(SESSION_KEY_ELEMENT_LIST)
            element_context_list = list()
            for e in element_list:
                if e[2] == '大小写金额':
                    element_context_list.append(strings_to_list(request.values.get('elem_' + str(e[0]))))
                else:
                    element_context_list.append(request.values.get('elem_' + str(e[0])))
            session[SESSION_KEY_ELEMENT_CONTEXT] = element_context_list
            print('element_context_list', element_context_list)
        return render_template('admin_gena4.html')
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
    return render_template("admin_gena.html")


@gen.route('/admin_gena_newdocx', methods=['POST', 'GET'])
def admin_gena_newdocx():
    """
    返回新生成的合同
    :return:
    """
    try:
        contract_filename = request.values.get("file_name")

        print("file_name", contract_filename)

        con_id = session.get(SESSION_KEY_GEN_TABLE)
        element_context_list = session.get(SESSION_KEY_ELEMENT_CONTEXT)
        print('element_context_list', element_context_list)

        element_context_dic = list_to_dict_by_name(element_context_list, con_id)

        choose_template_name = session.get(SESSION_KEY_TEMPLATE_DOCX_PATH)

        elem_id_dict, elem_key_dict, elem_gena_type_dict = ContGenElementTable.get_id_key_gena_type_dic(con_id)

        print("choose_template_name:", choose_template_name)
        print("contract_filename:", contract_filename)
        print("element_context_dic:", element_context_dic)
        print("elem_id_dict:", elem_id_dict)
        print('elem_key_dict:', elem_key_dict)
        print('elem_gena_type_dict:', elem_gena_type_dict)

        fill_docx_name = contract_generate_func(choose_template_name=choose_template_name,
                                                contract_filename=contract_filename,
                                                elem_content_dict=element_context_dic,
                                                elem_id_dict=elem_id_dict,
                                                elem_key_dict=elem_key_dict,
                                                elem_gena_type_dict=elem_gena_type_dict)

        # fill_docx_name = contract_filename + '.docx'

        return send_from_directory(directory=Config.OTHER_DOWNLOAD_PATH, filename=fill_docx_name, as_attachment=True)
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return ''


@gen.route('/check_input_data', methods=['POST', 'GET'])
def check_input_data():
    """
    检查输入字符串
    返回json
    :return:
    """
    try:
        data = request.values.get('data')
        data_type = request.values.get('type')
        fuc = check_some.check_dict.get(data_type, '')

        result = {'code': '', 'msg': ''}
        if fuc and data:
            code = fuc(data)
            result['code'] = 1 if code == 1 else 0
            result['msg'] = check_some.result_dict.get(data_type).get(code)
            return json.dumps(result)
        else:
            result['code'] = -1
            result['msg'] = '输入为空！'
            return json.dumps(result)
    except Exception as e:
        print(e)
        logger.logger.warning(traceback.format_exc())
        result['code'] = -2
        result['msg'] = '服务器错误，请检查网络！'
        return json.dumps(result)


@gen.route('/choose_contract', methods=['POST', 'GET'])
def choose_contract():
    """
    根据参数，选择合同模板，返回合同模板json字符串
    :return:
    """
    try:
        all_contracts = ContractGenTable.select_all()
        value = request.values.get('value')
        contracts = list(filter(lambda x: x.cont_category == value, all_contracts))
        if value:
            result = dict()
            result['conLen'] = len(contracts)
            result['conPid'] = [cont.cont_id for cont in contracts]
            result['conNames'] = [cont.cont_name for cont in contracts]
            result['conContent'] = dict((cont.cont_id, cont.cont_info) for cont in contracts)
            return json.dumps(result)
        else:
            return ''
    except Exception as e:
        print(e)
        logger.warning(traceback.format_exc())
        return ''
