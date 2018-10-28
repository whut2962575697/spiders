# -*- encoding=utf-8 -*-

from com.xin.common.MysqlManage import MysqlHandle
from com.xin.common.RequestManage import PageDownload
from com.xin.common.tools import to_md5
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Spider(object):
    def __init__(self, url_table, filter_table, page_table):

        self.url_table = url_table
        self.filter_table = filter_table
        self.page_table = page_table

    def process(self, tuple_from_queue, proxy):
        print tuple_from_queue
        (urlmd5, url, url_type) = tuple_from_queue
        download_tool = DownloadTool()
        if url_type != 0:
            res = download_tool.download_list_page(urlmd5=urlmd5, url=url, proxy=proxy, url_table=self.url_table,
                                             filter_table=self.filter_table, domain="http://www.51ape.com")

        else:
            res = download_tool.download_page(urlmd5=urlmd5, url=url, proxy=proxy, url_table=self.url_table,
                                        page_table=self.page_table)
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
    def __init__(self):
        self.headers = {
            'User_Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; '
                          'Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
        }
        self.reg = r'href="([^\s]+)"'

    def download_list_page(self, urlmd5, url, proxy, url_table, filter_table, domain=None):
        downloader = PageDownload(proxy=proxy)
        page = downloader.simple_download(url=url)
        if page is not None:
            new_urls = re.findall(self.reg, page)
            for _url in new_urls:
                if domain is not None:
                    if _url.startswith("/"):
                        new_url = domain + _url
                    else:
                        new_url = _url
                else:
                    new_url = _url
                url_type = self.filter_url(url=new_url, filter_table=filter_table)
                if url_type is not None:
                    new_urlmd5 = to_md5(in_str=new_url)
                    sql = "select * from  "+url_table+" where urlmd5='%s'" % (new_urlmd5)
                    db = MysqlHandle()
                    results = db.query(sql=sql)
                    db.close()
                    if not results:
                        db = MysqlHandle()
                        insert_sql = "insert into "+url_table+" values (%s,%s,%s,%s,now())"
                        db.insert(sql=insert_sql, value_list=[(new_urlmd5, new_url, url_type, 0)])
                        db.close()
                    else:
                        print "This url is already in the database!!"
                else:
                    pass
            update_sql = "update "+url_table+" set status=200 where urlmd5='%s'" % (urlmd5)
            db = MysqlHandle()
            db.update(sql=update_sql)
            db.close()
            return True
        else:
            return False

    def download_page(self, urlmd5, url, proxy, url_table, page_table):
        downloader = PageDownload(proxy=proxy)
        page = downloader.simple_download(url=url)
        if page is not None:
            file_name = self.extract_field_from_page(page=page, reg=r'<h1 class="yh mt_1 f_32">([^<]+\.[a-z]+)</h1>')
            file_size = self.extract_field_from_page(page=page, reg=r'<h3 class="c999 fl mt_05 f_12 n yh">'
                                                                    r'<em class="n ml_1 mr_1">·</em>(\d+\.?\d+M)</h3>')
            baiduyun_url = self.extract_field_from_page(page=page, reg=r'href="(https?://pan.baidu.com/[^\s]+)"')
            baiduyun_password = self.extract_field_from_page(page=page, reg=r'<em class="dn"></em>密码：(\w+)</b>')
            sql = "insert into " + page_table + "  values (%s,%s,%s,%s,%s,%s,now())"
            db = MysqlHandle()
            db.insert(sql=sql, value_list=[(urlmd5, url, file_name, file_size, baiduyun_url,
                                            baiduyun_password)])
            db.close()
            update_sql = "update " + url_table + " set status=200 where urlmd5='%s'" % (urlmd5)
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

    def filter_url(self, url, filter_table):
        sql = "select type, filter from "+filter_table
        db = MysqlHandle()
        filter_data = db.query(sql=sql)
        for _filter in filter_data:
            _type = _filter[0]
            _url = _filter[1]
            if re.match(_url, url) is not None:
                return _type
        return None







