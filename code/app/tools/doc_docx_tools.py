import base64
import json
import time

import requests
import os

from config import Config

from ..tools import random_fliename, join_path

DOC2DOCX_SERVICE_URL = Config.DOC2DOCX_SERVICE_URL
DOC2DOCX_SERVICE_URL_TIMEOUT = Config.DOC2DOCX_SERVICE_URL_TIMEOUT


def check_doc2docx_status() -> bool:
    """
    判断doc2docx服务的状态，是否能访问，能访问返回True
    :return:
    """
    try:
        code = requests.get(
            DOC2DOCX_SERVICE_URL,
            timeout=DOC2DOCX_SERVICE_URL_TIMEOUT
        ).status_code

        return code == 200
    except Exception as e:
        print(e)
        return False


def base64_to_docxfile(code_data, save_data_path: str) -> bool:
    """
    转换base64编码，将base64编码转换成docx文件

    :param code_data: base64编码的字符串数据
    :param save_data_path: docx保存路径
    :return:
    """
    text_content = base64.b64decode(code_data)

    with open(save_data_path, 'wb') as f:
        f.write(text_content)

    # 转换成功返回True
    if os.path.exists(save_data_path):
        return True


def doc2docx(post_name: str, post_data_path: str, save_data_path: str) -> bool:
    """
    访问doc2docx接口，将doc文件转换成docx文件，接口形式为 {"succeed": 1, "mgs": null, "data": base64}
    Config.DOC2DOCX_URL = 'http://127.0.0.1:5000/doc2docx'

    :param post_name: 文件名
    :param post_data_path: 上传文件的路径
    :param save_data_path: 下载文件的路径
    :return:
    """
    try:
        # if not check_doc2docx_status():
        #     return False
        if post_name[-4:] != ".doc":
            return False

        print("DOC2DOCX_SERVICE_URL", DOC2DOCX_SERVICE_URL)
        files = {'file': (post_name, open(post_data_path, 'rb'))}
        r = requests.post(DOC2DOCX_SERVICE_URL, files=files)
        data = json.loads(r.text)
        print(data)
        return base64_to_docxfile(data['data'], save_data_path)

    except Exception as e:
        print(e)
        return False


def doc2docx_for_files_list(file_name_list, file_dir):
    """
    批量将doc文件转换成docx文件

    :param file_name_list:  文件名列表
    :param file_dir:  文件目录名字
    :return:
    """
    new_file_name_list = []
    for file_name in file_name_list:
        if file_name[-4:] != ".doc":
            new_file_name_list.append(file_name)
            continue
        else:

            new_file_name = file_name + 'x'
            new_file_name_list.append(new_file_name)

            ok = doc2docx(
                file_name,
                join_path(file_dir, file_name),
                join_path(file_dir, new_file_name))
            print(ok)
    return new_file_name_list


def save_docx(request_files_io, save_path: str) -> str:
    """
    将flask request的文件数据流保存指指定目录，如果是doc文件则转换成docx文件。并返回保存后的路径

    :param request_files_io: flask request的文件数据流保
    :param save_path 保存指指定目录
    :return:
    """
    filename = random_fliename()
    print('request_files_io.filename：', request_files_io.filename)

    if request_files_io.filename[-4:] == ".doc":
        upload_path = join_path(save_path, filename + '.doc')
        request_files_io.save(upload_path)
        print("tag upload_path: ", upload_path)

        save_data_path = join_path(save_path, filename + '.docx')
        print("save_data_path: ", save_data_path)

        ok = doc2docx(filename + '.doc', upload_path, save_data_path)
        print(ok)
        return save_data_path
    else:
        upload_path = join_path(save_path, filename + '.docx')
        request_files_io.save(upload_path)
        print("save_data_path: ", upload_path)

        return upload_path


def save_base64_data_to_file(base64_data: str, file_name: str, save_path: str) -> str:
    """
    将base64zi字符文件数据流保存指指定目录，如果是doc文件则转换成docx文件。并返回保存后的路径

    :param base64_data: base64数据
    :param file_name: 文件名
    :param save_path: 保存指指定目录

    :return:
    """
    random_filename = random_fliename()
    print('file_name.filename：', file_name)

    if file_name[-4:] == ".doc":
        upload_path = join_path(save_path, random_filename + '.doc')
        print("tag upload_path: ", upload_path)
        base64_to_docxfile(base64_data, upload_path)

        save_data_path = join_path(save_path, random_filename + '.docx')
        print("save_data_path: ", save_data_path)

        ok = doc2docx(random_filename + '.doc', upload_path, save_data_path)
        print(ok)
        return save_data_path
    else:
        upload_path = join_path(save_path, random_filename + '.doc')
        print("save_data_path: ", upload_path)
        base64_to_docxfile(base64_data, upload_path)

        return upload_path


def get_word_file_ext_name(filename):
    """
    得到word文件的文件后缀

    :param filename:
    :return:
    """
    return filename[-4:] if filename[-4:] == ".doc" else filename[-5:]


def snowflake() -> str:
    """
    得到随机数字文件名字:
    :return: 得到随机数字文件名字
    """
    return str(id(list())) + str(round(time.time() * 1000))


def save_docx_return_path_and_name(request_files_io, save_path: str) :
    """
    将flask request的文件数据流保存指指定目录，如果是doc文件则转换成docx文件。并返回返回文件名和文件路径

    :param request_files_io: flask request的文件数据流保
    :param save_path 保存指指定目录
    :return: 返回文件名和文件路径
    """
    filename = random_fliename()
    print('request_files_io.filename：', request_files_io.filename)

    if request_files_io.filename[-4:] == ".doc":
        upload_path = join_path(save_path, filename + '.doc')
        request_files_io.save(upload_path)
        print("tag upload_path: ", upload_path)

        save_data_path = join_path(save_path, filename + '.docx')
        print("save_data_path: ", save_data_path)

        ok = doc2docx(filename + '.doc', upload_path, save_data_path)
        print(ok)
        return save_data_path
    else:
        upload_path = join_path(save_path, filename + '.docx')
        request_files_io.save(upload_path)
        print("save_data_path: ", upload_path)

        return filename + '.docx', upload_path
