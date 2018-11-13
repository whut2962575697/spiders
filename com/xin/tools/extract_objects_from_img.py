# -*- encoding:utf-8 -*-

from libtiff import TIFF
import glob,os
import xlrd,xlwt
import cv2
import json
import numpy as np
import copy
import matplotlib.pyplot as plt
from config import small_color_cls
from Queue import Queue


def extract_object_plus_plus(image, save_path):
    img = TIFF.open(image)
    img = img.read_image()
    nrows = img.shape[0]
    ncols = img.shape[0]
    file_name = image.split("/")[-1]
    #clip_cells = [] # item:(row_index,column_index)
    count = 0
    while is_not_black(img):
        segments = {}  # item:row_index:[(begin,end),...]
        clip_segments = []
        cls = 0

        for i, row in enumerate(img):
            segments[i] = []
            segment = [0, 0]
            last_cell = (0, 0, 0)
            for j, cell in enumerate(row):
                if tuple(cell) != (0, 0, 0) and cls == 0:
                    cls = small_color_cls[tuple(cell)]["cls_num"]
                    segment[0] = j
                    segment[1] = j
                if cls != 0:

                    if small_color_cls[tuple(cell)]["cls_num"] == cls:

                        segment[1] = j
                        if j == ncols-1:
                            segments[i].append(copy.copy(segment))
                    else:
                        if small_color_cls[tuple(last_cell)]["cls_num"] == cls:
                            segments[i].append(copy.copy(segment))

                        segment[0] = j + 1
                        segment[1] = j + 1
                last_cell = cell
            if not segments[i] and cls!=0:
                segments.pop(i)
                break

        queue = Queue()
        queue_dic = {}
        # now_segment = []
        for x in range(len(segments)):
            if len(segments[x]) != 0:
                # clip_segments.append([x,segments[x][0][0],segments[x][0][1]])
                queue.put_nowait((x, segments[x][0][0], segments[x][0][1]))
                queue_dic[(x, segments[x][0][0], segments[x][0][1])] = 0
                break
        while not queue.empty():
            seg = queue.get_nowait()
            queue_dic.pop(seg)
            clip_segments.append(seg)
            row_index = seg[0]

            if row_index != 0:
                last_row_segs = segments[row_index - 1]
                for last_seg in last_row_segs:

                    if (row_index - 1, last_seg[0], last_seg[1]) not in clip_segments and not queue_dic.has_key((row_index - 1, last_seg[0], last_seg[1])):
                        if seg[1] < last_seg[1] and seg[2] > last_seg[0]:

                            queue.put_nowait((row_index - 1, last_seg[0], last_seg[1]))
                            queue_dic[(row_index - 1, last_seg[0], last_seg[1])] = 0
            if row_index != len(segments)-1:
                next_row_segs = segments[row_index + 1]
                for next_seg in next_row_segs:

                    if (row_index + 1, next_seg[0], next_seg[1]) not in clip_segments and not queue_dic.has_key((row_index + 1, next_seg[0], next_seg[1])):
                        if seg[1] < next_seg[1] and seg[2] > next_seg[0]:
                            queue.put_nowait((row_index + 1, next_seg[0], next_seg[1]))
                            queue_dic[(row_index + 1, next_seg[0], next_seg[1])] = 0
        rectangle = [float("inf"), float("-inf"), float("inf"), float("-inf")]  # [row_min,row_max,column_min,column_max]
        copy_img = np.ones([nrows, ncols, 3]) * 0
        # points = []
        # copy_img_boundary = np.ones([200, 200, 3]) * 255
        # for seg in clip_segments:
        #     row_index = seg[0]
        #     begin = seg[1]
        #     end = seg[2]
            # for x in range(begin,end+1):
            #     if calculate_surround(img,(row_index,x),img[row_index][x]):
            #         points.append((row_index,x))
        # for point in points:
        #
        #     copy_img_boundary[point[0]][point[1]] = tuple(img[point[0]][point[1]])
        # copy_img_boundary = cv2.cvtColor(copy_img_boundary.astype(np.uint8), cv2.COLOR_RGB2BGR)
        # cv2.imwrite( "boundary.tif", copy_img_boundary)
        for seg in clip_segments:
            row_index = seg[0]
            begin = seg[1]
            end = seg[2]
            if row_index < rectangle[0]:
                rectangle[0] = row_index
            if row_index > rectangle[1]:
                rectangle[1] = row_index
            # if begin < rectangle[2]:
            #     rectangle[2] = begin
            # if end > rectangle[3]:
            #     rectangle[3] = end
            if row_index == nrows-1 :
                x = 2
            for j in range(begin, end + 1):
                if j < rectangle[2]:
                    rectangle[2] = j
                if j > rectangle[3]:
                    rectangle[3] = j
                # x =  tuple(img[row_index][j])
                copy_img[row_index][j] = tuple(img[row_index][j])
                img[row_index][j] = (0, 0, 0)
        row_min = rectangle[0]
        row_max = rectangle[1]
        column_min = rectangle[2]
        column_max = rectangle[3]
        if row_max-row_min < 20 and column_max-column_min < 20:
            continue
        # rec_img = copy_img[row_min:row_max + 1,column_min:column_max + 1]
        rec_img = copy_img
        # x = len(rec_img)
        # y = len(rec_img[0])
        if len(rec_img) > 10 and len(rec_img[0]) > 10:
            rec_img = cv2.cvtColor(rec_img.astype(np.uint8), cv2.COLOR_RGB2BGR)
            cv2.imwrite(save_path+"/"+file_name.strip(".tif") + "_" + str(count) + ".tif", rec_img)
            count = count + 1


