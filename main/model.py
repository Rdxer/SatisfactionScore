# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午2:54
# @Author  : Rdxer
# @Email   : Rdxer@foxmail.com
# @File    : parser_conf.py.py
# @Software: PyCharm

import re
import main.conf
import main.parser_conf






class Question:
    index=0
    desc=""
    value=""
    intvalue=-1


    def __init__(self, i, h, r):
        self.index = int(i)
        self.desc = h
        self.value = r


    def tryGetIntValue(self):
        """
        :return: None | int value
        """
        try:
            return self.intValue()
        except:
            return None


    def isIntValue(self):
        try:
            self.intValue()
            return True
        except:
            return False

    def intValue(self):
        """

        :return:Int
        """

        if self.intvalue != -1:
            return self.intvalue

        if self.value=="极有可能":
            self.intvalue = 10

        elif self.value=="不可能":
            self.intvalue = 1

        v= int(self.value)

        return v


class AnswerRecord:
    # 序号
    id = 0
    # 提交答卷时间
    commitAt = ""
    # 所用时间
    totalTime = ""
    # 来源
    source = ""
    # 来源详情
    sourceDetails = ""
    # 来自IP
    ip = ""

    questionList = []
    questionGroupBy = None
    analysisQuestionList = []

    header = []
    rowv = []

    configObj = main.parser_conf.ConfigObject()

    def __init__(self, _header, _rowv):
        self.header = _header
        self.rowv = _rowv
        self.questionList =[]
        self.analysisQuestionList =[]
        pattern = re.compile(main.conf.questionRegStr, re.I)
        for index in range(0,len(self.header)):

            h = self.header[index]
            r = self.rowv[index]

            if h == "序号":
                self.id = r
            elif h == "提交答卷时间":
                self.commitAt=r
            elif h == "所用时间":
                self.totalTime=r
            elif h == "来源":
                self.source =r
            elif h == "来源详情":
                self.sourceDetails=r
            elif h == "来自IP":
                self.ip=r
            else:
                m = pattern.findall(h)
                #print(m)  # 匹配成功，返回一个 Match 对象
                if len(m) > 0:
                    q = Question(m[0],h,r)
                    self.questionList.append(q)
                else:
                    pass

    def setConfigObj(self,conObj):
        self.configObj = conObj
        self.execFilter(self.configObj.configCalculateItems)
        self.questionGroupBy = self.tryGetQuestion(self.configObj.projectIndex)
        if self.questionGroupBy == None:
            print("找不到 分组"+conObj.projectIndex)
            exit(400)


    def execFilter(self,needCol):
        """
        过滤需要分析的列
        :param needCol:需要分析的列
        """
        for col in needCol:
            for q in self.questionList:
                if q.index == col.index:
                    self.analysisQuestionList.append(q)
                else:
                    # print("no ")
                    pass

    def tryGetQuestion(self,index):
        for q in self.questionList:
            if q.index == index:
                return q



