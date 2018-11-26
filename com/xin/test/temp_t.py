# -*- encoding:utf-8 -*-

import random
import numpy as np
import xlwt
import glob
import shutil
import xlrd
import com.xin.common.MysqlManage
import arcpy

def generate_sample(path):
    x = [_ for _ in range(1589)]
    random.shuffle(x)
    train = x[:953]
    valid = x[953:1270]
    test = x[1270:]
    print len(train),len(valid),len(test)
    work_book = xlwt.Workbook()
    sheet = work_book.add_sheet("sheet0")
    for i in range(1589):
        for x in train:
            if x == i:
                cell_value = "train"
                for j in range(3):
                    sheet.write(3*i+j,0,i)
                    sheet.write(3*i+j,1,cell_value)
        for y in valid:
            if y == i:
                cell_value = "valid"
                for j in range(3):
                    sheet.write(3*i+j,0,i)
                    sheet.write(3*i+j,1,cell_value)
        for z in test:
            if z == i:
                cell_value = "test"
                for j in range(3):
                    sheet.write(3*i+j,0,i)
                    sheet.write(3*i+j,1,cell_value)
    work_book.save(path)
def move_data(src_path,des1,des2,excel_path):
    work_book = xlrd.open_workbook(excel_path)
    sheet = work_book.sheet_by_index(0)
    row_num = 2076
    for i in range(1,row_num):
        generate_l = sheet.cell(i,2).value
        file_name = sheet.cell(i, 3).value
        file_name = file_name.replace("caption", "gt_")
        file_name = file_name.replace("jpg", "tif")
        if generate_l == "mainroad .":
            shutil.copy(src=src_path+"/"+file_name,dst=des1)
        else:
            shutil.copy(src=src_path + "/" + file_name, dst=des2)

#generate_sample("tt.xlsx")


def extract_data(txt_path,save_path):

    files = glob.glob(txt_path+"/*.TXT")
    for file in files:
        work_book = xlwt.Workbook()
        sheet = work_book.add_sheet("sheet1")
        file_name = file[file.rindex("\\")+1:]
        print file_name
        with open(file,"r") as f:
            lines = f.readlines()
        i = 0
        for line in lines:
            data = line.replace("   "," ").replace("     "," ").replace("  "," ").split(" ")
            if data[0] == "57483" or data[0] == "57482" or data[0] == "57583" or data[0] == "57494" or data[0]=="57395" or data[0] == "57493" or data[0]=="57595" or data[0]=="57399" or data[0] == "58407" or data[0]=="58500" or data[0]=="58402" :
                for x,d in enumerate(data[:11]):
                    sheet.write(i,x,d)
                i = i+1
        work_book.save(save_path+"/"+file_name.replace("TXT","xls"))


def transform_coord(in_xy,out_xy):
    pass


def create_polyline(geo_str):
    arcpy.env.workspace = r"G:\xin.data\test_data"
    points = geo_str.split("_")
    wkt = "POLYGON(( "
    for point in points:

        pos = point.split(",")

        wkt = wkt+pos[0]+" "+pos[1]+","
    wkt = wkt.strip(",")+"))"
    polygon = arcpy.FromWKT(wkt)
    arcpy.CopyFeatures_management(polygon, "temp.shp")






def htr(excel):
    workbook = xlrd.open_workbook(excel)
    sheet = workbook.sheet_by_index(0)
    savebook = xlwt.Workbook()
    savesheet = savebook.add_sheet("sheet1")
    i = 0
    for x in range(sheet.nrows):
        filename = sheet.cell(x, 0).value
        caption = sheet.cell(x, 1).value
        if caption != "":
            savesheet.write(i, 0, filename)
            savesheet.write(i, 1, caption)
            i = i+1
    savebook.save("area10.xls")



