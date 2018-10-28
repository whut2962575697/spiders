# -*- coding:utf-8 -*-

"""
Created on 20171001
智能代理管理 version 1.0
@author:xin
"""
import time
import random
import Queue
import MysqlManage


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class ProxyMgr(object):
    def __init__(self):
        self.ip_queue = Queue.Queue()  # 代理队列
        self.load_proxy()  # 加载可用ip进入队列
        self.INTERVAL = 3*4  # 间隔时间
        self.used_buffer = {}  # 可用代理缓存
        self.TRYCOUNT = 4  # 最大重用次数
        self.IP_COUNT = 0  # 每次加载的ip数量

    # 按照活动时间顺序将代理ip加入到队列中
    def load_proxy(self):
        db = MysqlManage.MysqlHandle()
        sql = 'SELECT * FROM TEMP_IPS_MANAGE WHERE AVAILABITY!=0 ORDER BY LAST_VISIT_DATE ASC '
        datas = db.query(sql)
        db.close()
        self.IP_COUNT = len(datas)
        datas = [data for data in datas]
        random.shuffle(datas)
        for data in datas:  # 将代理加入到队列中
            self.ip_queue.put_nowait((data[0], time.mktime(data[1].timetuple()), 0))

    # 获取一个ip
    def get_proxy(self):
        try:
            (proxy, timestrp, failcount) = self.ip_queue.get_nowait()
            now = time.time()  # 现在时间
            if now - timestrp < self.INTERVAL:
                #  没到时间原封不动放回队列
                self.ip_queue.put_nowait((proxy, timestrp, failcount))
                return (0, proxy)  # 返回该ip不可用 ，0代表不可用
            else:
                update_sql = "update temp_ips_manage set last_visit_date= now() where proxy= '" + proxy + "'"
                db = MysqlManage.MysqlHandle()
                db.update(update_sql)
                db.close()
                self.used_buffer[proxy] = failcount  # 将代理加入可用缓存
                print u'[IPMANAGER]成功分配ip:%s,代理池里还有%d个。' % (proxy, self.ip_queue.qsize())
                return (1, proxy)
        except Queue.Empty:  # 抛出代理队列已空异常
            print u'ip池已空，请稍等！！'
            self.load_proxy()
            (proxy, timestrp, failcount) = self.ip_queue.get_nowait()
            return (1, proxy)

    def change_proxy(self, proxy_ip):
        update_sql = "update temp_ips_manage set last_visit_date= now() where proxy= '" + proxy_ip+"'"
        db = MysqlManage.MysqlHandle()
        db.update(update_sql)
        db.close()
        return  self.get_proxy()

    # 回收ip，succrate为下载成功率
    def recycle_proxy(self, used_proxy):
        try:
            failcount = self.used_buffer.pop(used_proxy)  # 代理缓存中去除回收的IP
            failcount += 1
        except Exception, e:
            print str(e)
            print u'获取的ip不是从线程池中加载出来的'  # 去除不了说明代理不是从缓存池中加载出来的
            return
        update_sql = 'UPDATE TEMP_IPS_MANAGE SET LAST_VISIT_DATE=NOW(),failed_count=%s' \
                     % (failcount)
        db = MysqlManage.MysqlHandle()
        db.update(update_sql)
        db.close()
        if failcount >10 :
            # 如果下载率小于0.25，失败次数加1
            #failcount = failcount+1
              # 失败次数大于最大重用次数
                # 将失败的ip写回数据库
            update_sql = 'UPDATE TEMP_IPS_MANAGE SET LAST_VISIT_DATE=NOW(), AVAILABITY=%s' \
                         % (0)
            db = MysqlManage.MysqlHandle()
            db.update(update_sql)
            db.close()

        else:
            self.ip_queue.put_nowait((used_proxy, time.time(), failcount))
        print u'[IPMANAGER]成功回收ip:%s,这个ip重试次数为[%d], 代理池里还有%d个。' % (used_proxy, failcount, self.ip_queue.qsize())


