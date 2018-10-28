# -*- encoding:utf-8 -*-

from com.xin.common.MysqlManage import MysqlHandle

import web
import json



import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class search(object):
    def GET(self):
        inputs = web.input()
        if  inputs.has_key("token"):
            token = inputs.get("token")
            sql = "select * from token_table where token='"+token+"'"
            db = MysqlHandle()
            res = db.query(sql=sql)
            if not res:
                result = {
                    "status": "1",
                    "msg": "failed,your token is false!",

                }
            else:
                if inputs.has_key("name"):
                    music_name = inputs["name"]
                    db = MysqlHandle()
                    sql = "select file_name,singer,baiduyun_url,baiduyun_password from sq688_page_table where file_name " \
                          "like '%" + "%s" % (music_name) + "%'"
                    print sql
                    res = db.query(sql=sql)
                    db.close()
                    if not res:
                        sql = "select file_name,singer,baiduyun_url,baiduyun_password from 51ape_page_table where file_name " \
                              "like '%" + "%s" % (music_name) + "%'"
                        db = MysqlHandle()
                        res = db.query(sql=sql)
                        db.close()
                    items = []
                    for item in res:
                        file_name = item[0]
                        singer = item[1]
                        baiduyun_url = item[2]
                        baiduyun_password = item[3]
                        item_dic = {"music": file_name, "singer": singer, "url": baiduyun_url,
                                    "password": baiduyun_password}
                        items.append(item_dic)
                    result = {
                        "status": "1",
                        "msg": "success",
                        "results": items
                    }

                elif inputs.has_key("singer"):
                    singer = inputs["singer"]
                    db = MysqlHandle()
                    sql = "select file_name,singer,baiduyun_url,baiduyun_password from sq688_page_table where singer " \
                          "like '%s'" % (singer)
                    res = db.query(sql=sql)
                    db.close()
                    if not res:
                        sql = "select file_name,singer,baiduyun_url,baiduyun_password from 51ape_page_table where singer" \
                              "like '%s'" % (singer)
                        db = MysqlHandle()
                        res = db.query(sql=sql)
                        db.close()
                    items = []
                    for item in res:
                        file_name = item[0]
                        singer = item[1]
                        baiduyun_url = item[2]
                        baiduyun_password = item[3]
                        item_dic = {"music": file_name, "singer": singer, "url": baiduyun_url,
                                    "password": baiduyun_password}
                        items.append(item_dic)
                    result = {
                        "status": "0",
                        "msg": "success",
                        "results": items
                    }

                else:
                    result = {
                        "status": "1",
                        "msg": "failed,params is not enough!"}
        else:
            result = {
                "status": "1",
                "msg": "failed,you need a token!"
            }

        result = json.dumps(result)
        return result





