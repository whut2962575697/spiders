# -*- encoding:utf-8 -*-
from com.xin.common.MysqlManage import MysqlHandle
from com.xin.common.RequestManage import WebSelenium

from  Queue import Queue
import re
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def load_urls():
    db = MysqlHandle()
    sql = "select urlmd5,url from cphi_page_table where urlmd5 not in (select urlmd5 FROM cphi_info_table)"
    results = db.query(sql)
    queue = Queue()
    for item in results:
        _url = item[1].replace("/introduce/","/")
        #print _url
        queue.put_nowait((item[0],_url+"contactinfo/"))
    return queue

def get_info(urlmd5,url,driver):
    driver.get(url)
    page = driver.page_source.encode("utf-8")
    # print page
    contacts = re.findall(r"<strong>联系人</strong>：([^=]+)<a",page)
    if contacts:
        contacts = contacts[0]
    else:
        contacts = None
    e_mail = re.findall(r'<a href="mailto:([^"]+@[^"]+)"',page)
    if e_mail:
        e_mail = e_mail[0]
    else:
        e_mail = None
    phone_num = re.findall(r"<p><strong>电话</strong>： ([^/]+)</p>",page)
    if phone_num:
        phone_num = phone_num[0]
    else:
        phone_num = None
    #print phone_num
    db = MysqlHandle()
    sql = "insert into cphi_info_table values(%s,%s,%s,%s,%s)"
    print e_mail
    db.insert(sql,[(urlmd5,url,contacts,e_mail,phone_num)])
    db.close()



if __name__ == "__main__":
    queue = load_urls()
    webSelenium = WebSelenium()
    driver = webSelenium.simple_download("http://www.cphi.cn/member/login.php", browser="foxfire")
    time.sleep(30)
    while 1:
        if queue.empty():
            print "queue is empty"
            break
        else:
            urlmd5, url = queue.get_nowait()
            try:
                print url
                get_info(urlmd5, url, driver)
            except Exception,e:
                print e.message
                queue.put_nowait((urlmd5,url))




