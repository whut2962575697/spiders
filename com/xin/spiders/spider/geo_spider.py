# -*- encoding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Spider(object):
    def __init__(self,  page_table, url_table=None):
        if url_table:
            self.url_table = url_table
        self.page_table = page_table

    def process(self, proxy):
        pass

