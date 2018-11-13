# -*- encoding:utf-8 -*-

from com.xin.common.RequestManage import WebSelenium
from com.xin.common.MysqlManage import MysqlHandle
import urllib


def download(division, d_type, abb_name=None):
    base_url = "http://xzqh.mca.gov.cn/defaultQuery?shengji=%s&diji=%s&xianji=%s"
    webSelenium = WebSelenium()
    if d_type == 1:
        url = base_url % (urllib.quote((division+"("+abb_name+")").encode("gb2312")), "-1", "-1")
        driver = webSelenium.simple_download(url, "chrome")
        print url
        rows = driver.find_elements_by_xpath("/html/body/div[@id='center']/div[@class='mid_con_qt']/table[@class='info_table']/tbody/tr[@class='shi_nub']")
        for row in rows:
            c_division = row.find_element_by_xpath("td[@class='name_left']/a[@class='name_text']").text
            population = row.find_element_by_xpath("td[3]").text
            area = row.find_element_by_xpath("td[4]").text
            code = row.find_element_by_xpath("td[5]").text
            zone = row.find_element_by_xpath("td[6]").text
            zip_code = row.find_element_by_xpath("td[7]").text
            if population == u'':
                population = None
            if area == u'':
                area = None
            if code == u'':
                code = None
            if zone == u'':
                zone = None
            if zip_code == u'':
                zip_code = None
            print (c_division, population, area, code, zone, zip_code)
            db = MysqlHandle()
            sql = "insert into divisions values(%s,%s,NULL ,%s,%s,%s,%s,%s,%s,0)"
            is_ok = db.insert(sql, [(c_division, code, 2, population, area, zone, zip_code, division)])
            db.close()
            if is_ok:
                db = MysqlHandle()
                sql = 'update divisions set status=200 where division="'+division+'" and type='+str(d_type)
                db.update(sql)

    elif d_type == 2:
        db = MysqlHandle()
        #sql = 'select parent from divisions where division="'+division+'"'
        sql = 'SELECT division, abb_name FROM divisions where division in (select parent from divisions where division="'+division+'")'
        res = db.query(sql)
        parent_division = res[0][0]+"("+res[0][1]+")"
        url = base_url % (urllib.quote(parent_division.encode("gb2312")), urllib.quote(division.encode("gb2312")), "-1")
        driver = webSelenium.simple_download(url, "chrome")
        print url
        rows = driver.find_elements_by_xpath("/html/body/div[@id='center']/div[@class='mid_con_qt']/table[@class='info_table']/tbody/tr")
        for row in rows[2:]:
            c_division = row.find_element_by_xpath("td[@class='name_left']").text
            population = row.find_element_by_xpath("td[3]").text
            if population == u'':
                population = None
            area = row.find_element_by_xpath("td[4]").text
            if area == u'':
                area = None
            code = row.find_element_by_xpath("td[5]").text
            if code == u'':
                code = None
            zone = row.find_element_by_xpath("td[6]").text
            if zone == u'':
                zone = None
            zip_code = row.find_element_by_xpath("td[7]").text
            if zip_code == u'':
                zip_code = None
            print (c_division, population, area, code, zone, zip_code)
            db = MysqlHandle()
            sql = "insert into divisions values(%s,%s,NULL ,%s,%s,%s,%s,%s,%s,0)"
            is_ok = db.insert(sql, [(c_division, code, 3, population, area, zone, zip_code, division)])
            if is_ok:
                db = MysqlHandle()
                sql = 'update divisions set status=200 where division="' + division + '" and type=' + str(d_type)
                db.update(sql)

    else:
        pass


def spider(d_type):
    db = MysqlHandle()
    sql = "select division, abb_name from divisions where status=0 and type ="+str(d_type)
    query_res = db.query(sql)
    for (division, abb_name) in query_res:
        print division
        try:
            download(division, d_type, abb_name)
        except Exception, e:
            print (e.message)


if __name__ == "__main__":
    spider(2)
