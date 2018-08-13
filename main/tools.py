# -*- coding: utf-8 -*-
# @Time    : 2018/8/13 下午5:15
# @Author  : Rdxer
# @Email   : Rdxer@foxmail.com
# @File    : tools.py
# @Software: PyCharm


import os


def get_filePath_fileName_fileExt(filepath):
    """
    获取文件路径、文件名、后缀名
    :param filepath: 
    :return: 
    """
    (filepath,tempfilename) = os.path.split(filepath)
    (shotname,extension) = os.path.splitext(tempfilename)
    return filepath,shotname,extension