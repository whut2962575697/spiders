# -*- coding:utf-8 -*-


import sys
reload(sys)
sys.setdefaultencoding("utf-8")



# config dic,‘database’:mysql database，‘redis’redis database
config = {
    # mysql
    'mysql': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': '257313',
        'db': 'mysql',
        'charset': 'utf8'
    }


 }

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

meituan_cls = {"food":"meishi","hotel":"jiudian","entertainment":"xiuxianyule","ktv":"xiuxianyule","easylife":"shenghuo","beauty":"jiankangliren",
               "married":"jiehun","fitness":"yundongjianshen","domestic":"jiazhuang","education":"xuexipeixun","medicine":"yiliao"}

