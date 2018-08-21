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
from main.parser_conf import *
from main import readExcel,conf
from main.model import AnswerRecord,Question


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

    for excelObject in excelDataList:

        sumDict = {}
        countDict = {}
        confobj:ConfigObject = excelObject[0]
        total = len(excelObject[1])

        groupDict = {}

        #  [9,10] (0,6]

        #    count([9,10]) - count((0,6]) / total
        count9_10 = 0
        count0_6 = 0

        rowData: AnswerRecord

        for rowData in excelObject[1]:

            if confobj.nps != -1:
                que:Question = rowData.tryGetQuestion(confobj.nps)
                if que != None:
                    v = que.tryGetIntValue()
                    if v is not None:

                        if v >= 9 and v <= 10:
                            count9_10 += 1
                        elif v >= 0 and v <= 6:
                            count0_6 += 1

            if confobj.projectIndex != -1:
                que: Question = rowData.tryGetQuestion(confobj.projectIndex)
                if que != None:
                    v = que.value
                    if v is not None:
                        groupRowList = groupDict.get(v,[])
                        groupRowList.append(rowData)
                        groupDict[v] = groupRowList

            col:Question
            for col in rowData.analysisQuestionList:

                sum = sumDict.get(col.index)
                count = countDict.get(col.index)

                if sum is None:
                    sum = 0

                if count is None:
                    count = 0

                intv = col.tryGetIntValue()
                if intv is not None:
                    sum += intv
                    count += 1

                sumDict[col.index] = sum
                countDict[col.index] = count


        print(groupDict.keys())

        print("{} {} {} {}%    <<<".format(count9_10,count0_6,total,(count9_10 - count0_6) / total * 100))
        print(sumDict)
        print("----")
        print(countDict)
        print("======")

        # print(excelObject[0])

        for key in sumDict.keys():
            co = countDict[key]
            su = sumDict[key]

            configCalculateItem = confobj.getConfigCalculateItem(key)

            if configCalculateItem.calculateType == conf.configCalculateType_scale:
                rowCount = len(excelObject[1])
                scale = co / rowCount
                scale *= 100
                print("{} {} {}%  {}".format(su, co, scale,rowCount))
            else:
                avg = ((su / co) - 1) * 25
                print("{} {} {}".format(su, co, avg))


        print("XXXXXXXXXXXXXX")








