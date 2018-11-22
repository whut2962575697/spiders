# -*- encoding:utf-8 -*-

from libtiff import TIFF
import cv2
from config import small_label_color, small_cls_color
import glob
import json, xlrd, xlwt


def determine_big_object(res, sentence, big_scale_img, filename, s_objects_path):
    if filename == "563.tif":
        pass
    label_words = dict()
    subsentences = sentence.split("with")
    res[filename] = {}
    wi = 0
    for s, subsentence in enumerate(subsentences):
        words = subsentence.split(" ")
        for k, word in enumerate(words):
            if word in small_label_color.keys():
                label_words[wi] = s
                wi = wi + 1
    for s, subsentence in enumerate(subsentences):
        words = subsentence.split(" ")
        class_words = dict()
        sub_res = {
            "status": 0,

            "big_scale": [-1, -1]
        }
        res[filename][s] = sub_res
        for k, word in enumerate(words):
            if word in small_label_color.keys():
                class_words[k] = word


        for k, class_word in class_words.items():
            s_obs = glob.glob(s_objects_path + "/" + filename.strip(".tif") + "_" + class_word + "*.tif")
            if len(s_obs) == 0:
                sub_res["status"] = 1
                res[filename]["wi"] = label_words
                break
            if class_word in big_scale_img["0"]:
                if sub_res["big_scale"][0] != 1:
                    sub_res["big_scale"][0] = 0
            else:
                sub_res["big_scale"][0] = 1


        if big_scale_img.has_key("1"):
            for k, class_word in class_words.items():
                if class_word in big_scale_img["1"]:
                    if sub_res["big_scale"][1] != 1:
                        sub_res["big_scale"][1] = 0
                else:
                    sub_res["big_scale"][1] = 1
    res[filename]["wi"] = label_words


def analyse(excel, json_file):

    with open(json_file, 'r') as f:
        json_data = json.load(f)
    save_book = xlwt.Workbook()
    save_sheet = save_book.add_sheet("sheet1")
    work_book = xlrd.open_workbook(excel)
    sheet = work_book.sheet_by_index(0)
    cin = 0
    for x in range(2,sheet.nrows):
        file_name = sheet.cell(x, 0).value
        file_name = file_name.replace("_caption.jpg", ".tif")
        if file_name == "32.tif":
            pass
        if file_name == u"":
            continue
        if file_name!=u"" and sheet.cell(x-1, 0).value == u"":
            cin = 0
        info = json_data[file_name]

        wi = info["wi"][str(cin)]

        status = info[str(wi)]["status"]
        if status == 0:
            big_scale = info[str(wi)]["big_scale"]
            if big_scale[0] == 0 and big_scale[1] != 0:
                big_scale_cls = 0
                true_cls = int(sheet.cell(x, 2).value.strip(".tif").split("_")[1])
                save_sheet.write(x, 0, file_name)
                save_sheet.write(x, 1, sheet.cell(x, 1).value)
                save_sheet.write(x, 2, wi)
                save_sheet.write(x, 3, big_scale_cls)
                save_sheet.write(x, 4, true_cls)
                if big_scale_cls == true_cls:
                    save_sheet.write(x, 5, "True")
                else:
                    save_sheet.write(x, 5, "False")


            elif big_scale[0] != 0 and big_scale[1] == 0:
                big_scale_cls = 1
                true_cls = int(sheet.cell(x, 2).value.strip(".tif").split("_")[1])
                save_sheet.write(x, 0, file_name)
                save_sheet.write(x, 1, sheet.cell(x, 1).value)
                save_sheet.write(x, 2, wi)
                save_sheet.write(x, 3, big_scale_cls)
                save_sheet.write(x, 4, true_cls)
                if big_scale_cls == true_cls:
                    save_sheet.write(x, 5, "True")
                else:
                    save_sheet.write(x, 5, "False")

            elif big_scale[0] == 0 and big_scale[1] == 0:
                big_scale_cls = str([0, 1])
                true_cls = int(sheet.cell(x, 2).value.strip(".tif").split("_")[1])
                save_sheet.write(x, 0, file_name)
                save_sheet.write(x, 1, sheet.cell(x, 1).value)
                save_sheet.write(x, 2, wi)
                save_sheet.write(x, 3, big_scale_cls)
                save_sheet.write(x, 4, true_cls)

                save_sheet.write(x, 5, "True")

            else:
                big_scale_cls = str([0, 1])
                true_cls = int(sheet.cell(x, 2).value.strip(".tif").split("_")[1])
                save_sheet.write(x, 0, file_name)
                save_sheet.write(x, 1, sheet.cell(x, 1).value)
                save_sheet.write(x, 2, wi)
                save_sheet.write(x, 3, "error")
                save_sheet.write(x, 4, true_cls)
                if big_scale_cls == true_cls:
                    save_sheet.write(x, 5, "True")
                else:
                    save_sheet.write(x, 5, "False")

        else:

            true_cls = int(sheet.cell(x, 2).value.strip(".tif").split("_")[1])
            save_sheet.write(x, 0, file_name)
            save_sheet.write(x, 1, sheet.cell(x, 1).value)
            save_sheet.write(x, 2, wi)
            save_sheet.write(x, 3, "error")
            save_sheet.write(x, 4, true_cls)
        cin = cin+1
    save_book.save("res.xls")






if __name__ == "__main__":
    # analyse(r'C:\Users\29625\Desktop\newdata_areamean.xls', 'big_ob.json')
    work_book = xlrd.open_workbook(r"C:\Users\29625\Desktop\newdata_gencap.xls")
    sheet = work_book.sheet_by_index(0)
    res = {}
    with open("final_json.json", "r") as f:
        json_data = json.load(f)
    for x in range(sheet.nrows):
        file_name = sheet.cell(x, 0).value.replace("_caption.jpg", ".tif")
        caption = sheet.cell(x, 1).value.strip(".")
        if json_data.has_key(file_name):
            print (file_name)
            big_scale_img = json_data[file_name]
            if big_scale_img != {}:
                for k ,v in big_scale_img.items():
                    for i, _vi in enumerate(v):
                        big_scale_img[k][i] = small_cls_color[_vi]["label"]

                determine_big_object(res, caption, big_scale_img, file_name,
                                 r'G:\xin.data\new_sample\val_gt\rename_extract_objects')

    with open("big_ob.json", "w") as f:
        json.dump(res, f)



















