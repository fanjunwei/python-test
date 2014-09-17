#!/usr/bin/env python
# coding=utf-8
import sys


def set_lcm_name(path, str_flag, str_value):
    file = open(path, 'rb')
    data = file.read()
    file.close()
    index = data.find(str_flag)
    if not index == -1:
        start = index + len(str_flag)
        end = start
        i = 0
        while True:
            if data[end] == '\0':
                break

            if i < len(str_value):
                data = data[:end] + str_value[i] + data[end + 1:]
            else:
                data = data[:end] + '#' + data[end + 1:]
            end = end + 1
            i = i + 1
        file = open(path, 'wb')
        file.write(data)
        file.close()


if __name__ == '__main__':
    if len(sys.argv) == 4:
        set_lcm_name(sys.argv[1], sys.argv[2], sys.argv[3])
