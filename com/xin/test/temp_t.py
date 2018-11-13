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
    lines = geo_str.split("|")[2].strip(";")
    segments = lines.split(";")
    wkt = "MULTILINESTRING( "
    for segment in segments:
        wkt = wkt+"("
        segment = segment.split(",")
        for i in range(0, len(segment), 2):
            wkt = wkt+segment[i]+" "+segment[i+1]+","
        wkt = wkt.strip(",")+"),"
    wkt = wkt.strip(",")+")"
    polyline = arcpy.FromWKT(wkt)
    arcpy.CopyFeatures_management(polyline, "temp.shp")






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
    generate_sample("sample.xls")
    #create_polyline("2|12719995.79,3559398.70;12720591.53,3559571.20|12720572.97,3559446.14,12720585.21,3559447.43;12720397.94,3559427.72,12720463.26,3559434.60,12720572.97,3559446.14;12720310.22,3559419.71,12720383.37,3559426.18;12720585.21,3559447.43,12720591.53,3559448.10;12719995.79,3559571.20,12720012.02,3559467.19,12720022.96,3559398.70,12720056.37,3559399.67,12720180.23,3559409.36;12720180.23,3559409.36,12720310.22,3559419.71;12720383.37,3559426.18,12720397.94,3559427.72;")
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


