__author__ = 'fanjunwei003'
import urllib2
import  cookielib
import  urllib

HOST='https://mobile.12306.cn'
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

urllib2.install_opener(opener)
UserAgent='Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a (392691824)/Worklight/6.0.0'
def post(url,parm):
    postData=urllib.urlencode(parm)
    req = urllib2.Request(url,postData)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('User-Agent', UserAgent)
    req.add_header('Cache-Control', 'no-cache')
    req.add_header('Accept', 'text/javascript, text/html, application/xml, text/xml, */*')
    req.add_header('Connection', 'Keep-Alive')
    req.add_header('WL-Instance-Id','ek5lkqim1s17aothtk0rt7kij4')
    req.add_header('x-wl-platform-version','6.0.0')
    req.add_header('X-Requested-With','XMLHttpRequest')
    req.add_header('x-wl-app-version','1.21')
    req.add_header('Origin','file://')
    req.add_header('Accept-Encoding','gzip, deflate')
    req.add_header('Accept-Language','zh_CN')
    resp=None
    try:
        resp = urllib2.urlopen(req)
        print resp.read()
    except urllib2.HTTPError ,e:
        print e.headers
        print e.read()
        print '==================================================='


url=HOST+'/otsmobile/apps/services/api/MobileTicket/iphone/query'
parm={
    'adapter':'CARSMobileServiceAdapter',
    'procedure':'login',
    'compressResponse':'true',
    'parameters':'[{"baseDTO.os_type":"i","baseDTO.device_no":"7F61686E-4A28-4B5A-A814-70E2CACE6D24","baseDTO.mobile_no":"123444","baseDTO.time_str":"20131225131148","baseDTO.check_code":"b9a6fa0b846f91ab0bf4a9efa1c6240d","baseDTO.version_no":"1.1","baseDTO.user_name":"yiyang9140","password":"c9d0ae765600e825405eb155c30df244"}]',

}

url=HOST+'/otsmobile/apps/services/api/MobileTicket/iphone/init'
parm={
    'skin':'default',
    'isAjaxRequest':'true'
}
txt=post(url,parm)

txt=post(url,parm)
print txt


