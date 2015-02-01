# coding=utf-8
# Date: 14/11/14
# Time: 18:05
# Email:fanjunwei003@163.com
import hashlib
import json
import time
import requests

__author__ = u'范俊伟'
timestamp = str(int(time.time()))

appkey = '4f5cc2495270151e6e00001d'
app_master_secret = 's4qhrn6xod00tlqg8e509qzrysh5ge32'
src_str = appkey.lower() + app_master_secret.lower() + timestamp
validation_token = hashlib.md5(src_str).hexdigest()
device_tokens = 'AlL5OyzPiLE96s-CdFF4aqf6Ho1atPY8GbFnlbTwFOyS'
arg = {
    "appkey": appkey,  # 必填 应用唯一标识
    "timestamp": timestamp,  # 必填 时间戳，10位或者13位均可。
    "validation_token": validation_token,  # 必填 验证码，validation_token为appkey, app_master_secret与timestamp的MD5码,
    # 示例代码参照附录G。
    "type": "unicast",  # 必填 消息发送类型,其值为unicast,broadcast,groupcast,customizedcast或者filecast.
    # unicast-单播
    # filecast-文件播(多个device_token可以通过文件形式批量发送）
    # broadcast-广播
    # groupcast-组播(按照filter条件筛选特定用户群, 具体请参照filter参数)
    # customizedcast(通过开发者定义的alias和友盟的device_tokens进行映射,
    # 可以传入单个alias, 也可以传入文件id。具体请参照alias和file_id参数)
    "device_tokens": device_tokens,  # 可选 设备唯一表示
    # 当type=unicast时,必填, 表示指定的单个设备
    # 当type=broadcast,groupcast,filecast或者customizedcast时, 无需填写此参数。
    #"alias": "xx",  # 可选 当type=customizedcast时,开发者填写自己的alias,友盟根据alias进行反查找,
    #      得到对应的device_token。
    #"alias_type": "xx",  # 可选 当type=customizedcast时，必填。 表示alias的类型。
    #"file_id": "xx",  # 可选 当type=filecast时，开发者需要填写此参数按照文件形似来发送。
    #      当type=customizedcast时，开发者可以把alias存到文件里进行批量发送，注意这些
    #        alias的type必须和参数alias_type一致，否则不会命中。
    #      file_id通过文件上传接口获取, 具体请参照"2.4文件上传接口"。
    #"filter": {},  # 可选 终端用户筛选条件,如用户标签、地域、应用版本以及渠道等,详细请参考附录G。
    "payload":  # 必填 消息内容(Android最大为824B, iOS为2012B), 包含参数说明如下(JSON格式):
        {
            # Android
            "display_type": "notification",  # 必填 消息类型，值为notification或者message
            #      notification-通知, message-消息.
            "body":  # 必填 消息体。
            #      display_type=message时,body的内容只需填写custom字段。
            #      display_type=notification时, body可以包含如下参数:
                {
                    # 通知展现内容:
                    "ticker": "xx1",  # 必填 通知栏提示文字
                    "title": "xx2",  # 必填 通知标题
                    "text": "xx3",  # 必填 通知文字描述

                    # 自定义通知样式:
                    #"builder_id": 'xx',  # 可选 默认为0，用于标识该通知采用的样式。 开发者在集成SDK时，可为
                    #     不同的id指定不同的通知样式。
                    #    注意: 该字段从SDK-V1.3.0开始支持。

                    # 自定义通知图标:
                    #"icon": "xx",  # 可选 状态栏图标ID, R.drawable.[smallIcon],如果没有, 默认使用应用图标。
                    #      图片要求为24*24dp的图标,或24*24px放在drawable-mdpi下。
                    #      注意四周各留1个dp的空白像素
                    #"largeIcon": "xx",  # 可选 通知栏拉开后左侧图标ID, R.drawable.[largeIcon].
                    #      图片要求为64*64dp的图标,可设计一张64*64px放在drawable-mdpi下,
                    #      注意图片四周留空，不至于显示太拥挤
                    #"img": "xx",  # 可选 通知栏大图标的URL链接。该字段的优先级大于largeIcon。
                    #       该字段要求以http或者https开头。
                    #       注意: 该字段从SDK-V1.3.0后开始支持。

                    # 通知到达设备后的提醒方式
                    "play_vibrate": "true",  # 可选 收到通知是否震动,默认为"true".注意，"true/false"为字符串
                    "play_lights": "false",  # 可选 收到通知是否闪灯,默认为"true"
                    "play_sound": "true",  # 可选 收到通知是否发出声音,默认为"true"

                    # 自定义通知声音:
                    #"sound": "xx",  # 可选 通知声音，R.raw.[sound].
                    #       如果该字段为空，采用SDK默认的声音, 即res/raw/下的
                    #           umeng_push_notification_default_sound声音文件
                    #      如果SDK默认声音文件不存在，则使用系统默认的Notification提示音。
                    #       注意: 该字段从SDK-V1.3.0后开始支持。

                    # 点击"通知/消息"的后续行为，默认为打开app。
                    "after_open": "go_custom",  # 必填 值为"go_app", "go_url", "go_activity", "go_custom"
                    #      "go_app": 打开应用
                    #      "go_url": 跳转到URL
                    #      "go_activity": 打开特定的activity
                    #      "go_custom": 用户自定义内容。
                    #"url": "xx",  # 可选 当"after_open"为"go_url"时，必填。
                    #      通知栏点击后跳转的URL，要求以http或者https开头
                    #"activity": "xx",  # 可选 当"after_open"为"go_activity"时，必填。
                    #      通知栏点击后打开的Activity
                    #"custom": "xx"  # 可选 display_type=message, 或者
                    #      display_type=notification且"after_open"为"go_custom"时，
                    #      该字段必填。用户自定义内容, 可以为字符串或者JSON格式。
                },
            'extra':  # 可选 用户自定义key-value。只对"通知(display_type=notification)"生效。
            #      可以配合通知到达后, 打开App, 打开URL, 打开Activity使用。
            #      注意: SDK V1.2.3后开始支持
                {
                    'event_type': 'file_update',
                    "cartoon_id": "84D32947-9C28-4DDB-AA2C-DD77801E9FA4",
                    "file_id": "8336427c783e444db014e3ac9d0b229b",
                },

        }
}

url = 'http://msg.umeng.com/api/send'
data = json.dumps(arg)
response = requests.post(url, data)
print response
