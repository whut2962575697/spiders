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
    # generate_sample("sample.xls")
    create_polyline("2|14492041.90,5692768.33;14709401.30,6010746.04|14707496.40,5960532.15,14513599.70,5693239.81,14687442.60,5721942.60,14660696.70,5760328.88,14666609.00,5977608.65,14666609.00,5977608.65,14655920.60,5977622.27,14498065.10,6006184.31,14492041.90,5918807.61,14702541.00,5761552.46,14674307.00,5977609.77,14662129.30,5692768.33,14550851.40,5975763.49,14504690.00,5950217.66,14530624.10,5769365.07,14530624.10,5769365.07,14701787.30,5931563.29,14652357.20,5999543.85,14682428.30,5769724.80,14652398.10,5966384.47,14532613.20,6010746.04,14686538.80,6006189.57,14655166.10,5999730.66,14674589.70,5981044.23,14674589.70,5981044.23,14686010.40,5921836.14,14539191.60,5783696.24,14663188.30,5961816.95,14703235.30,5961699.70,14703235.30,5961699.70,14647761.00,5743998.88,14647761.50,5771812.13,14660454.00,5968406.47,14688518.00,6007769.04,14512638.30,5991970.95,14512640.70,5733391.98,14649787.00,5932020.23,14649791.00,5999815.75,14647759.40,6010577.61,14647759.40,6010577.61,14546635.80,5989921.64,14546636.70,5722798.68,14551240.60,5734255.32,14511821.20,6008631.70,14707567.40,5987062.01,14702890.10,5783064.35,14518301.30,6009555.05,14518301.30,6009555.05,14660136.50,5723608.54,14688149.80,5695717.54,14701493.80,5957962.73,14544950.50,5762549.46,14654010.30,5969648.51,14707437.20,5762371.08,14524862.70,5702864.94,14695382.00,5742026.39,14709401.30,5780331.71,14526184.20,5733167.34,14701400.40,5919014.01,14688706.20,5980756.16,14693345.00,5760844.01,14550852.60,5733908.91,14504106.10,5959989.50,14662791.80,5948155.18,14674305.20,5929518.51,14702540.10,5778829.55,14498066.40,5693696.28,14519508.60,5957978.99,14544915.20,6006178.19,14544915.20,6006178.19,14544914.60,5928540.78,14649463.80,5917724.41,14680225.00,5704208.68,14532490.10,5760622.30,14656360.70,5703250.59,14695776.30,5946214.54,14493341.20,5936420.59,14689548.30,5926544.80,14527025.90,5978485.47,14527025.90,5978485.47,14526356.80,5750920.64,14669494.90,5969697.84,14521004.10,5928485.53,14547725.70,5780708.16,14668218.10,5750849.35,14675605.50,5759330.19,14675660.60,5969318.27,14707791.60,5948652.53,14707791.60,5948652.53;")
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


