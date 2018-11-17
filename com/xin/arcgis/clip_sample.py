# -*- encoding:utf-8 -*-

import arcpy
import os
import xlrd
import xlwt


def clip_sample(workspace, shp_file_name, clip_shp):

    arcpy.env.workspace = workspace
    if not os.path.exists(workspace+"/"+"temp"):
        os.mkdir(workspace+"/"+"temp")
    if not os.path.exists(workspace+"/"+"output"):
        os.mkdir(workspace+"/"+"output")
    desc = arcpy.Describe(shp_file_name)
    fields = ["SHAPE@"]

    fields.append("SHAPE@")
    for row in arcpy.SearchCursor(clip_shp):
        mask = row.getValue("Shape")
        FID = row.getValue("FID")
            # arcpy.CopyFeatures_management(polygons, 'temp/temp_'+str(i)+'_'+str(j)+'.shp')
        arcpy.Clip_analysis(shp_file_name, mask, 'output/'+str(FID)+'.shp')

        print ('output/'+str(FID)+'.shp is generated successfully!')


def merge_shp(excel, workspace, output):
    arcpy.env.workspace = workspace
    work_book = xlrd.open_workbook(excel)
    sheet = work_book.sheet_by_index(0)
    temp_list = []
    save_class = sheet.cell(4, 4).value.replace("tif", "shp")
    temp_list.append(save_class)
    save_class = save_class.decode("gbk").encode("utf-8")
    arcpy.CopyFeatures_management(save_class, output)
    arcpy.AddField_management(output, "file_name", "text")
    field = ('file_name')
    cursor = arcpy.da.UpdateCursor(output, field)
    for row in cursor:
        row[0] = save_class
        cursor.updateRow(row)
    del cursor

    for x in range(4, sheet.nrows, 3):
        f_class = sheet.cell(x, 4).value.replace("tif", "shp")
        if f_class in temp_list:
            continue
        print f_class
        arcpy.AddField_management(f_class, "file_name", "text")
        field = ('file_name')
        cursor = arcpy.da.UpdateCursor(f_class, field)
        for row in cursor:
            row[0] = f_class
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
                values.append(row)
            except Exception, e:
                print str(e)
        del cursor
        cursor = arcpy.da.InsertCursor(output, fields)
        for row in values:
            cursor.insertRow(row)
        del cursor


