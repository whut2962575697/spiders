# -*- coding:utf-8 -*-

import sys
import os,subprocess
import glob
import json
import hashlib
import redis
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr
from email.header import Header
from ConfigManage import config

# 重新设置编码
reload(sys)
sys.setdefaultencoding("utf-8")


# 判断字符串是否为json串的工具,如果是则返回转化后的结果
# 否则返回None
def is_json(in_str):
    try:
        out_json = json.loads(in_str)
        return out_json
    except Exception, e:
        print str(e)
        return None


# 字符串进行MD5加密工具，返回加密后的结果
def to_md5(in_str):
    m = hashlib.md5()
    m.update(in_str)
    out_st = m.hexdigest()
    return out_st


# 分割地理区间
def split_boundary(lat_max, lat_min, lng_max, lng_min, divide_num,random_rate=0.1):
    assert divide_num > 1, u"分割数必须大于1"
    assert lat_max > lat_min, u'分割区间必须大于0'
    assert lng_max > lng_min, u'分割区间必须大于0'
    delt_lat = (lat_max - lat_min) / divide_num
    delt_lng = (lng_max - lng_min) / divide_num
    generate_boundary = []
    for i in range(divide_num):
        for j in range(divide_num):
            lat_interval = (lat_min + i * delt_lat - random_rate * delt_lat, lat_min + (i+1) * delt_lat + random_rate * delt_lat)
            lng_interval = (lng_min + j * delt_lng - random_rate * delt_lng, lng_min + (j+1) * delt_lng + random_rate * delt_lng)
            generate_boundary.append([lat_interval, lng_interval])
    return generate_boundary


# 清除redis
def delete_redis(keyList):
    r = redis.Redis(host=config['redis']['host'], port=config['redis']['port'], db=config['redis']['db'])
    print r.keys()
    for item in keyList:
        r.delete(item)

def create_file(path,file_name,context=""):
    try:
        if os.path.exists(path) == False:
            os.mkdir(path)
        file = open(path + "/" + file_name, 'w')
        file.write(context)
        file.close()
        return True
    except Exception, e:
        print e.message
        return False

def you_get(url,output_path,file_name):
    shell_script = "you-get -o "+output_path+" -O "+file_name+" "+url
    try:
        handle = os.popen(shell_script)
        handle.read()
    except Exception,e:
        print e.message


def send_email_qq(from_address, to_address, password_key,subject, msg_str, attach_file):
    msg = MIMEMultipart(msg_str)
    msg["Subject"] = subject
    msg["From"] = from_address
    msg["To"] = to_address
    attach = MIMEApplication(open(attach_file, 'rb').read())
    attach["Content-Disposition"] = 'attachment; filename=' + attach_file.decode("utf-8").encode("gbk")
    msg.attach(attach)
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(from_address,password_key)
        s.sendmail(from_address,to_address,msg.as_string())
        s.quit()
        print (attach_file+" Success!")
        pass
    except Exception, e:
        print str(e)


if __name__ == "__main__":
    # mobi_files = glob.glob("C:/Users/29625/Desktop/*.mobi")
    # for file in mobi_files:
    #     send_email_qq("whut.hexin@foxmail.com", "whut.hexin@kindle.cn","fswrotwfpixlddha","test","success",file.decode("gbk"))
    # delete_redis(['hotqueue:cphi_url_table', 'zhihu:info:user', 'zhihu:seeds:all', 'zhihu:seeds:to_crawl', 'hotqueue:51ape_url_table'])
    # #print to_md5("https://www.sq688.com/")
    r = redis.Redis(host=config['redis']['host'], port=config['redis']['port'], db=config['redis']['db'])
    print r.keys()
    delete_redis(['hotqueue:bdmap_college_url_table'])
    #start_redis_server(path="F:\Redis-x64-3.2.100")
    #create_file(path="../spiders/carflac_spider",file_name="spider.py")
    #you_get(url="https://www.bilibili.com/bangumi/play/ep91588",output_path=r"C:\Users\29625\Desktop",file_name="1")