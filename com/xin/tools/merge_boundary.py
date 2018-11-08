# -*- encoding:utf-8 -*-

import arcpy
import glob


def merge(shp_path):
    arcpy.env.workspace =shp_path
    arcpy.CreateFeatureclass_management(shp_path, "merge.shp", "POLYGON")
    # arcpy.AddField_management("merge.shp", "FID", "LONG")
    arcpy.AddField_management("merge.shp", "division", "TEXT")

    shp_files = glob.glob(shp_path+"/*.shp")
    fields = ('SHAPE@')
    i = 0
    for shp_file in shp_files:
        shp_name = shp_file[shp_file.rindex("\\")+1:]
        shp_name = shp_name.decode("gbk").encode("utf-8")
        if shp_name.endswith("区.shp") or shp_name.endswith("县.shp"):
            cursor = arcpy.da.SearchCursor(shp_name, fields)
            values = []

            for row in cursor:
                try:
                    value = [i, shp_name.strip(".shp"), row[0]]
                    values.append(value)
                    i = i+1
                except Exception, e:
                    print str(e)
            del cursor
            merge_fields = ("FID", "division", "SHAPE@")
            cursor = arcpy.da.InsertCursor("merge.shp", merge_fields)
            for row in values:
                cursor.insertRow(row)
            del cursor


if __name__ =="__main__":
    merge(r"G:\xin.src\c#\TrastationSystem\TrastationSystem\TrastationSystem\bin\divisions")
