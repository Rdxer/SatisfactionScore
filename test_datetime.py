# -*- coding: utf-8 -*-
# @Time    : 2018/8/29 下午4:35
# @Author  : Rdxer
# @Email   : Rdxer@foxmail.com
# @File    : test_datetime.py
# @Software: PyCharm

from datetime import datetime,timedelta

def date_correction(date1_str:str,date2_str:str,input_format='%Y-%m-%d'):
    """
    排队
    :param date1_str:
    :param date2_str:
    :param input_format:
    :return:
    """
    date1 = datetime.strptime(date1_str, input_format)
    date2 = datetime.strptime(date2_str, input_format)

    if date1 > date2:
        return date2,date1
    return date1, date2



def gen_date_list(start_date_str:str, end_date_str:str, input_format='%Y-%m-%d', out_format='%Y-%m-%d'):
    """
    start = "2018-11-01"
    end = "2018-01-01"
    res = gen_date_list(start,end)
    print(res)
    :param start_date_str: 开始时间字符串
    :param end_date_str: 结束字符串
    :param input_format: 输入字符串格式
    :param out_format: 输出格式
    :return: list
    """

    start_date = datetime.strptime(start_date_str, input_format)
    end_date = datetime.strptime(end_date_str, input_format)

    resList = []

    interval =  end_date - start_date

    if interval.days < 0:
        temp = start_date
        start_date = end_date
        end_date =temp

        interval = end_date - start_date

    for offset in range(interval.days+1):
         date = start_date + timedelta(days=offset)
         resList.append(date.strftime(out_format))

    return resList


if __name__ == '__main__':

    start = "2018-11-01"
    end = "2018-01-01"

    res = gen_date_list(start,end)

    print(res)

    print(res[-1])
