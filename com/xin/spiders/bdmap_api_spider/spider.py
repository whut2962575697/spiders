# -*- encoding:utf-8 -*-

from com.xin.common.tools import split_boundary
from com.xin.common.RequestManage import PageDownload
from com.xin.common.MysqlManage import MysqlHandle
from com.xin.spiders.spider.init_spider import Initializer
from com.xin.common.tools import to_md5, is_json
import json


def init_spider(city_code, name, boundary):
    # Initializer(source="bdmap_api_"+name+"_"+str(city_code), table_config="table_config.json", filter_config=None, need_proxy=False)
    boundary_table = "bdmap_api_"+name+"_"+str(city_code)+"_boundary_table"
    lng_min, lat_min, lng_max, lat_max = boundary
    boundarys = split_boundary(float(lat_max), float(lat_min), float(lng_max),
                               float(lng_min), 10, 0.1)
    for _boundary in boundarys:
        _lng_min = _boundary[1][0]
        _lat_min = _boundary[0][0]
        _lng_max = _boundary[1][1]
        _lat_max = _boundary[0][1]
        _boundary_st = str(_boundary[0][0]) + "," + str(_boundary[1][0]) + "," + str(_boundary[0][1]) + "," + str(
            _boundary[1][1])
        md5 = to_md5(_boundary_st)
        db = MysqlHandle()
        sql = "insert into "+boundary_table+" values(%s,%s,1,%s,%s,%s,%s,0,0,now())"
        db.insert(sql, [[md5, _boundary_st, _lng_min, _lat_min, _lng_max, _lat_max]])
        db.close()


def spider(city_code, name, keyword, key_token):
    boundary_table = "bdmap_api_" + name + "_" + str(city_code) + "_boundary_table"
    page_table = "bdmap_api_" + name + "_" + str(city_code) + "_page_table"
    base_url = "http://api.map.baidu.com/place/v2/search?query=%s&scope=2&bounds=%s&output=json&ak=%s&page_num=%d"
    sql = "select md5, boundary from "+boundary_table+" where status=0"
    db = MysqlHandle()
    res_data = db.query(sql)
    for (md5, boundary) in res_data:
        url = base_url % (keyword, boundary, key_token, 0)
        downloader = PageDownload()
        page = downloader.simple_download(url)
        if is_json(page):
            json_data = json.loads(page)
            status = json_data["status"]
            total = json_data["total"]
            print (boundary, url, total)
            if status == 0 and int(total)>0:
                page_count = int(total)/10
                for x in range(0, page_count+2):
                    _url = base_url % (keyword, boundary, key_token, x)
                    downloader = PageDownload()
                    _page = downloader.simple_download(_url)
                    if is_json(_page):
                        _json_data = json.loads(_page)
                        results = _json_data["results"]
                        for item in results:
                            name = item["name"]
                            address = item["address"]
                            province = item["province"]
                            city = item["city"]
                            area = item["area"]
                            uid = item["uid"]
                            _md5 = to_md5(uid)
                            lat = item["location"]["lat"]
                            lng = item["location"]["lng"]
                            try:
                                tag = item["detail_info"]["tag"]
                            except Exception, e:
                                tag = None
                                print (e.message)
                            sql = "insert into "+page_table+" values(%s,%s,%s,%s,null,%s,%s,%s,%s,%s,null,null,%s,null,now(),null)"
                            db = MysqlHandle()
                            db.insert(sql, [[_md5, uid, name, address, province, city, area, lng, lat, tag]])
                            db.close()

            sql = 'update '+boundary_table+' set status=200,total_count='+str(total)+' where md5="'+md5+'"'
            db = MysqlHandle()
            db.update(sql)
            db.close()


def split_boundary_outline(b_type, city_code, name):
    boundary_table = "bdmap_api_" + name + "_" + str(city_code) + "_boundary_table"
    sql = 'select lng_min,lat_min,lng_max,lat_max from '+boundary_table+" where type="+str(b_type)+" and total_count=400"
    db = MysqlHandle()
    query_res = db.query(sql)
    for (lng_min, lat_min, lng_max, lat_max) in query_res:
        boundarys = split_boundary(float(lat_max), float(lat_min), float(lng_max),
                                   float(lng_min), 10, 0.1)
        for _boundary in boundarys:
            _lng_min = _boundary[1][0]
            _lat_min = _boundary[0][0]
            _lng_max = _boundary[1][1]
            _lat_max = _boundary[0][1]
            _boundary_st = str(_boundary[0][0]) + "," + str(_boundary[1][0]) + "," + str(_boundary[0][1]) + "," + str(
                _boundary[1][1])
            md5 = to_md5(_boundary_st)
            db = MysqlHandle()
            sql = "insert into " + boundary_table + " values(%s,%s,2,%s,%s,%s,%s,0,0,now())"
            db.insert(sql, [[md5, _boundary_st, _lng_min, _lat_min, _lng_max, _lat_max]])
            db.close()


if __name__ == "__main__":
    #init_spider(218, "school", [113.707703, 29.972900, 115.086123, 31.367126])
    split_boundary_outline(1, 218, "school")
    spider(218, "school", "大学", "XwpZGfXMn45W9Czd1UwmC6RwMMULD1Ue")











