# -*- encoding:utf-8 -*-
from com.xin.common.RequestManage import PageDownload
from com.xin.common.MysqlManage import MysqlHandle
from com.xin.common.tools import is_json, to_md5
import json
import random, time


def update_geo_data(uid, l_type, city_code, name):
    page_table = "bdmap_api_" + name + "_" + str(city_code) + "_page_table"
    url = "http://map.baidu.com/?qt=ext&newmap=1&uid=%s&c=%d&nn=0&l=%d&ext_ver=new" % (uid, city_code, l_type)
    downloader = PageDownload()
    page = downloader.simple_download(url)
    if is_json(page):
        json_data = json.loads(page)
        if json_data.has_key("content"):
            content = json_data["content"]
            if content.has_key("geo"):
                geo = content["geo"]
                print (uid)
                md5 = to_md5(uid)
                sql = "update "+page_table+' set geo="'+geo+'" where md5="'+md5+'"'
                db = MysqlHandle()
                db.update(sql)
                db.close()
    time.sleep(random.uniform(0.5, 1.0))


def download(city_code, l_type, name, tag, city):
    page_table = "bdmap_api_" + name + "_" + str(city_code) + "_page_table"
    sql = 'select uid from '+page_table+' where tag like "%'+tag+'%"  and city="'+city+'" and geo is null'
    db = MysqlHandle()
    query_data = db.query(sql)
    for (uid,) in query_data:
        update_geo_data(uid, l_type, city_code, name)


if __name__ == "__main__":
    download(218, 10, "school", '高等院校', '武汉市')

