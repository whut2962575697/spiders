# -*- encoding:utf-8 -*-
from libtiff import TIFF
import glob
import numpy as np
import cv2

cls_color = {
    0: (0,0,255),
    1: (0,255,0),
    2:(255,0,0),
    3:(0,0,0)
}


def colouring(in_path, out_path):
    img_files = glob.glob(in_path+"/*.tif")
    for img_file in img_files:
        img_name = img_file[img_file.rindex("\\")+1:]

        img = TIFF.open(img_file)
        img = img.read_image(img)
        nrows = img.shape[0]
        ncols = img.shape[1]
        img_size = max(nrows, ncols)
        print (img_name, img_size)
        new_img = np.zeros([img_size, img_size, 3])
        for i, row in enumerate(img):
            for j, cell in enumerate(row):
                if cls_color.has_key(cell):
                    new_img[i][j] = cls_color[cell]
                else:
                    new_img[i][j] = (0,0,0)
        cv2.cvtColor(new_img.astype(np.uint8), cv2.COLOR_RGB2BGR)
        cv2.imwrite(out_path+"/"+img_name, new_img)


if __name__ == "__main__":
    colouring(r'G:\xin.data\new_sample\RESD', r'G:\xin.data\new_sample\resd_new')