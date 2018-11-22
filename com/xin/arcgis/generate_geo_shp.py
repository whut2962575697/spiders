# -*- encoding:utf-8 -*-

import arcpy
import json

from com.xin.common.MysqlManage import MysqlHandle



def load_geo_page(table):
    db = MysqlHandle()
    sql = "select uid,name,type, page from "+table+" where status is null limit 40000 "
    res_query = db.query(sql)
    return res_query


def mk_new_shp(shp, workspace):
    arcpy.env.workspace = workspace
    arcpy.CreateFeatureclass_management(workspace, shp, "POLYLINE", spatial_reference=3857)
    arcpy.AddField_management(shp, "uid", "text", field_length=50)
    arcpy.AddField_management(shp, "name", "text", field_length=500)
    arcpy.AddField_management(shp, "province", "text", field_length=300)
    arcpy.AddField_management(shp, "city", "text", field_length=300)
    arcpy.AddField_management(shp, "geo_type", "LONG")
    arcpy.AddField_management(shp, "timetable", "text", field_length=300)
    arcpy.AddField_management(shp, "price", "double")


def insert_into_shp(shp, workspace, query_item):
    uid = query_item[0]
    name = query_item[1]
    geo_type = query_item[2]
    page = query_item[3]
    json_page = json.loads(page)
    if not json_page.has_key("content"):
        return
    content = json_page["content"]
    item_info = content[0]
    geo = item_info["geo"]
    _geo = geo.split("|")[2].strip(";")
    real_geo = "MULTILINESTRING("
    for segement in _geo.split(";"):
        real_geo = real_geo + "("
        los = segement.split(",")
        for i in range(0, len(los), 2):
            # if i>2 :
            #     if los[i]==los[i - 2] and los[i + 1]==los[i - 1]:
            #         continue
            real_geo = real_geo + los[i] + " " + los[i + 1] + ","
        real_geo = real_geo.strip(",") + "),"
    real_geo = real_geo.strip(",") + ")"

    timetable = item_info["timetable"]
    if timetable is None:
        timetable = ""
    price = int(item_info["ticketPrice"])/100.0
    current_city = json_page["current_city"]

    city = current_city["name"]
    if city is None:
        city = ""
    province = current_city["up_province_name"]
    if province is None:
        province = ""
    arcpy.env.workspace = workspace
    polyline = arcpy.FromWKT(real_geo)
    fields = ["UID", "NAME", "PROVINCE", "CITY", "GEO_TYPE", "TIMETABLE", "PRICE"]
    fields.append("SHAPE@")
    values = [uid, name, province, city, geo_type, timetable, price, polyline]
    cursor = arcpy.da.InsertCursor(shp, fields)
    cursor.insertRow(values)
    del cursor

    db = MysqlHandle()
    sql = 'update baidu_busline_page set status=200 where uid="' + item[0] + '"'
    db.update(sql)



def mk_stations_shp(shp, workspace):
    arcpy.env.workspace = workspace
    arcpy.CreateFeatureclass_management(workspace, shp, "POINT", spatial_reference=3857)
    arcpy.AddField_management(shp, "uid", "text", field_length=50)
    arcpy.AddField_management(shp, "name", "text", field_length=500)
    arcpy.AddField_management(shp, "province", "text", field_length=300)
    arcpy.AddField_management(shp, "city", "text", field_length=300)
    arcpy.AddField_management(shp, "l_uid", "text", field_length=50)
    arcpy.AddField_management(shp, "l_name", "text", field_length=500)


def insert_into_stations(shp, workspace, query_item):
    l_uid = query_item[0]
    name = query_item[1]
    page = query_item[3]
    json_page = json.loads(page)
    if not json_page.has_key("content"):
        return
    content = json_page["content"]
    item_info = content[0]
    stations = item_info["stations"]
    current_city = json_page["current_city"]

    city = current_city["name"]
    if city is None:
        city = ""
    province = current_city["up_province_name"]
    if province is None:
        province = ""
    for station in stations:
        station_name = station["name"]
        station_geo = station["geo"].strip(";").split("|")[-1].replace(","," ")
        geo_str = "POINT(%s)" % (station_geo)
        station_uid = station["uid"]
        arcpy.env.workspace = workspace
        point = arcpy.FromWKT(geo_str)
        fields = ["UID", "NAME", "PROVINCE", "CITY", "L_UID", "L_NAME"]
        fields.append("SHAPE@")
        values = [station_uid, station_name, province, city, l_uid, name, point]
        cursor = arcpy.da.InsertCursor(shp, fields)
        cursor.insertRow(values)
        del cursor
    db = MysqlHandle()
    sql = 'update baidu_busline_page set status=200 where uid="' + item[0] + '"'
    db.update(sql)


if __name__ == "__main__":
    # mk_new_shp("gl_bd_busline.shp", r'G:\xin.data\spiders_data\busline')
    mk_stations_shp("gp_bd_busstations.shp", r'G:\xin.data\spiders_data\busline')
    res_items = load_geo_page("baidu_busline_page")
    for item in res_items:
        print (item[0])
        # insert_into_shp("gl_bd_busline.shp", r'G:\xin.data\spiders_data\busline', item)
        insert_into_stations("gp_bd_busstations.shp", r'G:\xin.data\spiders_data\busline', item)



