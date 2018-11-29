# -*- encoding:utf-8 -*-

from MysqlManage import MysqlHandle
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Model(object):
    def __init__(self, table_name):
        self.table = table_name
        self.create_table()

    def create_table(self):
        sql = "create table " + self.table + " (_id_temp_ int)"
        db = MysqlHandle()
        db.excute(sql=sql)
        db.close()

    def add_medium_blob_field(self, field_name):
        sql = "alter table "+self.table+" add "+field_name+" MEDIUMBLOB"
        db = MysqlHandle()
        db.excute(sql=sql)
        db.close()

    def add_char_field(self, field_name, field_length):
        sql = "alter table "+self.table+" add "+field_name+" varchar("+str(field_length)+")"
        db = MysqlHandle()
        db.excute(sql=sql)
        db.close()

    def add_number_field(self, field_name, field_length=4, field_precision=0):
        if field_precision == 0:
            sql = "alter table " + self.table + " add " + field_name + " int("+str(field_length)+")"
        else:
            sql = "alter table " + self.table + " add " + field_name + " double("+str(field_length)+", "\
                  + str(field_precision)+")"
        db = MysqlHandle()
        db.excute(sql=sql)
        db.close()

    def add_datetime_field(self, field_name):
        sql = "alter table " + self.table + " add " + field_name + " datetime"
        db = MysqlHandle()
        db.excute(sql=sql)
        db.close()

    def add_blob_field(self, field_name):
        sql = "alter table " + self.table + " add "+field_name + " blob"
        db = MysqlHandle()
        db.excute(sql=sql)
        db.close()

    def drop_field(self, field_name):
        sql_de = "alter table " + self.table + " drop column " + field_name
        db = MysqlHandle()
        db.excute(sql=sql_de)
        db.close()

    def set_primary_key(self, fields):
        primary_str = ""
        for field in fields:
            primary_str += field + ","
        primary_str = primary_str.strip(",")
        sql = "alter table " + self.table + " add primary key (" + primary_str + ")"
        db = MysqlHandle()
        db.excute(sql=sql)

    def commit(self):
        self.drop_field(field_name="_id_temp_")


if __name__ == "__main__":
        table1 = Model("tk1")
        table1.add_char_field(field_name="name", field_length=10)
        table1.set_primary_key(fields=["name"])
        table1.commit()
