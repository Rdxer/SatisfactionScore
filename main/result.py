# -*- coding: utf-8 -*-
# @Time    : 2018/8/22 上午10:45
# @Author  : Rdxer
# @Email   : Rdxer@foxmail.com
# @File    : result.py
# @Software: PyCharm
from main import ConfigObject, conf
from main.model import AnswerRecord, Question


class ResultColValue:
    """
    列值
    """

    title:str = ""
    # key key 对应
    nps_value = {}

    # key key 对应
    not_infer_value = {}

    # key key 对应
    infer_group_value = {}

    # 数据
    rowDataList: list = []
    total = -1

    def __init__(self,rowDataList:list,resultMate):
        self.nps_value = {}
        self.not_infer_value = {}
        self.infer_group_value = {}
        self.rowDataList = rowDataList
        self.total = len(rowDataList)
        self.resultMate = resultMate


    def cal_nps_dict(self):
        # 计算 净推荐值

        count9_10_dict = {}
        count0_6_dict = {}
        rowData: AnswerRecord
        for rowData in self.rowDataList:
            for (key, v) in self.resultMate.nps.items():
                que: Question = rowData.tryGetQuestion(key)
                if que != None:
                    v = que.tryGetIntValue()
                    if v is not None:

                        if v >= 9 and v <= 10:
                            count9_10 = count9_10_dict.get(key, 0)
                            count9_10 += 1
                            count9_10_dict[key] = count9_10
                        elif v >= 0 and v <= 6:
                            count0_6 = count0_6_dict.get(key, 0)
                            count0_6 += 1
                            count0_6_dict[key] = count0_6

        for (key, v) in self.resultMate.nps.items():
            count9_10 = count9_10_dict.get(key)
            count0_6 = count0_6_dict.get(key)
            cal_v = (count9_10 - count0_6) / self.total * 100
            self.nps_value[key] = cal_v

    def cal_not_infer_value(self):

        sumDict = {}
        countDict = {}
        rowData: AnswerRecord

        for rowData in self.rowDataList:
            for (key, v) in self.resultMate.not_infer.items():
                que: Question = rowData.tryGetQuestion(key)
                if que != None:
                    v = que.tryGetIntValue()
                    if v is not None:
                        # 只统计 不为 空的项
                        sum = sumDict.get(key,0)
                        count = countDict.get(key,0)
                        sum += v
                        count += 1
                        sumDict[key] = sum
                        countDict[key] = count

        for (key, v) in self.resultMate.not_infer.items():

            co = countDict.get(key,0)
            su = sumDict.get(key,0)

            if v.calculateType == conf.configCalculateType_scale:
                rowCount = self.total

                if co == 0 or rowCount == 0:
                    self.not_infer_value[key] = conf.cal_empty_value
                else:
                    scale = co / rowCount
                    scale *= 100
                    self.not_infer_value[key] = scale
            else:
                if co == 0:
                    self.not_infer_value[key] = conf.cal_empty_value
                else:
                    avg = ((su / co) - 1) * 25
                    self.not_infer_value[key] = avg

    def cal_infer_value(self):
        """
        计算推导项
        """

        for (group_name,v) in self.resultMate.infer_group.items():
            configGroupItem = v[0]
            col_list = v[1]
            group_value = self.infer_group_value.get(group_name,(0,{}))
            group_value_list = group_value[1]

            sumDict = {}
            countDict = {}

            rowData: AnswerRecord
            for rowData in self.rowDataList:

                for (key, v) in col_list.items():
                    que: Question = rowData.tryGetQuestion(key)
                    if que != None:
                        v = que.tryGetIntValue()
                        if v is not None:
                            # 只统计 不为 空的项
                            sum = sumDict.get(key, 0)
                            count = countDict.get(key, 0)
                            sum += v
                            count += 1
                            sumDict[key] = sum
                            countDict[key] = count

            for (key, v) in col_list.items():

                co = countDict.get(key,0)
                su = sumDict.get(key,0)

                if v.configCalculateItem.calculateType == conf.configCalculateType_scale:

                    rowCount = self.total

                    if rowCount == 0 or co == 0:
                        group_value_list[key] = conf.cal_empty_value
                    else:
                        scale = co / rowCount
                        scale *= 100
                        group_value_list[key] = scale
                else:
                    if su == 0 or co == 0:
                        group_value_list[key] = conf.cal_empty_value
                    else:
                        avg = ((su / co) - 1) * 25
                        group_value_list[key] = avg

            sum = 0
            for (k, value) in col_list.items():
                group_item_value = group_value_list.get(k)
                v = group_item_value * value.stand_weight
                sum += v

            group_avg = sum / len(col_list)

            self.infer_group_value[group_name] = (group_avg,group_value_list)


class ResultMate:
    """
    输出结果
    """

    # 表名
    name:str = ""

    # 净推荐值
    nps = {}

    # 不进行推导的列
    not_infer = {}

    # 进行推导的列的分组 {name : {}}
    infer_group = {}


    def __init__(self,confObj:ConfigObject):

        # 初始化
        self.nps = {}
        self.not_infer = {}
        self.infer_group = {}

        # 1. name
        self.name = confObj.name

        # 2. 净推荐值
        if confObj.nps != -1:
            self.nps[confObj.nps] = conf.nps_defaultname


        # 3. 不推导
        for item in confObj.configNotInferCalculateItems:
            self.not_infer[item.index] = item

        # 4. 推导的
        for groupItem in confObj.configGroupItems:

            itemDict = self.infer_group.get(groupItem.name, (groupItem, {}))[1]

            for item in groupItem.itemList:
                itemDict[item.index] = item

            self.infer_group[groupItem.name] = (groupItem, itemDict)


def genColResult(colTitle:str,rowDataList:list,resultMate:ResultMate):
    """
    根据 行数据集合 生成 结果列
    :param name: 列名
    :param rowDataList:行数据集合
    :param resultMate:结果元数据
    :return: ResultColValue
    """

    resColValue = ResultColValue(rowDataList,resultMate)
    resColValue.title = colTitle

    # 计算

    # 计算 纯推荐值
    resColValue.cal_nps_dict()

    # 计算 不 推导的项
    resColValue.cal_not_infer_value()

    # 计算 推导的项
    resColValue.cal_infer_value()



    return  resColValue

def genSheetResult(sheetName:str,allRowDataList:list,confObj:ConfigObject):
    """
    :param sheetName: 表名
    :param allRowDataList: 所有的行数据
    :param confObj: 表对应的配置
    :return: (ResultMeta,dict(ResultColValue))
    """

    resMeta = ResultMate(confObj)


    resColValueDict = {}


    allColValue = genColResult(conf.all_defaultname,allRowDataList,resMeta)

    resColValueDict[conf.all_defaultname] = allColValue

    # 分组
    groupDict = {}
    for rowData in allRowDataList:
        que: Question = rowData.tryGetQuestion(confObj.projectIndex)
        if que != None:
            v = que.value
            if v is not None:
                groupRowList = groupDict.get(v, [])
                groupRowList.append(rowData)
                groupDict[v] = groupRowList

    for (name,rowDataList) in groupDict.items():

        colValue = genColResult(name, rowDataList, resMeta)

        resColValueDict[name] = colValue

    return resMeta,resColValueDict

