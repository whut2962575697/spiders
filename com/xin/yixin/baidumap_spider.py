# -*- encoding:utf-8 -*-

from RequestManage import PageDownload
from sqllite_manange import SqlLiteHandle

import sys
import re
import json
import time
import argparse
import os
reload(sys)
sys.setdefaultencoding("utf-8")

class BaiDuMapSpider(object):
    def __init__(self, keyword,num):
        self.keyword = keyword
        self.num = num
        self.base_url = "http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=spot&from=webmap&c=268&wd=%s&wd2=&pn=%d&nn=%d&db=0&sug=0&addr=0&&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=11&rn=50&tn=B_NORMAL_MAP"

    def download_page_info(self,json_data):
        if json_data.has_key("content"):
            content = json_data["content"]
            value_list = []
            for item in content:
                company_name = item["name"]
                addr = item["addr"]
                if item.has_key("tel"):
                    phone_num = item["tel"]
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
        while status:
            url = self.base_url % (self.keyword, i, i*10)
            downloader = PageDownload()
            page = downloader.simple_download(url)
            if page:
                json_data = json.loads(page)
                if json_data.has_key("content"):
                    self.download_page_info(json_data)
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

    spider = BaiDuMapSpider(args.keyword.decode("gbk").encode("utf-8"),int(args.num))
    spider.spider()
    # spider = BaiDuMapSpider("郑州市广告公司")
    # spider.spider()