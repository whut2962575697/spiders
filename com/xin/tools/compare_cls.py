# -*- encoding:utf-8 -*-

from libtiff import TIFF
from skimage.io import imread
import xlrd, xlwt

from config import small_label_color

def compare_generate_caption_with_image(generate_caption,img_file):
    img = imread(img_file)
    img_cls_list = []
    for row in img:
        for cell in row:
            if tuple(cell) != (255,255,255):
                s = ""
            if tuple(cell) == small_label_color["road"]["color"]:
                if "road" not in img_cls_list:
                    img_cls_list.append("road")
            if tuple(cell) == small_label_color["residence"]["color"]:
                if "residence" not in img_cls_list:
                    img_cls_list.append("residence")
            if tuple(cell) == small_label_color["industry"]["color"]:
                if "industry" not in img_cls_list:
                    img_cls_list.append("industry")
            if tuple(cell) == small_label_color["greenland"]["color"]:
                if "greenland" not in img_cls_list:
                    img_cls_list.append("greenland")
            if tuple(cell) == small_label_color["uncompleted"]["color"]:
                if "uncompleted" not in img_cls_list:
                    img_cls_list.append("uncompleted")
            if tuple(cell) == small_label_color["forest"]["color"]:
                if "forest" not in img_cls_list:
                    img_cls_list.append("forest")
            if tuple(cell) == small_label_color["playground"]["color"]:
                if "playground" not in img_cls_list:
                    img_cls_list.append("playground")
            if tuple(cell) == small_label_color["waterbody"]["color"]:
                if "waterbody" not in img_cls_list:
                    img_cls_list.append("waterbody")
            if tuple(cell) == small_label_color["village"]["color"]:
                if "village" not in img_cls_list:
                    img_cls_list.append("village")
            if tuple(cell) == small_label_color["service"]["color"]:
                if "service" not in img_cls_list:
                    img_cls_list.append("service")
            if tuple(cell) == small_label_color["farmland"]["color"]:
                if "farmland" not in img_cls_list:
                    img_cls_list.append("farmland")
            if tuple(cell) == small_label_color["other"]["color"]:
                if "other" not in img_cls_list:
                    img_cls_list.append("other")
    word_list = generate_caption.split(" ")
    caption_cls_list = []
    for word in word_list:
        if word == "road" and "road" not in caption_cls_list:
            caption_cls_list.append("road")
        if word == "residence" and "residence" not in caption_cls_list:
            caption_cls_list.append("residence")
        if word == "industry" and "industry" not in caption_cls_list:
            caption_cls_list.append("industry")
        if word == "greenland" and "greenland" not in caption_cls_list:
            caption_cls_list.append("greenland")
        if word == "uncompleted" and "uncompleted" not in caption_cls_list:
            caption_cls_list.append("uncompleted")
        if word == "forest" and "forest" not in caption_cls_list:
            caption_cls_list.append("forest")
        if word == "playground" and "playground" not in caption_cls_list:
            caption_cls_list.append("playground")
        if word == "waterbody" and "waterbody" not in caption_cls_list:
            caption_cls_list.append("waterbody")
        if word == "village" and "village" not in caption_cls_list:
            caption_cls_list.append("village")
        if word == "service" and "service" not in caption_cls_list:
            caption_cls_list.append("service")
        if word == "farmland" and "farmland" not in caption_cls_list:
            caption_cls_list.append("farmland")
        if word == "other" and "other" not in caption_cls_list:
            caption_cls_list.append("other")

    return caption_cls_list, img_cls_list


def calculate_rank():
    work_book = xlrd.open_workbook(r"error_cls.xls")
    sheet = work_book.sheet_by_index(0)
    n_rows = sheet.nrows
    distrinct_list = list()
    for x in range(n_rows):
        file_name = sheet.cell(x, 5).value
        img_num = int(file_name.strip(".jpg"))
        if img_num not in distrinct_list:
            distrinct_list.append(img_num)
    area1 = 0
    area2 = 0
    area3 = 0
    area4 = 0
    area5 = 0
    area6 = 0
    area7 = 0
    area8 = 0
    area9 = 0
    area10 = 0
    for item in distrinct_list:
        if item<250:
            area1 = area1 + 1
        if item>=230 and item<480:
            area2 = area2 + 1
        if item>=460 and item<710:
            area3 = area3 + 1
        if item>=690 and item<940:
            area4 = area4 + 1
        if item>=920 and item<1170:
            area5 = area5 + 1
        if item>=1150 and item<1400:
            area6 = area6 + 1
        if item>=1380 and item<1630:
            area7 = area7 + 1
        if item>=1610 and item<1738:
            area8 = area8 + 1
        if item>=1717 and item<1844:
            area9 = area9 + 1
        if item>=1824 and item<1950:
            area10 = area10 + 1
    print (area1, area2, area3, area4, area5, area6, area7, area8, area9, area10)
    print (len(distrinct_list))



if __name__ == "__main__":
    calculate_rank()
    # work_book = xlrd.open_workbook(r"C:\Users\29625\Desktop\FCNtrain.xls")
    # save_book = xlwt.Workbook()
    # save_sheet = save_book.add_sheet("sheet0")
    # i = 0
    # img_path = r"G:\xin.data\new_sample\huiducolor"
    # sheet = work_book.sheet_by_index(0)
    # n_rows = sheet.nrows
    # n_cols = sheet.ncols
    # for x in range(1,n_rows):
    #     generate_caption = sheet.cell(x, 1).value
    #     file_name = sheet.cell(x, 4).value
    #     file_name = file_name.replace("jpg", "png")
    #     caption_cls_list, img_cls_list = compare_generate_caption_with_image(generate_caption,img_path+"/"+file_name)
    #     res = True
    #     times = []
    #     for cls_word in caption_cls_list:
    #
    #         if cls_word not in img_cls_list:
    #             for index, word in enumerate(generate_caption.split(" ")):
    #                 if cls_word == word:
    #                     times.append(index+1)
    #             res = False
    #     if not res:
    #         print file_name+" is not true"
    #         print str(img_cls_list)
    #         print str(times)
    #         save_sheet.write(i, 0, str(img_cls_list))
    #         save_sheet.write(i, 1, str(times))
    #         for y in range(1, n_cols):
    #             save_sheet.write(i, y+1, sheet.cell(x, y).value)
    #         i = i+1
    #     # save_sheet.write(i, 0, str(file_name))
    #     # save_sheet.write(i, 1, str(img_cls_list))
    #     # i = i+1
    #
    #     else:
    #         print file_name+" is  true"
    # save_book.save("error_cls.xls")
     #caption_cls_list, img_cls_list = compare_generate_caption_with_image("service.", "imgs/rec_small_imgs/00032_8.tif")















