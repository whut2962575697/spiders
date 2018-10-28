# -*- encoding:utf-8 -*-

import numpy as np
import datetime
import threading
import time,random
import json
import Queue
from com.xin.common.RequestManage import PageDownload
from com.xin.common.ConfigManage import mobike_headers
from com.xin.common.MysqlManage import MysqlHandle
from com.xin.common.tools import is_json
from com.xin.common.ProxyManage import ProxyMgr
from com.xin.common.ProxyCollectByApi import Collect
from com.xin.common.ProxyFilter import filter_avaliable_ips


import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def slice_boundary(right_top_loc, left_bottom_loc, offset):
    min_lat = left_bottom_loc[1]
    min_lng = left_bottom_loc[0]
    max_lat = right_top_loc[1]
    max_lng = right_top_loc[0]
    x_list = np.arange(start=min_lng, stop=max_lng, step=offset)
    y_list = np.arange(start=min_lat, stop=max_lat, step=offset)
    geo_queue = Queue.Queue()
    for x in x_list:
        for y in y_list:
            geo_queue.put_nowait((x, y))
    return geo_queue


def start_spider(thread_num, sec):
    threads = []
    queue = slice_boundary(right_top_loc=(114.497855,30.711301), left_bottom_loc=(114.152043,30.458607),
                                        offset=0.005)
    for x in range(thread_num):
        thread = Spider(sources="mobike",queue=queue, sec=sec)
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

class Spider(threading.Thread):
    def __init__(self,  sources, queue, sec, url_table=None):
        threading.Thread.__init__(self)
        self.base_url = "http://mwx.mobike.com/mobike-api/rent/nearbyBikesInfo.do"
        self.page_table = sources+"_page_table"
        self.queue = queue
        self.city_code = 131
        self.sec = sec
        self.proxy_mgr = ProxyMgr()
        self.lock = threading.RLock()

    def run(self):
        # geo_list = self.slice_boundary(right_top_loc=(116.570132,40.028621), left_bottom_loc=(116.209085,39.768678),
        #                                offset=0.002)
        #self.lock.acquire()
        proxy = self.proxy_mgr.get_proxy()[1]
        time.sleep(2)
        #self.lock.release()
        s_time = time.time()
        while not self.queue.empty():
            self.lock.acquire()
            geo = self.queue.get_nowait()
            downloader = DownloadTool()
            res = downloader.download_page(base_url=self.base_url, geo=geo, city_code=self.city_code,sec=self.sec,
                                     page_table=self.page_table, proxy={"http":"http://"+proxy})
            if not res:
                self.queue.put_nowait(geo)
                self.proxy_mgr.recycle_proxy(proxy)
            print geo, proxy
            self.lock.release()
            time.sleep(random.randint(3,8))
            e_time = time.time()
            if e_time-s_time>20:
                proxy = self.proxy_mgr.change_proxy(proxy)[1]
                print "proxy has changed to: "+proxy
                s_time = time.time()
        print 'The queue is empty, finished task!!'





class DownloadTool():
    def __init__(self):
        pass

    def download_page(self, base_url, geo, proxy, city_code, sec, page_table):
        downloader = PageDownload(proxy=proxy, hd=mobike_headers)
        post_dic = {
            'longitude': str(geo[0]),
            'latitude': str(geo[1]),
            'citycode': str(city_code),
            'errMsg': 'getMapCenterLocation:ok'
        }
        page = downloader.download_with_post(url=base_url, post_data=post_dic)
        if is_json(page):
            json_page = json.loads(page)
            if json_page.has_key("object"):
                mobike_object = json_page["object"]
                items = []
                for mobike in mobike_object:
                    bike_id = mobike["distId"]
                    bike_type = mobike["biketype"]
                    b_type = mobike["type"]
                    lng = mobike["distX"]
                    lat = mobike["distY"]
                    dis_source = str(geo[0])+","+str(geo[1])
                    item = (bike_id, bike_type, b_type, lat, lng, dis_source,sec)
                    items.append(item)
                db = MysqlHandle()
                sql = "insert into "+page_table+" values(%s,%s,%s,%s,%s,%s,%s,now())"
                db.insert(sql=sql, value_list=items)
                return True
        else:
            return False



if __name__ == "__main__":
    i = 1
    while 1:
        now_time = datetime.datetime.now()
        if now_time.hour >= 6 and now_time.hour <= 21:
            "start"
            collector = Collect(50)
            collector.process()
            filter_avaliable_ips()
            start_spider(50, i)
            "end"
            time.sleep(30)
            i += 1







