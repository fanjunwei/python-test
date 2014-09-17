#!/usr/bin/env python
# coding=utf-8
import sys


def main(lcm_names, file_path):
    lcm_names_array = lcm_names.split(' ')
    first_lcm = None
    for i in lcm_names_array:
        if i:
            first_lcm = i
            break
    res = 'char lcm_name[]="@lcm_name@'
    res += first_lcm
    for i in range(0, 50):
        res += '#'
    res += '";\n'
    res += 'char lcm_name_list[]="@lcm_name_list@'
    res += lcm_names
    res += '";\n'
    file = open(file_path, 'w')
    file.write(res)
    file.close()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
