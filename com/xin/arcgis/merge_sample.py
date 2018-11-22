# -*- encoding:utf-8 -*-

import arcpy
import xlrd
import json


def choose_sample(workspace, shp, save_shp, excel):
    work_book = xlrd.open_workbook(excel)
    sheet = work_book.sheet_by_index(0)
    arcpy.env.workspace = workspace
    all_fields = arcpy.ListFields(shp)
    fields = []
    for field in all_fields:
        fields.append(field.name)
    fields.append("SHAPE@")
    values = []
    desc = arcpy.Describe(shp)
    spatial_reference = desc.spatialReference
    arcpy.CreateFeatureclass_management(workspace, save_shp, "POLYGON", shp, "DISABLED", "DISABLED",spatial_reference)
    for x in range(0, sheet.nrows, 3):
        file_name = sheet.cell(x, 4).value
        cursor = arcpy.da.SearchCursor(shp, fields)
        for row in cursor:
            _file_name = row[25]
            # print (file_name, _file_name)
            if file_name.replace("tif", "shp") == _file_name:
                values.append(row)
        del cursor
    print (len(values))
    cursor = arcpy.da.InsertCursor(save_shp, fields)
    for row in values:
        cursor.insertRow(row)
    del cursor


def mk_json(workspace, shp, excel, json_name):
    arcpy.env.workspace = workspace
    work_book = xlrd.open_workbook(excel)
    sheet = work_book.sheet_by_index(0)
    res_dict = dict()
    for x in range(0, sheet.nrows, 3):
        file_name = sheet.cell(x, 4).value
        res_dict[file_name] = {

        }

        #where_clause = "\"FILE_NAME\" ='"+file_name.replace("tif", "shp")+"'"
        where_clause = """"file_name" = '"""+file_name.replace("tif", "shp")+"'"
        cursor = arcpy.SearchCursor(shp, where_clause)
        for row in cursor:
            if row.JUDGE_CLAS == 0:
                if not res_dict[file_name].has_key("0"):
                    res_dict[file_name]["0"] = [row.VALUE]
                else:
                    res_dict[file_name]["0"].append(row.VALUE)
            elif row.JUDGE_CLAS == 1:
                if not res_dict[file_name].has_key("1"):
                    res_dict[file_name]["1"] = [row.VALUE]
                else:
                    res_dict[file_name]["1"].append(row.VALUE)
        del cursor
        with open(json_name, "w") as f:
            json.dump(res_dict, f)

def concat_json():
    res_dict = {}
    i = 0
    m = 0
    for x in range(8):
        with open("sample"+str(x+1)+".json", "r") as f:
            json_datas = json.load(f)
            for k, v in json_datas.items():
                res_dict[k] = v
                print k, v
                for _k, _v in v.items():
                    if len(_v) != len(set(_v)):
                        m = m + 1
                        break
                i = i+1
    print (i)
    print (m)
    with open("final_json.json", "w") as f:
        json.dump(res_dict, f)


if __name__ == "__main__":
    concat_json()
    # choose_sample(r"G:\xin.data\new_sample\big_scale\7&8&error_wzw\7&8&error_wzw", "save7_8_wzw.shp", "final_save8.shp",
    #               r"G:\xin.data\new_sample\big_scale\7&8&error_wzw\7&8&error_wzw\sample8error_wzw.xls")
    # mk_json(r"G:\xin.data\new_sample\big_scale_shp", "final_save1.shp", r"G:\xin.data\new_sample\clip_shp\save\sample1.xls", "sample1.json")

