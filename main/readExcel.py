# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午4:46
# @Author  : Rdxer
# @Email   : Rdxer@foxmail.com
# @File    : readExcel.py
# @Software: PyCharm

import xlrd
import os
from main import model,parser_conf,tools,conf


def read(excelFilePath):

    path,name,ex = tools.get_filePath_fileName_fileExt(excelFilePath)

    confObj = parser_conf.ParserConf(os.path.join(path,name)+conf.configFileEx)

    # print(confObj)

    ExcelFile = xlrd.open_workbook(excelFilePath)

    sheet = ExcelFile.sheet_by_index(0)

    tableHeader = sheet.row_values(0)  # 表头

    resList = []

    for index in range(1,sheet.nrows):
        rowv = sheet.row_values(index)
        ar = model.AnswerRecord(tableHeader,rowv)
        resList.append(ar)

        ar.setConfigObj(confObj)

    return resList


if __name__ == '__main__':

    modelList = read("/Users/Rdxer/Desktop/原始数据+txt/第一教育.xls")
    print(modelList)

    #
    #
    # listConvertFails = []
    #
    # # 筛选
    # for m in listModel:
    #     # print(m.id)
    #     for q in m.questionList:
    #         try:
    #             if len(q.value) != 0:
    #                 temp = q.intValue()
    #         except:
    #             listConvertFails.append(m.questionList.index(q))
    #
    # for m in listModel:
    #     for index in range(0,len(m.questionList)):
    #         if index not in listConvertFails:
    #             m.analyisQuestionList.append(m.questionList[index])
    #
    # # jisuan
    # for m in listModel:
    #     # print(m.id)
    #     for q in m.analyisQuestionList:
    #         print(q.value)
