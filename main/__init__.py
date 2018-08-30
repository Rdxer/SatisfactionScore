# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午2:14
# @Author  : Rdxer
# @Email   : Rdxer@foxmail.com
# @File    : parser_conf.py.py
# @Software: PyCharm

import datetime
import sys
import os
import os.path
import re
import main.parser_conf
from main.parser_conf import *
from main import readExcel,conf
from main.model import AnswerRecord,Question



import main.result as result
from main.write_to_file import writeToFile


def filtrFile(dirPath):
    excelList = []
    for parent, dirnames, filenames in os.walk(dirPath, followlinks=False):
        for filename in filenames:

            # print('文件名：%s' % filename)
            # print('文件完整路径：%s\n' % file_path)

            if re.match(conf.excelRegStr, filename) != None:
                file_path = os.path.join(parent, filename)
                excelList.append(file_path)

    # for f in excelList:
    #     print(f)
    return excelList


if __name__ == '__main__':


    # modelList = readExcel.read("/Users/Rdxer/Desktop/原始数据+txt/第一教育.xls")
    #
    # print(modelList)
    # print("请输入所在文件路径:\n")
    # dirPath = input()
    # dirPath = "E:/第一资产/配置文件/原始数据+txt(1)/"

    dirPath = "/Users/Rdxer/Desktop/test1"

    excelList = filtrFile(dirPath)

    for excel in excelList:
        print(excel)

    excelObjectList = []

    for excel in excelList:
        excelObjectList.append(readExcel.read(excel))

    sheetResList = []
    for excelObject in excelObjectList:

        confobj:ConfigObject = excelObject[0]
        excelDataList = excelObject[1]

        # exeCal()
        sheetRes = result.genSheetResult(confobj.name,excelDataList,confobj)

        sheetResList.append(sheetRes)

    # 写入文件
    writeToFile(dirPath,sheetResList)












