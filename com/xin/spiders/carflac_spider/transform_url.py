# -*- ENCODING:UTF-8 -*-


from com.xin.common.RequestManage import PageDownload
from com.xin.common.MysqlManage import MysqlHandle

from Queue import Queue
import re,requests

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class TransformUrl():
    def __init__(self):
        self.queue = Queue()
        self.load_urls()

    def load_urls(self):
        sql = "select urlmd5,baiduyun_url from carflac_page_table"
        db = MysqlHandle()
        res = db.query(sql)
        for item in res:
            self.queue.put_nowait(item)

    def transform(self):
        urls = []
        while not self.queue.empty():
            (urlmd5,baiduyun_url) = self.queue.get_nowait()
            downloader = PageDownload(timeout=8)
            page = downloader.simple_download(baiduyun_url)
            if page is not None:
                _url = re.findall(r'<a href="..(/doaction.php\?enews=DownSoft&classid=\d+&id=\d+&pathid=\d+&'
                                  r'pass=\w+&p=:::)"',page)
                if _url is not []:
                    _url = "http://www.carflac.com/e/DownSys"+_url[0]

                    respond = requests.get(_url)
                    url = respond.url
                    print url
                    urls.append([urlmd5,baiduyun_url,url])
        print "url queue is empty,we will quit"
        return urls

    def insert_to_table(self):
        urls = self.transform()
        sql = "insert into carflac_transform_table values(%s,%s,%s)"
        db = MysqlHandle()
        db.insert(sql=sql,value_list=urls)
        db.close()


if __name__ == "__main__":
    transformer = TransformUrl()
    transformer.insert_to_table()






