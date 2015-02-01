# coding=utf-8
# Date: 14/11/11
# Time: 19:28
# Email:fanjunwei003@163.com
from datetime import datetime
from mongoengine import *
import datetime

__author__ = u'范俊伟'

connect('manba', port=9000)


class DocUserLoginLog(Document):
    uid = IntField()
    login_time = DateTimeField(default=datetime.datetime.now())
    ip = StringField(max_length=15)
    type = IntField()


class DocNitpick(Document):
    uid = IntField(required=True)
    file_id = StringField(max_length=32)
    cartoon_name = StringField(max_length=100)
    sub_title = StringField(max_length=100)
    username = StringField(max_length=100)
    nickname = StringField(max_length=100)
    title = StringField(max_length=20)
    page_index = IntField(required=True)
    create_time = DateTimeField(default=datetime.datetime.now())
    content = StringField(default='', max_length=1000)
    support_count = IntField(default=0)
    oppose_count = IntField(default=0)
    hate_count = IntField(default=0)
    complaint_count = IntField(default=0)
    discuss_count = IntField(default=0)
    ex1_count = IntField(default=0)
    ex2_count = IntField(default=0)
    ex3_count = IntField(default=0)
    p_id = ReferenceField('DocNitpick')
    p_uid = IntField()
    push_do = BooleanField(default=False)
    enable = BooleanField(default=True)
    score = IntField(default=0)
    meta = {
        'indexes': ['cartoon_name', 'sub_title', 'username', 'nickname', 'title']
    }


class DocNitpickScore(Document):
    nitpick = ReferenceField(DocNitpick)
    uid = IntField(default=-1)
    create_time = DateTimeField(default=datetime.datetime.now())
    type = IntField(required=True)
    complaint_content = StringField(default='', max_length=1000)
    do = BooleanField(default=False)


class DocCartoon(Document):
    cartoon_id = StringField(unique=True, max_length=38)  # Field name made lowercase.
    cartoon_name = StringField(max_length=100, unique=True)  # Field name made lowercase.
    type_id = StringField(max_length=38)
    author = StringField(max_length=20)  # Field name made lowercase.
    country = StringField(max_length=10)  # Field name made lowercase.
    summarize = StringField()  # Field name made lowercase.
    kye_word = StringField(max_length=50)  # Field name made lowercase.
    recommend_flag = BooleanField(default=False)  # Field name made lowercase.
    recommend_time = DateTimeField(default=datetime.datetime.now())  # Field name made lowercase.
    create_time = DateTimeField(default=datetime.datetime.now())  # Field name made lowercase.
    modify_time = DateTimeField(default=datetime.datetime.now())  # Field name made lowercase.
    img_url = StringField(max_length=255)  # Field name made lowercase.
    mini_img_url = StringField(max_length=255)  # Field name made lowercase.
    en_file_name = StringField(max_length=100)  # Field name made lowercase.
    cartoon_name_ex = StringField(max_length=100)  # Field name made lowercase.
    top_flag = BooleanField(default=False)  # Field name made lowercase.
    top_time = DateTimeField(default=datetime.datetime.now())  # Field name made lowercase.
    short_name = StringField(max_length=100)  # Field name made lowercase.
    recommend = StringField(max_length=255)  # Field name made lowercase.
    sold_out = IntField(default=0)  # Field name made lowercase.
    pc_enable = BooleanField(default=True)
    j2me_enable = BooleanField(default=True)
    android_enable = BooleanField(default=True)
    ios_enable = BooleanField(default=True)
    html5_enable = BooleanField(default=True)


class DocDownloadLog(Document):
    db_id = StringField(max_length=38, required=True, unique=True)
    file_id = StringField(max_length=32, required=True)
    cartoon_id = StringField(max_length=38, required=True)
    uid = IntField(required=True)
    time = DateTimeField(default=datetime.datetime.now())
    read_mode = IntField(required=True)
    title = StringField(max_length=100)
    sub_title = StringField(max_length=100)

    meta = {
        'indexes': ['file_id', 'cartoon_id', 'time', ('cartoon_id', 'time')]
    }


def getHotListThread(platform, type):
    try:
        if type == 'day':
            start_data = datetime.datetime.now() - datetime.timedelta(days=1)
        elif type == 'week':
            start_data = datetime.datetime.now() - datetime.timedelta(days=7)
        elif type == 'month':
            start_data = datetime.datetime.now() - datetime.timedelta(days=30)
        elif type == 'all':
            start_data = datetime.datetime(1970, 1, 1)
        # download_count
        if platform == 'pc':
            query_set = DocCartoon.objects(pc_enable=True)
        elif platform == 'j2me':
            query_set = DocCartoon.objects(j2me_enable=True)
        elif platform == 'android':
            query_set = DocCartoon.objects(android_enable=True)
        elif platform == 'ios':
            query_set = DocCartoon.objects(ios_enable=True)
        elif platform == 'html5':
            query_set = DocCartoon.objects(html5_enable=True)
        options = {'start_data': start_data}
        if type == 'day':
            js = '''
function() {
var results=[];
db[collection].find(query).forEach(function(doc){
    var id = doc[~cartoon_id];
    var max_count=0;
    db['doc_download_log'].distinct('file_id',{'cartoon_id':id,'time':{'$gte':options.start_data}}).forEach(
        function(file_id){
            var count=db['doc_download_log'].find({'file_id':file_id,'time':{'$gte':options.start_data}}).count();
            if (count>max_count)
            {
                max_count=count;
            }
        }
    );

    doc.download_count=max_count;
    results.push(doc);
    });
 function desc(x,y)
    {
        if (x.download_count > y.download_count)
            return -1;
        if (x.download_count < y.download_count)
            return 1;
        else
            return 0;
    }
return results.sort(desc);
}
'''
        else:
            js = '''
function() {
var results=[];
db[collection].find(query).forEach(function(doc){
    var id = doc[~cartoon_id];
    doc.download_count=db['doc_download_log'].find({'cartoon_id':id,'time':{'$gte':options.start_data}}).count();
    results.push(doc);
    });
 function desc(x,y)
    {
        if (x.download_count > y.download_count)
            return -1;
        if (x.download_count < y.download_count)
            return 1;
        else
            return 0;
    }
return results.sort(desc);
}
'''
        data = query_set.exec_js(js, **options)

        return data
    except Exception, e:
        pass

print getHotListThread('android', 'day')
for i in getHotListThread('android', 'day'):
    print i['cartoon_name'], i['download_count']
    # print i


