# -*- coding:utf-8 -*-

from com.xin.common.RequestManage import PageDownload
from com.xin.common.tools import is_json
from com.xin.common.MysqlManage import MysqlHandle
import json
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')


def get_lines(url, type):
    downloader = PageDownload()
    page = downloader.simple_download(url)
    reg = r'<a href="/x_[^<]+" >([^<]+)</a>'
    res = re.findall(reg, page)
    lines = []
    for item in res:
        lines.append((item, type))
    return lines


def get_page_url(line_name, line_type):
    base_url = 'http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=bl&da_src=searchBox.button&wd='+line_name+'&c=218&l=13&b=(12658020.44,3478524.27;12811429.27,3658064.64)&from=webmap&sug_forward=&tn=B_NORMAL_MAP&nn=0'
    downloader = PageDownload()
    page = downloader.simple_download(base_url)
    if is_json(page):
        json_data = json.loads(page)
        if not json_data.has_key('content'):
            print base_url
            return
        contents = json_data['content']
        line_list = []
        for item in contents:
            name = item['name']

            if not item.has_key("uid"):
                print name, base_url
                continue
            uid = item['uid']
            page_url = 'http://map.baidu.com/?qt=bsl&tps=&newmap=1&uid='+uid+'&c=218'
            line_list.append((name, uid, page_url, line_type))
        db = MysqlHandle()
        insert_sql = "insert into baidu_busline_url_analyse values(%s,%s,%s,%s,0)"
        db.insert(insert_sql, line_list)
        db.close()


def download_page():
    db = MysqlHandle()
    query_sql = "select name,type,url from baidu_busline_url_analyse where http_status=0"
    page_infs = db.query(query_sql)
    db.close()
    downloader = PageDownload()

    for item in page_infs:
        page = downloader.simple_download(item[2])
        db = MysqlHandle()
        insert_sql = "insert into baidu_busline_page values(%s,%s,%s)"
        is_success = db.insert(insert_sql, [(item[0], item[1], page)])
        if is_success:
            update_sql = "update baidu_busline_url_analyse set http_status=200 where name='%s'" %(item[0])
            db.update(update_sql)
        db.close()


if __name__=="__main__":
    base_url = "http://shanghai.8684.cn/line"
    for x in range(16):
        url = base_url+str(x+1)
        lines = get_lines(url=url, type=x+1)
        for line in lines:
            get_page_url(line[0], line[1])

    download_page()

