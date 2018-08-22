# -*- coding: utf-8 -*-
# @Time    : 2018/8/22 上午11:25
# @Author  : Rdxer
# @Email   : Rdxer@foxmail.com
# @File    : test_list_clone.py
# @Software: PyCharm


if __name__ == '__main__':
    # print(__name__)
    list1 = ["1","2","3","4","5"]

    list2 = list1.copy()

    list2.remove("1")

    print(list1)
    print(list2)



