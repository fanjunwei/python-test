__author__ = 'fanjunwei003'


def set_lcm_name(path, lcm_name):
    name_flag='@lcm_name@'
    file = open(path,'rb')
    data = file.read()
    file.close()
    index=data.find(name_flag)
    if not index == -1:
        start=index+len(name_flag)
        end=start
        i=0
        while True:
            if data[end] == '\0':
                break

            if i<len(lcm_name):
                data=data[:end]+lcm_name[i]+data[end+1:]
            else:
                data=data[:end]+'#'+data[end+1:]
            end=end+1
            i=i+1
        file=open(path,'wb')
        file.write(data)
        file.close()

if __name__ == '__main__':
    set_lcm_name('/Users/fanjunwei003/Desktop/lk.bin', 'bxt70_rgb_6572')
