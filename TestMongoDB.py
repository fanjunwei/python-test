# coding=utf-8
# Date: 14/11/11
# Time: 19:28
# Email:fanjunwei003@163.com
from datetime import datetime
from mongoengine import *
import uuid

__author__ = u'范俊伟'

connect('test')
# connect('admin', host='www.baoxuetech.com', port=27017, username='fanjunwei', password='123654')
class User(Document):
    username = StringField()


class Log(Document):
    ' 继承Document类,为普通文档 '
    name = StringField(max_length=50, required=True)
    artnum = IntField()
    uuids=StringField(max_length=40,unique=True,required=False)
    date = DateTimeField(default=datetime.now(), required=True)
    p = ReferenceField('Log')
    user = ReferenceField(User)


# user=User(username='qq')
# user.save()
#
# for i in range(0,100000):
#     log = Log(name=str(uuid.uuid1()),user=user)
#     log.artnum=i
#     log.save()


# user=User.objects(username='qq').exec_js('''
# function() {
# var results=[];
# db[collection].find(query).forEach(function(doc){
#     var id = doc[~id];
#     doc.count=db['log'].find({'user':id}).count();
#     results.push(doc);
#     });
#  function desc(x,y)
#     {
#         if (x.count > y.count)
#             return -1;
#         if (x.count < y.count)
#             return 1;
#         else
#             return 0;
#     }
# return results.sort(desc);
# }
# ''')
# print user
#
# c = Log.objects.filter(user__in=user).count()
# # for i in c:
# #     print i['name']
# print c
log = Log(name='sfd')
log.save()
