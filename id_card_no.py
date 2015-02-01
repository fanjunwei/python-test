# coding=utf-8
# Date: 14/11/10
# Time: 23:54
# Email:fanjunwei003@163.com
import datetime

__author__ = u'范俊伟'


def jiaoyanma(shenfenzheng17):
    def haoma_validate(shenfenzheng17):
        if type(shenfenzheng17) in [str, list, tuple]:
            if len(shenfenzheng17) == 17:
                return True
        raise Exception('Wrong argument')

    if haoma_validate(shenfenzheng17):
        if type(shenfenzheng17) == str:
            seq = map(int, shenfenzheng17)
        elif type(shenfenzheng17) in [list, tuple]:
            seq = shenfenzheng17

        t = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        s = sum(map(lambda x: x[0] * x[1], zip(t, map(int, seq))))
        b = s % 11
        bd = {
            0: '1',
            1: '0',
            2: 'x',
            3: '9',
            4: '8',
            5: '7',
            6: '6',
            7: '5',
            8: '4',
            9: '3',
            10: '2'
        }
        return bd[b]


def get_full_no(no):
    if len(no)==17:
        return "%s%s"%(no,jiaoyanma(no))


if __name__ == '__main__':
    #print get_full_no('41010619860303003')
    for i in range(0,100):
        date = datetime.date(1986,1,1)+datetime.timedelta(i)
        no17="410106%s322"%date.strftime('%Y%m%d')
        print(get_full_no(no17))