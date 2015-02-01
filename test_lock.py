# coding=utf-8
# Date: 15/1/25
# Time: 12:15
# Email:fanjunwei003@163.com

import time
import thread

__author__ = u'范俊伟'

import os
# 需要win32all来工作在Windows下（NT、2K、XP、不包括9x）
if os.name == 'nt':
    import win32con, win32file, pywintypes

    LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
    LOCK_SH = 0  # 默认
    LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
    __overlapped = pywintypes.OVERLAPPED()

    def lock(file, flags):
        hfile = win32file._get_osfhandle(file.fileno())
        win32file.LockFileEx(hfile, flags, 0, 0xffff0000, __overlapped)

    def unlock(file):
        hfile = win32file._get_osfhandle(file.fileno())
        win32file.UnlockFileEx(hfile, 0, 0xffff0000, __overlapped)
elif os.name == 'posix':
    import fcntl
    from fcntl import LOCK_EX, LOCK_SH, LOCK_NB

    def lock(file, flags):
        fcntl.flock(file.fileno(), flags)

    def unlock(file):
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)
else:
    raise RuntimeError("PortaLocker only defined for nt and posix platforms")


def lock_fun(name):
    with open('1.lock', 'w') as fp:
        fcntl.flock(fp, LOCK_EX)
        print name + '文件锁开始执行'
        time.sleep(5)


thread.start_new_thread(lock_fun, ('1',))
time.sleep(2)
lock_fun('2')