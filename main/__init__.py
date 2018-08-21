# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午2:14
# @Author  : Rdxer
# @Email   : Rdxer@foxmail.com
# @File    : parser_conf.py.py
# @Software: PyCharm

import sys
import os
import os.path
import re
import main.parser_conf
from main import readExcel,conf


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

    dirPath = "/Users/Rdxer/Desktop/原始数据+txt/"
    excelList = filtrFile(dirPath)

    for excel in excelList:
        print(excel)


    excelDataList = []

    for excel in excelList:
        excelDataList.append(readExcel.read(excel))

    # print(excelDataList)
    #
    # print(excelDataList[0][0].ip)
    #
    #
    #
    #



    for excelData in excelDataList:

        
        sumDict = {}
        for rowData in excelData:
            for col in rowData.analysisQuestionList:
                sum = sumDict.get(str(col.index))
                if sum is None:
                    sum = 0

                intv = col.tryGetIntValue()
                if intv is not None:
                    sum += intv

                sumDict[str(col.index)] = sum

        print(sumDict)




