from channels.generic.websocket import WebsocketConsumer
import json
from templates.polls import detect_depair
from django.core.management.base import BaseCommand
import sys
import asyncio
from asgiref.sync import async_to_sync


class MyCommand(BaseCommand):
    def handle(self, *args, **options):
        # Do something
        sys.exit()


def fun_exit():
    MyCommand().run_from_argv(sys.argv)


class Cons(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.count = 1
        super().__init__(*args, **kwargs)

    def connect(self):  # 定义产生连接时的回调函数
        print('新的连接')
        self.accept()  # 同意连接

    def disconnect(self, code):  # 定义断开时的回调函数
        print('连接已经断开', code)

    def receive(self, text_data=None, bytes_data=None):
        print(text_data, bytes_data)
        text_data = json.loads(text_data)
        if text_data.get('command') == 'start':
            detect_depair.from_path_main(self)
        elif text_data.get('command') == 'con':
            self.count += 1
            detect_depair.from_path_main(self)
        elif text_data.get('command') == 'conF':
            self.count += 1
            detect_depair.from_path_main(self)
        elif text_data.get('command') == 'conB':
            self.count -= 1
            detect_depair.from_path_main(self)
        elif text_data.get('command') == 'exit':
            pass
        else:
            self.count = 0
        print('send to browse')
        # data_dict = {"text": text_data}
        # # 将字典转换为JSON格式
        # json_data = json.dumps(data_dict)
        # 发送JSON数据给客户端
        # 重载了super中的send方法的text_data
        # 文本text_data
        # 二进制bytes_data
        # self.send(bytes_data=json_data)
        # self.send({"text": text_data})
