# -*- encoding:utf-8 -*-

from RequestManage import PageDownload
from sqllite_manange import SqlLiteHandle
import time
import json
import re
import argparse
import os
import sys

class ALiBBSpider():
    def __init__(self,keyword, num):
        self.keyword = keyword
        self.base_url = "http://data.p4psearch.1688.com/data/ajax/get_premium_offer_list.json?beginpage=%d&asyncreq=1&keywords=%s&sortType=&descendOrder=&province=&city=&priceStart=&priceEnd=&dis="
        self.hc_contact_filter = r'class="membername" target="_blank">([^<]+)</a>'
        #self.hc_contact_filter_ = r'<span class="ContactLeft letter04">联系人</span><span>：<em>([^<]+)</em>'
        self.hc_phoneNum_filter = r'<dd class="mobile-number">                        (\d+)'
        #self.hc_phoneNum_filter_ = r'<span class="ContactLeft letterLeft">手机</span><span>：(\d+)</span>'
        self.hc_company_name_filter = r'content="name=([^<]+);'
        #self.hc_company_name_filter_ = r'var infoname="([^<+])";'
        # self.hc_address_filter = r"</h3><p>地址：([^<]+)</p><p>"
        self.num = num


    def download_list_urls(self, url):
        downloader = PageDownload()
        page = downloader.simple_download(url)
        json_data = json.loads(page)
        content = json_data["data"]["content"]
        urls = []
        if content.has_key("offerResult"):
            items = content["offerResult"]
            for item in items:
                id = item["offerid"]
                _url = "http://detail.1688.com/offer/%s.html" % (id)
                urls.append(_url)
        return urls


    def download_company_page(self, url):
        downloader = PageDownload()
        page = downloader.simple_download(url)
        if not page:
            return False

        phone_num = re.findall(self.hc_phoneNum_filter, page)
        contact = re.findall(self.hc_contact_filter, page)
        company_name = re.findall(self.hc_company_name_filter, page)
        #address = re.findall(self.hc_address_filter, page)
        if company_name:
            company_name = company_name[0]
        # if address:
        #     address = address[0]
        if contact:
            contact = contact[0]
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
        print url, contact, phone_num
        db = SqlLiteHandle()
        sql = "insert into tt_1 values (?,?,?,NULL ,?,?,?)"
        db.insert(sql, [(phone_num, contact,company_name, province, city, yys)])
        db.close()
        time.sleep(0.2)
        return True


    def create_table(self):
        # time_str = time.time()

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
        url = "http://v.showji.com/Locating/showji.com20180331.aspx?&output=json&&m=" + phone_num
        downloader = PageDownload()
        page = downloader.simple_download(url)
        if page is None:
            return None
        json_data = json.loads(page)
        # s = type(json_data)
        if json_data["QueryResult"] == "True":
            return [json_data["Province"], json_data["City"], json_data["Corp"]]
        else:
            return None


    def spider(self):
        if os.path.exists("temp_tt.dat"):
            # 删除文件，可使用以下两种方法。
            os.remove("temp_tt.dat")
        self.create_table()


        # baidu_sq_url = self.base_url % (self.keyword + "顺企网")
        #
        # sq_url, next_url = self.download_list_urls(baidu_sq_url, r' href = "(http://www.baidu.com/link\?url=[^=]+)"')

        i = 1
        # for b_url in sq_url[:2]:
        next_url = self.base_url % (i, self.keyword)
        while True:
                company_list = self.download_list_urls(next_url)

                # if next_url and not next_url.startswith("http"):
                #     next_url = "http:" + next_url
                if not company_list:
                    return
                for company in company_list:
                    if not company.startswith("http"):
                        company = "http:" + company
                    print company
                    rk = self.download_company_page(company)
                    time.sleep(1)
                    if rk:
                        print i
                        i = i + 1
                        next_url = self.base_url % (i, self.keyword)

                        if i > self.num:
                            print "finished hc"
                            return



if __name__ == "__main__":
    spider = ALiBBSpider("培训机构",20)
    spider.spider()