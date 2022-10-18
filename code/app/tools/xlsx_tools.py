from xlsxwriter.workbook import Workbook

# 序列1仅有的字符的标签（deleted lab）
LAB_SEQ1_UNIQUE = '-'

# 序列2仅有的字符的标签（added lab）
LAB_SEQ2_UNIQUE = '+'

# 序列1和序列2共有的字符的标签(common lab)
LAB_SEQ1_SE2_COMMON = ' '

# 序列1和序列2不共有的字符的标签(changed lab)
LAB_SEQ1_SE2_NOT_COMMON = '^'

XLSX_TABLE_FONT_SIZE = 14

XLSX_TABLE_COLOR_DICT = {
    LAB_SEQ2_UNIQUE: {'font_color': 'green', 'font_size': XLSX_TABLE_FONT_SIZE},
    LAB_SEQ1_SE2_NOT_COMMON: {'font_color': 'orange', 'font_size': XLSX_TABLE_FONT_SIZE},
    LAB_SEQ1_UNIQUE: {'font_color': 'pink', 'font_size': XLSX_TABLE_FONT_SIZE},
    LAB_SEQ1_SE2_COMMON: {'font_color': 'black', 'font_size': XLSX_TABLE_FONT_SIZE},
    '#':{'font_color': 'black', 'font_size': XLSX_TABLE_FONT_SIZE}
}

del_add_format = {'font_color': 'blue', 'font_size': XLSX_TABLE_FONT_SIZE}
text_wrap_format = {'font_color': 'black', 'font_size': XLSX_TABLE_FONT_SIZE}

# 设置换行
cell_format_set_text_wrap = {'align': 'center', 'valign': 'vcenter', 'border': 1}
cell_format_set_text_wrap2 = {'valign': 'vcenter', 'border': 1}


def __set_title(workbook, worksheet, *args):
    """
    设置表头

    :param workbook: xlsx文档
    :param worksheet:xlsx文档的sheet
    :param args:表头的字符串
    :return:
    """
    title_cell_format = workbook.add_format({
        'font_size': XLSX_TABLE_FONT_SIZE, 'align': 'center',
        'valign': 'vcenter', 'border': 1
    })
    for i, a in enumerate(args):
        worksheet.write(0, i, a, title_cell_format)


def __set_color_string_column(workbook, worksheet, row: int, col: int,
                              content_list: 'str', highlight_dict_list: 'list[dict]'):
    """
    设置一段的颜色
    :param workbook:
    :param worksheet:
    :param row:
    :param col:
    :param content_list:
    :param highlight_dict_list:
    :return:
    """
    # print('写文件——————————————————————————————————————————————————————', row, col)
    # print('content_list:', content_list, 'highlight_dict_list:', highlight_dict_list)
    if not content_list:  # 原句被删除或添加
        font = workbook.add_format(del_add_format)
        text_wrap = workbook.add_format(cell_format_set_text_wrap)
        text_wrap.set_text_wrap()
        worksheet.write_rich_string(row, col, font, '原句被删除', font, '或新添加', text_wrap)
        return
    else:
        args = []
        for i, content in enumerate(content_list):

            if highlight_dict_list[i]:  # 字典非空
                highlight_list = sorted(highlight_dict_list[i].keys(), key=lambda x: x[0])
                highlight_dict = highlight_dict_list[i]

                if len(highlight_list) == 1:
                    font_color = XLSX_TABLE_COLOR_DICT[highlight_dict[highlight_list[0]]]  # 该片段颜色
                    font_format = workbook.add_format(font_color)
                    args.extend(
                        (font_format, content[0:len(content) // 2], font_format, content[len(content) // 2:] + '\n'))
                    continue

                for s, t in highlight_list:
                    font_color = XLSX_TABLE_COLOR_DICT[highlight_dict[(s, t)]]  # 该片段颜色
                    font_format = workbook.add_format(font_color)
                    args.extend((font_format, content[s:t]))
                args[-1] += '\n'
            else:  # 字典为空
                font_format = workbook.add_format(text_wrap_format)
                args.extend(
                    (font_format, content[0:len(content) // 2], font_format, content[len(content) // 2:] + '\n'))
        text_wrap = workbook.add_format(cell_format_set_text_wrap2)
        text_wrap.set_text_wrap()
        args.append(text_wrap)
        worksheet.write_rich_string(row, col, *args)


def gen_xlsx(new_result_list1: 'list[dict]', new_result_list2: 'list[dict]', download_path: str):
    """
    写入xlsx
    :param new_result_list1:
    :param new_result_list2:
    :param download_path:
    :return:
    """

    workbook = Workbook(download_path)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:C', 80)

    __set_title(workbook, worksheet, '文档1', '文档2', '备注')

    count = 1
    for i, main_clause1 in enumerate(new_result_list1):
        main_clause2 = new_result_list2[i]
        for j, sub_clause1 in enumerate(main_clause1):
            sub_clause2 = main_clause2[j]

            __set_color_string_column(
                workbook, worksheet, count, 0,
                sub_clause1['content'], sub_clause1['highlight_dict'])
            __set_color_string_column(
                workbook, worksheet, count, 1,
                sub_clause2['content'], sub_clause2['highlight_dict'])
            count += 1

    workbook.close()
