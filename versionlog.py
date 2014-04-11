import urllib
import urllib2
import sys

def postVersion(v):
    url='http://192.168.1.2:8000/version/log.py'
    values={'v':v}
    data=urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()

postVersion(sys.argv[1])
