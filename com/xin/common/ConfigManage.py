# -*- coding:utf-8 -*-


import sys
reload(sys)
sys.setdefaultencoding("utf-8")

"""
@author:xin
@date:2017/11/10
@content:the config file of my project
"""

# config dic,‘database’:mysql database，‘redis’redis database
config = {
    # mysql
    'mysql': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': '257313',
        'db': 'spiders',
        'charset': 'utf8'
    },
    # redis
    'redis': {
        'name': 'xin_queue',
        'host': '127.0.0.1',
        'port': 6379,
        'db': 1
    }

 }


test_headers = {
"Accept": "application/json",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "zh-CN,zh;q=0.9",
"AID": "20180129114744msuXCgQlXtKVED7P",
"APIVER": "v1.0",
"Connection": "keep-alive",
"Content-Length": "21",
"Content-Type": "application/x-www-form-urlencoded",
"Host": "www.indata3.com",
"Origin": "http://www.indata3.com",
"Referer": "http://www.indata3.com/ig/itsa1803/w/home.html",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
"X-Requested-With": "XMLHttpRequest"
}


# headers of normal spider,use for request headers
normal_headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/56.0.2924.87 Safari/537.36'
}

# headers of baiduyun tool,use for request headers
baidupan_headers  = {
    "Accept": "application/json, text/javascript, text/html, */*; q=0.01",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
    "Referer":"http://pan.baidu.com/disk/home",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Connection": "keep-alive",
}


# headers of mobike spider,use for request headers
mobike_headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E304 MicroMessenger/6.5.7 NetType/WIFI Language/zh_CN',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://servicewechat.com/wx80f809371ae33eda/23/page-frame.html',
}

# headers of ofo spider,use for request headers
ofo_headers = {
'Accept': '*/*',
				'Accept-Encoding': 'gzip, deflate',
				'Accept-Language': 'zh-CN',
				'Content-Length': '524',
				'Content-Type': 'multipart/form-data; boundary=----ofo-boundary-MC40MjcxMzUw',
				'Host': 'san.ofo.so',
				'Origin': 'https://common.ofo.so',
				'Referer': 'https://common.ofo.so/newdist/?Journey',
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
}


# keys of AMap
amap_api_key = [
    "d8c233ceebafb768af55fe0853fa4cc1",
    "1453369625ea5bcb39a7563a77e3f778",
    "6e2e2f8269122365d9c3d2050eff18ff",
    "d26d2ff5612da9d671cf656c5f2ec424",
    "802d924f47282e1561d7495e040bd2d5",
    "c201609d5cd393f0a9aebbc6f3eeea05",
    "433702cbb9533cd45c738318aa745bd7",
    "3a2381e4b304c682ea28e28f01ca389e",
    "0ff1b3881373950f91d5f917787fb062",
    "07951403e6b381506b92f8be599c3aa6",
    "a5e9e94b6ca1cfaf644bd9676d72681b",
    "95c35f2007dfc1240b16550639acc7b6",
    "f1c1f6f7cad2c5f14ebf2c3cf4034e99",
    "65d99321cc12daea1b73a0ee77ac6ee8",
    "a7311f294e92b1e8254dfa2fe6555a15",
    "a46f662357e489279a38f29f9b9a1a72",
    "7a3fc15a93dd8bcbbae845d6f4d6b4f3"
]