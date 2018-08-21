# -*- coding: utf-8 -*-
# @Time    : 2018/8/21 下午2:51
# @Author  : Rdxer
# @Email   : Rdxer@foxmail.com
# @File    : math_test.py
# @Software: PyCharm

import scipy
import numpy


if __name__ == '__main__':
    list = numpy.sqrt([13, 53])
    ji = list[0] * list[1]
    v = 20/ji
    a = numpy.arccos(v)
    # 弧度
    print(a/numpy.pi * 180)




