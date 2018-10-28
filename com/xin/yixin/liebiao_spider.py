# -*- encoding:utf-8 -*-

from RequestManage import PageDownload
from sqllite_manange import SqlLiteHandle
import time
import json
import re
import argparse
import os
import sys

class LieBiaoSpider():
    def __init__(self,keyword, num):
        self.keyword = keyword
        self.base_url = "http://s.hc360.com/?w=%s&mc=enterprise&ee=%d"
        self.hc_contact_filter = r'<span class="conLeft">联系人：</span><span class="conRight"><samp>([^<]+)</samp>'
        self.hc_contact_filter_ = r'<span class="ContactLeft letter04">联系人</span><span>：<em>([^<]+)</em>'
        self.hc_phoneNum_filter = r'<span class="conLeft">手机：</span><span class="conRight">(\d+)</span>'
        self.hc_phoneNum_filter_ = r'<span class="ContactLeft letterLeft">手机</span><span>：(\d+)</span>'
        self.hc_company_name_filter = r"<li><span>公司名称：</span>([^<]+)</li>"
        self.hc_company_name_filter_ = r'var infoname="([^<+])";'
        # self.hc_address_filter = r"</h3><p>地址：([^<]+)</p><p>"
        self.num = num