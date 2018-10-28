# -*- coding:utf-8 -*-

"""
Created  on 20171010
免费代理ip收集器
一般网站：http://www.ip181.com/daili/1.html
          http://www.xicidaili.com/nn/1
@author:xin
"""

import re
from threading import Thread
import time
from RequestManage import PageDownload
from MysqlManage import MysqlHandle
from Queue import Queue
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# 主操作类
class MainProcess(object):
    def __init__(self, txt_path, test_url):
        self.txt_path = txt_path  # 代理网页列表文件
        self.test_url = test_url  # 测试url
        self.queue = Queue()  # 存放代理网页的队列
        self.feed_url()  # 初始化队列方法

    # 导入代理ip所在网页
    def feed_url(self):
        with open(self.txt_path, 'r') as f:
            url_list = f.readlines()
        for url in url_list:
            self.queue.put_nowait(url.strip('\n'))

    # 主操作函数，将网页中的代理ip收集到AI_PROXY_IPS表中
    def main_process(self):
        while not self.queue.empty():
            url = self.queue.get_nowait()
            collect = Collector(url, self.test_url)
            collect.collect_proxy()
            collect.vertify_proxy()
            db = MysqlHandle()
            insert_sql = 'INSERT INTO AI_PROXY_IPS VALUES (%s,NOW(),100)'
            is_success= db.insert(insert_sql,collect.avaliable_ips)
            if is_success:
                print r'oh,successfully collected proxy from ' + url
            else:
                print r'sorry,unsuccessfully collected proxy from ' + url
            db.close()
            time.sleep(3)


# 收集代理类
class Collector(object):
    def __init__(self, proxy_url, test_url):
        self.proxy_url = proxy_url
        self.test_url = test_url
        self.reg = r'\d{1,2,3}\.\d{1,2,3}\.\d{1,2,3}\.\d{1,2,3}:\d{2,3,4,5}'
        self.reg_table = r'[^<]*<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[^<]*<td>(\d{2,5})</td>'
        self.ips = []
        self.avaliable_ips = []

    # 收集页面代理，先将所有的IP采集，加入到IP列表中
    def collect_proxy(self):
        downloader = PageDownload()
        page = downloader.simple_download(self.proxy_url)
        if page is not None:
            if page.find('table') and page.find('td') and page.find('tr'):
                ip_list = re.findall(self.reg_table,page)
                for ip_ in ip_list:
                    ip = ip_[0]+":"+ip_[1]
                    self.ips.append(ip)
            else:
                ip_list = re.findall(self.reg, page)
                for ip in ip_list:
                    self.ips.append(ip)

    # 验证IP列表中代理的有效性，提取有效代理
    def vertify_proxy(self):
        for ip in self.ips:
            proxy = {'http': 'http://'+ip}
            downloader = PageDownload(proxy)
            page = downloader.simple_download(self.test_url)
            if page is not None:
                print ip
                self.avaliable_ips.append(ip)

if __name__ == '__main__':
    threads = []
    file_path = "../data/url_list.txt"
    test_url = "http://www.51ape.com/"
    process = MainProcess(txt_path=file_path, test_url=test_url)
    # 多线程采集
    for x in xrange(10):
        thread = Thread(target=process.main_process)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
