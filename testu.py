# coding=utf-8
import base64
import os
import urllib
import urllib2

__author__ = 'fanjunwei003'


def encrypt(value):
    encrypt_jar = os.path.join(os.path.dirname(__file__), "shiming.jar").replace('\\', '/')
    res = os.popen('java -jar %s %s' % ( encrypt_jar, value))
    data = res.read()
    data = base64.decodestring(data)
    return data


if __name__ == "__main__":
    username = "BJ040_01"
    password = "pass010203"
    username = encrypt(username)
    password = encrypt(password)
    data = {
        "u": username,
        "p": password
    }
    str = urllib.urlencode(data)
    req = urllib2.Request("http://channel.bj.chinamobile.com/channelApp/sys/login", str)
    req.add_header('Content-Type', "application/x-www-form-urlencoded")
    resp = urllib2.urlopen(req)

    print resp.read()