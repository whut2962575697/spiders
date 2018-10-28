# -*- encoding:utf-8 -*-

import glob
import xlrd, xlwt


def filter_urls():
    with open("S201807041519234171500.txt","r") as f:
        lines = f.readlines()
    for line in lines:
        # line = line.strip("\n")
        if "/EVP/" in line:
            with open("download_urls.txt","a") as f:
                f.write(line)


def extract_excel(path):
    files = glob.glob(path+"/*.TXT")
    save_book = xlwt.Workbook()
    sheet1 = save_book.add_sheet(u"老河口")
    sheet2 = save_book.add_sheet(u"恩施")
    sheet3 = save_book.add_sheet(u"宜昌")
    sheet4 = save_book.add_sheet(u"武汉")
    # stations = {"57265":"老河口","57447":"恩施","57461":"宜昌","57494":"武汉"}
    x1 = 0
    x2 = 0
    x3 = 0
    x4 = 0
    for file in files:
        print file
        with open(file,"r") as f:
            lines  = f.readlines()
        for line in lines:
            line = line.strip("\n")
            line = line.replace("     "," ").replace("   ", " ").replace("  "," ")
            split_datas = line.split(" ")
            _station = split_datas[0]
            if _station == "57265":
                for y, data in enumerate(split_datas):
                    sheet1.write(x1, y, int(data))
                x1 = x1 + 1
            if _station == "57447":
                for y, data in enumerate(split_datas):
                    sheet2.write(x2, y, int(data))
                x2 = x2 + 1
            if _station == "57461":
                for y, data in enumerate(split_datas):
                    sheet3.write(x3, y, int(data))
                x3 = x3 + 1
            if _station == "57494":
                for y, data in enumerate(split_datas):
                    sheet4.write(x4, y, int(data))
                x4 = x4 + 1
    save_book.save("res.xls")






extract_excel(r"C:\Users\29625\Desktop\wh")



