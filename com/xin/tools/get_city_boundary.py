# -*- encoding:utf-8 -*-

from com.xin.common.RequestManage import WebSelenium
import time
import json


def get_boundary():
    with open(r"bd_city.json", "r") as f:
        json_data = json.load(f)
    webSelenium = WebSelenium()
    for city in json_data.keys():
        print (city)
        try:
            webdriver = webSelenium.simple_download("http://127.0.0.1/common/get_bmap_boundary?city=" + city,
                                                    "chrome")

            # webdriver = webSelenium.login_with_cookies(login_url="http://pan.baidu.com/s/1c03zJGW", cookies_data=cookies, domain="pan.baidu.com")
            button_path = webdriver.find_elements_by_xpath("/html/body/input[2]")[0]

            button_path.click()

            time.sleep(3)
            button_path.click()

            time.sleep(3)
            webdriver.close()
        except Exception, e:
            print (e.message)

if __name__ == "__main__":
    get_boundary()