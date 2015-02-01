# coding=utf-8
# Date: 15/1/4
# Time: 14:16
# Email:fanjunwei003@163.com
from threading import local
import base64
import os
import datetime
import requests
from util.tools import common_except_log

__author__ = u'范俊伟'


class Shiming:
    cookies = {}
    username = None
    password = None
    errorMsg = local()
    photo = local()
    exception = local()
    result = local()
    signature = None
    transactionID = None
    phone_number = None
    cardno = None
    name = None
    address = None
    pic_url = None


    def __init__(self, phone_number, username=None, password=None, cardno=None, name=None, address=None):
        self.phone_number = phone_number
        if username and password:
            self.username = username
            self.password = password
        self.cardno = cardno
        self.name = name
        self.address = address

    def execute(self):
        success = True
        if success:
            success = self.login()
        if success:
            success = self.getSignature()
        if success:
            success = self.submitToCheck()
        # if success:
        #     success = self.ftpUploadServlet_Z()
        # if success:
        #     success = self.ftpUploadServlet_F()
        if success:
            success = self.saveIdentity()
        return success

    def encrypt(self, value):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, str):
            pass
        else:
            value = str(value)
        base_dir = os.path.dirname(os.path.dirname(__file__))
        encrypt_jar = os.path.join(base_dir, 'tools', "shiming.jar").replace('\\', '/')
        res = os.popen('java -jar %s %s' % ( encrypt_jar, base64.encodestring(value).replace('\n', '')))
        data = res.read()
        data = base64.decodestring(data)
        return data


    def login(self):
        try:
            username = self.encrypt(self.username)
            password = self.encrypt(self.password)
            data = {
                "u": username,
                "p": password
            }

            r = requests.post("http://channel.bj.chinamobile.com/unichannelApp/sys/login", data=data)

            if r.status_code == 200:
                self.cookies['JSESSIONID'] = r.cookies['JSESSIONID']
                # {u'data': {u'registerVer': u'1394435524000'}, u'success': u'true'}
                # {u'msg': {u'code': u'1', u'desc': u'\u8d26\u53f7\u4e0d\u5b58\u5728\uff01'}, u'success': u'false'}
                try:
                    res = r.json()
                except:
                    self.errorMsg.value = u'移动数据返回错误,请稍后重试'
                    return False
                self.result.value = res
                success = res.get('success')
                self.errorMsg.value = res.get('msg', {}).get('desc', None)
                if self.errorMsg.value:
                    self.errorMsg.value = self.errorMsg.value + u',请检查此店铺的实名账户是否正确'
                return success == 'true'
            else:
                self.errorMsg.value = u'网络错误(%d),请稍后重试' % r.status_code
                return False
        except Exception, e:
            common_except_log()
            self.exception.value = e
            self.errorMsg.value = u'内部错误,请稍后重试'
            return False

    def getSignature(self, *args, **kwargs):
        try:
            now = datetime.datetime.now()
            str1 = now.strftime('%Y%m%d%H%M%S')
            str2 = now.strftime('%H%M%S')
            self.transactionID = '100' + str1 + str2
            data = {
                "phone": self.phone_number,
                "transactionID": self.transactionID,
            }

            r = requests.post("http://channel.bj.chinamobile.com/unichannelApp/identity/getSignature", data=data,
                              cookies=self.cookies)
            if r.status_code == 200:
                try:
                    res = r.json()
                except:
                    self.errorMsg.value = u'移动数据返回错误,请稍后重试'
                    return False
                self.result.value = res
                self.errorMsg.value = res.get('msg', {}).get('desc', None)

                success = res.get('success')
                self.signature = res.get('data', {}).get('signature', None)
                return success == 'true'
            else:
                self.errorMsg.value = u'网络错误(%d),请稍后重试' % r.status_code
                return False
        except Exception, e:
            common_except_log()
            self.exception.value = e
            self.errorMsg.value = u'内部错误,请稍后重试'
            return False


    def submitToCheck(self, *args, **kwargs):
        try:
            data = {
                "INDICTSEQ": self.transactionID,
                "CUST_CERT_ADDR": self.address,
                "CERT_EXPDATE": '2020-03-11',
                "CUST_CERT_NO": self.cardno,
                "LOGINTYPE": '2',
                "CHANNEL_ID": self.username.replace("WW", "").split('_')[0],
                "MS_TEL": '',
                "CUST_CERT_TYPE": '1',
                "PROV_CODE": '100',
                "BILL_ID": self.phone_number,
                "MS_OPCODE": '',
                "CERT_VALIDDATE": '2010-03-11',
                "SIGNATURE": self.signature,
                "BIRTHDAY": '0000年00月00日',
                "MODE_TYPE": '3',
                "GENDER": '1',
                "CUST_NAME": self.name,
                "NATION": '汉',
                "ISSUING_AUTHORITY": self.address,
                "ACCOUNT": self.username,
            }

            # data = {
            # "INDICTSEQ": self.transactionID,
            # "CUST_CERT_ADDR": '郑州市上街区',
            # "CERT_EXPDATE": '2020-03-11',
            # "CUST_CERT_NO": self.cardno,
            # "LOGINTYPE": '2',
            # "CHANNEL_ID": self.username.replace("WW", "").split('_')[0],
            # "MS_TEL": '',
            # "CUST_CERT_TYPE": '1',
            # "PROV_CODE": '100',
            # "BILL_ID": self.phone_number,
            # "MS_OPCODE": '',
            # "CERT_VALIDDATE": '2010-03-11',
            # "SIGNATURE": self.signature,
            # "BIRTHDAY": '1986年03月03日',
            # "MODE_TYPE": '3',
            # "GENDER": '1',
            # "CUST_NAME": self.name,
            # "NATION": '汉',
            # "ISSUING_AUTHORITY": 'sddfd',
            # "ACCOUNT": self.username,
            # }
            r = requests.post("http://211.138.17.31:25000/rnmsol/front/realname/prnca!submitToCheck", data=data,
                              cookies=self.cookies)
            if r.status_code == 200:
                try:
                    res = r.json()
                except:
                    self.errorMsg.value = u'移动数据返回错误,请稍后重试'
                    return False
                self.result.value = res
                self.errorMsg.value = res.get('bean', {}).get('NOPASS_RESON', None)
                self.pic_url = res.get('bean', {}).get('PIC_URL', None)
                if not self.errorMsg.value:
                    return True
                else:
                    return False

            else:
                self.errorMsg.value = u'网络错误(%d),请稍后重试' % r.status_code
                return False
        except Exception, e:
            common_except_log()
            self.exception.value = e
            self.errorMsg.value = u'内部错误,请稍后重试'
            return False

    def ftpUploadServlet_Z(self, *args, **kwargs):
        try:
            f = open('/Users/fanjunwei003/Desktop/1.jpg', 'rb')
            data = {
                "fileparam": self.pic_url,
            }
            files = {

                'file': ('12342342343.jpg', f, 'application/octet-stream'),
            }

            r = requests.post("http://211.138.17.31:25000/rnmsol/ftpUploadServlet", data=data, files=files,
                              cookies=self.cookies)
            f.close()
            if r.status_code == 200:
                try:
                    res = r.json()
                except:
                    self.errorMsg.value = u'移动数据返回错误,请稍后重试'
                    return False
                self.result.value = res
                self.errorMsg.value = res.get('returnMessage', None)
                success = res.get('returnCode', None) == '0000'
                return success
            else:
                self.errorMsg.value = u'网络错误(%d),请稍后重试' % r.status_code
                return False
        except Exception, e:
            common_except_log()
            self.exception.value = e
            self.errorMsg.value = u'内部错误,请稍后重试'
            return False

    def ftpUploadServlet_F(self, *args, **kwargs):
        try:
            f = open('/Users/fanjunwei003/Desktop/2.jpg', 'rb')
            data = {
                "fileparam": self.pic_url.replace('_Z', '_F'),
            }
            files = {
                'file': ('12342342343.jpg', f, 'application/octet-stream'),
            }

            r = requests.post("http://211.138.17.31:25000/rnmsol/ftpUploadServlet", data=data, files=files,
                              cookies=self.cookies)
            f.close()
            if r.status_code == 200:
                try:
                    res = r.json()
                except:
                    self.errorMsg.value = u'移动数据返回错误,请稍后重试'
                    return False
                self.result.value = res
                self.errorMsg.value = res.get('returnMessage', None)
                success = res.get('returnCode', None) == '0000'
                return success
            else:
                self.errorMsg.value = u'网络错误(%d),请稍后重试' % r.status_code
                return False
        except Exception, e:
            common_except_log()
            self.exception.value = e
            self.errorMsg.value = u'内部错误,请稍后重试'
            return False

    def saveIdentity(self, *args, **kwargs):
        try:

            data = {
                "transactionID": self.encrypt(self.transactionID),
                "phone": self.encrypt(self.phone_number),
                "channelCode": self.encrypt(self.username.replace("WW", "").split('_')[0]),
            }

            r = requests.post("http://channel.bj.chinamobile.com/unichannelApp/identity/newSaveIdentity", data=data,
                              cookies=self.cookies)
            if r.status_code == 200:
                try:
                    res = r.json()
                except:
                    self.errorMsg.value = u'移动数据返回错误,请稍后重试'
                    return False
                self.result.value = res
                self.errorMsg.value = res.get('msg', {}).get('desc', None)

                success = res.get('success')
                self.signature = res.get('data', {}).get('signature', None)
                return success == 'true'
            else:
                self.errorMsg.value = u'网络错误(%d),请稍后重试' % r.status_code
                return False
        except Exception, e:
            common_except_log()
            self.exception.value = e
            self.errorMsg.value = u'内部错误,请稍后重试'
            return False

    def getLastError(self):
        message = getattr(self.errorMsg, "value", u"")
        if type(message) == str:
            message = message.encode('utf-8')
        return message

    def getLastException(self):
        return getattr(self.exception, "value", None)

    def getLastResult(self):
        return getattr(self.result, "value", {})

    def getPhoto(self):
        return getattr(self.photo, "value", None)

