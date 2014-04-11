# coding=utf8
import sys
out=''
partition_name=''
path=sys.argv[1]
f = open(path,'r')
line = f.readline()
while line:
    line=line.strip('\n')
    parms = line.split(':')
    if len(parms)==2 :
        key = parms[0].strip(' ')
        value = parms[1].strip(' ')
        if key == 'partition_name':
            partition_name=value
        if partition_name=='FAT':
            if key=='file_name':
                line='  file_name: fat_sparse.img'
            elif key=='is_download':
                line='  is_download: true'
            elif key=='type':
                line = '  type: fat'
    out += line+'\n'
    line = f.readline()
f.close()
#print out
f = open(path,'w')
f.write(out)
f.close()
