# -*- encoding:utf-8 -*-

from libtiff import TIFF
import cv2
from config import small_label_color
import glob


def determine_big_object(sentence, big_scale_img, img_id, s_objects_path):
    subsentences = sentence.split("with")
    for subsentence in subsentences:
        words = subsentence.split(" ")
        class_words = dict()
        for word in words:
            if word in small_label_color.keys():
                class_words[word] = 2
            s_obs = glob.glob(s_objects_path + "/" + img_id + "_" + word + "*.tif")
            if len(s_obs) == 0:
                return False
            elif len(s_obs) == 1:
                pass





