# -*- encoding:utf-8 -*-

import re
import requests
import sys
from  urllib import quote
import glob
import os
reload(sys)
from com.xin.spiders.carflac_spider.spider import DownloadTool
from com.xin.common.ConfigManage import normal_headers
from com.xin.common.RequestManage import PageDownload
sys.setdefaultencoding("utf-8")

# # respond  = requests.get(url="http://www.cphi.cn/s-biochem/contactinfo/",timeout=3,headers=normal_headers)
# # if respond.encoding != "utf-8":
# #     respond.encoding = "utf-8"
# # page = respond.content
# #print respond.url
# #print text
# page = """
# <html><head></head><body>document.write('<div class="fn-left" style="width:358px;"><strong>联系人</strong>：吴建平<a href="mailto:qzwryh@qzweirong.com" class="z-tab-send fn-right z-tab-right " style="margin-right:40px;">邮件联系</a> <p><strong>电话</strong>： 86-0570-8761072</p> <p><strong>传真</strong>： 86-0570-8761071</p></div>')</body></html>
# """
# # downloder = DownloadTool("")
# # r = downloder.extract_field_from_page(page=text, reg=r"""<a href="#ecms" onclick="window.open\('([^<]+)','','width=300,height=300,resizable=yes'\)""")
# #
# # # r'<p class="downurl">链接: (https?://pan.baidu.com/s/[^=]+) 密码: (\w+)</p>'
# #
# # # r'<h2>([^=]+)     				<span class="cb">WAV</span>'
# # # r'<p><a href="/detail/\d+.html" style="color:#217fbc">([^=]+)</a></p>'
# # results1 = re.findall(r'<h1 class="title">([^<]+)</h1>', text)
# # results2 = re.findall(r'专辑艺人：([^<]+)', text)
# # results3 = re.findall(r'&nbsp;<a href="/\w+/">([^<]+)</a>', text)
# # res = re.findall(r"""<a href="#ecms" onclick="window.open\('([^<]+)','','width=300,height=300,resizable=yes'\)""",text)
# # results4 = re.findall(r'密码: (\w+)', text)
# e_mail = re.findall(r'<a href="mailto:(\w+@\w+.\w+")',page)
# print e_mail
# contacts = re.findall(r"<strong>联系人</strong>：([^=]+)<a", page)
# print contacts
# phone_num = re.findall(r"<p><strong>电话</strong>： ([^/]+)</p>",page)
# print phone_num
# print r

# from com.xin.common.RequestManage import PageDownload
# import json
# downloader = PageDownload(timeout=10)
# page = downloader.simple_download("http://china.coovee.net/SearchList/search.html?k=%E6%AD%A6%E6%B1%89%E5%B8%82%E5%B9%BF%E5%91%8A%E5%85%AC%E5%8F%B8_p=1")
# print page
# res = re.findall(r'<a href="([^<]+)">联系我们></a>',page)
# print res
# print page
# res = re.findall(r'" href="/jobs/searchresult.ashx?jl=739&bj=4010200" target="_blank">销售业务</a>',page)
# print res
# # json_data = json.loads(page)
# province = re.findall(r"province:'([^:]+)',",page)
# yys = re.findall(r"catName:'([^:]+)',",page)
# print province,yys
# contact = re.findall(r'href="(//www.11467.com/\w+/\w+/\d+.htm)"',page)
# #phone_num = re.findall(r'</b>(\d+-?\d+-?\d+-?\d+)</p><div class="p_5_0">',page)
# #手机：(\d+-?\d+-?\d+)
# print contact

# s = "郑州市广告公司黄页88网"
# print quote(s)
# s = "600-900元/月"
# s = s.strip("元/月")
# print s

# downloader = PageDownload(timeout=5)
# page = downloader.simple_download("http://detail.1688.com/offer/571218706862.html")
# print page
#
# res = re.findall(r'<dd class="mobile-number">                        (\d+)',page)
# print res
# with open("view-source_www.meituan.com_changecity_.html","r") as f:
#     page = f.read()
#     # print page
#
# meituan_ids = re.findall(r'\{"id":(\d+),"name":"[^,]+"',page)
# for item in  meituan_ids:
#     print item

files = glob.glob("D:/vd/*.MKV")
for file in files:
    os.rename(file,file.replace("MKV", "mkv"))
