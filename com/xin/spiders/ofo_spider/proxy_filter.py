# -*- coding:UTF-8 -*-



from com.xin.common.RequestManage import PageDownload
import json,time
from com.xin.common.tools import is_json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from com.xin.common.MysqlManage import MysqlHandle
from com.xin.common.ConfigManage import ofo_headers

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 测试url,用于过滤代理ip
TEST_URL = "http://san.ofo.so"
# 用于存放可用代理
AVALIABLE_IPS = []


# 过滤代理ip，先将TEMP_IPS_MANAGE表清空
def filter_avaliable_ips():
    db = MysqlHandle()
    is_success = db.delete('DELETE  FROM TEMP_IPS_MANAGE')
    if not is_success:
        db.close()
        return
    db.close()
    sql = 'SELECT PROXY FROM AI_PROXY_IPS'
    db = MysqlHandle()
    # 查询出所有代理ip
    IP_LIST = db.query(sql)
    db.close()
    for ip in IP_LIST:
        PROXY = {'http': 'http://'+ip[0]}  # 代理
        print 'filtering ip:'+ip[0]
        downloader = PageDownload(hd=ofo_headers,proxy=PROXY)
        try:
            post_data = MultipartEncoder(
    {
        "lat": "30.515133",
        "lng": "114.346161",
        "token": "7eb9b200-3d7f-11e8-b714-e9d19c19f7b0",
        "source": "-5",
        "source-version": "10005"
    },
		boundary='----ofo-boundary-MC40MjcxMzUw'
	)
            page = downloader.download_with_post(url=TEST_URL,post_data=post_data)
            if page is not None:
                AVALIABLE_IPS.append(ip)
                print ip[0]+" is ok!"
            else:
                pass
        except Exception, e:
            print str(e)
            pass
    db = MysqlHandle()
    db.insert('INSERT INTO TEMP_IPS_MANAGE VALUES (%s,now(),0,100)', AVALIABLE_IPS)
    db.close()
    district_table('TEMP_IPS_MANAGE')


#  去除重复代理ip
def district_table(table_name):
    query_sql = 'select distinct proxy  from '+table_name
    db = MysqlHandle()
    proxys = db.query(query_sql)
    db.close()
    delete_sql = 'delete from '+table_name
    db = MysqlHandle()
    db.delete(delete_sql)
    db.close()
    db = MysqlHandle()
    insert_sql = 'insert into '+table_name+' values (%s,now(),0,100)'
    is_success = db.insert(insert_sql, proxys)
    if is_success:
        print u'The filtering has finished!'
    db.close()

if __name__ == '__main__':
    filter_avaliable_ips()
