# -*- encoding:utf-8 -*-

from com.xin.common.ConfigManage import baidupan_headers


import requests

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class BaiduPanTool(object):
    def __init__(self):
        self.cookie_file = "bp.cookies"
        self.session = requests.session()
        self.session.headers.update(baidupan_headers)

    def is_cookie(self,cookie):
        return 'BDUSS=' in cookie and 'PANPSC=' in cookie and len(cookie) > 150

    def parse_cookie(self,cookie):
        cookies = {}
        for item in cookie.split("; "):
            key,value = item.split("=")
            cookies[key] = value
        return cookies

    def login(self, user_name,password):
        if self.is_cookie(password):
            cookies = self.parse_cookie(password)
            self.session.cookies.update(cookies)


