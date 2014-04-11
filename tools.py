#coding=utf-8
import json
import os
import urllib2
import math
import smtplib
from email.mime.text import MIMEText
from email.header import Header
#from Sell3_server.settings import DEVICEID
import thread
import re




def splitVersion2(v):
    r=re.compile(r"([^-_]+)_([^-_]+)_([^-_]+)-([^-_]+)_(.*)")
    m=r.match(v)
    if m :
        groups=m.groups()
        project=groups[0]
        custom=groups[1]
        branch=groups[2]
        subbranch=groups[3]
        timestamp=groups[4]
        return project,custom,branch,subbranch,timestamp
    else:
        r=re.compile(r"([^-_]+)_([^-_]+)_([^-_]+)_(.*)")
        m=r.match(v)
        if m :
            groups=m.groups()
            project=groups[0]
            custom=groups[1]
            branch=groups[2]
            subbranch=None
            timestamp=groups[3]
            return project,custom,branch,subbranch,timestamp

    return None,None,None,None,None

def getDirUrls(v):
    project,custom,branch,subbranch,timestamp=splitVersion2(v)
    baseurl='http://www.baoxuetech.com:900/'
    if project:
        url1=os.path.join(baseurl,custom,project,"%s_%s_%s"%(project,custom,branch))
        url2=os.path.join(baseurl,custom,project,"%s_%s_%s"%(project,custom,branch),"user_%s_%s_%s_%s"%(project,custom,branch,timestamp))
        url3=os.path.join(baseurl,custom,project,"%s_%s_%s"%(project,custom,branch),"eng_%s_%s_%s_%s"%(project,custom,branch,timestamp))
        return [url1,url2,url3]
    return None
def getNames(v):
    project,custom,branch,subbranch,timestamp=splitVersion2(v)
    if project:
        if subbranch:
            name1=('user_%s_%s_%s-%s_%s.zip'%(project,custom,branch,subbranch,timestamp))
            name2=('eng_%s_%s_%s-%s_%s.zip'%(project,custom,branch,subbranch,timestamp))
            name3=('user.%s_%s_%s-%s_%s.zip'%(project,custom,branch,subbranch,timestamp))
            name4=('eng.%s_%s_%s-%s_%s.zip'%(project,custom,branch,subbranch,timestamp))
        else:
            name1=('user_%s_%s_%s_%s.zip'%(project,custom,branch,timestamp))
            name2=('eng_%s_%s_%s_%s.zip'%(project,custom,branch,timestamp))
            name3=('user.%s_%s_%s_%s.zip'%(project,custom,branch,timestamp))
            name4=('eng.%s_%s_%s_%s.zip'%(project,custom,branch,timestamp))
        return [name1,name2,name3,name4]
    else:
        return None

def getDownloadUrl(v):
    dirs=getDirUrls(v)
    names=getNames(v)
    for i in dirs:
        try:
            html= urllib2.urlopen(i).read()
            for j in names:

                if not html.find('>'+j+'<') == -1 :
                    return os.path.join(i,j)
        except:
            pass
    return None

#print getDownloadUrl('A22_BXT_13V3-20I7_V01_2014-04-09_17_30')
html= urllib2.urlopen(u'http://www.baoxuetech.com:900/BXT/A22/A22_BXT_13V3').read().decode('utf-8')

print html