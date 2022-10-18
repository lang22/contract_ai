import json

# dic = {}
#
# with open('law_library', 'r', encoding='utf-8') as f:
#
#     j_dict = json.load(f)
#     results = j_dict['hits']['hits']
#     for result in results:
#         key = result['_source']['title']
#         dic[key] = result
#
# with open('law_library_data.json', 'w', encoding='utf-8') as f_load:
#
#     json.dump(dic, f_load)
#     print('加载文件完成......')

title = "1.101-中国银监会办公厅关于票据业务风险提示的通知.docx"

with open('law_library_data.json', 'r', encoding='utf-8') as f:

    j_dict = json.load(f)
    print(j_dict[title]['_source']['additionFileds']['fullText'])
