# coding=utf8

from  rc4 import RC4
import urllib
import urllib2

sid = '2ab919cfc3a74789bd84d4724b83639b'
key = 'bbfdb3e757c81ca77f4a5d3699efa816'

'''
url = "http://127.0.0.1:9090/plugins/sso/status"


ejid = RC4(key).crypt('aaa@localhost')
etokey = RC4(key).crypt('04198d91-3702-4e6e-b1d6-23888fbdf900')
print ejid
print etokey
values = {'sid':sid,'jid':ejid,'token':etokey}
data = urllib.urlencode(values)
print  data
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()
print the_page
'''

url = "http://127.0.0.1:9090/plugins/sso/roster"

ejid = RC4(key).crypt('aaa@localhost')
values = {'sid':sid,'jid':ejid}
data = urllib.urlencode(values)
print  data
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()
print the_page


url = "http://127.0.0.1:9090/plugins/sso/message"

jid0 = RC4(key).crypt('fjw@localhost')
jid1 = RC4(key).crypt('aaa@localhost')
emsg = RC4(key).crypt('123')
values = {'sid':sid,'jid_0':jid0,'jid_1':jid1,'msg':emsg}
data = urllib.urlencode(values)
print  data
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()
print the_page