if __name__ == "__main__":
    # generate_sample("sample.xls")
    create_polyline("114.354735,30.522037_114.354986,30.522004_114.35542,30.521984_114.355419,30.521793_114.355424,30.521243_114.355978,30.521246_114.355962,30.520909_114.355929,30.520868_114.355925,30.520319_114.35705,30.520315_114.357061,30.519871_114.357043,30.519577_114.35696,30.519198_114.356667,30.518701_114.356595,30.518312_114.356458,30.51804_114.356365,30.517908_114.356065,30.517382_114.355915,30.517158_114.355902,30.516831_114.355883,30.516732_114.355885,30.515958_114.356011,30.51596_114.356032,30.515677_114.356049,30.515412_114.355949,30.515398_114.355912,30.515394_114.355879,30.515389_114.355844,30.515382_114.355825,30.515363_114.355809,30.515345_114.355775,30.515299_114.355714,30.5152_114.355687,30.515093_114.355665,30.514992_114.355668,30.514932_114.355678,30.514873_114.355705,30.514812_114.355746,30.514758_114.355818,30.514701_114.355862,30.514674_114.355883,30.514665_114.355896,30.514651_114.355902,30.514645_114.355905,30.514636_114.355903,30.514608_114.355901,30.514569_114.355897,30.51449_114.355872,30.514485_114.355849,30.514471_114.355835,30.51444_114.355823,30.514401_114.355796,30.51431_114.355756,30.514154_114.355629,30.513659_114.355373,30.513665_114.354213,30.513714_114.353695,30.513741_114.353409,30.513752_114.353338,30.513894_114.35328,30.514002_114.353202,30.514123_114.353056,30.514385_114.352774,30.514899_114.35281,30.515028_114.353329,30.514998_114.353331,30.515963_114.352772,30.515989_114.352774,30.516164_114.35244,30.516279_114.352244,30.516378_114.351926,30.516422_114.351275,30.516503_114.35077,30.516545_114.35087,30.517599_114.350948,30.518274_114.35099,30.518575_114.351058,30.518565_114.351931,30.518566_114.35281,30.518562_114.352839,30.51947_114.352211,30.519455_114.352151,30.519466_114.35211,30.519491_114.352091,30.519529_114.352087,30.519587_114.352085,30.519903_114.352036,30.519904_114.351173,30.519914_114.351178,30.519944_114.351252,30.520233_114.351341,30.520558_114.35138,30.520684_114.3515,30.520984_114.351635,30.521336_114.351702,30.521349_114.35182,30.521417_114.351887,30.521472_114.351951,30.521557_114.351975,30.521666_114.351976,30.52176_114.351955,30.521848_114.351934,30.521897_114.351905,30.521943_114.351869,30.521982_114.351958,30.522206_114.352054,30.522494_114.352689,30.522388_114.35274,30.522554_114.352777,30.522723_114.352788,30.52274_114.3528,30.522744_114.352813,30.52274_114.352921,30.522701_114.352975,30.522682_114.353002,30.522673_114.35303,30.522675_114.353049,30.522695_114.353082,30.522781_114.353227,30.523199_114.353243,30.523229_114.353265,30.523238_114.35331,30.523224_114.35339,30.523196_114.353576,30.523142_114.353784,30.523096_114.35401,30.523061_114.354043,30.523215_114.354091,30.523372_114.354188,30.523687_114.35466,30.523542_114.35453,30.523055_114.354372,30.52307_114.354369,30.52302_114.354358,30.522901_114.35464,30.522894_114.35465,30.522296_114.354409,30.522288_114.354417,30.522174_114.354552,30.522101_114.354735,30.522037")
    # htr(r"C:\Users\29625\Desktop\area10.xlsx")
    # import random
    # import xlwt
    #
    # sample_list = [_ for _ in range(1589)]
    # random.shuffle(sample_list)
    #
    # work = xlwt.Workbook()
    # sheet = work.add_sheet("sheet1")
    # train = sample_list[:int(0.6 * len(sample_list))]
    # val = sample_list[int(0.6 * len(sample_list)):int(0.8 * len(sample_list))]
    # test = sample_list[int(0.8 * len(sample_list)):]
    # for x in range(1589):
    #     if x in train:
    #         sheet.write(x,0,"train")
    #     elif x in val:
    #         sheet.write(x,0,"val")
    #     else:
    #         sheet.write(x,0,"test")
    # work.save("yy.xls")


