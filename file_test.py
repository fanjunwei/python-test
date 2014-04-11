# coding=utf-8
import hashlib
import os
import struct
import subprocess
import datetime

__author__ = 'fanjunwei003'


def createEmptyFile(path, length):
    if os.path.exists(path):
        os.remove(path)
    file = open(path, 'wb')
    file.seek(int(length), 0)
    file.write('\x00')
    file.truncate(length)
    file.close()
    if os.path.exists(path):
        return True
    else:
        return False


def writeData(path, start, data):
    file = open(path, 'Ub+')
    file.seek(int(start), 0)
    file.write(data)
    file.close()


def parseValue(list):
    res = ''
    res += struct.pack('i', len(list))
    for i in list:
        if type(i) == unicode:
            str = i.encode('utf-8')
        else:
            str = i
        res += struct.pack('i', len(str))
        res += str
    return res


#path='aa'
#createEmptyFile(path,255)

# writeData(path,23,'1')
# writeData(path,15,'1')


# file = open('/Users/fanjunwei003/Documents/PycharmProjects/manba/media/cartoon_file/4a88e1d1-b330-11e3-b9b7-20c9d04376f3.rmf', 'rb')
# file_md5 = hashlib.md5(file.read()).hexdigest().upper()
# file.close()
# print file_md5
# file=open('cc','w')
#
# file.close

# itemcount=4
# pagesieze=2
# pagecount=itemcount%pagesieze
#
# print pagecount
def compareVersion(ver1, ver2):
    ver1s = ver1.split('.')
    ver2s = ver2.split('.')
    for i in range(max(len(ver1s), len(ver2s))):
        if i >= len(ver1s):
            n1 = 0
        else:
            n1 = int(ver1s[i])
        if i >= len(ver2s):
            n2 = 0
        else:
            n2 = int(ver2s[i])
        if n2 > n1:
            return 1
        elif n2 < n1:
            return -1
    return 0


def formatTime(db_time):
    now = datetime.datetime.now().date()
    if type(db_time) == datetime.datetime:
        db_time = db_time.date()
    inv = now - db_time
    if inv==0:
        return '今天'
    elif inv==1:
        return '昨天'
    else:
        return db_time.strftime('%Y/%m/%d')


print formatTime(datetime.datetime(2012,3,3))