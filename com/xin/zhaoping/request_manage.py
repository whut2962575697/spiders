# -*- encoding:utf-8 -*-


import requests
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/56.0.2924.87 Safari/537.36'
}

# 网页下载类，主要有简单下载、cookies下载、post登录等功能
class PageDownload(object):

    def __init__(self, proxy=None, timeout=3, hd=headers):
        self.proxy = proxy  # 代理，格式为 {'http': "120.89.173.13:80"}
        self.timeout = timeout  # 超时时间
        # 模拟浏览器头
        self.headers =hd

        # 简单下载，仅支持代理
    def simple_download(self, url):
        try:
            respond = requests.get(url=url, proxies=self.proxy, timeout=self.timeout, headers=self.headers)
            if respond.status_code == 200:
                content = respond.content

                coding = re.findall(r'charset="?([^=]+)"', content)
                if not coding:
                    coding = respond.encoding
                else:
                    coding = coding[0]
                if coding != "utf-8":
                    content = content.decode(coding).encode("utf-8")
                return content
            else:
                print u'网页返回为非200'
                return None
        except Exception, e:
            print str(e)
            return None

#自动化测试类，selenium自动测试，有三种浏览器可供选择
# 火狐：firefox，谷歌：chrome，phantomjs无界面浏览器：phantomjs
class WebSelenium(object):
    def __init__(self, firefox_path=r'geckodriver.exe', chrome_path=r'chromedriver.exe',
                 phantomjs_path=r'phantomjs.exe', proxy=None):
        self.firefox_path = firefox_path  # 火狐浏览器驱动的路径
        self.chrome_path = chrome_path  # 谷歌浏览器驱动的路径
        self.phantomjs_path = phantomjs_path  # phantomjs浏览器驱动的路径
        self.proxy = proxy  # 代理， 形式为{"http":"127.0.0.1:8080"}


    def simple_download(self, url, browser="phantomjs"):
        if browser == 'foxfire':  # 选择火狐浏览器
            profile = webdriver.FirefoxProfile()  # 火狐的配置文件类
            if self.proxy is not None:  # 判断是否使用代理，如果使用则获取ip和端口
                ip = self.proxy.split(':')[0]
                port = self.proxy.split(':')[1]
                profile.set_preference("network.proxy.type", 1)
                profile.set_preference("network.proxy.http", ip)  # 默认代理方式为http,可以修改
                profile.set_preference("network.proxy.http_port", port)
            driver = webdriver.Firefox(executable_path=self.firefox_path, firefox_profile=profile)

        elif browser == 'chrome':  # 选择谷歌浏览器
            options = webdriver.ChromeOptions()  # 谷歌浏览器的配置选项类
            if self.proxy is not None:  # 判断是否使用代理
                options.add_argument('--proxy-server=http://' + self.proxy)
            options.add_argument(
                    r'--user-data-dir=C:\Users\29625\AppData\Local\Google\Chrome\User Data')  # 设置成用户自己的数据目录

            driver = webdriver.Chrome(executable_path=self.chrome_path, chrome_options=options)

        elif browser == 'phantomjs':  # 选择phantomjs浏览器
            desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
            if self.proxy is not None:
                proxy = webdriver.Proxy()
                proxy.proxy_type = ProxyType.MANUAL
                proxy.http_proxy = self.proxy
                proxy.add_to_capabilities(desired_capabilities)
            #desired_capabilities["phantomjs.page.settings.loadImages"] = False  # 禁止加载图片，可以提高速度
            driver = webdriver.PhantomJS(executable_path=self.phantomjs_path, desired_capabilities=desired_capabilities)
        else:
            print u'浏览器类型不存在'
            return None
        driver.get(url)
        #time.sleep(3)
        #print driver.page_source

        # fs = driver.find_elements_by_xpath("//div[@class='search_left_bg']/div[@class='clearfixed']/div[@id='search_right_demo']/div[1]/p[1]/a']")
        # url = fs.get_attribute('href')
        # print url
        return driver