# -*- encoding:utf-8 -*-

from com.xin.common.RequestManage import PageDownload
from com.xin.common.tools import is_json

import json
import time
from  Queue import  Queue
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

base_api_url = "http://restapi.amap.com/v3/direction/transit/integrated?origin=%s&destination=%s&city=%d&output=json&key=%s"

def get_busline(origin,destination,city_code,key):
    url = base_api_url % (origin,destination,city_code,key)
    downloader = PageDownload(timeout=10)
    page = downloader.simple_download(url)
    if page is not None:
        if is_json(page):
            json_data = json.loads(page)
            if json_data["status"]=="1":
                print "successful!!"
                return page
            else:
                if json_data["info"]=="DAILY_QUERY_OVER_LIMIT":
                    return False
                else:
                    return None

        else:
            print "return not json!!"
            return None
    else:
        print "request error!!"
        return None

def main(path, keys):
    #work_book = xlrd.open_workbook(path)
    with open(path,"r") as f:
        reader = csv.reader(f)
        queue = Queue()
        for key in keys:
            queue.put_nowait(key)
        key = queue.get_nowait()
        count = 0
        s_time = time.time()
        for row in reader:
            origin_lng = row[0]
            origin_lat = row[1]
            destination_lng = row[2]
            destination_lat = row[3]
            origin = origin_lng + ","+origin_lat
            destination = destination_lng + ","+destination_lat
            print origin + " " + destination
            result = get_busline(origin=origin, destination=destination, city_code=131, key=key)
            if result is not None:
                if result == False:
                    print "key : " + key + " has use out!!"
                    key = queue.get_nowait()
                count += 1
            # if count == 50:
            #     e_time = time.time()
            #     if e_time - s_time < 60:
            #         time.sleep(e_time - s_time)
            #     time.sleep(1)
            #     s_time = time.time()
            #     count = 0
    # shell = work_book.sheet_by_index(0)
    # row_num = shell.nrows



if __name__=="__main__":
    main(path=r"C:\Users\29625\Desktop\Trans_xtoy_1.csv",keys=["32a458e41efdbe19661d25aced19bde0","7086b6ef4994ff2b57f4bb91d742ebed"])






