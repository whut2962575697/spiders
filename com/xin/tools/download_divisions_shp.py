# -*- encoding:utf-8 -*-

import xlrd
from com.xin.common.RequestManage import WebSelenium
import time


def download(excel_file):
    work_book = xlrd.open_workbook(excel_file)
    sheet = work_book.sheet_by_index(0)
    webSelenium = WebSelenium()
    for x in range(1, sheet.nrows):

        division = sheet.cell(x, 0).value
        print (division)
        webdriver = webSelenium.simple_download("http://127.0.0.1/common/get_bmap_boundary?city="+division, "chrome")

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


if __name__ == "__main__":
    download(u"行政区域列表.xls")
