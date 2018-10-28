# -*- encoding:utf-8 -*-

from com.xin.spiders.spider.init_spider import Initializer

initializer = Initializer(source="mobike",table_config="table_config.json",filter_config=None,test_url="http://mwx.mobike.com/mobike-api/rent/nearbyBikesInfo.do")