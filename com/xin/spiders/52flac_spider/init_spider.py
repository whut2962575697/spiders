# -*- encoding:utf-8 -*-

from com.xin.spiders.spider.init_spider import Initializer

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

initializer = Initializer(source="52flac", table_config="table_config.json",
                          filter_config="init_data.json", test_url="")

