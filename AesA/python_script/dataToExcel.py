# 内建模块
import os
import re
# Excel模块（扩展模块）
import xlrd
import xlwt
from xlutils.copy import copy

import functools


def init_workbook(path):
    # 判断Excel文件是否存在
    if not os.path.exists(path):

        # 打开工作簿，添加工作表
        w_workbook = xlwt.Workbook()
        w_sheet = w_workbook.add_sheet('data', cell_overwrite_ok=True)

        # 工作表的表头
        row_head = ['info', 'enThreadAvg(A)', 'enThreadAvg(PD)', 'enThreadAvg(PS)', 'info', 'enTimeAvg(A)',
                    'enTimeAvg(PD)', 'enTimeAvg(PS)']

        # 设置字体样式
        cell_font = xlwt.Font()
        cell_font.bold = True
        cell_style = xlwt.XFStyle()
        cell_style.font = cell_font

        # 写入表头
        for ncols in range(0, len(row_head)):
            w_sheet.write(0, ncols, row_head[ncols], cell_style)

        # 保存工作簿
        w_workbook.save(path)


def order_cmp(order1, order2):
    order_i_1 = 0
    order_i_2 = 0
    for i, order in enumerate(["b", "k", "m"]):
        if order1 == order:
            order_i_1 = i
        if order2 == order:
            order_i_2 = i
    return order_i_1 - order_i_2


def info_cmp(info1, info2):
    info_match1 = re.match("([0-9]+)([a-z])([0-9]+)C([0-9]+)T", info1)
    info_match2 = re.match("([0-9]+)([a-z])([0-9]+)C([0-9]+)T", info2)
    if info_match1 and info_match2:
        if order_cmp(info_match1.group(2), info_match2.group(2)) > 0:
            return 1
        elif order_cmp(info_match1.group(2), info_match2.group(2)) < 0:
            return -1
        else:
            for i in (1, 3, 4):
                if int(info_match1.group(i)) > int(info_match2.group(i)):
                    return 1
                elif int(info_match1.group(i)) < int(info_match2.group(i)):
                    return -1
                else:
                    if i == 4:
                        return 0


def dict_item_cmp(item1, item2):
    return info_cmp(item1[0], item2[0])


def main():
    # set path
    out_dir = "../out"
    save_path = "../data/dataToExcel.xls"
    out_arachne_enable_avg_dir = os.path.join(out_dir, "ArachneEnable/avg")
    out_pthread_diff_core_avg_dir = os.path.join(out_dir, "PthreadDiffCore/avg")
    out_pthread_sibling_core_avg_dir = os.path.join(out_dir, "PthreadSiblingCore/avg")

    # init workbook
    init_workbook(save_path)
    r_workbook = xlrd.open_workbook(save_path, formatting_info=True)
    w_workbook = copy(r_workbook)
    w_worksheet = w_workbook.get_sheet(0)

    # get info_to_detail_dict
    info_to_detail_dict = {}
    for fileDir in (out_arachne_enable_avg_dir, out_pthread_diff_core_avg_dir, out_pthread_sibling_core_avg_dir):
        for root, dirs, files in os.walk(fileDir):
            for fileName in files:
                file_name_match = re.match("([0-9a-z]+)_([a-zA-Z]+)_([0-9]+)core_([0-9]+)thread_avg", fileName)
                if file_name_match:
                    info = file_name_match.group(1) + file_name_match.group(3) + "C" + file_name_match.group(4) + "T"
                    mode = file_name_match.group(2)
                    with open(os.path.join(fileDir, fileName), "r") as fin:
                        for line in fin:
                            line_match = re.match("EnThreadAvg: ([0-9]*[.]?[0-9]*) ms EnTimeAvg: ([0-9]*[.]?[0-9]*) ms",
                                                  line)
                            if line_match:
                                if info not in info_to_detail_dict.keys():
                                    detail_dict = {}
                                else:
                                    detail_dict = info_to_detail_dict[info]
                                detail_dict['EnThreadAvg_' + mode] = float(line_match.group(1))
                                detail_dict['EnTimeAvg_' + mode] = float(line_match.group(2))
                                info_to_detail_dict[info] = detail_dict
    info_to_detail_list = sorted(info_to_detail_dict.items(), key=functools.cmp_to_key(dict_item_cmp))
    # print(info_to_detail_dict)
    row = 1
    for info_to_detail in info_to_detail_list:
        w_worksheet.write(row, 0, info_to_detail[0])
        w_worksheet.write(row, 1, info_to_detail[1]["EnThreadAvg_ArachneEnable"])
        w_worksheet.write(row, 2, info_to_detail[1]["EnThreadAvg_PthreadDiffCore"])
        w_worksheet.write(row, 3, info_to_detail[1]["EnThreadAvg_PthreadSiblingCore"])
        w_worksheet.write(row, 4, info_to_detail[0])
        w_worksheet.write(row, 5, info_to_detail[1]["EnTimeAvg_ArachneEnable"])
        w_worksheet.write(row, 6, info_to_detail[1]["EnTimeAvg_PthreadDiffCore"])
        w_worksheet.write(row, 7, info_to_detail[1]["EnTimeAvg_PthreadSiblingCore"])
        row += 1
    w_workbook.save(save_path)


if __name__ == "__main__":
    main()
