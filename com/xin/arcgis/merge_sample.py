# -*- encoding:utf-8 -*-

import arcpy
import xlrd


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
    for x in range(sheet.nrows):
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


if __name__ == "__main__":
    choose_sample(r"G:\xin.data\new_sample\big_scale\PHW01\PHW01", "save.shp", "final_save.shp",
                  r"G:\xin.data\new_sample\big_scale\PHW01\PHW01\sample5.xls")

