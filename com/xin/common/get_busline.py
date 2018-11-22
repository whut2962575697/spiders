# -*- coding:utf-8 -*-

from com.xin.common.RequestManage import PageDownload
from com.xin.common.tools import is_json
from com.xin.common.MysqlManage import MysqlHandle
import json
import sys
import re
import time
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


def get_page_url(line_name, line_type, city_code, coords):
    base_url = 'http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=bl&da_src=searchBox.button&wd=%s&c=%d&l=13&b=(%s)&from=webmap&sug_forward=&tn=B_NORMAL_MAP&nn=0'
    downloader = PageDownload(timeout=5)
    page = downloader.simple_download(base_url % (line_name, city_code, coords))
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
            page_url = 'http://map.baidu.com/?qt=bsl&tps=&newmap=1&uid='+uid+'&c=%d' %(city_code)
            line_list.append((name, uid, page_url, line_type))
        db = MysqlHandle()
        insert_sql = "insert into baidu_busline_url_analyse values(%s,%s,%s,%s,0)"
        db.insert(insert_sql, line_list)
        db.close()


def download_page():
    db = MysqlHandle()
    query_sql = "select uid,min(name),min(line_type), min(page_url) from baidu_busline_url_analyse where status=0 group by uid "
    page_infs = db.query(query_sql)
    db.close()
    downloader = PageDownload()

    for item in page_infs:
        print (item[0])
        page = downloader.simple_download(item[3])
        # if is_json(page):
        #     json_page = json.loads(page)
        #     if json_page.has_key("content"):
        #         main_info = json_page["content"][0]
        #         name = main_info["name"]
        #         timeable = main_info["timeable"]
        db = MysqlHandle()
        is_success = False
        if page is not None:
            insert_sql = "insert into baidu_busline_page values(%s,%s,%s,%s,NULL )"
            is_success = db.insert(insert_sql, [(item[0], item[1], item[2], page)])
        if is_success and page is not None:
            update_sql = "update baidu_busline_url_analyse set status=200 where uid='%s'" %(item[0])
            db.update(update_sql)
        db.close()


if __name__ == "__main__":
    # db = MysqlHandle()
    # query_sql = "select name,code,jc,coords from bd_city_info where status=0"
    # query_res = db.query(query_sql)
    # db.close()
    #
    #
    # for [city_name, city_code, jc, coords] in query_res:
    #     print city_name
    #     base_url = "http://"+jc+".8684.cn/line"
    #     i = 0
    #     for x in range(16, 30):
    #         url = base_url+str(x+1)
    #         try:
    #             lines = get_lines(url=url, type=x+1)
    #         except Exception, e:
    #             print (e.message)
    #             continue
    #         for line in lines:
    #             i = i+1
    #             get_page_url(line[0], line[1], int(city_code), coords)
    #     print (i)
    #     db = MysqlHandle()
    #     sql = 'update bd_city_info set status=200 where name="'+city_name+'"'
    #     db.update(sql)
    #     db.close()
    #     time.sleep(1)








    download_page()

