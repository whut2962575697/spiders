# -*- encoding:utf-8 -*-

from com.xin.common.MysqlManage import MysqlHandle

import web
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class register(object):
    def GET(self):
        inputs = web.input()
        if inputs.has_key("token"):
            token = inputs["token"]
            if token == "whanys":
                if inputs.has_key("username") and inputs.has_key("password"):
                    username = inputs["username"]
                    password = inputs["password"]
                    sql = "select * from user_table_yixin where username='"+username+"'"
                    db = MysqlHandle()
                    res = db.query(sql)
                    if res:
                        result = {
                            "status": "1",
                            "msg": "failed,the username is already exist!"
                        }
                    else:
                        db = MysqlHandle()
                        sql = "insert into user_table_yixin values(%s,%s,now(),%s)"
                        res = db.insert(sql, [(username, password, 0)])
                        if res:
                            result = {
                                "status": "0",
                                "msg": "success"
                            }

                else:
                    result = {
                        "status": "1",
                        "msg": "failed,parameters not enough!"
                    }
            else:
                result = {
                    "status": "1",
                    "msg": "failed,your token is not true!"
                }
        else:
            result = {
                "status": "1",
                "msg": "failed,you need a token!"
            }
        return result


class login(object):
    def GET(self):
        inputs = web.input()
        if inputs.has_key("token"):
            token = inputs["token"]
            if token == "whanys":
                if inputs.has_key("username") and inputs.has_key("password"):
                    username = inputs["username"]
                    password = inputs["password"]
                    sql = "select * from user_table_yixin where username='"+username+"' and password='"+password+"' and status=0"
                    db = MysqlHandle()
                    res = db.query(sql)
                    if res:
                        result = {
                            "status": "0",
                            "msg": "success"
                        }
                    else:
                        result = {
                            "status": "1",
                            "msg": "failed!"
                        }
                else:
                    result = {
                        "status": "1",
                        "msg": "failed,parameters not enough!"
                    }
            else:
                result = {
                    "status": "1",
                    "msg": "failed,your token is not true!"
                }
        else:
            result = {
                "status": "1",
                "msg": "failed,you need a token!"
            }
        return result