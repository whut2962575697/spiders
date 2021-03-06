
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
        self.domain = "http://www.carflac.com"

    def process(self, tuple_from_queue, proxy):
        print tuple_from_queue
        (urlmd5, url, url_type) = tuple_from_queue
        download_tool = DownloadTool(source=self.source)
        if url_type != 0:
            res = download_tool.download_list_page(urlmd5=urlmd5, url=url, proxy=proxy, domain=self.domain)

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
                "failed_list": [tuple_from_queue]
            }
        return download_result


class DownloadTool(object):
    def __init__(self, source):

        self.url_table = source+"_url_table"
        self.filter_table = source + "_filter_table"
        self.page_table = source + "_page_table"
        self.domain = "http://www.carflac.com"
        self.reg = r'href="([^\s]+)"'
        self.js0_reg = r'<a href="javascript:void\(0\)" class="gs_b ajs">([^=]+)<span>[^=]+</span></a>'

    def download_list_page(self, urlmd5, url, proxy, domain=None):
        downloader = PageDownload(proxy=proxy,timeout=10)
        page = downloader.simple_download(url=url)
        if page is not None:
            new_urls = re.findall(self.reg, page)
            # singer_names = re.findall(self.js0_reg, page)
            # for singer_name in singer_names:
            #     merge_url = "http://www.51ape.com/skin/ape/php/qx_2.php?qx=" + singer_name
            #     new_urls.append(merge_url)
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
            #print page.decode("utf-8")
            file_name = self.extract_field_from_page(page=page, reg=r'专辑名称：([^<]+)')
            if file_name is None:
                file_name = self.extract_field_from_page(page=page, reg=r'<h1 class="title">([^<]+)</h1>')
            music_type = self.extract_field_from_page(page=page, reg=r'&nbsp;<a href="/\w+/">([^<]+)</a>')

            # if file_name is None:
            #     file_name = self.extract_field_from_page(page=page, reg=r'<h1>([^<]+)下载?</h1>')
            singer_name = self.extract_field_from_page(page=page, reg=r'专辑艺人：([^<]+)')
            baiduyun_url = self.extract_field_from_page(page=page, reg=r"""<a href="#ecms" onclick="window.open\('([^<]+)','','width=300,height=300,resizable=yes'\)""")
            print baiduyun_url
            if baiduyun_url is None:
                return False
            if baiduyun_url is not None:
                baiduyun_url = self.domain+baiduyun_url
            baiduyun_password = self.extract_field_from_page(page=page, reg=r'密码: (\w+)')
            sql = "insert into " + self.page_table + "  values (%s,%s,%s,%s,%s,%s,%s,now())"
            db = MysqlHandle()
            db.insert(sql=sql, value_list=[(urlmd5, url, file_name,music_type, singer_name, baiduyun_url,
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
    