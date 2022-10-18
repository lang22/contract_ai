import copy
import traceback
import json

from flask import Blueprint, render_template, session, request, send_from_directory
from flask_login import login_required

from app.algorithm.contract_generation_v3 import contract_generation
from app.models.cont_gen_element_table import ContGenElementTable
from app.models.contract_ext_table import ContractExtTable
from app.models.contract_gen_table import ContractGenTable
from app.tools import check_some
from app.tools.list_tools import strings_to_list, list_to_dict, list_to_dict_by_name
from config import Config
from cont_gen import contract_generate_func
from .. import logger

cont_gen = Blueprint('cont_gen', __name__)

SUCCESS = 1

NOT_SUCCESS = 0

OK = 'ok!'

ERROR = "error!"

ERROR_00: str = "error 00:参数为空!"

ERROR_01 = "error 00:文档1或文档2不存在！"

ERROR_02 = "error 02:文档1或文档2格式错误！"

ERROR_03 = "error 03:文档解析错误！"

DEFAULT_RESULT_JSON = {
    "success": NOT_SUCCESS,
    "msg": ERROR,
}


@cont_gen.route('/get_contract_type_list_by_json', methods=['GET', 'POST'])
def get_contract_type_list_by_json():
    """
    获取合同数据
    http:// 114.116.74.129:9097/exam_risk/get_contract_type_list_by_json
    http://127.0.0.1:5000/exam_risk/get_contract_type_list_by_json

    {"success": 1, "msg": "ok!", "result": {"type_list": ["XXXX","XXXX","XXXX"] }}
    :return:
    """
    result_json = copy.deepcopy(DEFAULT_RESULT_JSON)
    result = {"typeList": ''}
    try:
        contracts = ContractGenTable.select_all()
        result["typeList"] = [cont.cont_name for cont in contracts]
        result_json["success"] = SUCCESS
        result_json["msg"] = OK
        result_json["result"] = result
    except Exception as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
    finally:
        return json.dumps(result_json)


@cont_gen.route("/get_contract_gen_elem_list", methods=['GET', 'POST'])
def get_contract_gen_elem_list():
    """
    获取合同生成的要素的列表
    :return:
    """
    result_json = copy.deepcopy(DEFAULT_RESULT_JSON)
    result_item = {
        "elemID": "",
        "elemName": "",
        "elemType": "",
        "elemHint": ""
    }

    try:
        cont_type_name = request.values.get("type")
        print('cont_type_name:', cont_type_name)
        if not cont_type_name:
            raise ValueError(ERROR_00)

        template_id = ContractGenTable.select_one_by_name(cont_type_name).cont_id
        element_list = ContGenElementTable.get_elements(template_id)
        element_list = [(e.elem_id, e.elem_name, e.elem_type, e.elem_check_re)
                        for e in element_list]
        element_list = [{
            "elemID": 'e' + str(e1),
            "elemName": e2,
            "elemType": e3,
            "elemHint": e4}
            for e1, e2, e3, e4 in element_list]

        print('element_list', element_list)
        result_json["success"] = SUCCESS
        result_json["msg"] = OK
        result_json['result'] = element_list

    except ValueError as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
    except FileNotFoundError as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
    except Exception as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = ERROR_03
    finally:
        return json.dumps(result_json)


@cont_gen.route("/gena_contract", methods=['GET', 'POST'])
def gena_contract():
    """
    获取合同生成的要素的列表
    :return:
    """
    result_json = copy.deepcopy(DEFAULT_RESULT_JSON)
    try:

        json_data = request.get_data(as_text=True)
        if not json_data:
            raise ValueError(ERROR_00)
        # 获取前端POST请求传过来的 json 数据
        json_data = json.loads(json_data)
        print(json_data)

        cont_type_name = json_data["type"]
        contract_filename = json_data["contractFilename"]
        contract_content_list = json_data["contractContentList"]

        choose_cont = ContractGenTable.select_one_by_name(cont_type_name)
        cont_id = choose_cont.cont_id
        choose_template_name = choose_cont.cont_docx_path
        elem_id_dict, elem_key_dict, elem_gena_type_dict = ContGenElementTable.get_id_key_gena_type_dic(cont_id)

        element_context_dic = {}

        elem_id_dict_tmp = {elem_id_dict[key]: key for key in elem_id_dict}
        for item in contract_content_list:
            elem_id = int(item["elemID"][1:])
            content = item.get("elemContent", "")
            key = elem_id_dict_tmp[elem_id]
            element_context_dic[key] = content

        print("choose_template_name:", choose_template_name)
        print("contract_filename:", contract_filename)
        print("element_context_dic:", element_context_dic)
        print("elem_id_dict:", elem_id_dict)
        print('elem_key_dict:', elem_key_dict)
        print('elem_gena_type_dict:', elem_gena_type_dict)

        filled_docx_filename = contract_generate_func(
            choose_template_name=choose_template_name,
            contract_filename=contract_filename,
            elem_content_dict=element_context_dic,
            elem_id_dict=elem_id_dict,
            elem_key_dict=elem_key_dict,
            elem_gena_type_dict=elem_gena_type_dict)

        result_json["success"] = SUCCESS
        result_json["msg"] = OK
        result_json["result"] = filled_docx_filename

    except ValueError as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
    except FileNotFoundError as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
    except Exception as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = ERROR_03
    finally:
        return json.dumps(result_json)


@cont_gen.route('/check_input_data', methods=['POST', 'GET'])
def check_input_data():
    """
    检查输入字符串
    返回json
    :return:
    """

    result_json = copy.deepcopy(DEFAULT_RESULT_JSON)
    try:
        data = request.values.get('elemContent')
        data_type = request.values.get('elemType')
        fuc = check_some.check_dict.get(data_type, '')

        print(data, data_type, fuc)
        result = {'code': '', 'msg': ''}
        if fuc and data:
            code = fuc(data)
            result['code'] = 1 if code == 1 else 0
            result['msg'] = check_some.result_dict.get(data_type).get(code)
        else:
            result['code'] = -1
            result['msg'] = '输入为空！'

        result_json["success"] = SUCCESS
        result_json["msg"] = OK
        result_json["result"] = result

    except ValueError as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
    except FileNotFoundError as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = str(e)
    except Exception as e:
        print(e, "\n", traceback.format_exc())
        logger.warning(traceback.format_exc())
        result_json['msg'] = ERROR_03
    finally:
        return json.dumps(result_json)