# this.channelCode = this.account.replace("WW", "").split("_")[0]; 渠道号
'''
http://211.138.17.31:25000/rnmsol/front/realname/prnca!submitToCheck
INDICTSEQ:          10020150101230459041471 时间戳
CUST_CERT_ADDR:     郑州市上街区彭号檀44号
CERT_EXPDATE:       2020-03-11  过期时间
CUST_CERT_NO:       41010619860303003 身份证号
LOGINTYPE:          2 d登录类型
CHANNEL_ID:         BJ040 渠道id
MS_TEL:
CUST_CERT_TYPE:     1
PROV_CODE:          100
BILL_ID:            18210832791
MS_OPCODE:
CERT_VALIDDATE:     2010-03-11
SIGNATURE:          mzO57JvIzVIfYFsP+5AJO/nJZNSIhQbpZ7e2FFxKNg5cClhAxfwL1kE/uO4Ev8mU3Bf42p1llgSFZ+4fJFtTQu9nP4viGhG2BYbjdEnQ7XyhaYJl4anUdlQPkFwZw5LEKNu35CJPTWoNJD7MYUkEaFjSI4sZt9DVgYqLXfnoXRmSWcidOM8gDd
                    GgMaD6f64JCWlvvBuTvGv1ftHtk7BxWB8CabucyCiPVnxmsVSr7w5j/gED5ZYogkWhhVpmdmAHwKruKv/EtUX4HXEqCaACACoWc8hNidCSS1rI3PcBDlY006qoA29PrQE0TH6xPQ/ZBPvEC3ZwwFh/LMBzZf2ZJQ==
BIRTHDAY:           01月1986
MODE_TYPE:          3
GENDER:             1
CUST_NAME:          范俊伟 姓名
NATION:             汉 民族
ISSUING_AUTHORITY:  号牟县公安寿 颁发机关
ACCOUNT:            BJ040_01

http://211.138.17.31:25000/rnmsol/ftpUploadServlet



http://211.138.17.31:25000/rnmsol/front/realname/prnca!submitToCheck

INDICTSEQ:          10020150102092732072953
CUST_CERT_ADDR:     郑州市上街区
CERT_EXPDATE:       2016-09-20
CUST_CERT_NO:       410106198603030038
LOGINTYPE:          2
CHANNEL_ID:         BJ040
MS_TEL:
CUST_CERT_TYPE:     1
PROV_CODE:          100
BILL_ID:            18210832791
MS_OPCODE:
CERT_VALIDDATE:     2006-09-20
SIGNATURE:          phulSDdoHM8dUvcVonqFxtHqbAhT91EQaGgDg6Q7BkplCsrZ0HVUH+x3SBXQQASr+3cCyOfNOLk5keQXh8Jgajlh4L/llBTA2aockdOpuwdtUTKmV88ZFOucOwhtX+S9Yxo2B3yMvcK2073mysBiqCYRpK5hqYbqLB9Jt+UsnlUXw3R4rE7bI7
                    6d77JAc8GffeCp2ZSCtjOsWQ4tt7I4b/e4XM6xLoe62hbu/dpVl+hukJuuLBAJSqvjESUTcRTswgJd60J5dvPSm6svLtkGK5LzZ72m+9FJSLaoMWEwra5E12F97JPpnWTnONkfGwr3fV8H7mYd+Iep0EBSynJiYg==
BIRTHDAY:           1986年03月03日
MODE_TYPE:          3
GENDER:             1
CUST_NAME:          范俊伟
NATION:             汉
ISSUING_AUTHORITY:  she
ACCOUNT:            BJ040_01
'''

if __name__ == '__main__':
    shiming = Shiming('13621016779', 'BJ040_01', 'pass010203', cardno='331021198708011262', name='张圣泽', address='郑州')
    if not shiming.execute():
        print shiming.getLastError()
    else:
        print('成功')
