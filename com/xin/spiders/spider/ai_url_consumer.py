# -*- encoding=utf-8 -*-

from threading import Thread, RLock
from com.xin.common.ConfigManage import config
from com.xin.common.ProxyManage import ProxyMgr
from com.xin.common.MysqlManage import MysqlHandle
from hotqueue import HotQueue
import time
import random
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class UrlConsumer(Thread):
    def __init__(self, interval_upp, interval_down, source,need_proxy=True):
        Thread.__init__(self)
        redis_config = config["redis"]
        url_table = source+"_url_table"
        if redis_config.has_key("password"):
            self.queue = HotQueue(name=url_table, host=redis_config["host"],
                                  port=redis_config["port"],password=redis_config["password"], db=redis_config["db"])
        else:
            self.queue = HotQueue(name=url_table, host=redis_config["host"],
                              port=redis_config["port"], db=redis_config["db"])
        self.activity = 0.0
        self.spider = None
        self.check_round = 20
        self.interval_upp = interval_upp  #
        self.interval_down = interval_down  #
        self.lock = RLock()
        self.tuple_from_queue = ()
        self.proxy_manger = ProxyMgr()
        self.proxy_ip = self.proxy_manger.get_proxy()[1]
        self.CHKTHD = 20
        self.proxy = {'http': 'http://' + self.proxy_ip}
        self.need_proxy = need_proxy

    def set_spider(self, spider):
        self.spider = spider


    def run(self):
        download_count = 0
        total_count = 0
        fail_count_20 = 0
        start_time = time.time()
        while 1:
            try:
                self.tuple_from_queue = self.queue.get()
                if self.tuple_from_queue is None:
                    print u'urls pool is empty,please wait for 90s'
                    time.sleep(90)
                    break
                else:
                    print self.tuple_from_queue
                    start_time_this_round = time.time()
                    download_count += 1
                    self.lock.acquire()
                    if not self.need_proxy:
                        self.proxy = None
                    download_result = self.spider.process(tuple_from_queue=self.tuple_from_queue, proxy=self.proxy)
                    self.lock.release()

                    total_count += download_result['total']
                    if download_result['total'] != download_result['success']:  # 如果爬取url没有全部成功，失败的次数相应增加
                        fail_count_20 += download_result['total'] - download_result['success']
                        for failed_data in download_result['failed_list']:  # 将失败的url记录再加入持久队列
                            self.queue.put(failed_data)
                            print failed_data
                batch = download_count % self.CHKTHD
                if batch == 0:
                    self.activity = 1 - float(fail_count_20) / float(total_count)
                    print '[%s]COUNT: %d, FAIL-IN-this%d:%d , avail:%f:' % (
                        self.proxy_ip, self.CHKTHD, total_count, fail_count_20,
                        self.activity)
                    fail_count_20 = 0
                    total_count = 0
                    if self.activity < 0.3:
                        print '[%s]rate of download is %f，too low' % (self.proxy_ip, self.activity)
                        db = MysqlHandle()
                        sql = "update temp_ips_manage set availabity=%s where proxy='%s'" % (
                        self.activity, self.proxy_ip)
                        db.update(sql=sql)
                        db.close()
                        # self.change_proxy()
                        self.proxy = {'http': 'http://' + self.proxy_manger.change_proxy(self.proxy_ip)[1]}
                spider_time = time.time() - start_time
                if spider_time > 600:
                    print '[%s]timeout，we will quit' % (self.proxy_ip)
                    self.proxy = {'http': 'http://' + self.proxy_manger.change_proxy(self.proxy_ip)[1]}
                    start_time = time.time()
                elaspsed = time.time() - start_time_this_round
                interval = random.randint(self.interval_down, self.interval_upp)
                if elaspsed < interval:
                    time.sleep(interval - elaspsed)
            except Exception,e:
                print e.message
                print self.tuple_from_queue
                if type(self.tuple_from_queue)==list and len(self.tuple_from_queue)==3:

                    self.queue.put(self.tuple_from_queue)

        print u'[%s]close the connection with database successfully' % (self.proxy_ip)



