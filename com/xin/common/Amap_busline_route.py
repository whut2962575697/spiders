# -*- encoding:utf-8 -*-

from com.xin.common.RequestManage import PageDownload
from com.xin.common.MysqlManage import MysqlHandle
from com.xin.common.ConfigManage import config,amap_api_key
from com.xin.common.tools import is_json
from com.xin.common.ProxyManage import ProxyMgr

import csv
import json
import time
from hotqueue import HotQueue
from threading import Thread,RLock

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

"""
@author:xin
@date:2018/05/01
@content:Get bus route with AMap api(work for a custom)
"""


class Bus_Route(Thread):
    def __init__(self,queue,key):
        Thread.__init__(self)
        self.queue = queue  # a queue putting (num, origin, destination)
        self.proxy_mgr = ProxyMgr()  # proxy manager
        self.lock = RLock()  # a lock for thread
        self.key = key  # AMap key
        self.count = 0  # successful result count of request


    def run(self):
        proxy = self.proxy_mgr.get_proxy()[1]
        time.sleep(2)
        s_time = time.time()  # start time
        sl_time = time.time()  # start time of a proxy

        while 1:
            tuple_from_queue = self.queue.get()
            if tuple_from_queue is not None:
                try:
                    self.lock.acquire()
                    (num, origin, destination) = tuple_from_queue

                    url = "http://restapi.amap.com/v3/direction/transit/integrated?origin=%s&" \
                          "destination=%s&city=%d&output=json&key=%s" % (origin, destination, 131, self.key)
                    # print url
                    downloader = PageDownload()
                    page = downloader.simple_download(url)
                    print num, origin, destination
                    self.count += 1
                    if page is not None:
                        if is_json(page):
                            json_data = json.loads(page)
                            if json_data["status"] == "1":
                                route = json_data['route']
                                transits = route["transits"]
                                distance = None
                                duration = None
                                cost = None
                                for transit in transits:
                                    distance = float(transit["distance"])
                                    distance = round(distance / 1000, 2)
                                    duration = float(transit['duration']) / 3600
                                    duration = round(duration, 2)
                                    cost = transit['cost']
                                    if type(cost) is not list:
                                        cost = float(transit['cost'])
                                        cost = round(cost, 2)
                                        break
                                    else:
                                        continue

                                db = MysqlHandle()
                                # print "insert into table "
                                sql = "insert into amap_busline_route VALUES (%s,%s,%s,%s,%s,%s)"
                                db.insert(sql=sql, value_list=[(num, origin, destination, distance, duration, cost)])
                                db.close()
                            else:
                                if json_data["info"] == "DAILY_QUERY_OVER_LIMIT":  # the limit use of a day
                                    print "key: " + self.key + " use out"
                                    break
                                else:
                                    print json_data["info"]
                        else:
                            print "result is not json format"
                            self.queue.put_nowait((num, origin, destination))
                    else:
                        self.queue.put_nowait((num, origin, destination))
                        print "the page is None"
                    time.sleep(2)
                    self.lock.release()
                    e_time = time.time()
                    if self.count == 50:  # make sure that we will not get move than 50 result in a minutes
                        if e_time - s_time < 60:
                            time.sleep(60 - e_time + s_time)
                            s_time = time.time()
                    if e_time - sl_time > 300: # if a proxy ip is used for more than 6 minutes,we will change it!
                        proxy = self.proxy_mgr.change_proxy(proxy)[1]
                        print "proxy has changed to: " + proxy
                        sl_time = time.time()

                except Exception:
                    with open("error.txt", "a") as f:
                        f.write(str(tuple_from_queue[0]) + "\n")
                    self.queue.put_nowait(tuple_from_queue)
            else:
                print 'queue is empty,please wait'
                time.sleep(10)


def add_to_queue():
    """
    we use HotQueue to store input info
    :return:
    """
    with open(r"C:\Users\29625\Desktop\Trans_xtoy_1.csv","r") as f:
        reader = csv.reader(f)
        redis_config = config["redis"]
        queue = HotQueue(name="amap_busline_route", host=redis_config["host"],
                         port=redis_config["port"], db=redis_config["db"])


        print "start adding to queue"
        for row in reader:
            num = row[0]
            origin_lng = row[1]
            origin_lng = origin_lng.strip(" ")
            origin_lat = row[2]
            origin_lat = origin_lat.strip(" ")
            destination_lng = row[3]
            destination_lng = destination_lng.strip(" ")
            destination_lat = row[4]
            destination_lat = destination_lat.strip(" ")
            origin = origin_lng + ","+origin_lat
            destination = destination_lng + ","+destination_lat
            print origin + " " + destination
            queue.put((num,origin,destination))
        print "finished adding to queue"


def do_with_error(path):
    redis_config = config["redis"]
    queue = HotQueue(name="amap_busline_route", host=redis_config["host"],
                     port=redis_config["port"], db=redis_config["db"])
    with open(r"C:\Users\29625\Desktop\Trans_xtoy_1.csv", "r") as f_1:
        reader = csv.reader(f_1)
        reader = list(reader)
        with open(path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            num = line.strip("\n")
            row = reader[int(num)-1]
            origin_lng = row[1]
            origin_lng = origin_lng.strip(" ")
            origin_lat = row[2]
            origin_lat = origin_lat.strip(" ")
            destination_lng = row[3]
            destination_lng = destination_lng.strip(" ")
            destination_lat = row[4]
            destination_lat = destination_lat.strip(" ")
            origin = origin_lng + "," + origin_lat
            destination = destination_lng + "," + destination_lat
            print origin + " " + destination
            queue.put((num, origin, destination))


if __name__ == "__main__":
    # do_with_error("error.txt")
    #add_to_queue()
    redis_config = config["redis"]
    queue = HotQueue(name="amap_busline_route", host=redis_config["host"],
                     port=redis_config["port"], db=redis_config["db"])
    threads = []
    for api_key in amap_api_key:
        thread = Bus_Route(queue=queue, key=api_key)
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()







