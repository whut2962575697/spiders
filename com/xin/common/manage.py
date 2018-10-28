# -*- encoding:utf-8 -*-

from com.xin.common.tools import create_file

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

"""
@author:xin
@date:2018/05/01
@content:create a new spider package
"""

def create_spider(source):
    path = "../spiders/"+source+"_spider"
    create_file(path=path, file_name="_init_.py")
    init_spider_context = """
    # -*- encoding:utf-8 -*-

from com.xin.spiders.spider.init_spider import Initializer

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

initializer = Initializer(source="""+'"'+source+'"'+""", table_config="table_config.json",filter_config="init_data.json")"""
    create_file(path=path, file_name="init_spider.py",context=init_spider_context)
    start_steal_context = """
    # -*- encoding:utf-8 -*-

from com.xin.spiders.spider.ai_url_consumer import UrlConsumer
from spider import Spider

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def main_run(thread_num, source):
    thread_pool = []
    for i in range(thread_num):
        url_consumer = UrlConsumer(50, 25, source)
        spider = Spider(source=source)
        url_consumer.set_spider(spider=spider)
        thread_pool.append(url_consumer)

    for thread in thread_pool:
        thread.start()


if __name__ == "__main__":
    main_run(10, """+'"'+source+'"'+""")"""
    create_file(path=path, file_name="start_steal.py",context=start_steal_context)
    spider_context = """
    # -*- encoding=utf-8 -*-

from com.xin.common.MysqlManage import MysqlHandle
from com.xin.common.RequestManage import PageDownload
from com.xin.common.tools import to_md5
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Spider(object):
    def __init__(self, source):

        self.url_table = source+"_url_table"
        self.filter_table = source+"_filter_table"
        self.page_table = source+"_page_table"
        self.source = source

    def process(self, tuple_from_queue, proxy):
        print tuple_from_queue
        (urlmd5, url, url_type) = tuple_from_queue
        download_tool = DownloadTool(source=self.source)
        if url_type != 0:
            res = download_tool.download_list_page(urlmd5=urlmd5, url=url, proxy=proxy, domain="http://www.51ape.com")

        else:
            res = download_tool.download_page(urlmd5=urlmd5, url=url, proxy=proxy)
        if res:
            download_result = {
                "total": 1,
                "success": 1
            }
        else:
            download_result = {
                "total": 1,
                "success": 0,
                "failed_list": tuple_from_queue
            }
        return download_result


class DownloadTool(object):
    def __init__(self, source):

        self.url_table = source+"_url_table"
        self.filter_table = source + "_filter_table"
        self.page_table = source + "_page_table"
        self.reg = r'href="([^\s]+)"'
        self.js0_reg = r'<a href="javascript:void\(0\)" class="gs_b ajs">([^=]+)<span>[^=]+</span></a>'

    def download_list_page(self, urlmd5, url, proxy, domain=None):
        downloader = PageDownload(proxy=proxy)
        page = downloader.simple_download(url=url)
        if page is not None:
            new_urls = re.findall(self.reg, page)
            singer_names = re.findall(self.js0_reg, page)
            for singer_name in singer_names:
                merge_url = "http://www.51ape.com/skin/ape/php/qx_2.php?qx=" + singer_name
                new_urls.append(merge_url)
            for _url in new_urls:
                if domain is not None:
                    if _url.startswith("/"):
                        new_url = domain + _url
                    else:
                        new_url = _url
                else:
                    new_url = _url
                url_type = self.filter_url(url=new_url)
                if url_type is not None:
                    new_urlmd5 = to_md5(in_str=new_url)
                    sql = "select * from  "+self.url_table+" where urlmd5='%s'" % (new_urlmd5)
                    db = MysqlHandle()
                    results = db.query(sql=sql)
                    db.close()
                    if not results:
                        db = MysqlHandle()
                        insert_sql = "insert into "+self.url_table+" values (%s,%s,%s,%s,now())"
                        db.insert(sql=insert_sql, value_list=[(new_urlmd5, new_url, url_type, 0)])
                        db.close()
                    else:
                        print "This url is already in the database!!"
                else:
                    pass
            update_sql = "update "+self.url_table+" set status=200 where urlmd5='%s'" % (urlmd5)
            db = MysqlHandle()
            db.update(sql=update_sql)
            db.close()
            return True
        else:
            return False

    def download_page(self, urlmd5, url, proxy):
        downloader = PageDownload(proxy=proxy)
        page = downloader.simple_download(url=url)
        if page is not None:
            file_name = self.extract_field_from_page(page=page, reg=r'<li class="fl ml_1 mt_08 c999">([^=]+)</li>')
            # if file_name is None:
            #     file_name = self.extract_field_from_page(page=page, reg=r'<h1>([^<]+)下载?</h1>')
            singer_name = self.extract_field_from_page(page=page, reg=r'<li><a class="fl c3b ml_1 mt_08" href="http:'
                                                                      r'//www.51ape.com/[^=]+/" title="[^=]+">([^=]+)'
                                                                      r'</a></li>')
            baiduyun_url = self.extract_field_from_page(page=page, reg=r'href="(https?://pan.baidu.com/s/[^=]+)"')
            baiduyun_password = self.extract_field_from_page(page=page, reg=r'提取<em class="dn"></em>密码：(\w+)</b>')
            sql = "insert into " + self.page_table + "  values (%s,%s,%s,%s,%s,%s,now())"
            db = MysqlHandle()
            db.insert(sql=sql, value_list=[(urlmd5, url, file_name, singer_name, baiduyun_url,
                                            baiduyun_password)])
            db.close()
            update_sql = "update " + self.url_table + " set status=200 where urlmd5='%s'" % (urlmd5)
            db = MysqlHandle()
            db.update(sql=update_sql)
            db.close()
            return True
        else:
            return False

    def extract_field_from_page(self, page, reg):
        res = re.findall(reg, page)
        if res:
            return res[0]
        else:
            return None
    
    def filter_url(self, url):
        sql = "select type, filter from "+self.filter_table
        db = MysqlHandle()
        filter_data = db.query(sql=sql)
        for _filter in filter_data:
            _type = _filter[0]
            _url = _filter[1]
            if re.match(_url, url) is not None:
                return _type
        return None

    """
    create_file(path=path, file_name="spider.py",context=spider_context)
    table_config_context = """{
  "url_table":{
    "fields":
    [
      {"field_name":"urlmd5", "field_type":"varchar2", "field_length":50},
      {"field_name":"url", "field_type":"varchar2", "field_length":800},
      {"field_name":"type", "field_type":"number"},
      {"field_name":"status", "field_type":"number"},
      {"field_name":"datetime", "field_type":"datetime"}
    ],
    "primary_key":["urlmd5"]
  },
  "filter_table":{
    "fields":
    [
      {"field_name":"type", "field_type":"number"},
      {"field_name":"filter", "field_type":"varchar2", "field_length":100}
    ]
  },
     "page_table":{
       "fields":
       [
         {"field_name":"urlmd5", "field_type":"varchar2", "field_length":50},
         {"field_name":"url", "field_type":"varchar2", "field_length":800},
         {"field_name":"file_name", "field_type":"varchar2", "field_length":300},
         {"field_name":"singer", "field_type":"varchar2", "field_length":100},
         {"field_name":"baiduyun_url", "field_type":"varchar2", "field_length":200},
         {"field_name":"baiduyun_password", "field_type":"varchar2", "field_length":8},
         {"field_name":"datetime", "field_type":"datetime"}
       ],
        "primary_key":["urlmd5"]
     }

}
    """
    create_file(path=path, file_name="table_config.json",context=table_config_context)
    init_data_context = """{
"filters":[
  {"type":0, "filter":"http://www.51ape.com/ape/\\d+.html"},
  {"type":2, "filter":"http://www.51ape.com/\\w+/"},
  {"type":3, "filter":"http://www.51ape.com/\\w+/index_\\d.html"},
  {"type":3, "filter":"http://www.51ape.com/skin/ape/php/qx_2.php?qx=[^=]+"}
],
  "url":{"urlmd5":"278caa6494cf393b5653d5240c6624c1", "url":"http://www.51ape.com/", "type":1, "status":0}
}
    """
    create_file(path=path, file_name="init_data.json",context=init_data_context)
    proxy_filter_context = """"""



if __name__ == "__main__":
    create_spider("aqi")
