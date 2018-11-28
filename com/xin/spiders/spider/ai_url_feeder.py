# -*- coding:utf-8 -*-

from com.xin.common.MysqlManage import MysqlHandle
from com.xin.common.ConfigManage import config
from hotqueue import HotQueue
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class UrlFeeder(object):
    def __init__(self, source):
        self.url_table = source+"_url_table"
        redis_config = config["redis"]
        if redis_config.has_key("password"):
            self.queue = HotQueue(name=self.url_table, host=redis_config["host"],
                                  port=redis_config["port"],password=redis_config["password"], db=redis_config["db"])
        else:
            self.queue = HotQueue(name=self.url_table, host=redis_config["host"],
                              port=redis_config["port"], db=redis_config["db"])
        self.sql = "select urlmd5, url, type, boundary from " + self.url_table + " where status=0 limit 5000"
        self.update_sql_base = "update " + self.url_table + " set status=100 where urlmd5='%s'"
        self.run_sign = True
        self.start_feed()

    def set_stop(self):
        self.run_sign = False

    def start_feed(self):
        round_num = 0
        last_url_count = 0
        this_url_count = 0
        same_count = 0

        while self.run_sign:
            if len(self.queue) < 2500:
                start_time = time.time()
                round_index = round_num % 10
                db = MysqlHandle()
                url_list = db.query(self.sql)
                db.close()
                count = 0
                for url_data in url_list:
                    self.queue.put((url_data[0], url_data[1], url_data[2],url_data[3]))
                    update_sql = self.update_sql_base % url_data[0]
                    db = MysqlHandle()
                    db.update(update_sql)
                    db.close()
                    count += 1
                print 'FinishedQueue-' + self.url_table + ': %d TIME ELASPSED: %f ' % (count, time.time() - start_time)

                if round_index == 0:
                    if this_url_count == last_url_count:
                        same_count += 1
                    else:
                        last_url_count = this_url_count
                        same_count = 0
                    this_url_count = 0
                else:
                    this_url_count += 1
                round_num += 1
            else:
                print 'The Queue is full!'
            if same_count == 100:
                print 'THE SAME NUM %d appeared for 10 rounds, feeding frequency turn down.'
                time.sleep(360)
                self.set_stop()
            else:
                time.sleep(5)
        print 'Existed Successfully!!'


if __name__ == "__main__":
    url_feeder = UrlFeeder(source="bdmap_college")
    url_feeder.start_feed()

