# -*- encoding:utf-8 -*-

from RequestManage import PageDownload
from sqllite_manange import SqlLiteHandle
from ConfigManage import amap_api_key

import sys
import re
import json
import time
import argparse
import os
reload(sys)
sys.setdefaultencoding("utf-8")


class AMapSpider(object):
    def __init__(self, keyword, num):
        self.keyword = keyword
        self.num = num
        self.base_url_nm = "https://www.amap.com/service/poiInfo?query_type=TQUERY&city=100000&pagesize=20&pagenum=%d&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=14&keywords=%s"
        self.base_url = "https://restapi.amap.com/v3/place/text?keywords=%s&city=beijing&output=json&offset=20&page=%d&key=%s&extensions=all"
    def download_page_info(self,json_data):

            if json_data.has_key("pois"):
                data_list = json_data["pois"]
                for poi in data_list:
                    company_name = poi["name"]
                    addr = poi["address"]
                    phone_num = poi["tel"]
                    if phone_num:
                        print (company_name, phone_num, addr)
                        try:
                            with open("temp_ts.dat", "a") as f:
                                f.write(phone_num + "*" + company_name + "\n")
                        except:
                            pass
                        res = self.get_phone_info(phone_num)

                        time.sleep(0.5)
                        if res:
                            province = res[0]
                            city = res[1]
                            yys = res[2]
                        else:
                            province = "未知"
                            city = "未知"
                            yys = "未知"

                        db = SqlLiteHandle()
                        sql = "insert into ts_1 values (?,?,?,?,?,?,?)"
                        db.insert(sql, [(phone_num, company_name, company_name, addr, province, city, yys)])
                        db.close()

    def download_page_info_nm(self,json_data):
        if json_data.has_key("data"):
            data = json_data["data"]
            if data.has_key("poi_list"):
                data_list = data["poi_list"]
                for poi in data_list:
                    company_name = poi["disp_name"]
                    addr = poi["address"]
                    phone_num = poi["tel"]
                    if phone_num:
                        print (company_name, phone_num, addr)
                        try:
                            with open("temp_ts.dat", "a") as f:
                                f.write(phone_num + "*" + company_name + "\n")
                        except:
                            pass
                        res = self.get_phone_info(phone_num)

                        time.sleep(5)
                        if res:
                            province = res[0]
                            city = res[1]
                            yys = res[2]
                        else:
                            province = "未知"
                            city = "未知"
                            yys = "未知"

                        db = SqlLiteHandle()
                        sql = "insert into ts_1 values (?,?,?,?,?,?,?)"
                        db.insert(sql, [(phone_num, company_name, company_name, addr, province, city, yys)])
                        db.close()

    def get_phone_info(self, phone_num):
        url = "http://v.showji.com/Locating/showji.com20180331.aspx?&output=json&&m="+phone_num
        downloader = PageDownload()
        page = downloader.simple_download(url)
        if page is None:
            taobao_api = "http://tcc.taobao.com/cc/json/mobile_tel_segment.htm?tel="+phone_num
            downloader = PageDownload()
            page = downloader.simple_download(taobao_api)
            if page :
                province = re.findall(r"province:'([^:]+)',", page)
                yys = re.findall(r"catName:'([^:]+)',", page)
                city = None
                return [province,city,yys]
            else:
                return None

        else:
            json_data = json.loads(page)

            # s = type(json_data)
            if json_data["QueryResult"] == "True":
                return [json_data["Province"], json_data["City"], json_data["Corp"]]
            else:
                return None


    def create_table(self):
        #time_str = time.time()

        sql = "drop table ts_1"
        db = SqlLiteHandle()
        db.excute(sql)
        db.close()
        sql = """
        CREATE TABLE ts_1 (
        "phoneNum"  TEXT(20),
        "contact"  TEXT(200),
         "companyName" TEXT(400),
        "address" TEXT(600),
        "provice"  TEXT(40),
        "city"  TEXT(80),
        "yys"  TEXT(40));
        """
        db = SqlLiteHandle()
        db.excute(sql)
        db.close()


    def spider(self):
        if os.path.exists("temp_ts.dat"):
            # 删除文件，可使用以下两种方法。
            os.remove("temp_ts.dat")
        self.create_table()
        status = True
        i = 0
        id_i = 0
        key = amap_api_key[id_i]
        while status:
            url = self.base_url_nm % (i,self.keyword)
            downloader = PageDownload()
            page = downloader.simple_download(url)
            if page:
                json_data = json.loads(page)
                if json_data.has_key("status"):
                    status = json_data["status"]
                    if status != "1":
                        url = self.base_url % (self.keyword, i, key)
                        downloader = PageDownload()
                        page = downloader.simple_download(url)
                        if page:
                            json_data = json.loads(page)
                            if json_data.has_key("status"):
                                status = json_data["status"]
                                if status != "1":
                                    if id_i < 16:
                                        id_i = id_i + 1
                                    else:
                                        id_i = 0
                                    key = amap_api_key[id_i]
                                    continue
                                else:
                                    self.download_page_info(json_data)


                    else:
                        self.download_page_info_nm(json_data)
                    status = True
                else:
                    status = False
                i = i + 1
                if i == self.num:
                    return

            else:
                pass



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='input keyword')
    parser.add_argument("keyword", help="keyword string")
    parser.add_argument("num",help="the num of result")
    args = parser.parse_args()

    spider = AMapSpider(args.keyword.decode("gbk").encode("utf-8"),int(args.num))
    spider.spider()
    # spider = AMapSpider("郑州市广告公司".encode("utf-8"),20)
    # spider.spider()