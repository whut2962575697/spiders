# -*- encoding:utf-8 -*-

import arcpy
import xlrd


def shp_to_raster(workspace, excel, shp, c_field, save_path):
    arcpy.env.workspace = workspace
    if arcpy.Exists("temp.shp"):
        arcpy.Delete_management("temp.shp")


    work_book = xlrd.open_workbook(excel)
    sheet = work_book.sheet_by_index(0)
    for x in range(0, sheet.nrows, 3):
        desc = arcpy.Describe(shp)
        spatial_reference = desc.spatialReference
        arcpy.CreateFeatureclass_management(workspace, "temp.shp", "POLYGON", shp, "DISABLED", "DISABLED",
                                            spatial_reference)
        fields = ["FID", "JUDGE_CLAS", "SHAPE@"]
        values = []
        file_name = sheet.cell(x, 4).value

        where_clause = """"file_name" = '""" + file_name.replace("tif", "shp") + "'"
        cursor = arcpy.SearchCursor(shp, where_clause)
        for row in cursor:
            values.append([row.FID, row.JUDGE_CLAS, row.Shape])

        print (file_name)

        insert_cursor = arcpy.da.InsertCursor("temp.shp", fields)
        for insert_row in values:
            insert_cursor.insertRow(insert_row)
        del insert_cursor
        arcpy.FeatureToRaster_conversion("temp.shp", c_field, save_path+"/"+file_name.replace("shp", "tif"), 0.6)
        # update_cursor = arcpy.da.UpdateCursor("temp.shp", fields)
        # for _ in update_cursor:
        #     update_cursor.deleteRow()
        # del update_cursor
        arcpy.Delete_management("temp.shp")



if __name__ == "__main__":
    for x in range(7):

        shp_to_raster(r"G:\xin.data\new_sample\big_scale_shp", r'G:\xin.data\new_sample\clip_shp\save\sample'+str(x+1)+'.xls', "final_save"+str(x+1)+".shp", "JUDGE_CLAS", r"G:\xin.data\new_sample\RESD")
