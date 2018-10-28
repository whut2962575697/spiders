# -*- encoding:utf-8 -*-

import sys
import re
from Queue import Queue
reload(sys)
sys.setdefaultencoding("utf-8")

from mysql_manage import MysqlHandle
from request_manage import PageDownload, WebSelenium

class Spider(object):
    def __init__(self,init_url):
        self.init_url = init_url
        self.queue = Queue()

    def download_init_page(self):
        init_url_list = []
        downloader = WebSelenium()
        driver = downloader.simple_download(self.init_url)
        pds = driver.find_element_by_class_name("search_left_bg").find_element_by_class_name(
            "clearfixed").find_element_by_id("search_right_demo").find_elements_by_tag_name(
            "div")
        for pd in pds:
            pos = pd.find_elements_by_tag_name("p")
            for pi in pos:
                ps = pi.find_elements_by_tag_name("a")
                for p in ps:
                    url = p.get_attribute("href")
                    url = url.replace("jl=739","jl=489")
                    print url

                    #print url
                    self.queue.put_nowait(url)
        driver.close()

    def get_url_list(self):
        self.download_init_page()
        i = 0
        while not self.queue.empty():
            try:
                _url = self.queue.get_nowait()

                downloader = WebSelenium()
                driver = downloader.simple_download(_url)

                try:
                    pds = driver.find_element_by_xpath(
                    "//div[@class='newlist_sx']/div[@class='newlist_list1'][1]/div[@class='clearfix']/div[@id='search_jobtype_tag']").find_elements_by_tag_name(
                    "a")
                    big_cls = pds[1].text.split("(")[0]
                except :
                    try:
                        page = driver.page_source
                        res = re.findall(r'"Name":[^<]+",', page)[0]
                        big_cls = res.split("+")[1].strip("\",")
                    except:
                        big_cls = "未知"

                it_pds = driver.find_element_by_xpath(
                    "//div[@id='newlist_list_div']/div[@id='newlist_list_content_table']")
                table_pds = it_pds.find_elements_by_tag_name("table")

                for table in table_pds[1:]:
                    items = table.find_elements_by_class_name("zwmc")
                    for item in items:
                        url_list = item.find_elements_by_tag_name("a")
                        for url_item in url_list:
                            url = url_item.get_attribute("href")
                            if not re.match(r"http://jobs.zhaopin.com/[^<]+\.htm", url):
                                continue
                            [zwmc, gsmc, zwyx_min, zwyx_max, zzdd, fbrq, gzxz, zzjy, zdxl, zwlb, xxms, url,
                             big_cls] = self.get_page_info(
                                url, big_cls)
                            print url, url_item.text

                            value_list = [(i, zwmc, gsmc, zwyx_min, zwyx_max, zzdd, fbrq, gzxz, zzjy, zdxl, zwlb, xxms,
                                           url, big_cls)]
                            self.insert_to_db(value_list)
                            i = i + 1
                next_page_url = driver.find_element_by_xpath("//a[@class='next-page']").get_attribute("href")
                self.queue.put_nowait(next_page_url)
                driver.close()
            except Exception,e:
                print str(e)





    def get_page_info(self,url,big_cls):
        print url
        downloader = WebSelenium()
        driver = downloader.simple_download(url)
        try:
            zwmc = driver.find_element_by_xpath("//div[@class='fixed-inner-box']/div[@class='fl']/h1").text
            gsmc = driver.find_element_by_xpath("//div[@class='fixed-inner-box']/div[@class='fl']/h2/a").text
        except:
            zwmc = driver.find_element_by_xpath("//div[@class='fixed-inner-box']/div[@class='inner-left fl']/h1").text
            gsmc = driver.find_element_by_xpath("//div[@class='fixed-inner-box']/div[@class='inner-left fl']/h2/a").text

        zwyx = driver.find_element_by_xpath("//div[@class='terminalpage-left']/ul[@class='terminal-ul clearfix']/li[1]/strong").text

        zwyx = zwyx.strip("元/月 ")
        zwyx_min = zwyx.split("-")[0]
        zwyx_max = zwyx.split("-")[1]
        zzdd = driver.find_element_by_xpath("//div[@class='terminalpage-left']/ul[@class='terminal-ul clearfix']/li[2]/strong/a").text
        fbrq = driver.find_element_by_xpath("//ul[@class='terminal-ul clearfix']/li[3]/strong/span[@id='span4freshdate']").text
        gzxz = driver.find_element_by_xpath("//div[@class='terminalpage-left']/ul[@class='terminal-ul clearfix']/li[4]/strong").text
        zzjy = driver.find_element_by_xpath("//div[@class='terminalpage-left']/ul[@class='terminal-ul clearfix']/li[5]/strong").text
        zdxl = driver.find_element_by_xpath("//div[@class='terminalpage-left']/ul[@class='terminal-ul clearfix']/li[6]/strong").text
        #zprs = driver.find_element_by_xpath("//div[@class='terminalpage-left']/ul[@class='terminal-ul clearfix']/li[7]/strong").text
        zwlb = driver.find_element_by_xpath("//div[@class='terminalpage-left']/ul[@class='terminal-ul clearfix']/li[8]/strong/a").text
        xxms = driver.find_element_by_xpath("//div[@class='terminalpage-left']/div[@class='terminalpage-main clearfix']/div[@class='tab-cont-box']/div[@class='tab-inner-cont'][1]").text
        print zwmc,gsmc,zwyx_min,zwyx_max,zzdd,fbrq,gzxz,zzjy,zdxl,zwlb,xxms
        driver.close()
        #self.queue.put_nowait([zwmc,gsmc,zwyx_min,zwyx_max,zzdd,fbrq,gzxz,zzjy,zdxl,zwlb,xxms,url,big_cls])
        return [zwmc,gsmc,zwyx_min,zwyx_max,zzdd,fbrq,gzxz,zzjy,zdxl,zwlb,xxms,url,big_cls]

    def insert_to_db(self,info_list):
        db = MysqlHandle()
        sql = "insert into zhaopin_table values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        db.insert(sql,info_list)
        db.close()



if __name__ == "__main__":
    spider = Spider("http://sou.zhaopin.com/")
    #spider.ge_page_info("http://jobs.zhaopin.com/CZ657696680J00125275205.htm ")
    spider.get_url_list()



