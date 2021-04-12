import operator
import cv2
import os
import numpy as np
import glob
from shutil import copy2

from multiprocessing import Pool
from pathlib import Path
from itertools import repeat
from scipy.ndimage import binary_fill_holes
from skimage.measure import regionprops, label


lower_thr = 190
upper_thr = 170

COLOR_OPTIONS = {
    'red'    :  [ '>', upper_thr,  '<', lower_thr, '<', lower_thr],
    'green'  : [ '<', lower_thr,  '>', upper_thr, '<', lower_thr],
    'blue'   :  [ '<', lower_thr,  '<', lower_thr, '>', upper_thr],
    'cyan'   : [ '<', lower_thr,  '>', upper_thr, '>', upper_thr],
    'yellow' :  [ '>', upper_thr,  '>', upper_thr, '<', lower_thr]
}

    
def seperate_train_val_test(new_directory, data_folder_list, val_percentage = 15, test_percentage = 15):

    Path(new_directory).mkdir(parents=True, exist_ok=True)

    train_dir = os.path.join(new_directory, 'train')
    val_dir = os.path.join(new_directory, 'val')
    test_dir = os.path.join(new_directory, 'test')

    save_dir_ = [train_dir,
                 val_dir,
                 test_dir
                 ]

    for dir_ in save_dir_:
        Path(dir_).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(dir_, 'annot')).mkdir(parents=True, exist_ok=True)
        Path(os.path.join(dir_, 'annot_coco')).mkdir(parents=True, exist_ok=True)

    for data_folder in data_folder_list:

        im_dir = glob.glob(os.path.join(data_folder, '*.jpg')) + glob.glob(os.path.join(data_folder, '*.JPG'))

        num_org_image = len(im_dir)
        num_val = int(len(im_dir) * val_percentage / 100)
        num_test = int(len(im_dir) * test_percentage / 100)

        train_idx = np.zeros((num_org_image - num_val - num_test, 1))
        val_idx = np.ones((num_val, 1))
        test_idx = np.ones((num_test, 1)) * 2

        img_idx = np.vstack((train_idx, val_idx))
        img_idx = np.vstack((img_idx, test_idx))

        # Suffle the order of train / val / test
        np.random.shuffle(img_idx)
        np.random.shuffle(img_idx)

        img_idx = img_idx.astype(int)

        org_img_dir = glob.glob(os.path.join(data_folder, '*.jpg')) + glob.glob(os.path.join(data_folder, '*.JPG'))

        for count, img_ in enumerate(org_img_dir):  # To - do : Add multi threading here

            img_name = os.path.splitext(os.path.basename(img_))[0]
            annot_dir_color = glob.glob(os.path.join(data_folder, 'annot', img_name + '*.jpg'))
            annot_dir_bin = glob.glob(os.path.join(data_folder, 'annot_coco', img_name + '*.png'))

            save_dir = save_dir_[img_idx[count][0]]
            copy2(img_, save_dir)

            for annot_img in annot_dir_color:
                copy2(annot_img, os.path.join(save_dir, 'annot'))

            for annot_img in annot_dir_bin:
                copy2(annot_img, os.path.join(save_dir, 'annot_coco'))

def distribute_files(count, data_folder, img_dir, save_dir_, img_idx):
    img_name = os.path.splitext(os.path.basename(img_dir))[0]
    annot_dir_color = glob.glob(os.path.join(data_folder, 'annot', img_name + '*.jpg'))
    annot_dir_bin = glob.glob(os.path.join(data_folder, 'annot_coco', img_name + '*.png'))

    save_dir = save_dir_[img_idx[count][0]]
    copy2(img_dir, save_dir)

    for annot_img in annot_dir_color:
        copy2(annot_img, os.path.join(save_dir, 'annot'))

    for annot_img in annot_dir_bin:
        copy2(annot_img, os.path.join(save_dir, 'annot_coco'))
        
        
