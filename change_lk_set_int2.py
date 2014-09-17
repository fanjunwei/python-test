#!/usr/bin/env python
# coding=utf-8
import sys


def set_tp_index(path, name_flag, tp_index):
    tp_index = int(tp_index)
    file = open(path, 'rb')
    data = file.read()
    file.close()
    index = data.find(name_flag)
    if not index == -1:
        start = index + len(name_flag)
        str_tp_index = '%02d' % tp_index
        data = data[:start] + str_tp_index + data[start + 2:]
        file = open(path, 'wb')
        file.write(data)
        file.close()


if __name__ == '__main__':
    if len(sys.argv) == 4:
        set_tp_index(sys.argv[1], sys.argv[2], sys.argv[3])
