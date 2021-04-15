# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Author:       ZERONE40
# Date:         2021-04-15 14:30
# Description:  

# -------------------------------------------------------------------------------
import json
import requests

headers = {'Content-Type': 'application/json;charset=utf-8'}


class EpicDingMessage:

    def __init__(self, web_hook):
        self.web_hook = web_hook

    @staticmethod
    def parse_response(response):
        print(response.content)

    def send_text(self, content, at_mobiles=None, is_at_all=False):
        """
            钉钉消息以 文本 形式发送到钉钉群

            参数          参数类型          必须         说明
            msgtype         String          是           消息类型，此时固定为：text
            content         String          是           消息内容
            atMobiles       Array           否           被@人的手机号（在content里添加@人的手机号）
            isAtAll         Boolean         否           是否@所有人

        """
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": at_mobiles,
                "isAtAll": is_at_all
            }
        }
        response = requests.post(self.web_hook, data=json.dumps(data), headers=headers)
        self.parse_response(response)

    def send_link(self, title, text, message_url, pic_url=None):
        """
        钉钉消息以 带图文超链接 形式发送到钉钉群

        参数          参数类型          必须         说明
        msgtype         String          是           消息类型，此时固定为：link
        title           String          是           消息标题
        text            String          是           消息内容。如果太长只会部分展示
        messageUrl      String          是           点击消息跳转的URL
        picUrl          String          否           图片URL

        """
        data = {
            "msgtype": "link",
            "link": {
                "title": title,
                "text": text,
                "picUrl": pic_url,
                "messageUrl": message_url
            }
        }
        response = requests.post(self.web_hook, data=json.dumps(data), headers=headers)
        self.parse_response(response)

    def send_action_card_single(self, title, text, single_title="去看看", single_url=None):
        """
        钉钉消息以 带单个跳转动作的卡片 形式发送到钉钉群

        参数          参数类型          必须         说明
        msgtype         String          是           此消息类型为固定actionCard
        title           String          是           首屏会话透出的展示内容
        text            String          是           markdown格式的消息
        singleTitle     String          是           单个按钮的标题。(设置此项和singleURL后btns无效)
        singleURL       String          是           点击singleTitle按钮触发的URL
        btnOrientation  String          否           0-按钮竖直排列，1-按钮横向排列

        """
        data = {
            "actionCard": {
                "title": title,
                "text": text,
                "btnOrientation": "0",
                "singleTitle": single_title,
                "singleURL": single_url
            },
            "msgtype": "actionCard"
        }
        response = requests.post(self.web_hook, data=json.dumps(data), headers=headers)
        self.parse_response(response)

    def send_action_card_multi(self, title, text, btns, btn_orientation="0"):
        """
        钉钉消息以 带多个跳转动作的卡片 形式发送到钉钉群

        参数          参数类型          必须         说明
        msgtype         String          是           此消息类型为固定actionCard
        title           String          是           首屏会话透出的展示内容
        text            String          是           markdown格式的消息
        btns            Array           是           按钮
        └ title        String          是           按钮标题
        └ actionURL    String          是           点击按钮触发的URL
        btnOrientation  String          否           0-按钮竖直排列，1-按钮横向排列

        示例：
        {
            "actionCard": {
                "title": "乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
                "text": "![screenshot](https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png)  ### 乔布斯 20 年前想打造的苹果咖啡厅   Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划",
                "btnOrientation": "0",
                "btns": [
                    {
                        "title": "内容不错",
                        "actionURL": "https://www.dingtalk.com/"
                    },
                    {
                        "title": "不感兴趣",
                        "actionURL": "https://www.dingtalk.com/"
                    }
                ]
        },
        "msgtype": "actionCard"
    }


        """
        data = {
            "actionCard": {
                "title": title,
                "text": text,
                "btnOrientation": btn_orientation,
                "btns": btns
            },
            "msgtype": "actionCard"
        }

        response = requests.post(self.web_hook, data=json.dumps(data), headers=headers)
        self.parse_response(response)

    def send_feed_card(self, links):
        """
            钉钉消息以 带多个跳转动作的卡片 形式发送到钉钉群

            参数          参数类型          必须         说明
            msgtype         String          是           此消息类型为固定feedCard
            title           String          是           单条信息文本
            messageURL      String          是           点击单条信息到跳转链接
            picURL          String          是           单条信息后面图片的URL

            示例：
            {
                "feedCard": {
                    "links": [
                        {
                            "title": "时代的火车向前开",
                            "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                            "picURL": "https://gw.alicdn.com/tfs/TB1ayl9mpYqK1RjSZLeXXbXppXa-170-62.png"
                        },
                        {
                            "title": "时代的火车向前开2",
                            "messageURL": "https://www.dingtalk.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI",
                            "picURL": "https://gw.alicdn.com/tfs/TB1ayl9mpYqK1RjSZLeXXbXppXa-170-62.png"
                        }
                    ]
                },
                "msgtype": "feedCard"
            }

        """
        data = {
            "feedCard": {
                "links": links
            },
            "msgtype": "feedCard"
        }
        response = requests.post(self.web_hook, data=json.dumps(data), headers=headers)
        self.parse_response(response)
