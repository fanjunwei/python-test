# coding=utf-8
import hashlib
import mimetypes
import struct
import time
import datetime
import urllib
import urllib2
import uuid

__author__ = 'fanjunwei003'
#
# public static String encode(int id, String route, JSONObject msg) {
# String str = msg.toString();
# if (route.length() > 255) {
# throw new RuntimeException("route max length is overflow.");
# }
# 		byte[] arr = new byte[HEADER + route.length()];
# 		int index = 0;
# 		arr[index++] = (byte) ((id >> 24) & 0xFF);
# 		arr[index++] = (byte) ((id >> 16) & 0xFF);
# 		arr[index++] = (byte) ((id >> 8) & 0xFF);
# 		arr[index++] = (byte) (id & 0xFF);
# 		arr[index++] = (byte) (route.length() & 0xFF);
#
# 		for (int i = 0; i < route.length(); i++) {
# 			arr[index++] = (byte) route.codePointAt(i);
# 		}
# 		return bt2Str(arr, 0, arr.length) + str;
# 	}
#
# 	private static String bt2Str(byte[] arr, int start, int end) {
# 		StringBuffer buff = new StringBuffer();
# 		for (int i = start; i < arr.length && i < end; i++) {
# 			buff.append(String.valueOf(Character.toChars((arr[i]+256) % 256)));
# 		}
# 		return buff.toString();
# 	}
#
def download_news_image(url):
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    if res.code==200:
        type=res.headers.type
        ext= mimetypes.guess_all_extensions(type)
        if ext:
            fileName = str(uuid.uuid1()) + ext[0]
        else:
            fileName = str(uuid.uuid1()) + ".jpg"
        path = '/Users/fanjunwei003/Desktop/' + "news_img/" + fileName
        file=open(path,'wb')
        file.write(res.read())
        file.close()
        res.close()
        return ''+fileName
    else:
        return None


download_news_image('http://www.baidu.com/img/baidu_sylogo1.gif')



