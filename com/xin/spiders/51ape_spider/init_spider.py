# -*- encoding:utf-8 -*-

from com.xin.spiders.spider.init_spider import Initializer

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

initializer = Initializer(source="51ape", table_config="table_config.json",test_url="http://www.51ape.com/",
                          filter_config="init_data.json")