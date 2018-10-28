# -*- encoding:utf-8 -*-

import arcpy
import xlrd
import sys
reload(sys)
sys.setdefaultencoding("utf-8")




def read_data(file_path):
    data = xlrd.open_workbook(file_path)
    table = data.sheet_by_index(0)
    row_num = table.nrows
    geo_data = []
    for x in range(1, row_num):
        #name = table.cell(x, 0).value
        lng = table.cell(x, 0).value
        lat = table.cell(x, 1).value
        #[114.184813, 30.376357, 114.670253, 30.700619]
        if lng<114.184813 or lng>114.670253 or lat<30.376357 or lat>30.700619:
            continue
        point = {}
        #point["name"] = name
        point["lng"] = str(lng)
        point["lat"] = str(lat)
        geo_data.append(point)
    return geo_data

def create_geometry(source_file,save_path):
    geo_data = read_data(source_file)
    arcpy.env.workspace = save_path

    points = []
    for geo in geo_data:
        wkt = 'POINT ('+geo['lng']+' '+geo['lat']+')'
        point = arcpy.FromWKT(wkt)
        points.append(point)
    arcpy.CopyFeatures_management(points, 'mobike_points.shp')

    #arcpy.AddField_management('sites.shp', 'name', 'text')
    #cursor = arcpy.UpdateCursor('sites.shp')
    # for i, row in enumerate(cursor):
    #     row.setValue('name', geo_data[i]['name'])
    #     cursor.updateRow(row)


if __name__ == "__main__":
    create_geometry(r"C:\Users\29625\Desktop\mobike.xlsx",r"G:\gisdata")