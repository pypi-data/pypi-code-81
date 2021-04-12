import numpy as np 
import datetime
import glob
import os 
import json
import argparse

from psd_tools import PSDImage
from pycococreatortools import pycococreatortools
from tqdm import tqdm
from cv2 import resize
from pathlib import Path

from utils import imwrite, comparison_operator, color_to_binary_annotation


'''
 Setting annotation options 
 1. [damage type, annotation color, overlap type, filling void area ] # overlapping is not allowed for panoptic segmentation 
 2. set training data folder to be used 
 3. set num of train / val / test images 
 
'''

parser = argparse.ArgumentParser()
parser.add_argument("--psd-dir")
args = parser.parse_args()

PSD_DIR = args.psd_dir

CONVERSION_OPTIONS = [
    { 
        'damage_type' : 'crack',
        'supercategory' : 'concrete_damage',
        'annot_color' : 'red',
        'bbox_type' : 'overlap',
        'fill_void' : True, 
        'dilate'    : 0,
        
    },
    { 
        'damage_type' : 'effl',
        'supercategory' : 'concrete_damage',
        'annot_color' : 'green',
        'bbox_type' : 'normal',
        'fill_void' : True, 
        'dilate'    : 0,

    },
{ 
        'damage_type' : 'rebar',
        'supercategory' : 'concrete_damage',
        'annot_color' : 'cyan',
        'bbox_type' : 'normal',
        'fill_void' : True,
        'dilate'    : 0,

    },
{ 
        'damage_type' : 'spll',
        'supercategory' : 'concrete_damage',
        'annot_color' : 'yellow',
        'bbox_type' : 'normal',
        'fill_void' : True,
        'dilate'    : 0,
    },
]
    
DATA_TYPE = 'train'

CATEGORIES = []

for opt_num, conversion_opt in enumerate(CONVERSION_OPTIONS) :
    category = {} 
    category['id'] = opt_num  # coco dataset starts id from 1
    category['name'] = conversion_opt['damage_type']
    category['supercategory'] = conversion_opt['supercategory']
    
    CATEGORIES.append(category)
    

INFO = {
    "description": "Concrete Damage Dataset",
    "version": "0.1.0",
    "year": 2018,
    "contributor": "StringBottle",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]


lower_thr = 190
upper_thr = 170

COLOR_OPTIONS = {
    'red'    :  [ '>', upper_thr,  '<', lower_thr, '<', lower_thr],
    'green'  : [ '<', lower_thr,  '>', upper_thr, '<', lower_thr],
    'blue'   :  [ '<', lower_thr,  '<', lower_thr, '>', upper_thr],
    'cyan'   : [ '<', lower_thr,  '>', upper_thr, '>', upper_thr],
    'yellow' :  [ '>', upper_thr,  '>', upper_thr, '<', lower_thr]
}


coco_output = {
"info": INFO,
"licenses": LICENSES,
"categories": CATEGORIES,
"images": [],
"annotations": []
}

image_id = 1
segmentation_id = 1

JSON_SAVE_DIR = os.path.join(PSD_DIR, 'annotations')
Path(JSON_SAVE_DIR).mkdir(parents=True, exist_ok=True)

IMG_SAVE_DIR = os.path.join(PSD_DIR, '{}2018'.format(DATA_TYPE))
Path(IMG_SAVE_DIR).mkdir(parents=True, exist_ok=True)

psd_list = glob.glob(os.path.join(PSD_DIR, '*.psd'))


# run through all psd files 
for psd_filepath in tqdm(psd_list) : 
    
    psd = PSDImage.open(psd_filepath)
    (lyr_width, lyr_height) = psd.size 
    
    image_filename = os.path.splitext(os.path.basename(psd_filepath))[0] + '.jpg'
    image_info = pycococreatortools.create_image_info(
        image_id, image_filename, psd.size) 
    coco_output["images"].append(image_info)
    
    
    # run through each layer
    for layer_num in range(len(psd)):
        layer_name = psd[layer_num].name
        (lyr_left, lyr_top, lyr_right, lyr_bottom) = psd[layer_num].bbox
        psd[layer_num].visible = True
        
        
        # Check if a layer is background or contains object
        if ('Background' in layer_name) or ('배경' in layer_name) :
            
            # If a layer is background save the image in train folder 
            layer_img = np.array(psd[layer_num].composite())[:,:,:3] # from PIL image to np array
            imsave_filepath = os.path.join(IMG_SAVE_DIR, image_filename)
            imwrite(imsave_filepath, layer_img) 
            
            
        # if a layer contains an object
        elif lyr_right > 0 : 
            
            # convert the object information to coco json format 
            layer_img = np.ones((lyr_height, lyr_width, 3), dtype = np.uint8)*255
            layer_part = np.array(psd[layer_num].composite())[:,:,:3]
            
            # error exception 
            if (layer_part.shape[0] > lyr_height) or (layer_part.shape[1] > lyr_width):
                resize_height = layer_img[lyr_top:lyr_bottom, lyr_left:lyr_right, :].shape[0]
                resize_width = layer_img[lyr_top:lyr_bottom, lyr_left:lyr_right, :].shape[1]
                layer_part = resize(layer_part,
                                    dsize=(resize_width, resize_height))
            
        
            layer_img[lyr_top:lyr_bottom, lyr_left:lyr_right, :] = layer_part
            
            
            # create binary masks from the color annotations in layer 
            binary_masks, damage_type = color_to_binary_annotation(layer_img, CONVERSION_OPTIONS)
        
            class_id = [x['id'] for x in CATEGORIES if x['name'] in damage_type][0]
            category_info = {'id': class_id, 'is_crowd': 0}
            
            # convert binary mask to coco json format 
            for num in range(binary_masks.shape[2]) : 
                binary_mask = binary_masks[:, :, num]      

                annotation_info = pycococreatortools.create_annotation_info(
                    segmentation_id, image_id, category_info, binary_mask,
                     psd.size, tolerance=2)

                if annotation_info is not None:
                    coco_output["annotations"].append(annotation_info)

                segmentation_id = segmentation_id + 1

    image_id = image_id + 1
    

with open('{}/instances_{}2018.json'.format(JSON_SAVE_DIR, DATA_TYPE), 'w') as output_json_file:
    json.dump(coco_output, output_json_file)

