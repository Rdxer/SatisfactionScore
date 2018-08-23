# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午2:54
# @Author  : Rdxer
# @Email   : Rdxer@foxmail.com
# @File    : parser_conf.py.py
# @Software: PyCharm


import main.conf as conf
import re

from main import tools


class ConfigCalculateItem:
    index = -1
    name = ""
    calculateType = conf.configCalculateType_5to100

    def __init__(self, line):
        componentList = re.split(conf.configLineSeparator, line)
        self.index = int(componentList[0])
        self.name = componentList[1].strip()

        if len(componentList) == 3 and componentList[2] == conf.configCalculateType_scale:
            self.calculateType = conf.configCalculateType_scale
        else:
            self.calculateType = conf.configCalculateType_5to100


class ConfigItem:
    index = -1
    name = ""
    weight = -1.0

    stand_weight = 0.0

    configCalculateItem:ConfigCalculateItem

    def __init__(self, line):
        componentList = re.split(conf.configLineSeparator, line)
        self.name = componentList[0].strip()
        self.weight = float(componentList[1].strip())




class ConfigGroupItem:
    '''
    配置:组
    '''
    name = ""

    itemList = []

    def __init__(self, content):
        # print("--")
        # print(content)
        # print("--")

        lines = re.split("\n", content)

        self.name = lines[0].strip()

        self.itemList = []

        sum = 0
        for line in lines[1:]:
            line = line.strip()
            if len(line) > 0:
                citem = ConfigItem(line)
                self.itemList.append(citem)
                sum += citem.weight

        for item in self.itemList:
            item.stand_weight = item.weight / sum


class ConfigObject:

    name:str = ""

    # 需要计算的全部
    configCalculateItems = []

    # 不需要推导的
    configNotInferCalculateItems = []

    # 需要推导的组
    configGroupItems = []

    projectIndex = -1
    nps = -1

    def __init__(self, filepath=None):

        if filepath == None:
            return

        try:
            f = open(filepath, 'r', encoding='utf-8')
        except:
            f = open(filepath, 'r', encoding='gbk')

        _filepath, _shotname, _extension = tools.get_filePath_fileName_fileExt(filepath)

        self.name = _shotname

        conent = f.read()

        if conent.startswith("\ufeff"):
            conent = conent[1:]

        group = conent.split(conf.configGroupSeparator)

        # 1. 需要计算的列
        self.configCalculateItems = []
        for item in group[0].splitlines():
            item = item.strip()
            if len(item) > 0:
                citem = ConfigCalculateItem(item)
                self.configCalculateItems.append(citem)

        # 2. 需要 推算的组
        self.configGroupItems = []
        for item in re.split("\n-", group[1]):
            item = item.strip()
            if len(item) > 0:
                citem = ConfigGroupItem(item)
                self.configGroupItems.append(citem)
                for i in citem.itemList:
                    for ci in self.configCalculateItems:
                        if ci.name == i.name:
                            i.index = ci.index
                            i.configCalculateItem = ci

        # 3. 分项 列
        self.projectIndex = int(group[2])

        # 4. 净推荐值 配置
        if len(group) == 4:
            self.nps = int(group[3])


        # 5. 不需要推导的

        self.configNotInferCalculateItems = self.configCalculateItems.copy()


        for groupItem in self.configGroupItems:
            for item in groupItem.itemList:
                # if ci.name == i.name:
                #     i.index = ci.index
                # item.index
                tempItems = self.configNotInferCalculateItems.copy()
                for nici in tempItems:
                    if nici.index == item.index:
                        self.configNotInferCalculateItems.remove(nici)

        ## end


    def getConfigCalculateItem(self,index):
        """
        根据 index 获取 计算列的配置
        :param index:
        :return:
        """
        for configCalculateItem in self.configCalculateItems:
            if index == configCalculateItem.index:
                return configCalculateItem
        return None

def ParserConf(filepath):
    """
    解析配置文件,转化成对象
    :param filepath:
    :return: ConfigObject
    """

    # conf = ConfigObject(os.path.join(filepath,"第一教育.txt"))
    conf = ConfigObject(filepath)

    isexit = False

    # check 计算的列
    for gi in conf.configGroupItems:
        for i in gi.itemList:
            if i.index == -1:
                print("Error: 配置文件[{}]错误".format(conf.name))
                print("Reason: 推导的组[{}]中 [{}] 列不存在".format(gi.name ,i.name ))
                isexit = True

    if isexit:
        key = input("退出...")
        # if key.lower() == "q":
        print("正在退出...")
        exit(9)

    return conf
