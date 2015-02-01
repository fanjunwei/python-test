# coding=utf-8
# Date: 14/12/12
# Time: 13:04
# Email:fanjunwei003@163.com

__author__ = u'范俊伟'


def jisuan1(peibi, lilv):
    shengyu = zong = 20
    last = 0
    for i in range(1, 31):
        e = i % 7
        if e == 6 or e == 0:
            yield last
        else:
            jinru = shengyu * peibi
            shengyu -= jinru
            lixi = (zong - shengyu) * lilv
            last = lixi
            yield lixi


def jisuan2():
    shengyu = zong = 20
    last = 0
    diru = 0
    for i in range(1, 31):
        e = i % 7
        if e == 5:
            jinru = shengyu * 0.8
            shengyu -= jinru
            lixi = (zong - shengyu) * 2.85
            diru = last = lixi
            yield lixi
        elif e == 6 or e == 0:
            yield last
        elif e == 1 and diru > 0:

            jinru = shengyu * 0.3
            shengyu += diru
            shengyu -= jinru
            lixi = (zong - shengyu) * 3.56
            last = lixi
            yield lixi

        else:
            jinru = shengyu * 0.3
            shengyu -= jinru
            lixi = (zong - shengyu) * 3.56
            last = lixi
            yield lixi


zonghe = 0
for i in jisuan2():
    print "sddf%d"%i
    zonghe += i
    print zonghe