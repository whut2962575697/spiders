import os
from skimage.io import imread
import shutil

image_file = r'G:\xin.data\new_sample\val_gt\extract_objects'
save_file = r'G:\xin.data\new_sample\val_gt\rename_extract_objects'
filelist = os.listdir(image_file)
for img in filelist:
    image_class = ''
    img_path = image_file + '\\'+img
    image = imread(img_path)
    for i in range(image.shape[0]):
        if image_class == '':
            for j in range(image.shape[1]):
                rgb = tuple(image[i][j])
                if image_class != (0,0,0):
                    if rgb == (128, 0, 0):
                        image_class = 'road'
                    elif rgb == (0, 255, 0):
                        image_class = 'residence'
                    elif rgb == (128, 128, 0):
                        image_class = 'industry'
                    elif rgb == (0, 0, 128):
                        image_class = 'greenland'
                    elif rgb == (128, 0, 128):
                        image_class = 'uncompleted'
                    elif rgb == (0, 128, 128):
                        image_class = 'forest'
                    elif rgb == (128, 128, 128):
                        image_class = 'playground'
                    elif rgb == (64, 0, 0):
                        image_class = 'waterbody'
                    elif rgb == (192, 0, 0):
                        image_class = 'village'
                    elif rgb == (64, 128, 0):
                        image_class = 'service'
                    elif rgb == (64, 128, 128):
                        image_class = 'other'
                    elif rgb == (64, 0, 128):
                        image_class = 'farmland'
                    else:
                        continue
                    break
                else:
                    continue
        else:
            break
    for num in range(0,10):
        new_name = img.split('_')[0] + '_' + image_class + '_' + str(num) + '.tif'
        new_img_path = save_file + '\\'+ new_name
        if os.path.exists(new_img_path):
            continue
        else:
            shutil.copy(img_path, new_img_path)
            break