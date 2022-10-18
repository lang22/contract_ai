import json

# 查找到相似信息样例格式
__success_example = {
    "success": 1,
    "results": [
        {
            "filename": "商法",
            "content": "海商法",
            "sims": "0.99999999"
        }
    ]
}

# 未查找到相似信息样例格式
__fail_example = {
    "success": 0,
    "results": []
}


# def parse_json(text: str):
#     """
#     将数据处理成我们需要的json格式  系统ES模式
#     :param text:
#     :return:
#     """
#     dic = json.loads(text)['context']  # 存放着每一段的相似信息
#     # 在sims中存放着前十的文件
#     cur_dic = dic
#     results = list()
#
#     final_result = {'success': '0', 'results': ''}
#     if 'sims' in cur_dic[0]:
#         # 这一段存在相似段落信息
#         final_result['success'] = '1'
#         sims_dic = cur_dic[0]['sims']
#         for item in sims_dic:
#             cur_temp = {'filename': item['sim_documents_path'], 'content': item['sim_document'],
#                         'sims': item['sims']}
#             results.append(cur_temp)
#     else:
#         print('本段没有相似段落信息')
#
#     final_result['results'] = results
#
#     return final_result


def parse_json(text: str):
    """
    将数据处理成我们需要的json格式  本地数据模式
    :param text:
    :return:
    """
    final_result = {'success': '0', 'results': ''}
    results = list()
    dic = text

    if 'sims' in dic:
        # 这一段存在相似段落信息
        final_result['success'] = '1'
        sims_dic = dic['sims']

        for item in sims_dic:
            filename = item['sim_documents_path']
            if len(filename) >=20:
                simple_file = filename[:20] + '...'
            else:
                simple_file = filename

            cur_temp = {'filename': filename, 'content': item['sim_document'],
                        'sims': str(item['sims'])[:-11], 'simple_file': simple_file}
            results.append(cur_temp)
    else:
        # print('本段没有相似段落信息')
        pass

    final_result['results'] = results

    return final_result