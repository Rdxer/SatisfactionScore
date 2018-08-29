# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午5:40
# @Author  : Rdxer
# @Email   : Rdxer@foxmail.com
# @File    : test.py
# @Software: PyCharm


import re
import datetime

h = "11、对幼儿性格和兴趣方面培养方面，您还满意吗？（请用五分制表示，5分代表非常满意，1分代表非常不满意）"

if __name__ == '__main__ 1':
    # pattern = re.compile('^([0-9]+)、')
    # m = pattern.findall(h)
    # print(m)

    # regs = '^.*\.(xlsx|xls)'
    regs = '^[^>].*\.(xlsx|xls)$'

    pattern = re.compile(regs)

    # h = ">满意度分数.xls"
    h = "满意度分数.xlsx"

    print(re.match(regs, h))




if __name__ == '__main__':
    str = '2018-08-01'
    str_end = '2018-08-07'

    date_time = datetime.datetime.strptime(str, '%Y-%m-%d')
    date_time_end = datetime.datetime.strptime(str_end, '%Y-%m-%d')

    print(date_time)
    print(date_time_end)

    print("=======")

    print(date_time.strftime('%Y-%m-%d'))
    print(date_time_end.strftime('%Y-%m-%d'))

    print("=======")

    # datetime.timedelta(days=1)

    print(date_time_end - date_time)

    interval = date_time_end - date_time

    print(interval.days)

    for offset in range(interval.days+1):
         date = date_time + datetime.timedelta(days=offset)
         print(date.strftime('%Y-%m-%d'))

