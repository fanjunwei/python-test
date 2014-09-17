#!/usr/bin/env python
# coding=utf-8
import sys
import os
import re


def getSize(path):
    pip = os.popen('identify "%s"' % path)
    res = pip.readline()
    pip.close()
    size_re = re.compile('\S* \S* (\S*)')
    match = size_re.search(res)
    if match:
        sizex = match.groups()[0]
        size = sizex.lower().split('x')
        if len(size) == 2:
            return int(size[0]), int(size[1])

    return None, None


def resize(path, des_width, des_height):
    des_path='/tmp/'+os.path.basename(path)
    src_width, src_height = getSize(path)
    sw = float(des_width) / float(src_width)
    sh = float(des_height) / float(src_height)
    s = max(sw, sh)
    width = int(src_width * s)
    height = int(src_height * s)
    x = (float(width) - float(des_width)) / 2
    x = int(x)
    y = (float(height) - float(des_height)) / 2
    y = int(y)
    cmd = 'convert -resize %dX%d -crop %dX%d+%d+%d -resize !%dX%d "%s" "%s"' % (
        width, height, des_width, des_height, x, y, des_width, des_height, path, des_path)
    os.system(cmd)
    os.system('mv %s %s'%(des_path,path))
    print getSize(path)


os.environ['DYLD_LIBRARY_PATH'] = '/Users/fanjunwei003/ImageMagick-6.8.8/lib/'
os.environ['MAGICK_HOME'] = '/Users/fanjunwei003/ImageMagick-6.8.8/'
os.environ['PATH'] = os.environ['PATH'] + ':/Users/fanjunwei003/ImageMagick-6.8.8/bin/'
for line in sys.stdin:
    try:
        path = line.strip()
        print path
        width = int(os.environ['width'])
        height = int(os.environ['height'])
        resize(path, width, height)
    except Exception, e:
        print str(e)