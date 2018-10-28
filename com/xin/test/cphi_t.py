# -*- encoding:utf-8 -*-

from com.xin.common.MysqlManage import MysqlHandle
from com.xin.common.RequestManage import WebSelenium,PageDownload
import time,re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")



cookies = {

"ip":"172.16.26.212",
"count":2,
"D36_company":'a%3A1%3A%7Bi%3A0%3Ba%3A4%3A%7Bs%3A2%3A%22id%22%3Bs%3A5%3A%2241643%22%3Bs%3A7%3A%22linkurl%22%3Bs%3A29%3A%22http%3A%2F%2Fwww.cphi.cn%2Fs-weirong%2F%22%3Bs%3A5%3A%22title%22%3Bs%3A30%3A%22%E8%A1%A2%E5%B7%9E%E4%BC%9F%E8%8D%A3%E8%8D%AF%E5%8C%96%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%3Bs%3A5%3A%22thumb%22%3Bs%3A45%3A%22CompanyLogo%2F2014_02%2FMimg_1402120313922182.jpg%22%3B%7D%7D',
"PHPSESSID":"2m5aqnd6etlulud3ub198cej10",
"D36_forward_url":"http://www.cphi.cn/s-weirong/contact/",
"D36_subauth":"ADY",
"D36_auth":"AjkHbFdmBjNbOVcNA3AFOwJzDzIBNFtUUmcDCVU7DDgHY1Y7BWFbPFI9AzVXawdkUD8CMAZoVTBRM1NoW2gFMwIyBzxXZwY1Wz1XMgM3BWECPA8/AWhbOFIwAzFVCgw8",
"D36_username":"whxin",
"D36_sadm":3,
"D36_adm":1,
"D36_uusername":"whxin",
"D36_maxscore":	4,
"D36_logintime":"1525865002",
"D36_2132_saltkey":"Y551xUBN",
"D36_2132_lastvisit":"1525859934",
"D36_2132_sid":"ZpoK9k",
"36_2132_lastact":"1525863534 uc.php",
"D36_2132_auth":"0c97TQub0VvdTXzKkkvT/0J2LhsVglRQACXJOQHgHLyTCWnYrKwgagSWyta087mXtjJNGOyfGAi4ookvTK0kWH/d9z4"
}
webSelenium = WebSelenium()
driver = webSelenium.simple_download("http://www.cphi.cn/s-weirong/contactinfo/",browser="foxfire")
# time.sleep(30)
# driver.get("http://www.cphi.cn/s-weirong/contactinfo/")
page =  driver.page_source.encode("utf-8")
print page
# db = MysqlHandle()
# sql = "insert into tpage values(%s,%s)"
# db.insert(sql,[('uiui',page)])
e_mail = re.findall(r'<a href="mailto:(\w+@\w+.\w+")',page)
print e_mail
contacts = re.findall(r"<strong>联系人</strong>：([^=]+)<a", page)
print contacts
phone_num = re.findall(r"<p><strong>电话</strong>： ([^/]+)</p>",page)
print phone_num
# downloader = PageDownload()
# page = downloader.simple_download("http://www.cphi.cn/s-labworld/introduce/")
# page = page.decode("utf-8")
# print page
#
#
# res = re.findall(r"""<meta name="keywords" content="([^=]+)"/>""",page)
# print res[-1]

#webdriver = webSelenium.login_with_cookies(login_url="http://www.cphi.cn/", cookies_data=cookies, domain="cphi.cn")
#page = downloader.simple_download("http://www.cphi.cn/s-weirong/contactinfo/")
#page = downloader.download_with_cookies(login_url="http://www.cphi.cn/s-weirong/contactinfo/")
#print "".encode("utf-8")
#webSelenium.simple_download(url="http://www.cphi.cn/s-weirong/contactinfo/",browser='chrome')
