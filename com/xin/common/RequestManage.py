# -*- coding:utf-8 -*-

import sys
import requests
import re
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
from ConfigManage import normal_headers as headers
from ConfigManage import test_headers
import json
reload(sys)
sys.setdefaultencoding("utf-8")
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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
            respond = requests.get(url=url, proxies=self.proxy, timeout=self.timeout, headers=self.headers,verify=False)
            if respond.status_code == 200:
                content = respond.content

                coding = re.findall(r'charset="?([^<^"]+)"', content)
                if not coding:
                    coding = respond.encoding
                else:
                    coding = coding[0]
                if coding != "utf-8":
                    content = content.decode(coding,"ignore").encode("utf-8")
                return content
            else:
                print u'网页返回为非200'
                return None
        except Exception, e:
            print str(e)
            return None

        # cookies下载，可以使用cookies免登录下载，可跳过验证码
    def download_with_cookies(self, login_url, cookies, download_url=None):
        try:
            session = requests.session()
            requests.utils.add_dict_to_cookiejar(session.cookies, cookies)
            respond = session.get(login_url, headers=self.headers, proxies=self.proxy)
            if download_url is not None:
                respond = session.get(download_url, headers=self.headers)
            if respond.status_code == 200:
                content = respond.content
            else:
                print u'request return status is not 200'
                content = None
            return content
        except Exception, e:
            print str(e)
            return None

        # post 登录，利用post数据模拟登录，适用于无验证码的登录，dic_data为post数据（字典）
    def login_with_post(self, dic_data, login_url, download_url):
        try:
            session = requests.Session()
            session.post(login_url, dic_data, headers=self.headers, proxies=self.proxy)
            respond = session.get(download_url)
            if respond.status_code == 200:
                content = respond.content
            else:
                print u'网页返回为非200'
                content = None
            return content
        except Exception, e:
            print str(e)
            return None
    def download_with_post(self, url, post_data):
        try:
            respond = requests.post(url=url, data=post_data, headers=self.headers, proxies=self.proxy,
                                    timeout=self.timeout,verify=False)
            if respond.status_code == 200:
                content = respond.content
                return content
            else:
                print u'网页返回为非200'
                return None
        except Exception, e:
            print str(e)
            return None

# 自动化测试类，selenium自动测试，有三种浏览器可供选择
# 火狐：firefox，谷歌：chrome，phantomjs无界面浏览器：phantomjs
class WebSelenium(object):
    def __init__(self, firefox_path=r'H:\webdeiver\geckodriver.exe', chrome_path=r'H:\webdeiver\chromedriver.exe',
                 phantomjs_path=r'H:\webdeiver\phantomjs.exe', proxy=None):
        self.firefox_path = firefox_path  # 火狐浏览器驱动的路径
        self.chrome_path = chrome_path  # 谷歌浏览器驱动的路径
        self.phantomjs_path = phantomjs_path  # phantomjs浏览器驱动的路径
        self.proxy = proxy  # 代理， 形式为{"http":"127.0.0.1:8080"}

    # 利用cookies实现自动登录，返回一个driver对象，可用于后续自动化
    # login_url：登录url，cookies_data：cookies，domain：网站的ip或域名，browser：浏览器类型。默认使用火狐
    def login_with_cookies(self, login_url, cookies_data, domain, browser='foxfire'):
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
            driver = webdriver.Chrome(executable_path=self.chrome_path, chrome_options=options)

        elif browser == 'phantomjs':  # 选择phantomjs浏览器
            desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
            if self.proxy is not None:
                proxy = webdriver.Proxy()
                proxy.proxy_type = ProxyType.MANUAL
                proxy.http_proxy = self.proxy
                proxy.add_to_capabilities(desired_capabilities)
            desired_capabilities["phantomjs.page.settings.loadImages"] = False  # 禁止加载图片，可以提高速度
            driver = webdriver.PhantomJS(executable_path=self.phantomjs_path, desired_capabilities=desired_capabilities)
        else:
            print u'浏览器类型不存在'
            return None
        driver.get(login_url)
        # 添加cookies
        driver.delete_all_cookies()
        for cookie in cookies_data.items():
            driver.add_cookie(
                {
                    'domain': domain,
                    'name': cookie[0],
                    'value': cookie[1],
                    'path': '/',
                    'expires': None
                }
            )
        return driver

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
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            # options.add_argument('--no-sandbox')
            if self.proxy is not None:  # 判断是否使用代理
                options.add_argument('--proxy-server=http://' + self.proxy)
            # options.add_argument(
            #         r'--user-data-dir=C:\Users\29625\AppData\Local\Google\Chrome\User Data')  # 设置成用户自己的数据目录

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

    def execute_script(self,url,):
        pass

