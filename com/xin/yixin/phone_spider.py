# -*- encoding:utf-8 -*-

from RequestManage import PageDownload
from sqllite_manange import SqlLiteHandle
import time
import json
import re
import argparse
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")




"""
author:xin
created on 2018/6/01
"""



class BaiDuSearchSpider(object):
    def __init__(self, keyword, num):
        self.keyword = keyword
        #self.company_queue = Queue()
        self.base_url = "http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%s"
        self.h88_contact_filter = r'<li><label>联系人：</label><a href="http://b2b.huangye88.com/qiye\d+/company_contact.html" rel="nofollow">([^<]+)</a></li>'
        self.h88_phoneNum_filter = r'<label>手机：</label>([^<]+)</li>'
        self.h88_companyName_filter = r'公司名称：</label>([^<]+)</li><li><label>'
        self.h88_address_filter = r'meta name="location" content="province=河南;city=([^<]+)"'

        self.num = num
    def download_list_urls(self, url, filter_arg,next_url_filter=None):
        downloader = PageDownload()
        page = downloader.simple_download(url)
        company_host_list = re.findall(filter_arg, page)
        if next_url_filter:
            next_url = re.findall(next_url_filter, page)
            if next_url:
                next_url = next_url[0]
        else:
            next_url = None
        return company_host_list, next_url

    def download_company_page(self, url):
        downloader = PageDownload()
        page = downloader.simple_download(url)
        if not page:
            return False

        phone_num = re.findall(self.h88_phoneNum_filter, page)
        contact = re.findall(self.h88_contact_filter, page)
        company_name = re.findall(self.h88_companyName_filter, page)
        address = re.findall(self.h88_address_filter, page)
        if company_name:
            company_name = company_name[0]
        else:
            company_name = "未知"
        if address:
            address = address[0]
        else:
            address = "未知"
        if contact:
            contact = contact[0]
        else:
            contact = "未知"
        if phone_num:
            phone_num = phone_num[0]
        else:
            return False
        try:
            with open("temp_tt.dat", "a") as f:
                f.write(phone_num + "*" + contact + "\n")
        except:
            pass

        res = self.get_phone_info(phone_num)
        if res:
            province = res[0]
            city = res[1]
            yys = res[2]
        else:
            province = "未知"
            city = "未知"
            yys = "未知"
        print url, phone_num,contact,company_name,address
        db = SqlLiteHandle()
        sql = "insert into tt_1 values (?,?,?,?,?,?,?)"
        db.insert(sql,[(phone_num,contact,company_name,address,province,city,yys)])
        db.close()
        time.sleep(0.2)
        return True

    def create_table(self):
        #time_str = time.time()

        sql = "drop table tt_1"
        db = SqlLiteHandle()
        db.excute(sql)
        db.close()
        sql = """
        CREATE TABLE tt_1 (
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

    def get_phone_info(self, phone_num):
        url = "http://v.showji.com/Locating/showji.com20180331.aspx?&output=json&&m="+phone_num
        downloader = PageDownload()
        page = downloader.simple_download(url)
        if page is None:
            return None
        json_data = json.loads(page)
        #s = type(json_data)
        if json_data["QueryResult"] == "True":
            return [json_data["Province"], json_data["City"], json_data["Corp"]]
        else:
            return None


    def spider(self):
        if os.path.exists("temp_tt.dat"):
            # 删除文件，可使用以下两种方法。
            os.remove("temp_tt.dat")
        self.create_table()
        baidu_h88_url = self.base_url % (self.keyword+"黄页88网")
        h88_url, next_url = self.download_list_urls(baidu_h88_url, r' href = "(http://www.baidu.com/link\?url=[^=]+)"')
        i = 0
        for b_url in h88_url[:2]:
            next_url = b_url
            while next_url:
                company_list, next_url = self.download_list_urls(next_url,r'http://b2b.huangye88.com/qiye\d+/company_contact.html', r'<a href="(http://b2b.huangye88.com/[^<]+)">下一页</a>')
                for company in company_list:
                    rk = self.download_company_page(company)
                    if rk:
                        print i
                        i = i + 1
                        if i > self.num:
                            print "finished h88"
                            return






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='input keyword')
    parser.add_argument("keyword", help="keyword string")
    parser.add_argument("num", help="the num of result")
    args = parser.parse_args()

    spider = BaiDuSearchSpider(args.keyword.decode("gbk").encode("utf-8"), int(args.num))
    # spider = BaiDuSearchSpider("郑州市广告公司",20)
    spider.spider()
    #spider.get_phone_info("15172448316")