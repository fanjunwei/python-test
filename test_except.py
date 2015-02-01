# coding=utf-8
# Date: 15/1/28
# Time: 18:19
# Email:fanjunwei003@163.com

__author__ = u'范俊伟'

import traceback


def except_log():
    ss= traceback.format_exc()
    print ss


try:
    1 / 0
except Exception, e:
    except_log()