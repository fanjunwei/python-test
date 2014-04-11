import datetime

__author__ = 'fanjunwei003'

import sys
import time

prog_str = "%3d%% [%-20s]"

def output(i):
    i = i+1
    sys.stdout.write('sdfsdf\n')
    sys.stdout.flush()
    sys.stderr.write(chr(0x0d))
    sys.stderr.write(prog_str % (i * 5, i*'='))
    sys.stderr.flush()


for i in range(20):
    time.sleep(0.5)
    output(i)

print
