# -*- encoding:utf-8 -*-

from selenium import webdriver
#import execjs
import sys, time
reload(sys)
sys.setdefaultencoding("utf-8")

def get_bd_boundary():
    driver = webdriver.PhantomJS(executable_path=r"F:\webdeiver\phantomjs.exe")
    driver.get("get_baidu_boundary.html")
    driver.find_element_by_id("districtName").send_keys(u"武汉市")
    driver.find_element_by_id("get_boundary").click()
















get_bd_boundary()