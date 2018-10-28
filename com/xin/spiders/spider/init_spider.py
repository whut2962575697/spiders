# -*- encoding:utf-8 -*-

from com.xin.common.models import Model
from com.xin.common.MysqlManage import MysqlHandle
from com.xin.common.ProxyCollectByApi import Collect
from com.xin.common.ProxyFilter import filter_avaliable_ips
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Initializer(object):
    def __init__(self, source, table_config, filter_config, test_url="http://www.baidu.com"):

        self.url_table = source+"_url_table"
        self.filter_table = source + "_filter_table"
        self.page_table = source+"_page_table"
        self.table_config = table_config
        self.filter_config = filter_config
        self.init_spider()
        collector = Collect(50)
        collector.process()
        filter_avaliable_ips(test_url)

    def init_spider(self):
        with open(self.table_config, 'r') as f:
            config_json = json.load(f)

        if  config_json.has_key("url_table"):
            print "creating url_table....."
            url_table_config = config_json["url_table"]
            self.create_table(table_name=self.url_table, table_config=url_table_config)
            print "....ok...."
        if config_json.has_key("filter_table"):
            print "creating filter_table....."
            filter_table_config = config_json["filter_table"]
            self.create_table(table_name=self.filter_table, table_config=filter_table_config)
            print "....ok...."
        print "creating page_table....."
        page_table_config = config_json["page_table"]
        self.create_table(table_name=self.page_table, table_config=page_table_config)
        if self.filter_config:
            with open(self.filter_config, 'r') as f:
                filter_config_json = json.load(f)

            self.add_filter_urls(filter_table_name=self.filter_table, filter_config=filter_config_json)
            self.add_init_url(url_table_name=self.url_table, filter_config=filter_config_json)
            print "....ok...."



    def create_table(self, table_name, table_config):
        fields_config = table_config["fields"]
        model = Model(table_name)
        for field in fields_config:
            if field["field_type"] == "varchar2":
                model.add_char_field(field_name=field["field_name"], field_length=field["field_length"])
            elif field["field_type"] == "number":
                if field.has_key("field_length") and field.has_key("field_precision"):
                    model.add_number_field(field_name=field["field_name"], field_length=field["field_length"],
                                           field_precision=field["field_precision"])
                elif field.has_key("field_length"):
                    model.add_number_field(field_name=field["field_name"], field_length=field["field_length"])
                else:
                    model.add_number_field(field_name=field["field_name"])
            elif field["field_type"] == "datetime":
                model.add_datetime_field(field_name=field["field_name"])
            elif field["field_type"] == "blob":
                model.add_blob_field(field_name=field["field_name"])
            else:
                print "The field_type of "+field["field_name"]+" is not exist!!"
                pass
        if table_config.has_key("primary_key"):
            model.set_primary_key(fields=table_config["primary_key"])
        else:
            pass
        model.commit()

    def add_filter_urls(self, filter_table_name, filter_config):
        filters = filter_config["filters"]
        value_list = []
        for filter in filters:
            value_list.append((filter["type"], filter["filter"]))
        db = MysqlHandle()
        insert_sql = "insert into "+filter_table_name+" values(%s,%s)"
        db.insert(sql=insert_sql, value_list=value_list)
        db.close()

    def add_init_url(self, url_table_name, filter_config):
        url = filter_config["url"]
        db = MysqlHandle()
        insert_sql = "insert into " + url_table_name + " values(%s,%s,%s,%s,now())"
        db.insert(sql=insert_sql, value_list=[(url["urlmd5"], url["url"], url["type"], url["status"])])
        db.close()

if __name__ == "__main__":
    initializer = Initializer(source="test", table_config="table_config.json", filter_config=None)
