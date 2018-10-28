
    # -*- encoding:utf-8 -*-

from com.xin.spiders.spider.init_spider import Initializer
from com.xin.common.MysqlManage import MysqlHandle

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class BaiDuInitializer(Initializer):
    def add_init_url(self, url_table_name, filter_config):
        url = filter_config["url"]
        db = MysqlHandle()
        insert_sql = "insert into " + url_table_name + " values(%s,%s,%s,%s,%s,now())"
        db.insert(sql=insert_sql, value_list=[(url["urlmd5"], url["url"], url["type"], url["boundary"], url["status"])])
        db.close()


if __name__ == "__main__":
    initializer = BaiDuInitializer(source="bdmap_hotel", table_config="table_config.json", filter_config="init_data.json")