def color_to_binary_annotation(layer_img, training_option, bbox_size) :
    
    # annotation area should be assigned according to the designated color.
    
    # run through color options
    
    for option_ in training_option:
        annot_color = option_['annot_color']
        COLOR_OPTION = COLOR_OPTIONS[annot_color]

        R = comparison_operator(layer_img[:, :, 0], COLOR_OPTION[1], COLOR_OPTION[0])
        G = comparison_operator(layer_img[:, :, 1], COLOR_OPTION[3], COLOR_OPTION[2])
        B = comparison_operator(layer_img[:, :, 2], COLOR_OPTION[5], COLOR_OPTION[4])

        damage_area = (R & G & B)
        damage_area = np.asarray(damage_area, dtype = np.uint8)
        # damage_area = damage_area*255 

        labels, _ = label(damage_area, connectivity=2, return_num=True)

        dmg_type = option_['damage_type']
        
        for R in regionprops(labels):
            
            # fill area if an object is hollow
            if option_['fill_void'] == True and R.area:
                damage_area = binary_fill_holes(damage_area).astype('uint8') # * 255
                
            if option_['dilate'] > 0 and R.area:
                kernel = np.ones((option_['dilate'],option_['dilate']),np.uint8)
                damage_area = cv2.dilate(damage_area, kernel, iterations = 1).astype('uint8') # * 255
                
            # if annotation style is overlap or seperate, divide the object
            if option_['bbox_type'] == 'overlap' or option_['bbox_type'] == 'seperate':

                r_min, c_min, r_max, c_max = R.bbox[0], R.bbox[1], R.bbox[2], R.bbox[3]
                r_length, c_length = r_max - r_min, c_max - c_min
                
                if np.max([r_length, c_length]) > bbox_size :
                    if r_length > c_length:
                        num_seg = int(np.floor(r_length / bbox_size)) + 1
                        w_width = int(np.floor(r_length / num_seg))

                        if option_['bbox_type'] == 'overlap':
                            stepSize = int(np.floor(w_width / 2)) - 1
                        elif option_['bbox_type'] == 'seperate':
                            stepSize = int(np.floor(w_width))
                        
                        annot_seg_list = []

                        for y in range(r_min, r_max - w_width, stepSize):
                            annot_seg = np.zeros(np.asarray(damage_area).shape[:2], dtype='uint8')
                            annot_seg[y:y + w_width, c_min:c_max] = damage_area[y:y + w_width, c_min:c_max]
                            annot_seg_list.append(annot_seg)  
                            
                        annot_seg_stack = np.stack(annot_seg_list) 

                        return (np.transpose(annot_seg_stack, (1, 2, 0)), dmg_type)

                    else:
                        num_seg = int(np.floor(c_length / bbox_size)) + 1
                        w_width = int(np.floor(c_length / num_seg))

                        if option_['bbox_type'] == 'overlap':
                            stepSize = int(np.floor(w_width / 2)) - 1
                        elif option_['bbox_type'] == 'seperate':
                            stepSize = int(np.floor(w_width))

                        annot_seg_list = []
                        
                        for x in range(c_min, c_max - w_width, stepSize):
                            annot_seg = np.zeros(np.asarray(damage_area).shape[:2], dtype='uint8')
                            annot_seg[r_min:r_max, x:x + w_width] = damage_area[r_min:r_max, x:x + w_width]
                            annot_seg_list.append(annot_seg)  
                            
                        annot_seg_stack = np.stack(annot_seg_list) 
                        
                        return (np.transpose(annot_seg_stack, (1, 2, 0)), dmg_type)

                else:

                    return (damage_area[:, :, np.newaxis], dmg_type)


            elif option_['bbox_type'] == 'normal':

                return (damage_area[:, :, np.newaxis], dmg_type)


def image_size_normalization(im_dir, shorter_axis_length = 1024):
    # name and files have to be os.walk variable

    img = imread(im_dir)

    if shorter_axis_length != np.min(img.shape[:2]):
        if img.shape[0] > img.shape[1]:
            width = int(img.shape[0] * shorter_axis_length / img.shape[1] )
            height= shorter_axis_length
        else:
            width = shorter_axis_length
            height = int(img.shape[1] * shorter_axis_length / img.shape[0])

        dim = (height, width)
        imwrite(im_dir,cv2.resize(img, dim))


    else :
        print('Image is not resized since image shape is ', img.shape)
