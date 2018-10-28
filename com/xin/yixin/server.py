# -*- encoding:utf-8 -*-

from MysqlManage import MysqlHandle

import web
import time
import hashlib
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
                    sql = "select * from yixin_user where username='"+username+"'"
                    db = MysqlHandle()
                    res = db.query(sql)
                    if res:
                        result = {
                            "status": "1",
                            "msg": "failed,the username is already exist!"
                        }
                    else:
                        m = hashlib.md5()
                        m.update(username+"anys"+str(time.time())+password)
                        out_st = m.hexdigest()
                        db = MysqlHandle()
                        sql = "insert into yixin_user (username,password,register_date,status,remain_days,recharge_car) VALUES(%s,%s,now(),1,0,%s)"
                        res = db.insert(sql, [(username, password, out_st)])
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
                    sql = "select * from yixin_user where username='"+username+"' and password='"+password+"' and status=0"
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


class charge(object):
    def GET(self):
        inputs = web.input()
        if inputs.has_key("token"):
            token = inputs["token"]
            if token == "whanys":
                if inputs.has_key("username") and inputs.has_key("password") and inputs.has_key("key"):
                    username = inputs["username"]
                    password = inputs["password"]
                    key = inputs["key"]
                    sql = "select recharge_car from yixin_user where username='"+username+"' and password='"+password+"'"
                    db = MysqlHandle()
                    user_res = db.query(sql)
                    db.close()
                    if user_res:
                        if user_res[0][0] == key:
                            m = hashlib.md5()
                            m.update(username + "anys" + str(time.time()) + password)
                            out_st = m.hexdigest()
                            sql = "update yixin_user set status=0 ,remain_days = remain_days+30 ,recharge_car='"+out_st+"'"+" where username='"+username+"' and password='"+password+"'"
                            db = MysqlHandle()
                            res = db.update(sql)
                            if res:
                                result = {
                                    "status": "0",
                                    "msg": "success"
                                }
                            else:
                                result = {
                                    "status": "1",
                                    "msg": "failed!unknown error!"
                                }
                        else:
                            result = {
                                "status": "1",
                                "msg": "failed!key error!"
                            }

                    else:
                        result = {
                            "status": "1",
                            "msg": "failed!information error!"
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



class generate(object):
    def GET(self):
        inputs = web.input()
        if inputs.has_key("token"):
            token = inputs["token"]
            if token == "whanys":
                if inputs.has_key("username") and inputs.has_key("password"):
                    username = inputs["username"]
                    password = inputs["password"]
                    sql = "select * from yixin_user where username='" + username + "'"
                    db = MysqlHandle()
                    res = db.query(sql)
                    if not  res:
                        result = {
                            "status": "1",
                            "msg": "failed,the username is not exist!"
                        }
                    else:
                        m = hashlib.md5()
                        m.update(username + "anys" + str(time.time()) + password)
                        out_st = m.hexdigest()
                        db = MysqlHandle()
                        sql = "update yixin_user set recharge_car='"+out_st+"'"+" ,status=0 ,remain_days=30 where username='" + username + "'"
                        res = db.update(sql)
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
