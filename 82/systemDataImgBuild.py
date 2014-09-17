#!/usr/bin/env python
# coding=utf-8
import os

scatter_path = 'release_img/MT6582_Android_scatter.txt'
make_ext4fs = './out/host/linux-x86/bin/make_ext4fs'


def read_pt_size(pt_name):
    if os.path.exists(scatter_path):
        partition_name = ''
        f = open(scatter_path, 'r')
        line = f.readline()
        size_line = None
        while line:
            line = line.strip('\n')
            parms = line.split(':')
            if len(parms) == 2:
                key = parms[0].strip(' ')
                value = parms[1].strip(' ')
                if key == 'partition_name':
                    partition_name = value
                if partition_name == pt_name:
                    if key == 'partition_size':
                        size_line = line
                        break
            line = f.readline()
        f.close()
        if size_line:
            size16 = size_line.split(':')[1].strip()
            size = int(size16, 16)
            print ('%s partition_size:%d'%(partition_name,size))
            return size
    else:
        print('not found scatter')
    return None


def main():
    ANDROID_size = read_pt_size('ANDROID')
    USRDATA_size = read_pt_size('USRDATA')
    if ANDROID_size:
        os.system('%s -s -l %d -a system release_img/system.img release_img/system  >/dev/null 2>&1' %
                  (make_ext4fs, ANDROID_size))
    if USRDATA_size:
        os.system('%s -s -l %d -a data release_img/userdata.img release_img/data  >/dev/null 2>&1' %
                  (make_ext4fs, USRDATA_size))


main()
