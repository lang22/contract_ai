from docx import Document
from docx.shared import *
from docx.enum.text import WD_COLOR_INDEX


# 输入文档所在路径  如‘D:/docx/协议.docx’
# 返回 文档中高亮显示的段落 组成的 list

# 输入文档路径 得到文档中高亮段落组成的list
def get_highlight_paragraphs(filename):
    document = Document(filename)
    return_string = []
    for i_para in document.paragraphs:
        string = ''
        for run in i_para.runs:
            if run.font.highlight_color != None:
                string += run.text
        if string != '':
            # print (string)
            return_string.append(string)
    final_return_string = []
    for item in return_string:
        item = item.strip()
        item = ''.join(item.split())
        final_return_string.append(item)
    return final_return_string


# 测试
if __name__ == '__main__':
    string_list = get_highlight_paragraphs('source_data/HR-CK-05-E-债权转让协议（信托计划下回购特定资产形成债权）_标注.docx')
    for item in string_list:
        print(item)
