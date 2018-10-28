# -*- encoding:utf-8 -*-


import arcpy
import glob
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def merge(shp_path):
    arcpy.env.workspace = shp_path
    shp_files = glob.glob(shp_path + "/*.shp")
    save_class = shp_files[0][shp_files[0].rindex("\\")+1:]
    save_class = save_class.decode("gbk").encode("utf-8")
    arcpy.CopyFeatures_management(save_class, "save.shp")
    arcpy.AddField_management("save.shp", "layer_name", "text")
    field = ('layer_name')
    cursor = arcpy.da.UpdateCursor("save.shp", field)
    for row in cursor:
        row[0] = save_class.strip(".shp")
        cursor.updateRow(row)
    del cursor
    for x in range(1, len(shp_files)):
        file_name = shp_files[x][shp_files[x].rindex("\\")+1:]
        f_class = file_name.decode("gbk").encode("utf-8")
        arcpy.AddField_management(f_class, "layer_name", "text")
        field = ('layer_name')
        cursor = arcpy.da.UpdateCursor(f_class, field)
        for row in cursor:
            row[0] = f_class.strip(".shp")
            cursor.updateRow(row)
        del cursor
        all_fields = arcpy.ListFields(f_class)
        fields = []
        for field in all_fields:
            fields.append(field.name)
        fields.append("SHAPE@")
        cursor = arcpy.da.SearchCursor(f_class, fields)
        values = []
        for row in cursor:

            try:
                value = [x, row[1], x+1, row[3], row[4], x+1, row[6], row[7]]
                values.append(value)
            except Exception, e:
                print str(e)
        del cursor
        cursor = arcpy.da.InsertCursor("save.shp", fields)
        for row in values:
            cursor.insertRow(row)
        del cursor


merge(r'G:\gisdata\w\w')


