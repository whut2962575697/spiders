# -*- encoding:utf-8 -*-

from RequestManage import PageDownload, WebSelenium
from sqllite_manange import SqlLiteHandle
from ConfigManage import meituan_cls

import sys
import re
import json
import time
import argparse
import os
from Queue import Queue
reload(sys)
sys.setdefaultencoding("utf-8")

class MeiTuanSpider(object):
    def __init__(self, keyword,num):
        self.keyword = keyword
        self.num = num
        self.base_url = "http://apimobile.meituan.com/group/v4/poi/pcsearch/%s?uuid=47eefb9ce25349b38838.1531394245.1.0.0&userid=-1&limit=32&offset=%d&cateId=-1&q=%s"
        self.ids = Queue()
        self.get_city_codes()

    def download_page_info(self,json_data):
        if json_data.has_key("searchResult"):
            content = json_data["searchResult"]
            value_list = []
            for item in content:
                id = item["id"]
                company_name = item["title"]
                addr = item["address"]
                showType = item["showType"]
                try:
                    url = "http://www.meituan.com/%s/%s/" % ( meituan_cls[showType],id)
                except:
                    continue

                phone_num = self.get_phone_num(url)
                time.sleep(5)
                if phone_num:
                    print (company_name,phone_num,addr)
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
                    db.insert(sql,[(phone_num,company_name,company_name,addr,province,city,yys)])
                    db.close()


    def get_phone_num(self,url):
        print url
        downloader = WebSelenium()
        driver = downloader.simple_download(url)
        page = driver.page_source


        try:
            phone_num = re.findall(r'<span>电话：</span><span>(\d+/?\d+)</span>', page.encode("utf-8"))
        except:
            phone_num = []
        if phone_num:
            return phone_num[0]
        else:
            return None

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

    def get_city_codes(self):
        with open("view-source_www.meituan.com_changecity_.html","r") as f:
            page = f.read()
            #    print page

        meituan_ids = re.findall(r'\{"id":(\d+),"name":"[^,]+"',page)
        ids = []
        for item in meituan_ids:
            if item not in ids:
                ids.append(item)
                self.ids.put_nowait(item)

    def spider(self):
            if os.path.exists("temp_ts.dat"):
                # 删除文件，可使用以下两种方法。
                os.remove("temp_ts.dat")
            self.create_table()
            status = True
            i = 0
            city_code = self.ids.get_nowait()
            while status:
                url = self.base_url % (city_code, i * 10,self.keyword)
                # print url
                downloader = PageDownload()
                page = downloader.simple_download(url)
                if page:
                    json_data = json.loads(page)
                    if json_data.has_key("data"):
                        total_count = json_data["data"]["totalCount"]
                        if int(total_count) > 0:

                            self.download_page_info(json_data["data"])
                            status = True
                    else:
                        if not self.ids.empty():
                            city_code = self.ids.get_nowait()
                            continue
                        else:
                            status = False
                    i = i + 1
                    if i == self.num:
                        return

                else:
                    pass

if __name__ == "__main__":
        # parser = argparse.ArgumentParser(description='input keyword')
        # parser.add_argument("keyword", help="keyword string")
        # parser.add_argument("num", help="the num of result")
        # args = parser.parse_args()
        #
        # spider = MeiTuanSpider(args.keyword.decode("gbk").encode("utf-8"), int(args.num))
        # spider.spider()
        spider = MeiTuanSpider("广告公司",20)
        spider.spider()

