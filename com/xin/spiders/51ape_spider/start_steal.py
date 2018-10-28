# -*- encoding:utf-8 -*-

from com.xin.spiders.spider.ai_url_consumer import UrlConsumer
from spider import Spider

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def main_run(thread_num, source):
    thread_pool = []
    for i in range(thread_num):
        url_consumer = UrlConsumer(50, 25, source)
        spider = Spider(source=source)
        url_consumer.set_spider(spider=spider)
        thread_pool.append(url_consumer)

    for thread in thread_pool:
        thread.start()


if __name__ == "__main__":
    main_run(10, "51ape")