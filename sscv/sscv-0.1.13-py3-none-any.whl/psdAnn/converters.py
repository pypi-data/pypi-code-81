import numpy as np
import os
import glob
import json
import re
import cv2
import fnmatch
import datetime

from PIL import Image
from scipy.ndimage import binary_fill_holes
from skimage.measure import regionprops, label
from pycococreatortools import pycococreatortools
from utils import imread, imwrite, comparison_operator

lower_thr = 190
upper_thr = 190

COLOR_OPTIONS = {
    'red'    :  [ '>', upper_thr,  '<', lower_thr, '<', lower_thr],
    'green'  : [ '<', lower_thr,  '>', upper_thr, '<', lower_thr],
    'blue'   :  [ '<', lower_thr,  '<', lower_thr, '>', upper_thr],
    'cyan'   : [ '<', 180,  '>', 200, '>', 200],
    'yellow' :  [ '>', 200,  '>', 200, '<', 180]
}

INFO = {
    "description": "Example Dataset",
    "url": "https://github.com/waspinator/pycococreator",
    "version": "0.1.0",
    "year": 2018,
    "contributor": "waspinator", "StringBottle"
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

def filter_for_jpeg(root, files):
    file_types = ['*.jpeg', '*.jpg', '*.JPG']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    return files

def filter_for_annotations(root, files, image_filename):
    file_types = ['*.png']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    basename_no_extension = os.path.splitext(os.path.basename(image_filename))[0]
    file_name_prefix = basename_no_extension + '.*'
    print(file_name_prefix)
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    files = [f for f in files if re.match(file_name_prefix, os.path.splitext(os.path.basename(f))[0])]
    return files

def binary_to_json_annotation_main(DIR, training_option):

    IMAGE_DIR = os.path.join(DIR)
    ANNOTATION_DIR = os.path.join(DIR, "annot_coco")

    CATEGORIES = []
    class_idx = {}

    for idx,  each_option in enumerate(training_option) :

        class_idx[each_option['damage_type']] = idx

        CATEGORIES.append({
            'id': idx,
            'name': each_option['damage_type'],
            'supercategory': 'concrete_damage',
        })

    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }

    image_id = 1
    segmentation_id = 1
    depth = 1

    # filter for jpeg images
    for root, _, files in os.walk(IMAGE_DIR):
        if root[len(IMAGE_DIR):].count(os.sep) < depth:

            image_files = filter_for_jpeg(root, files)
            # go through each image
            # Multi-threading has to be added here.
            for image_filename in image_files:
                image = Image.open(image_filename)
                image_info = pycococreatortools.create_image_info(
                    image_id, os.path.basename(image_filename), image.size)
                coco_output["images"].append(image_info)

                # filter for associated png annotations
                for root, _, files in os.walk(ANNOTATION_DIR):
                    annotation_files = filter_for_annotations(root, files, image_filename)

                    # go through each associated annotation
                    for annotation_filename in annotation_files:

                        for CATEGORIES_ in CATEGORIES :
                            if CATEGORIES_['name'] in annotation_filename : class_id = CATEGORIES_['id']

                        category_info = {'id': class_id, 'is_crowd': 'crowd' in image_filename}
                        binary_mask = np.asarray(Image.open(annotation_filename)
                                                 .convert('1')).astype(np.uint8)

                        annotation_info = pycococreatortools.create_annotation_info(
                            segmentation_id, image_id, category_info, binary_mask,
                            image.size, tolerance=2)

                        if annotation_info is not None:
                            coco_output["annotations"].append(annotation_info)

                        segmentation_id = segmentation_id + 1

                image_id = image_id + 1

        with open('{}/instances_concrete_damage_train2018.json'.format(DIR), 'w') as output_json_file:
            json.dump(coco_output, output_json_file)


def binary_to_json_annotation(ROOT_DIR, training_option, SUB_DIRS = None ):

    # extract CATEGORIES from training_option
    # The input root_dir has to have at least one of train / val / test
    # Then IMAGE_DIR and ANNOTATION_DIR can be created from root_dir

    # ROOT_DIR = binary_to_json_annotation_main

    # SUB_DIRS = [
    #     os.path.join(ROOT_DIR, 'train'),
    #     os.path.join(ROOT_DIR, 'val'),
    #     os.path.join(ROOT_DIR, 'test'),
    # ]
    if SUB_DIRS :
        for DIR_ in SUB_DIRS:
            binary_to_json_annotation_main(DIR_, training_option)

    elif not SUB_DIRS :
        binary_to_json_annotation_main(ROOT_DIR, training_option)




