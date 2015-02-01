# coding=utf-8
import base64
import hashlib
import mimetypes
import struct
import threading
import time
import datetime
import urllib
import urllib2
import uuid
from xml.dom import minidom
import requests

__author__ = 'fanjunwei003'


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


def identify(file_path):
    try:
        url = 'http://eng.ccyunmai.com:5008/SrvEngine'
        action = 'idcard'
        username = 'testbjllkj'
        key = str(uuid.uuid1())
        time_str = str(int(time.time() * 1000))
        password = 'sjsj34953sdkdsu5ssek234ksd234dswpoiu'
        verify = strMD5(action + username + key + time_str + password)
        file = open(file_path, 'rb')
        data = '''<action>%s</action>
<client>%s</client>
<system>ubuntu</system>
<key>%s</key>
<time>%s</time>
<verify>%s</verify>
<file>%s</file>
<ext>jpg</ext>''' % (action, username, key, time_str, verify, file.read())
        file.close()
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        res = response.read()
        return parse_data(res)
    except:
        return None


res = identify('/Users/fanjunwei003/Desktop/test_f.jpg')

print res