def split_excel(excel):
    work_book = xlrd.open_workbook(excel)
    sheet = work_book.sheet_by_index(0)
    save_book = xlwt.Workbook()
    save_sheet = save_book.add_sheet("sheet")
    i = 0
    for x in range(1, 661):
        id = sheet.cell(x, 0).value
        caption = sheet.cell(x, 1).value
        caption_id = sheet.cell(x, 2).value
        file_name = sheet.cell(x, 3).value
        file_name2 = sheet.cell(x, 4).value
        image_id = sheet.cell(x, 5).value
        imgid = sheet.cell(x, 6).value
        split = sheet.cell(x, 7).value
        save_sheet.write(i, 0, id)
        save_sheet.write(i, 1, caption)
        save_sheet.write(i, 2, caption_id)
        save_sheet.write(i, 3, file_name)
        save_sheet.write(i, 4, file_name2)
        save_sheet.write(i, 5, image_id)
        save_sheet.write(i, 6, imgid)
        save_sheet.write(i, 7, split)
        i = i+1
    save_book.save("sample1.xls")

    save_book = xlwt.Workbook()
    save_sheet = save_book.add_sheet("sheet")
    i = 0
    for x in range(661, 1321):
        id = sheet.cell(x, 0).value
        caption = sheet.cell(x, 1).value
        caption_id = sheet.cell(x, 2).value
        file_name = sheet.cell(x, 3).value
        file_name2 = sheet.cell(x, 4).value
        image_id = sheet.cell(x, 5).value
        imgid = sheet.cell(x, 6).value
        split = sheet.cell(x, 7).value
        save_sheet.write(i, 0, id)
        save_sheet.write(i, 1, caption)
        save_sheet.write(i, 2, caption_id)
        save_sheet.write(i, 3, file_name)
        save_sheet.write(i, 4, file_name2)
        save_sheet.write(i, 5, image_id)
        save_sheet.write(i, 6, imgid)
        save_sheet.write(i, 7, split)
        i = i + 1
    save_book.save("sample2.xls")

    save_book = xlwt.Workbook()
    save_sheet = save_book.add_sheet("sheet")
    i = 0
    for x in range(1321, 1981):
        id = sheet.cell(x, 0).value
        caption = sheet.cell(x, 1).value
        caption_id = sheet.cell(x, 2).value
        file_name = sheet.cell(x, 3).value
        file_name2 = sheet.cell(x, 4).value
        image_id = sheet.cell(x, 5).value
        imgid = sheet.cell(x, 6).value
        split = sheet.cell(x, 7).value
        save_sheet.write(i, 0, id)
        save_sheet.write(i, 1, caption)
        save_sheet.write(i, 2, caption_id)
        save_sheet.write(i, 3, file_name)
        save_sheet.write(i, 4, file_name2)
        save_sheet.write(i, 5, image_id)
        save_sheet.write(i, 6, imgid)
        save_sheet.write(i, 7, split)
        i = i + 1
    save_book.save("sample3.xls")

    save_book = xlwt.Workbook()
    save_sheet = save_book.add_sheet("sheet")
    i = 0
    for x in range(1981, 2641):
        id = sheet.cell(x, 0).value
        caption = sheet.cell(x, 1).value
        caption_id = sheet.cell(x, 2).value
        file_name = sheet.cell(x, 3).value
        file_name2 = sheet.cell(x, 4).value
        image_id = sheet.cell(x, 5).value
        imgid = sheet.cell(x, 6).value
        split = sheet.cell(x, 7).value
        save_sheet.write(i, 0, id)
        save_sheet.write(i, 1, caption)
        save_sheet.write(i, 2, caption_id)
        save_sheet.write(i, 3, file_name)
        save_sheet.write(i, 4, file_name2)
        save_sheet.write(i, 5, image_id)
        save_sheet.write(i, 6, imgid)
        save_sheet.write(i, 7, split)
        i = i + 1
    save_book.save("sample4.xls")

    save_book = xlwt.Workbook()
    save_sheet = save_book.add_sheet("sheet")
    i = 0
    for x in range(2641, 3301):
        id = sheet.cell(x, 0).value
        caption = sheet.cell(x, 1).value
        caption_id = sheet.cell(x, 2).value
        file_name = sheet.cell(x, 3).value
        file_name2 = sheet.cell(x, 4).value
        image_id = sheet.cell(x, 5).value
        imgid = sheet.cell(x, 6).value
        split = sheet.cell(x, 7).value
        save_sheet.write(i, 0, id)
        save_sheet.write(i, 1, caption)
        save_sheet.write(i, 2, caption_id)
        save_sheet.write(i, 3, file_name)
        save_sheet.write(i, 4, file_name2)
        save_sheet.write(i, 5, image_id)
        save_sheet.write(i, 6, imgid)
        save_sheet.write(i, 7, split)
        i = i + 1
    save_book.save("sample5.xls")

    save_book = xlwt.Workbook()
    save_sheet = save_book.add_sheet("sheet")
    i = 0
    for x in range(3301, 3961):
        id = sheet.cell(x, 0).value
        caption = sheet.cell(x, 1).value
        caption_id = sheet.cell(x, 2).value
        file_name = sheet.cell(x, 3).value
        file_name2 = sheet.cell(x, 4).value
        image_id = sheet.cell(x, 5).value
        imgid = sheet.cell(x, 6).value
        split = sheet.cell(x, 7).value
        save_sheet.write(i, 0, id)
        save_sheet.write(i, 1, caption)
        save_sheet.write(i, 2, caption_id)
        save_sheet.write(i, 3, file_name)
        save_sheet.write(i, 4, file_name2)
        save_sheet.write(i, 5, image_id)
        save_sheet.write(i, 6, imgid)
        save_sheet.write(i, 7, split)
        i = i + 1
    save_book.save("sample6.xls")

    save_book = xlwt.Workbook()
    save_sheet = save_book.add_sheet("sheet")
    i = 0
    for x in range(3961, 4621):
        id = sheet.cell(x, 0).value
        caption = sheet.cell(x, 1).value
        caption_id = sheet.cell(x, 2).value
        file_name = sheet.cell(x, 3).value
        file_name2 = sheet.cell(x, 4).value
        image_id = sheet.cell(x, 5).value
        imgid = sheet.cell(x, 6).value
        split = sheet.cell(x, 7).value
        save_sheet.write(i, 0, id)
        save_sheet.write(i, 1, caption)
        save_sheet.write(i, 2, caption_id)
        save_sheet.write(i, 3, file_name)
        save_sheet.write(i, 4, file_name2)
        save_sheet.write(i, 5, image_id)
        save_sheet.write(i, 6, imgid)
        save_sheet.write(i, 7, split)
        i = i + 1
    save_book.save("sample7.xls")

    save_book = xlwt.Workbook()
    save_sheet = save_book.add_sheet("sheet")
    i = 0
    for x in range(4621, sheet.nrows):
        id = sheet.cell(x, 0).value
        caption = sheet.cell(x, 1).value
        caption_id = sheet.cell(x, 2).value
        file_name = sheet.cell(x, 3).value
        file_name2 = sheet.cell(x, 4).value
        image_id = sheet.cell(x, 5).value
        imgid = sheet.cell(x, 6).value
        split = sheet.cell(x, 7).value
        save_sheet.write(i, 0, id)
        save_sheet.write(i, 1, caption)
        save_sheet.write(i, 2, caption_id)
        save_sheet.write(i, 3, file_name)
        save_sheet.write(i, 4, file_name2)
        save_sheet.write(i, 5, image_id)
        save_sheet.write(i, 6, imgid)
        save_sheet.write(i, 7, split)
        i = i + 1
    save_book.save("sample8.xls")


if __name__ == "__main__":
    split_excel(r'C:\Users\29625\Desktop\caption.xlsx')
    #clip_sample(r'G:\xin.data\new_sample\clip_shp', '3parts.shp', "final_patch.shp")
    #merge_shp(r'C:\Users\29625\Desktop\caption.xlsx', r'G:\xin.data\new_sample\clip_shp\output', r'G:\xin.data\new_sample\clip_shp\save\save.shp')