# def color_to_binary_annotation(data_folder_list, img_, training_option) :

#     annot_dir = os.path.join(data_folder_list, 'annot')
#     img_name = os.path.splitext(os.path.basename(img_))[0]
#     annot_name = glob.glob(os.path.join(annot_dir, img_name + '*.jpg'))

#     for annot_idx, annot_name_ in enumerate(annot_name):
#         annot_img = imread(annot_name_)

#         # annotation area should be assigned according to the designated color.
#         for option_ in training_option:
#             annot_color = option_['annot_color']
#             COLOR_OPTION = COLOR_OPTIONS[annot_color]
#             kernel = np.ones((2, 2), np.uint8)

#             R = comparison_operator(annot_img[:, :, 0], COLOR_OPTION[1], COLOR_OPTION[0])
#             G = comparison_operator(annot_img[:, :, 1], COLOR_OPTION[3], COLOR_OPTION[2])
#             B = comparison_operator(annot_img[:, :, 2], COLOR_OPTION[5], COLOR_OPTION[4])

#             damage_area = (R & G & B)
#             damage_area = np.asarray(damage_area, dtype = np.uint8)
#             damage_area = cv2.dilate(damage_area, kernel, iterations=1)  # // make damage_area dilated
#             damage_area = damage_area*255

#             labels, _ = label(damage_area, connectivity=2, return_num=True)

#             damage_type = option_['damage_type']

#             for R in regionprops(labels):
#                 if option_['fill_void'] == True and R.area:
#                     damage_area = binary_fill_holes(damage_area).astype('uint8') * 255

#                 if option_['bbox_type'] == 'overlap' or option_['bbox_type'] == 'seperate':

#                     r_min, c_min, r_max, c_max = R.bbox[0], R.bbox[1], R.bbox[2], R.bbox[3]
#                     r_length, c_length = r_max - r_min, c_max - c_min

#                     if np.max([r_length, c_length]) > 256:
#                         if r_length > c_length:
#                             num_seg = int(np.floor(r_length / 256)) + 1
#                             w_width = int(np.floor(r_length / num_seg))

#                             if option_['bbox_type'] == 'overlap':
#                                 stepSize = int(np.floor(w_width / 2)) - 1
#                             elif option_['bbox_type'] == 'seperate':
#                                 stepSize = int(np.floor(w_width))

#                             n = 0
#                             for y in range(r_min, r_max - w_width, stepSize):
#                                 n = n + 1
#                                 annot_coco_dir = os.path.join(data_folder_list, 'annot_coco', img_name + '_' + damage_type + '_'
#                                                               + str(annot_idx) + '_' + str(n) + '.png')
#                                 annot_seg = np.zeros(np.asarray(damage_area).shape[:2], dtype='uint8')
#                                 annot_seg[y:y + w_width, c_min:c_max] = damage_area[y:y + w_width, c_min:c_max]
#                                 imwrite(annot_coco_dir, annot_seg)
#                         else:
#                             num_seg = int(np.floor(c_length / 256)) + 1
#                             w_width = int(np.floor(c_length / num_seg))

#                             if option_['bbox_type'] == 'overlap':
#                                 stepSize = int(np.floor(w_width / 2)) - 1
#                             elif option_['bbox_type'] == 'seperate':
#                                 stepSize = int(np.floor(w_width))

#                             n = 0
#                             for x in range(c_min, c_max - w_width, stepSize):
#                                 n = n + 1
#                                 annot_coco_dir = os.path.join(data_folder_list, 'annot_coco', img_name + '_' + damage_type + '_'
#                                                               + str(annot_idx) + '_' + str(n) + '.png')
#                                 annot_seg = np.zeros(np.asarray(damage_area).shape[:2], dtype='uint8')
#                                 annot_seg[r_min:r_max, x:x + w_width] = damage_area[r_min:r_max, x:x + w_width]
#                                 imwrite(annot_coco_dir, annot_seg)

#                     else:
#                         annot_coco_dir = os.path.join(data_folder_list, 'annot_coco', img_name + '_' + damage_type + '_'
#                                                       + str(annot_idx) + '.png')
#                         imwrite(annot_coco_dir, damage_area.astype('uint8'))

#                 elif option_['bbox_type'] == 'normal':
#                     annot_coco_dir = os.path.join(data_folder_list, 'annot_coco', img_name + '_' + damage_type + '_'
#                                                   + str(annot_idx) + '.png')
#                     imwrite(annot_coco_dir, damage_area.astype('uint8'))