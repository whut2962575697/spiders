# -*- encoding:utf-8 -*-

import csv
import xlrd
import xlwt,arcpy
from libtiff import TIFF
import glob,numpy as np
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def extract_data(path,sid_file,save_path):
    work_book = xlrd.open_workbook(sid_file)
    sheet = work_book.sheet_by_index(0)
    n_rows = sheet.nrows
    sids = []
    for i in range(1,n_rows):
        sid = sheet.cell(i,0).value
        sids.append(sid)
    csv_files = glob.glob(path+"/*.csv")
    results = []
    for file in csv_files:
        print file.split("_")[-1]
        with open(file,"r") as f:
            reader = csv.reader(f)
            reader = list(reader)
            rows_num = len(reader)
            sid_index = []
            for x,item in enumerate(reader[0]):
                for sid in sids:
                    if item == sid:
                        sid_index.append(x)
            for j in range(1,rows_num):
                row = reader[j]
                if row[2] == "PM2.5":
                    result = []
                    result.append(row[0])
                    result.append(row[1])
                    result.append(row[2])
                    for k in sid_index:
                        result.append(row[k])
                    results.append(result)
    work_book_save = xlwt.Workbook()
    sheet = work_book_save.add_sheet("sheet1")
    sheet.write(0, 0, label="date")
    sheet.write(0, 1, label="hour")
    sheet.write(0, 2, label="type")
    for i,sid in enumerate(sids):
        sheet.write(0, 3+i, label=sid)
    for x,result in enumerate(results):
        for y,item in enumerate(result):
            sheet.write(1+x, y, label=item)
    work_book_save.save(save_path)

def extract_data_city(path,save_path):
    csv_files = glob.glob(path + "/*.csv")
    results = []
    headers = []
    for file in csv_files:
        print file
        with open(file,"r") as f:
            reader = csv.reader(f)
            reader = list(reader)
            rows_num = len(reader)
            headers = reader[0]
            for j in range(1,rows_num):
                row = reader[j]
                if row[2] == "AQI":
                    results.append(row)
    with open(save_path,'wb') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for res in results:
            writer.writerow(res)
    # work_book_save = xlwt.Workbook()
    # sheet = work_book_save.add_sheet("sheet1")
    # for x,header in enumerate(headers):
    #     sheet.write(0,x,label=header)
    #
    # for i,res in enumerate(results):
    #     for j,cell in enumerate(res):
    #         sheet.write(i+1,j,label=cell)
    # work_book_save.save(save_path)
def get_begin(img,rgb_value,res):
    for i ,row in enumerate(img):
        for j ,cell in enumerate(row):
            if tuple(cell) == rgb_value:
                res.append([i,j])
                return [i,j]
    return [0,0]
