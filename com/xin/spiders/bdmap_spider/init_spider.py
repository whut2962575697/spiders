# -*- encoding:utf-8 -*-

from com.xin.spiders.spider.init_spider import Initializer
from com.xin.common.MysqlManage import MysqlHandle
from spider import Spider
from com.xin.common.tools import split_boundary, to_md5

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class BaiDuInitializer(Initializer):

    def add_init_url(self, url_table_name, filter_config, city_code, keyword):
        list_url = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=spot&from=webmap&c=%d&wd=%s&wd2=&pn=0&nn=0&db=0&sug=0&addr=0&pl_data_type=life&pl_sort_type=data_type&pl_sort_rule=0&pl_business_type=cinema&pl_business_id=&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=12&rn=10&tn=B_NORMAL_MAP&ie=utf-8&b=(%s)'
        url = filter_config["url"]
        # db = MysqlHandle()
        # insert_sql = "insert into " + url_table_name + " values(%s,%s,%s,%s,%s,now())"
        # db.insert(sql=insert_sql, value_list=[(url["urlmd5"], url["url"], url["type"], url["boundary"], url["status"])])
        # db.close()
        boundary = url["boundary"]
        min_interval = boundary.split(";")[0]
        max_interval = boundary.split(";")[1]
        lat_min = min_interval.split(",")[1]
        lat_max = max_interval.split(",")[1]
        lng_min = min_interval.split(",")[0]
        lng_max = max_interval.split(",")[0]

        boundarys = split_boundary(int(float(lat_max)), int(float(lat_min)), int(float(lng_max)), int(float(lng_min)),
                                   20, 0.2)
        for _boundary in boundarys:
            _boundary_st = str(_boundary[1][0]) + "," + str(_boundary[0][0]) + ";" + str(_boundary[1][1]) + "," + str(
                _boundary[0][1])
            new_url = list_url % (city_code, keyword, _boundary_st)
            new_urlmd5 = to_md5(in_str=new_url)
            url_type = 2
            boundary = _boundary_st
            status = 0
            db = MysqlHandle()
            insert_sql = "insert into " + self.url_table + " values (%s,%s,%s,%s,%s,now())"
            db.insert(sql=insert_sql, value_list=[(new_urlmd5, new_url, url_type, boundary, status)])
            db.close()



if __name__ == "__main__":
    initializer = BaiDuInitializer(source="bdmap_spot", table_config="table_config.json", filter_config="init_data.json", city_code=218, keywork="景点")