def is_not_black(img):
    for row in img:
        for cell in row:
            if tuple(cell) != (0,0,0):
                return True
    return False


def img_interpolation(input_img, save_path):
    img = TIFF.open(input_img)
    img = img.read_image()
    (row_num, column_num) = img.shape[:2]
    color_value_list = []
    for x in range(row_num):
        for y in range(column_num):
            cell = tuple(img[x][y])
            if cell not in color_value_list:
                color_value_list.append(cell)
    #img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_RGB2BGR)
    resize_img = cv2.resize(img, (200, 200), interpolation=cv2.INTER_CUBIC)
    (row_num, column_num) = resize_img.shape[:2]
    for x in range(row_num):
        for y in range(column_num):
            cell = tuple(resize_img[x][y])
            color_loss = []
            for _cell in color_value_list:
                loss = np.square(int(cell[0]) - int(_cell[0])) + np.square(int(cell[1]) - int(_cell[1])) + np.square(int(cell[2]) - (_cell[2]))
                color_loss.append(loss)

            if x > 0 or y > 0:
                near_color_list = []
                try:
                    cell_1 = tuple(resize_img[x-1][y])
                    if cell_1 in color_value_list and cell_1 not in near_color_list:
                        near_color_list.append(cell_1)
                except Exception as e:
                    print(e.message)
                try:
                    cell_1 = tuple(resize_img[x+1][y])
                    if cell_1 in color_value_list and cell_1 not in near_color_list:
                        near_color_list.append(cell_1)
                except:
                    pass
                try:
                    cell_1 = tuple(resize_img[x][y-1])
                    if cell_1 in color_value_list and cell_1 not in near_color_list:
                        near_color_list.append(cell_1)
                except:
                    pass
                try:
                    cell_1 = tuple(resize_img[x][y+1])
                    if cell_1 in color_value_list and cell_1 not in near_color_list:
                        near_color_list.append(cell_1)
                except:
                    pass
                near_color_loss = []
                for _cell in near_color_list:
                    loss = np.square(int(cell[0]) - int(_cell[0])) + np.square(
                        int(cell[1]) - int(_cell[1])) + np.square(int(cell[2]) - (_cell[2]))
                    near_color_loss.append(loss)
                color_index = np.argmin(near_color_loss)
                resize_img[x][y] = near_color_list[color_index]
            else:
                color_index = np.argmin(color_loss)
                resize_img[x][y] = color_value_list[color_index]
    resize_img = cv2.cvtColor(resize_img.astype(np.uint8), cv2.COLOR_RGB2BGR)
    cv2.imwrite(save_path, resize_img)


if __name__ == "__main__":
    img_files = glob.glob(r"G:\xin.data\new_sample\val_gt\res/*.tif")
    for img_file in img_files:
        file_name = img_file[img_file.rindex("\\") + 1:]
        img_file = img_file.replace("\\", "/")

        print img_file
        extract_object_plus_plus(img_file, r"G:\xin.data\new_sample\val_gt\extract_objects")
        # img_interpolation(img_file, r"G:\xin.data\new_sample\val_gt\res"+"/"+file_name)