def to_shp(img,rgb_value):
    res = []

    begin_cell = get_begin(img,rgb_value,res)

    end_cell = begin_cell
    while begin_cell != end_cell or len(res)==1:
        print end_cell
        (row_index,column_index) = end_cell
        count = 0
        satisfy_cells = []
        if column_index==0:
            if [row_index,column_index+1] not in res and  tuple(img[row_index][column_index+1]) == rgb_value:
                #res.append([row_index,column_index+1])
                #end_cell = [row_index,column_index+1]
                satisfy_cells.append([row_index,column_index+1])
                count = count+1
        elif column_index==199:
            if [row_index,column_index-1] not in res and tuple(img[row_index][column_index-1]) == rgb_value:
                satisfy_cells.append([row_index,column_index-1])
                #end_cell = [row_index,column_index-1]
                count = count+1
        else:
            if [row_index,column_index+1] not in res and tuple(img[row_index][column_index+1]) == rgb_value:
                satisfy_cells.append([row_index,column_index+1])
                # end_cell = [row_index,column_index+1]
                count = count+1
            if [row_index,column_index-1] not in res and tuple(img[row_index][column_index-1]) == rgb_value:
                satisfy_cells.append([row_index,column_index-1])
                # end_cell = [row_index,column_index-1]
                count = count+1
        if row_index==0:
            if [row_index-1,column_index] not in res and tuple(img[row_index+1][column_index]) == rgb_value:
                satisfy_cells.append([row_index+1,column_index])
                # end_cell = [row_index+1,column_index]
                count = count+1
        elif row_index==199:
            if [row_index-1,column_index] not in res and tuple(img[row_index-1][column_index]) == rgb_value:
                satisfy_cells.append([row_index-1,column_index])
                # end_cell = [row_index-1,column_index]
                count = count+1
        else:
            if [row_index+1,column_index] not in res and tuple(img[row_index+1][column_index]) == rgb_value:
                satisfy_cells.append([row_index+1,column_index])
                # end_cell = [row_index+1,column_index]
                count = count+1
            if [row_index-1,column_index] not in res and tuple(img[row_index-1][column_index]) == rgb_value:
                satisfy_cells.append([row_index-1,column_index])
                # end_cell = [row_index-1,column_index]
                count = count+1
        if count == 1:
            res.append(satisfy_cells[0])
            end_cell = satisfy_cells[0]
        elif count == 2:
            x= 9
            for cell in satisfy_cells:
                column_index = cell[1]
                row_index = cell[0]
                r_count = 0
                if column_index == 0:
                    if [row_index, column_index + 1] not in res and tuple(
                            img[row_index][column_index + 1]) == rgb_value:

                        r_count = r_count + 1
                elif column_index == 199:
                    if [row_index, column_index - 1] not in res and tuple(
                            img[row_index][column_index - 1]) == rgb_value:
                        r_count = r_count + 1
                else:
                    if [row_index, column_index + 1] not in res and tuple(
                            img[row_index][column_index + 1]) == rgb_value:
                        r_count = r_count + 1
                    if [row_index, column_index - 1] not in res and tuple(
                            img[row_index][column_index - 1]) == rgb_value:
                        r_count = r_count + 1
                if row_index == 0:
                    if [row_index - 1, column_index] not in res and tuple(
                            img[row_index + 1][column_index]) == rgb_value:
                        r_count = r_count + 1
                elif row_index == 199:
                    if [row_index - 1, column_index] not in res and tuple(
                            img[row_index - 1][column_index]) == rgb_value:
                        r_count = r_count + 1
                else:
                    if [row_index + 1, column_index] not in res and tuple(
                            img[row_index + 1][column_index]) == rgb_value:
                        r_count = r_count + 1
                    if [row_index - 1, column_index] not in res and tuple(
                            img[row_index - 1][column_index]) == rgb_value:
                        r_count = r_count + 1
                if r_count == 1:
                    res.append(cell)
                    end_cell = cell
                    break
        elif count == 0:
            break


    return res




if __name__ == "__main__":
    #extract_data(path=r"C:\Users\29625\Desktop\zxx\sites",sid_file=r"C:\Users\29625\Desktop\zxx\sids.xls", save_path="results.xls")
    #extract_data_city(path=r'G:\Data\city_20170101-20171231',save_path="res.csv")
    # dd = np.array([[1,2,3],[4,5,6],[7,8,9]])
    # x = dd[1:3,0:1]
    # img = TIFF.open(r"G:\xin.src\python\py3\com\xin\deeplearning\lstm\boundary.tif")
    # img = img.read_image()
    # res = to_shp(img,(128,0,0))
    # arcpy.env.workspace = r'G:\gisdata'
    # wkt = "POLYGON("
    # polygon = "("
    # for point in res:
    #     polygon = polygon+str(point[0])+" "+str(point[1])+","
    # polygon = polygon.strip(",") + ")"
    # wkt = wkt+polygon+")"
    # polygons = arcpy.FromWKT(wkt)
    # arcpy.CopyFeatures_management(polygons, 'raster_convert.shp')
    work_book = xlrd.open_workbook(r"points_res.xls")
    p_w_b = xlrd.open_workbook(r'C:\Users\29625\Desktop\isd-history.xls')
    sheet = work_book.sheet_by_index(0)
    p_w_b_sheet = p_w_b.sheet_by_index(0)
    save_book = xlwt.Workbook()
    save_sheet = save_book.add_sheet("sheet1")
    i = 0
    for x in range(1,sheet.nrows):
        code = int(sheet.cell(x, 0).value)
        province = sheet.cell(x, 1).value
        station = sheet.cell(x, 2).value
        code = str(code)+"0"
        for y in range(1,p_w_b_sheet.nrows):
            _code = p_w_b_sheet.cell(y,0).value
            s = type(_code)
            if type(_code) == type(1.0):
                _code = str(int(_code))
            if code == _code:
                for c in range(p_w_b_sheet.ncols):
                    save_sheet.write(i,c,p_w_b_sheet.cell(y,c).value)
                save_sheet.write(i,p_w_b_sheet.ncols,province)
                save_sheet.write(i, p_w_b_sheet.ncols+1, station)
                i = i +1



    save_book.save("fre.xls")















