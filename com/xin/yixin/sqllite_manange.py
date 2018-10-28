# -*- encoding:utf-8 -*-

import sqlite3 as db
import sys
reload(sys)


class SqlLiteHandle(object):
    def __init__(self, db_file="data.db"):
        self.con = db.connect(db_file)
        self.con.text_factory = str
        self.cur = None

 # 查询，返回查询结果，为一个list
    def query(self, sql):
        self.cur = self.con.cursor()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.cur.close()
        return result

    # 插入，插入的为一个列表
    # 返回布尔值，用来判断是否插入成功
    def insert(self, sql, value_list):

        self.cur = self.con.cursor()
        try:
            self.cur.executemany(sql, value_list)
            self.con.commit()
            self.cur.close()
            return True
        except Exception, e:
            print str(e)
            self.cur.close()
        return False

    # 删除, 捕获异常，返回布尔值
    def delete(self, sql):
        self.cur = self.con.cursor()
        try:
            self.cur.execute(sql)
            self.con.commit()
            self.cur.close()
            return True
        except Exception, e:
            print str(e)
            self.cur.close()
        return False

    # 更新
    def update(self, sql):
        self.cur = self.con.cursor()
        try:
            self.cur.execute(sql)
            self.con.commit()
            self.cur.close()
            return True
        except Exception, e:
            print str(e)
            self.cur.close()
        return False

    def excute(self, sql):
        self.cur = self.con.cursor()
        try:
            self.cur.execute(sql)
            self.con.commit()
            self.cur.close()
            return True
        except Exception, e:
            print str(e)
            self.cur.close()
        return False

    # 关闭数据库连接
    def close(self):
        if self.cur is not None:
            self.cur.close()
        self.con.close()

if __name__ == "__main__":
    sql = "insert into test values(?,?)"

    db = SqlLiteHandle(r'C:\Users\29625\Desktop\tt.db')
    #db.insert(sql, [(1, "hx")])
    res = db.query("select * from tt_1")
    print res