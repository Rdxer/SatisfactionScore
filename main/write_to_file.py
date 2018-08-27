# -*- coding: utf-8 -*-
# @Time    : 2018/8/22 下午4:31
# @Author  : Rdxer
# @Email   : Rdxer@foxmail.com
# @File    : write_to_file.py
# @Software: PyCharm
import xlsxwriter

from main import tools, conf,parser_conf
import os


from main.result import ResultMeta,ResultColValue


def writeToFile(dirPath:str,sheetResList:list):

    resFileName = conf.defaultResultFileName.format(tools.fileNameTimeString())

    path = os.path.join(dirPath,resFileName)

    # print(resFileName)
    # print(path)

    wb = xlsxwriter.Workbook(path)

    color_format = wb.add_format({'color': 'red'})
    bg_format = wb.add_format({'color': 'red'})
    bg_format.set_bg_color('#ccccc')


    # 设置表 的 第一列
    resMeta:ResultMeta
    colValueDict:dict
    resColValue:ResultColValue
    for (resMeta,colValueDict) in sheetResList:
        # 1
        table = wb.add_worksheet(resMeta.name)

        resMeta.colValueDictKey_order = list(colValueDict.keys())

        startCol = 1
        titleRow = 0
        col = 0
        # 设置 表 头
        for index in range(len(resMeta.colValueDictKey_order)):
            col = startCol + index
            colVKey = resMeta.colValueDictKey_order[index]
            # resColValue = colValueDict.get(colVKey)
            table.write_string(titleRow, col, "{}".format(colVKey))

        table.set_column(0,col,15)


        # 设置 行 头
        startRow = 1
        currRow = startRow


        # 净推荐值
        if len(resMeta.nps) == 1:
            table.write_string(currRow, 0, conf.nps_defaultname,bg_format)

            # 设置净推荐值
            for index in range(len(resMeta.colValueDictKey_order)):
                col = startCol + index
                colVKey = resMeta.colValueDictKey_order[index]
                resColValue = colValueDict.get(colVKey)
                # table.write_string(currRow, col, tools.value(resColValue))

                fv = list(resColValue.nps_value.values())[0]

                fv = tools.fillNumberValue(fv)

                table.write_number(currRow, col, fv,bg_format)

            currRow += 1


        citem:parser_conf.ConfigCalculateItem
        confGroItem:parser_conf.ConfigGroupItem
        citem:parser_conf.ConfigItem
        confItemDict:dict

        resMeta.not_infer_key_order =  list(resMeta.not_infer.keys())

        for k in resMeta.not_infer_key_order:
            citem = resMeta.not_infer[k]
            table.write_string(currRow, 0, citem.name)

            # 设置 不推导的数据 值
            for index in range(len(resMeta.colValueDictKey_order)):
                col = startCol + index
                colVKey = resMeta.colValueDictKey_order[index]
                resColValue = colValueDict.get(colVKey)
                # table.write_string(currRow, col, tools.value(resColValue))

                fv = resColValue.not_infer_value.get(k,conf.cal_empty_value)

                fv = tools.fillNumberValue(fv)

                table.write_number(currRow, col, fv)

            currRow += 1

        resMeta.infer_group_name_order = list(resMeta.infer_group.keys())
        for k in resMeta.infer_group_name_order:

            (confGroItem,confItemDict) = resMeta.infer_group[k]
            resMeta.infer_group_value_key_order[k] = list(confItemDict.keys())

            table.write_string(currRow, 0, k,bg_format)

            # 设置 推导的数据 推导值
            for index in range(len(resMeta.colValueDictKey_order)):
                col = startCol + index
                colVKey = resMeta.colValueDictKey_order[index]
                resColValue = colValueDict.get(colVKey)
                # table.write_string(currRow, col, tools.value(resColValue))

                fv = resColValue.infer_group_value.get(k)[0]

                fv = tools.fillNumberValue(fv)

                table.write_number(currRow, col, fv,bg_format)

            currRow += 1

            for itemKey in resMeta.infer_group_value_key_order[k]:
                citem = confItemDict[itemKey]
                table.write_string(currRow, 0, citem.name)

                # 设置 推导的数据 用于推导的值
                for index in range(len(resMeta.colValueDictKey_order)):
                    col = startCol + index
                    colVKey = resMeta.colValueDictKey_order[index]
                    resColValue = colValueDict.get(colVKey)
                    resCVList = resColValue.infer_group_value.get(k)[1]

                    fv = resCVList.get(itemKey)

                    fv = tools.fillNumberValue(fv)

                    table.write_number(currRow, col, fv)

                currRow += 1










    wb.close()

    print("结果表: "+path)

    # gg