if __name__ == "__main__":





    # cookies = {
    #    "BAIDUID": "B96C3563BF2F637009C796EFF6D94005:FG=1",
    #     "BDCLND": "m3xY8Eey0Ur5JVphY2MIXuEkrhxoyUdwK47e4kEfyG8%3D",
    #     "PANWEB": "1",
    #     "PSTM": "1519887999",
    #     "BIDUPSID": "533998306EEF53E168DFC1ADCDA388F0",
    #     "BDORZ": "B490B5EBF6F3CD402E515D22BCDA1598",
    #     "FP_UID": "62fd21bd43f08802852d866e44742006",
    #     "BDUSS": "RTNWVXSUw2ZTR-UFNtblFRSFNyTUw1MlBrMWtnbFVjfnpYdkVubjhnMHJPNzlhQVFBQUFBJCQAAAAAAAAAAAEAAAAnOs1o3ebJ2dD"
    #              "-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACuul1orrpdadz",
    #     "STOKEN": "8c872607a199b8941d236804d9cb7d4ae7803424eaa89ac7c75322a09752cfb0",
    #     "SCRC": "1de98da849a9525122422a179b4b892c",
    #     "Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0": "1519886364,1519890336",
    #     "Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0": "1519890336",
    #     "PANPSC": "3916381627938070527%3AW5fKWWSguZBODGOBl4FW9LHQG6qeixv0W3gk0j36GcGYvOBUKVBcBn5k87Cjw7JD36RmMWyu83GNTP"
    #               "It1rTOiaS63VeBUP8%2FIjNe%2FZa%2FcMRcqAh9P390KK1Sr93PEHDi%2B%2Bo8ht7g5D2LIWeznIUCtSkA0KYPulwlfkiV"
    #               "l%2Ff%2FRfx4kU4b9dv9by76Oxw8WnAw"
    #
    # }

    #downloader = PageDownload(proxy={"http": "http://202.100.83.139:80"})
    # page = downloader.simple_download(url="http://www.52flac.com/download/9108.html")
    # #page = downloader.download_with_cookies(login_url="http://www.52flac.com/download/9222.html", cookies=cookies)
    # print page
    webSelenium = WebSelenium()
    webdriver = webSelenium.simple_download("http://127.0.0.1/common/get_bmap_boundary?city=黄梅县", "chrome")

    # webdriver = webSelenium.login_with_cookies(login_url="http://pan.baidu.com/s/1c03zJGW", cookies_data=cookies, domain="pan.baidu.com")
    button_path = webdriver.find_elements_by_xpath("/html/body/input[2]")[0]
    button_path.click()
    time.sleep(5)
    button_path.click()
    button_download = webdriver.find_element_by_xpath("/html/body/input[3]")
    time.sleep(5)
    button_download.click()


    # textbox.send_keys("m43t")
    # button = webdriver.find_elements_by_xpath("//a[@class='g-button g-button-blue-large']")[0]
    # button.click()
    # WebDriverWait(webdriver, 30).until(lambda the_driver: the_driver.find_element_by_xpath(
    #         "//a[@class='g-button g-button-blue']").is_displayed())
    # save_button = webdriver.find_elements_by_xpath("//a[@class='g-button g-button-blue']")[0]
    # save_button.click()

    #webSelenium.simple_download(url="http://sou.zhaopin.com/")

    # dic_data = {}
    # dic_data["userName"] = "0121408900211"
    # dic_data["password"] = "257313"
    # dic_data["type"] = "xs"
    # dic_data["imageField.x"] = 46
    # dic_data["imageField.y"] = 17
    # dic_data["systemId"] = ""
    # dic_data["xmlmsg"] = ""
    # downloader = PageDownload()
    # page = downloader.login_with_post(dic_data=dic_data, login_url="http://sso.jwc.whut.edu.cn/Certification//login.do",
    #                                   download_url="http://sso.jwc.whut.edu.cn/Certification//toIndex.do")
    # if page:
    #     print page.decode("utf-8")
    # dic_data = {}
    # dic_data['__VIEWSTATE'] = '/wEPDwULLTIxMTE3OTcxMDcPZBYCZg9kFgICAw9kFgQCAw9kFgICBQ8WAh4LXyFJdGVtQ291bnQCBRYKAgEPZBYCZg8VAwIzNlrlhbPkuo4yMDE3LTIwMTjlrablubTnrKzkuIDlrabmnJ/jgIrkuK3lm73or63mlofjgIvlnKjnur/ogIPor5Xnu5/liIbmiKrmraLml7bpl7TnmoTpgJrnn6USMjAxNy82LzE1IDE2OjIwOjAxZAICD2QWAmYPFQMCMzVp5YWz5LqOMjAxNi0yMDE35a2m5bm056ys5LqM5a2m5pyf44CK5Lit5Zu96K+t5paH44CL5Zyo57q/6ICD6K+V77yI5q+V5Lia55Sf77yJ57uf5YiG5oiq5q2i5pe26Ze055qE6YCa55+lETIwMTcvMy83IDEwOjI5OjQwZAIDD2QWAmYPFQMCMzRa5YWz5LqOMjAxNi0yMDE35a2m5bm056ys5LqM5a2m5pyf44CK5Lit5Zu96K+t5paH44CL5Zyo57q/6ICD6K+V57uf5YiG5oiq5q2i5pe26Ze055qE6YCa55+lEjIwMTcvMS8xNiAxMTo0Mjo1MWQCBA9kFgJmDxUDAjMzWuWFs+S6jjIwMTYtMjAxN+WtpuW5tOesrOS4gOWtpuacn+OAiuS4reWbveivreaWh+OAi+WcqOe6v+iAg+ivlee7n+WIhuaIquatouaXtumXtOeahOmAmuefpRIyMDE2LzEwLzI1IDk6MzY6MzdkAgUPZBYCZg8VAwIzMVrlhbPkuo4yMDE1LTIwMTblrablubTnrKzkuozlrabmnJ/jgIrkuK3lm73or63mlofjgIvlnKjnur/ogIPor5Xnu5/liIbmiKrmraLml7bpl7TnmoTpgJrnn6URMjAxNi8zLzI4IDk6MzE6MDNkAgQPDxYCHgRUZXh0BQc5OTU3OTUwZGRkVqWs0bBhVS3ACXN/g8tGOehw1bw='
    # dic_data['ctl00$ContentPlaceHolder1$name'] = '0121408900211'
    # dic_data['ctl00$ContentPlaceHolder1$pwd'] = '0121408900211'
    # dic_data['ctl00$ContentPlaceHolder1$login'] = '登录'
    # downloader = PageDownload()
    # page = downloader.login_with_post(dic_data=dic_data,login_url='http://59.69.102.9/zgyw/index.aspx', download_url='http://59.69.102.9/zgyw/study/LearningIndex.aspx')
    # print page
    # cookies = {'ASP.NET_SessionId': 'gy2wpr45qghwjl45pi2mtdu5'}
    # downloader = PageDownload()
    # page = downloader.download_with_cookies(login_url='http://59.69.102.9/zgyw/index.aspx', download_url='http://59.69.102.9/zgyw/study/LearningIndex.aspx', cookies=cookies)
    # print page
    # webSelenium = WebSelenium()
    # cookies = {'ASP.NET_SessionId': 'uwlprc55uu3ebm455epy3hzh'}
    # driver = webSelenium.login_with_cookies(login_url='http://59.69.102.9/zgyw/index.aspx', cookies_data=cookies, domain='59.69.102.9', browser='foxfire')
    # driver.get('http://59.69.102.9/zgyw/study/LearningIndex.aspx')
    # fs = driver.find_element_by_class_name("search_left_bg")
    # pos = fs.find_element_by_class_name("clearfixed").find_element_by_id("search_right_demo").find_element_by_tag_name(
    #     "div").find_elements_by_tag_name("a")
    # for pi in pos:
    #     print pi.get_attribute("href")
    # downloader = WebSelenium()
    # driver = downloader.simple_download("http://sou.zhaopin.com/jobs/searchresult.ashx?jl=489&bj=4010200")
    # page = driver.page_source
    # print page
    # res = re.findall(r'"Name":[^<]+",', page)[0]
    # big_cls = res.split("+")[1].strip("\",")
    # print big_cls
    # pds = driver.find_element_by_class_name("search_left_bg").find_element_by_class_name(
    #     "clearfixed").find_element_by_id("search_right_demo").find_elements_by_tag_name(
    #     "div")
    #pds = driver.find_element_by_xpath("//div[@class='newlist_sx']/div[@class='newlist_list1'][1]/div[@class='clearfix']/div[@id='search_jobtype_tag']").find_elements_by_tag_name("a")
    # for pd in pds[2:]:
    #     print pd.text
        # pos = pd.find_elements_by_tag_name("p")
        # for pi in pos:
        #     ps =  pi.find_elements_by_tag_name("a")
        #     for p in ps:
        #         print p.get_attribute("href")
    # it_pds = driver.find_element_by_xpath("//div[@id='newlist_list_div']/div[@id='newlist_list_content_table']")
    # table_pds = it_pds.find_elements_by_tag_name("table")
    # # for table in table_pds[1:]:
    # #     items = table.find_elements_by_class_name("zwmc")
    # #     for item in items:
    # #         url_list = item.find_elements_by_tag_name("a")
    # #         for url_item in url_list:
    # #             url = url_item.get_attribute("href")
    # #             if not re.match(r"http://jobs.zhaopin.com/[^<]+\.htm",url):
    # #                 continue
    # #
    # #             print url,url_item.text
    # next_page_url = driver.find_element_by_xpath("//a[@class='next-page']").get_attribute("href")
    # print next_page_url