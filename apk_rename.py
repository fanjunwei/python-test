#!/usr/bin/env python
# coding=utf-8
# Date: 14/10/31
# Time: 11:13
# Email:fanjunwei003@163.com
import os
import re
import sys

__author__ = u'范俊伟'


def get_apk_packagename(apk_path):
    try:
        pop = os.popen('aapt d badging "' + apk_path + '"')
        line = pop.readline()
        pop.close()

        re_package = re.compile(r"package: name=\'(.*?)\'")
        match = re_package.search(line)
        if match:
            package = match.groups()[0]
            return package
    except:
        return None


def main(path):
    if os.path.isdir(path):
        index = 0
        res = []
        for i in os.listdir(path):
            if i.endswith('.apk'):
                index = index + 1
                file_path = os.path.join(path, i)
                package = get_apk_packagename(file_path)
                if not package:
                    package = "app%03d" % index
                new_name = "%s.apk" % (package,)
                new_path = os.path.join(path, new_name)
                res.append("%s : %s" % (i, new_name))
                os.rename(file_path, new_path)
        f = open(os.path.join(path, 'renamelist.log'), 'w')
        f.write('\n'.join(res))
        f.close()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])

