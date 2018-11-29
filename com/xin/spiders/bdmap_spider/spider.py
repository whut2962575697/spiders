# -*- encoding=utf-8 -*-

from com.xin.common.MysqlManage import MysqlHandle
from com.xin.common.RequestManage import PageDownload
from com.xin.common.tools import to_md5, split_boundary,is_json
import re
import json
import time
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
        (urlmd5, url, url_type,boundary) = tuple_from_queue
        download_tool = DownloadTool(source=self.source)
        if url_type != 0:
            res = download_tool.download_list_page(urlmd5=urlmd5, url=url, boundary=boundary, proxy=proxy, domain="http://www.51ape.com")

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
        self.city_code = 218
        self.keyword = "景点"
        self.url_table = source+"_url_table"
        self.filter_table = source + "_filter_table"
        self.page_table = source + "_page_table"
        self.reg = r'href="([^\s]+)"'
        self.js0_reg = r'<a href="javascript:void\(0\)" class="gs_b ajs">([^=]+)<span>[^=]+</span></a>'
        self.list_url = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=spot&from=webmap&c=%d&wd=%s&wd2=&pn=0&nn=0&db=0&sug=0&addr=0&pl_data_type=life&pl_sort_type=data_type&pl_sort_rule=0&pl_business_type=cinema&pl_business_id=&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=12&rn=10&tn=B_NORMAL_MAP&ie=utf-8&b=(%s)' # (city_code,keyword,boundary)
        self.page_url = 'https://map.baidu.com/?ugc_type=3&ugc_ver=1&qt=detailConInfo&device_ratio=2&compat=1&uid=%s&primaryUid=%s' # (uid,primaryUid)

    def download_list_page(self, urlmd5, url, proxy, boundary, domain=None):
        downloader = PageDownload(proxy=proxy)
        page = downloader.simple_download(url=url)
        if is_json(page):
            json_page = json.loads(page)
            result = json_page["result"]
            total_count = result["total"]
            print ("total:"+str(total_count))
            if int(total_count) <= 10 and int(total_count)>0:
                content = json_page["content"]
                for item in content:
                    uid = item["uid"]
                    primary_uid = item["primary_uid"]

                    new_url = self.page_url % (uid, primary_uid)
                    new_urlmd5 = to_md5(in_str=new_url)
                    url_type = 0
                    boundary = None
                    status = 0
                    sql = "select * from  " + self.url_table + " where urlmd5='%s'" % (new_urlmd5)
                    db = MysqlHandle()
                    results = db.query(sql=sql)
                    db.close()
                    if not results:
                        db = MysqlHandle()
                        insert_sql = "insert into " + self.url_table + " values (%s,%s,%s,%s,%s,now())"
                        db.insert(sql=insert_sql, value_list=[(new_urlmd5, new_url, url_type, boundary,status)])
                        db.close()
                    else:
                        print "This url is already in the database!!"
            elif int(total_count) <= 0:
                pass
            else:
                min_interval = boundary.split(";")[0]
                max_interval = boundary.split(";")[1]
                lat_min = min_interval.split(",")[1]
                lat_max = max_interval.split(",")[1]
                lng_min = min_interval.split(",")[0]
                lng_max = max_interval.split(",")[0]
                boundarys = split_boundary(int(float(lat_max)), int(float(lat_min)), int(float(lng_max)), int(float(lng_min)), 4, 0.2)
                for _boundary in boundarys:
                    _boundary_st = str(_boundary[1][0])+","+str(_boundary[0][0])+";"+str(_boundary[1][1])+","+str(_boundary[0][1])
                    new_url = self.list_url % (self.city_code,self.keyword, _boundary_st)
                    new_urlmd5 = to_md5(in_str=new_url)
                    url_type = 1
                    boundary = _boundary_st
                    status = 0
                    db = MysqlHandle()
                    insert_sql = "insert into " + self.url_table + " values (%s,%s,%s,%s,%s,now())"
                    db.insert(sql=insert_sql, value_list=[(new_urlmd5, new_url, url_type, boundary, status)])
                    db.close()
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
        if is_json(page):
            page_json = json.loads(page)
            content = page_json["content"]
            uid = content["uid"]
            name = content["name"]
            address = content["addr"]
            if content.has_key("phone"):
                phone = content["phone"]
            else:
                phone = None

            x = content["navi_x"]
            y = content["navi_y"]
            geo = content["geo"]
            ext = content["ext"]
            if type(ext) == type({"ee":""}):
                detail_info = ext["detail_info"]
            else:
                detail_info = {"info":""}
            if detail_info.has_key("tag"):
                tag = detail_info["tag"]
            else:
                tag = None
            if detail_info.has_key("image"):
                image = detail_info["image"]
            else:
                image = None
            if detail_info.has_key("display_info_redu"):
                dispaly_redu = detail_info["display_info_redu"]
            else:
                dispaly_redu = None
            if detail_info.has_key("price"):
                price = detail_info["price"]
            else:
                price = None

            sql = "insert into " + self.page_table + "  values (%s,%s,%s,%s,%s,%s,%s,%s,null,null,null,%s,%s,%s,null,%s,now())"
            db = MysqlHandle()
            db.insert(sql=sql, value_list=[(urlmd5, url, uid, name, address, phone, x, y, tag, image,  price, dispaly_redu)])
            db.close()
            update_sql = "update " + self.url_table + " set status=200 where urlmd5='%s'" % (urlmd5)
            db = MysqlHandle()
            db.update(sql=update_sql)
            db.close()
            return True
        else:
            return False


