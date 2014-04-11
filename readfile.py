# coding=utf8
import gzip
import StringIO

__author__ = 'fanjunwei003'

file = open('/Users/fanjunwei003/Desktop/res.txt','r')
txt= file.read()
data = StringIO.StringIO(txt)
gz = gzip.GzipFile(fileobj=data)
txt = gz.read()
gz.close()
print txt