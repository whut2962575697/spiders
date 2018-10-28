# -*- encoding:utf-8 -*-

from com.xin.common.MysqlManage import MysqlHandle
from com.xin.common.RequestManage import PageDownload

import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Spider(object):
    def __init__(self,page_num):
        self.page_num = page_num
        self.list_base_url = "http://exhibitor.diecastexpo.cn/catalog/search/Handle/ESresult.ashx?init=true&pageIndex=%d&pageSize=8&showId=&CateNo=&searchwords="
        self.page_base_url = "http://exhibitor.diecastexpo.cn/catalog/search/Eshow.aspx?Eid=%s"

    def download_list_page(self):
        for x in range(self.page_num):
            list_url = self.list_base_url % (x+1)
            downloader = PageDownload()
            page = downloader.simple_download(list_url)
            if page:
                ids = re.findall(r"onclick='javascript:Eshow\((\d+)\)'", page)
                for e_id in ids:
                    self.download_info_page(e_id)

    def download_info_page(self, e_id):
        page_url = self.page_base_url % (e_id)
        print page_url
        downloader = PageDownload()
        page = downloader.simple_download(page_url)
        if page:
            site = re.findall(r"<br />网址:([^<]+)<br />",page)
            if site:
                site = site[0]
            else:
                site = None
            company_name = re.findall(r"<strong>([^<]+)</strong>",page)
            if company_name:
                company_name = company_name[0]
            else:
                company_name = None
            zw_num = re.findall(r'<span class="glyphicon glyphicon-envelope"></span> 展位号: (\w+)',page)
            if zw_num:
                zw_num = zw_num[0]
            else:
                zw_num = None
            mail = re.findall(r'</span> 邮箱：<a href="mailto:([^<]+@[^<]+)">[^<]+@[^<]+</a>',page)
            if mail:
                mail = mail[0]
            else:
                mail = None

            db = MysqlHandle()
            sql = "insert into diecast VALUES (%s,%s,%s,%s)"
            db.insert(sql,[(site,company_name,zw_num,mail)])
            db.close()


if __name__ == "__main__":
    spider = Spider(26)
    spider.download_list_page()






