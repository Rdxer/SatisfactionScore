# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午5:40
# @Author  : Rdxer
# @Email   : Rdxer@foxmail.com
# @File    : test.py
# @Software: PyCharm


import re

h = "11、对幼儿性格和兴趣方面培养方面，您还满意吗？（请用五分制表示，5分代表非常满意，1分代表非常不满意）"

if __name__ == '__main__':
    # pattern = re.compile('^([0-9]+)、')
    # m = pattern.findall(h)
    # print(m)

    # regs = '^.*\.(xlsx|xls)'
    regs = '^[^>].*\.(xlsx|xls)$'

    pattern = re.compile(regs)

    # h = ">满意度分数.xls"
    h = "满意度分数.xlsx"

    print(re.match(regs, h))




