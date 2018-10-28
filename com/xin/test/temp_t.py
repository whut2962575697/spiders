# -*- encoding:utf-8 -*-

import random
import numpy as np
import xlwt
import glob
import shutil
import xlrd
import com.xin.common.MysqlManage

def generate_sample(path):
    x = [_ for _ in range(504)]
    random.shuffle(x)
    train = x[:378]
    valid = x[378:504]
    test = x[504:]
    print len(train),len(valid),len(test)
    work_book = xlwt.Workbook()
    sheet = work_book.add_sheet("sheet0")
    for i in range(630):
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



# move_data(src_path=r"C:\Users\29625\Desktop\image_part_gt\image_part_gt",
#           des1=r"C:\Users\29625\Desktop\image_part_gt\mainroad",
#           des2=r"C:\Users\29625\Desktop\image_part_gt\not",excel_path=r"C:\Users\29625\Desktop\gt_eachpart0.5.xls")pa


if __name__ == "__main__":

    import random
    import xlwt

    sample_list = [_ for _ in range(504)]
    random.shuffle(sample_list)

    work = xlwt.Workbook()
    sheet = work.add_sheet("sheet1")
    train = sample_list[:int(0.6 * len(sample_list))]
    val = sample_list[int(0.6 * len(sample_list)):int(0.8 * len(sample_list))]
    test = sample_list[int(0.8 * len(sample_list)):]
    for x in range(504):
        if x in train:
            sheet.write(x,0,"train")
        elif x in val:
            sheet.write(x,0,"val")
        else:
            sheet.write(x,0,"test")
    work.save("yy.xls")
    # generate_sample("tt.xls")
    # x = 9.800543790665742216e-01
    #
    # print x
    #extract_data(r"C:\Users\29625\Desktop\zxx\2016Precipitation",r"C:\Users\29625\Desktop\zxx\results\2016Precipitation")
    # work_book = xlrd.open_workbook(r"C:\Users\29625\Desktop\FCN.xlsx")
    # save_book = xlwt.Workbook()
    # work_book1 = xlrd.open_workbook(r"C:\Users\29625\Desktop\result.xls")
    # sheet2 = work_book1.sheet_by_index(0)
    # sheet1 = save_book.add_sheet("sheet1")
    # sheet = work_book.sheet_by_index(0)
    # row_num = sheet2.nrows
    # x = 0
    #
    # for i in range(row_num):
    #     res_caption = sheet2.cell(i,1).value
    #     file_name = sheet2.cell(i,2).value.strip("]").split("/")[-1]
    #     for x in range(3):
    #         caption = sheet.cell(3*i+x,0).value
    #         file = sheet.cell(3*i+x,1).value
    #         sheet1.write(3*i+x,0,caption)
    #         sheet1.write(3 * i + x, 1, file)
    #         if x==0:
    #             sheet1.write(3 * i + x, 2, res_caption)
    #             sheet1.write(3 * i + x, 3, file_name)
    #     # if sheet.cell(i,7).value == "val":
    #     #     caption = sheet.cell(i,1).value
    #     #     file_name = sheet.cell(i,4).value
    #     #     sheet1.write(x,0,caption)
    #     #     print file_name
    #     #     sheet1.write(x,1,file_name)
    #     #     x = x+1
    # save_book.save(r"C:\Users\29625\Desktop\FCN_RES.xlsx")
