# -*- encoding:utf-8 -*-

from MysqlManage import MysqlHandle
import json
import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Collect(object):
    def __init__(self, proxy_num):
        self.proxy_num = proxy_num

    def truncate_table(self):
        db = MysqlHandle()
        sql = "truncate table AI_PROXY_IPS"
        db.excute(sql=sql)
        db.close()

    def process(self):
        self.truncate_table()
        url = "http://127.0.0.1:8000/?types=0&count=%d&country=国内" % (self.proxy_num)
        respond = requests.get(url)
        page = respond.content
        _proxies = json.loads(page)
        proxies = []
        for _proxy in _proxies:
            ip = _proxy[0]
            port = _proxy[1]
            proxy = str(ip)+":"+str(port)
            proxies.append([proxy])
        db = MysqlHandle()
        sql = "INSERT INTO AI_PROXY_IPS VALUES (%s,NOW(),100)"
        db.insert(sql=sql, value_list=proxies)
        db.close()


if __name__ == "__main__":
    collector = Collect(50)
    collector.process()
