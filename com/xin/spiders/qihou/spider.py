# -*- encoding:utf-8 -*-

from com.xin.common.RequestManage import PageDownload

import re
import xlwt

class Spider(object):
    def __init__(self, url):
        self.begin_url = url
        self.downloader = PageDownload()


    def get_type_url_list(self):
        page = self.downloader.simple_download(self.begin_url)
        _types = re.findall(r'<a href="top/(\w+).html"', page)
        _labels = re.findall(r' <td style="height: 22px" align="center"><a href="top/\w+.html" title="[^<]+历史天气查询">([^<]+)</a></td>',page)
        type_url_list = ["http://lishi.tianqi.com/"+_type+"/index.html" for _type in _types]
        results = {}
        for _label, url in zip(_labels, type_url_list):
            results[_label] = url
        return results

    def get_month_url(self, url):
        page = self.downloader.simple_download(url)
        mon_urls = re.findall(r'<li><a href="(http://lishi.tianqi.com/\w+/\d+.html)">',page)
        return mon_urls


    def get_day_info(self,url):
        page = self.downloader.simple_download(url)
        days = re.findall(r'(\d+\-\d+\-\d+)', page)
        tems = re.findall(r'<li>(\-?\d+)</li>', page)
        result = {}
        print len(days),len(tems)
        for i, day in enumerate(days):
            result[day] = {}
            result[day]["max"] = tems[2*i]
            result[day]["min"] = tems[2*i+1]
        return result

    def main(self):
        url_res = self.get_type_url_list()


        index = 0
        for k, v in url_res.items():
            if index < 65:
                index = index + 1
                continue
            work_book = xlwt.Workbook()
            sheet = work_book.add_sheet("sheet1")
            print v
            month_urls = self.get_month_url(v)
            i = 0
            for month_url in month_urls:
                print k,month_url
                _res = self.get_day_info(month_url)
                res = sorted(_res)
                sorted_dict = map(lambda x: {x: _res[x]}, res)
                for item in sorted_dict:
                    day = item.keys()[0]
                    info = item.values()[0]
                    max_t = info["max"]
                    min_t = info["min"]
                    sheet.write(i, 0, k)
                    sheet.write(i, 1, day)
                    sheet.write(i, 2, max_t)
                    sheet.write(i, 3, min_t)
                    i = i + 1
            index = index+1

            work_book.save(k+str(index)+".xls")




if __name__ == "__main__":
    spider = Spider("http://www.tianqihoubao.com/weather/province.aspx?id=420000")
    spider.main()








