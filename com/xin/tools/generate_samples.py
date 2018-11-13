# -*- encoding:utf-8 -*-

from com.xin.common.MysqlManage import MysqlHandle
from com.xin.common.RequestManage import PageDownload
from com.xin.common.tools import is_json
import xlwt, json


def generate_samples():
    base_url = "http://api.map.baidu.com/geoconv/v1/?coords=%s,%s&from=5&to=6&ak=XwpZGfXMn45W9Czd1UwmC6RwMMULD1Ue"
    work_book = xlwt.Workbook()
    sheet = work_book.add_sheet("sheet")
    sql = "select x , y from bdmap_api_school_218_page_table LIMIT 1000"
    db = MysqlHandle()
    query_res = db.query(sql)
    i = 0
    for (x, y) in query_res:
        url = base_url % (str(x), str(y))
        downloader = PageDownload()
        page = downloader.simple_download(url)
        if is_json(page):

            json_page = json.loads(page)
            status = json_page["status"]
            if status == 0:
                new_x = json_page["result"][0]["x"]
                new_y = json_page["result"][0]["y"]
                print (x, y, new_x, new_y)
                sheet.write(i, 0, x)
                sheet.write(i, 1, y)
                sheet.write(i, 2, new_x)
                sheet.write(i, 3, new_y)
                i = i+1

    work_book.save("sample.xls")


if __name__ == "__main__":
    generate_samples()








