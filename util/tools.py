# coding=utf-8
# Date: 11-12-8
# Time: 下午10:28
import hashlib
import json
import logging
import threading
import datetime
import traceback
import urllib2
import uuid
from xml.dom import minidom

__author__ = u'王健'

wechatObjLock = threading.RLock()
dispatchRealNameLock = threading.RLock()
log = logging.getLogger('django')



def get_html_signature(token, timestamp, openid):
    tmp_list = [str(token), str(timestamp), str(openid)]
    tmp_list.sort()
    tmp_str = ''.join(tmp_list)
    return hashlib.sha1(tmp_str).hexdigest()


def format_row_data(data_array):
    res = []
    for i in data_array:
        if type(i) == float:
            if float(int(i)) == i:
                res.append(int(i))
            else:
                res.append(i)
        else:
            res.append(i)
    return res


def strMD5(str):
    if type(str) == unicode:
        str = str.encode('utf-8')
    return hashlib.md5(str).hexdigest().upper()


def parse_data(data):
    if data.startswith('<result>1</result>'):
        data = data.replace('<result>1</result>', '')
        result = {}
        if type(data) == unicode:
            data = data.encode('utf-8')
        elif type(data) == str:
            pass
        else:
            data = str(data)

        doc = minidom.parseString(data)

        params = [ele for ele in doc.childNodes[0].childNodes
                  if isinstance(ele, minidom.Element)]

        for param in params:
            if param.childNodes:
                text = param.childNodes[0]
                result[param.tagName] = text.data
        return result
    else:
        return None


def common_except_log():
    print('\n**common_except_log**\n' + traceback.format_exc())
