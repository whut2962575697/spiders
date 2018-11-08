# -*- encoding:utf-8 -*-

import xlrd
from com.xin.common.RequestManage import WebSelenium
from com.xin.common.MysqlManage import MysqlHandle
import time
import arcpy


def download():
    db = MysqlHandle()
    sql = "select division, parent from divisions where parent='武汉市'"
    query_res = db.query(sql)
    webSelenium = WebSelenium()
    for (division, parent) in query_res:
        division = division.replace("+", "")
        division = division.replace("☆", "")
        search_word = parent+division
        if arcpy.Exists(r'G:\xin.src\c#\TrastationSystem\TrastationSystem\TrastationSystem\bin\divisions' + "\\" + search_word + ".shp"):
            continue
        print (division)
        try:
            webdriver = webSelenium.simple_download("http://127.0.0.1/common/get_bmap_boundary?city=" + search_word,
                                                    "chrome")

            # webdriver = webSelenium.login_with_cookies(login_url="http://pan.baidu.com/s/1c03zJGW", cookies_data=cookies, domain="pan.baidu.com")
            button_path = webdriver.find_elements_by_xpath("/html/body/input[2]")[0]

            button_path.click()

            time.sleep(5)
            button_path.click()
            button_download = webdriver.find_element_by_xpath("/html/body/input[3]")
            time.sleep(5)

            button_download.click()
            time.sleep(3)
            webdriver.close()
        except Exception, e:
            print (e.message)


if __name__ == "__main__":
    download()
