import os

import zipfile
import re

from config import Config


def my_unzip(filename: str, unzip_path: str, save_path: str):
    """
    解压文件
    :param filename:
    :return:
    """
    filepath = os.path.join(save_path, filename)

    docxZip = zipfile.ZipFile(filepath)
    docxZip.extractall(unzip_path)


def get_list(unzip_path):
    """
    获取文件目录下所有的带有层级关系的文件名称
    :return:
    """
    results = []
    files = os.listdir(Config.CONT_PRE_DOCX_PATH)

    for file in files:

        if os.path.isdir(os.path.join(unzip_path, file)):
            lis = os.listdir(os.path.join(unzip_path, file))
            for item in lis:
                item_path = file + '/' + item
                if os.path.isdir(os.path.join(unzip_path, item_path)):
                    tt_lis = os.listdir(os.path.join(unzip_path, item_path))
                    results.extend(item_path + '/' + third_item for third_item in tt_lis)
                else:
                    results.append(item_path)
        else:
            results.append(file)
    return results


def zip(unzip_path: str, filename: str, save_path: str):
    """
    将docx文档解压出的文件压缩成docx文档形式
    :return:
    """
    docu_file = os.path.join(save_path, filename)

    f = zipfile.ZipFile(docu_file, 'w', zipfile.ZIP_DEFLATED)
    files = get_list(unzip_path)

    for file in files:
        f.write(os.path.join(unzip_path, file), file)
    f.close()


def alter(unzip_path: str):
    """
    修改解压出的word/document.xml文件，使批注内容可读
    :param unzip_path: 文件解压路径
    :return:
    """
    docu_file = os.path.join(unzip_path, 'word/document.xml')
    with open(docu_file, 'r', encoding='utf-8') as f:

        text = f.read()
        pre_length = len(text)

        while True:

            text = re.sub('<w:ins w:id.*?>|</w:ins>', '', text, re.S)
            length = len(text)
            if length == pre_length:
                break
            pre_length = length

    with open(docu_file, 'w', encoding='utf-8') as f1:
        f1.write(text)
        f1.close()


def del_file(path):
    """
    删除这个文件夹的所有内容
    :param path:
    :return:
    """
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

    ls = os.listdir(path)
    if not ls:
        os.rmdir(path)
    else:
        for i in ls:
            c_path = os.path.join(path, i)
            os.rmdir(c_path)


def delete(unzip_path: str):
    """
    压缩完之后，要将解压出的文件删除
    :return:
    """
    files = os.listdir(unzip_path)
    for file in files:
        file = os.path.join(unzip_path, file)
        if os.path.isdir(file):
            del_file(file)
            # os.rmdir(file)
        else:
            os.remove(file)


def pre_process_docx(filename: str, unzip_path: str, save_path: str):
    """
    预处理docx文件，将文件中修改的批注内容转变成正常的文本格式
    :param filepath: 读取文件路径
    :param unzip_path: 解压文件路径
    :return:
    """
    my_unzip(filename, unzip_path, save_path)
    alter(unzip_path)
    zip(unzip_path, filename, save_path)
    delete(unzip_path)


def multi_process(filenames: list, save_path: str):
    """
    预处理上传的所有文件
    :param save_path: 上传的文件保存的目录
    :param filenames: 文件名集合
    :return:
    """
    for file in filenames:

        unzip_path = Config.CONT_PRE_DOCX_PATH
        pre_process_docx(file, unzip_path, save_path)
