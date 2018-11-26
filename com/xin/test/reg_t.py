# -*- encoding:utf-8 -*-

import re
import requests
import sys
import json
from  urllib import quote
import glob,xlrd,random,xlwt
import os
reload(sys)
from skimage.io import imread
from com.xin.spiders.carflac_spider.spider import DownloadTool
from com.xin.common.ConfigManage import normal_headers
from com.xin.common.RequestManage import PageDownload
from com.xin.common.MysqlManage import MysqlHandle
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

# with open(r'city_boundary.txt', 'r') as f:
#     lines = f.readlines()

# with open(r'final_bd_city.json', 'r')as f:
#     json_data = json.load(f)
#
#
# for k, v in json_data.items():
#     db = MysqlHandle()
#     sql = "INSERT INTO BD_CITY_INFO VALUES(%s, %s, %s, %s, 0)"
#     db.insert(sql,[[k, v["city_code"], v["jc"], v["coords"]]])
#     db.close()


# new_json = {}
# for line in lines:
#     line = line.strip("\n")
#
#     [city_name, coords] = line.split(" ")
#     for k, v in json_data.items():
#         city_code = v["city_code"]
#         jc = v["jc"]
#         if city_name == k:
#             new_json[city_name] = {"city_code": city_code, "jc": jc, "coords": coords}
#
#
# with open('final_bd_city.json', 'w') as f:
#     json.dump(new_json, f)


# db = MysqlHandle()
# query_sql = "select uid,min(name),min(line_type), min(page_url) from (select * from baidu_busline_url_analyse where uid in (select uid from baidu_busline_page where status is null)) as tg group by uid"
# page_infs = db.query(query_sql)
# db.close()
# downloader = PageDownload()
# for item in page_infs:
#     print (item[0])
#     page = downloader.simple_download(item[3])
#     # if is_json(page):
#     #     json_page = json.loads(page)
#     #     if json_page.has_key("content"):
#     #         main_info = json_page["content"][0]
#     #         name = main_info["name"]
#     #         timeable = main_info["timeable"]
#     db = MysqlHandle()
#
#     if page is not None:
#         insert_sql = "update baidu_busline_page set page="
#         is_success = db.insert(insert_sql, [(item[0], item[1], item[2], page)])

work_book = xlrd.open_workbook(r'C:\Users\29625\Desktop\FCNtrain.xls')
sheet = work_book.sheet_by_index(0)
save_book = xlwt.Workbook()
save_sheet = save_book.add_sheet("sheet")
with_list = []
other_list = []
for x in range(1, sheet.nrows, 3):
    file_name = sheet.cell(x, 4).value
    caption = sheet.cell(x, 1).value
    if " with " in caption:
        with_list.append(file_name)
    else:
        other_list.append(file_name)
random.shuffle(with_list)
random.shuffle(other_list)
train_with_list = with_list[:int(0.8 * len(with_list))]
val_with_list = with_list[int(0.6 * len(with_list)):]
train_other_list = other_list[:int(0.8 * len(other_list))]
val_other_list = other_list[:int(0.6 * len(other_list)):]
for i in range(1, sheet.nrows):
    id = sheet.cell(i, 0).value
    caption = sheet.cell(i, 1).value
    caption_id = sheet.cell(i, 2).value
    file_name_p = sheet.cell(i, 3).value
    file_name = sheet.cell(i, 4).value
    image_id = sheet.cell(i, 5).value
    img_id = sheet.cell(i, 6).value
    save_sheet.write(i, 0, id)
    save_sheet.write(i, 1, caption)
    save_sheet.write(i, 2, caption_id)
    save_sheet.write(i, 3, file_name_p)
    save_sheet.write(i, 4, file_name)
    save_sheet.write(i, 5, image_id)
    save_sheet.write(i, 6, img_id)

    if file_name in train_with_list or file_name in train_other_list:
        save_sheet.write(i, 7, 0)
    if file_name in val_with_list or file_name in val_other_list:
        save_sheet.write(i, 8, 0)
save_book.save("final.xls")




