import argparse
import sys

sys.path.append("..")
import os
import xml.etree.ElementTree as ET

from tqdm import tqdm

import deeplite_torch_zoo.src.objectdetection.configs.voc_config as cfg


def parse_voc_annotation(data_path, file_type, anno_path, use_difficult_bbox=False):
    """
    解析 pascal voc数据集的annotation, 表示的形式为[image_global_path xmin,ymin,xmax,ymax,cls_id]
    :param data_path: 数据集的路径 , 如 D:\doc\data\VOC\VOCtrainval-2007\VOCdevkit\VOC2007
    :param file_type: 文件的类型， 'trainval''train''val'
    :param anno_path: 标签存储路径
    :param use_difficult_bbox: 是否适用difficult==1的bbox
    :return: 数据集大小
    """
    classes = cfg.DATA["CLASSES"]
    img_inds_file = os.path.join(data_path, "ImageSets", "Main", file_type + ".txt")
    with open(img_inds_file, "r") as f:
        lines = f.readlines()
        image_ids = [line.strip() for line in lines]

    excluded = 0
    with open(anno_path, "a") as f:
        for image_id in tqdm(image_ids):
            image_path = os.path.join(data_path, "JPEGImages", image_id + ".jpg")
            annotation = image_path
            label_path = os.path.join(data_path, "Annotations", image_id + ".xml")
            root = ET.parse(label_path).getroot()
            objects = root.findall("object")
            has_smt = False
            for obj in objects:
                difficult = obj.find("difficult").text.strip()
                if (not use_difficult_bbox) and (
                    int(difficult) == 1
                ):  # difficult 表示是否容易识别，0表示容易，1表示困难
                    continue
                bbox = obj.find("bndbox")
                name = obj.find("name").text.lower().strip()
                if name not in classes:
                    continue
                has_smt = True
                # class_id = classes.index(obj.find("name").text.lower().strip())
                class_id = classes.index(name)
                xmin = bbox.find("xmin").text.strip()
                ymin = bbox.find("ymin").text.strip()
                xmax = bbox.find("xmax").text.strip()
                ymax = bbox.find("ymax").text.strip()
                annotation += " " + ",".join([xmin, ymin, xmax, ymax, str(class_id)])
            annotation += "\n"
            # print(annotation)
            if has_smt:
                f.write(annotation)
            else:
                excluded = excluded + 1
    return len(image_ids) - excluded


def prepare_data(vockit_data_root, data_root_annotation):
    print("Preparing VOC dataset for YOLO. Onetime process...")
    # train_set :  VOC2007_trainval 和 VOC2012_trainval
    train_data_path_2007 = os.path.join(vockit_data_root, "VOC2007")
    train_data_path_2012 = os.path.join(vockit_data_root, "VOC2012")
    train_annotation_path = os.path.join(
        str(data_root_annotation), "train_annotation.txt"
    )
    if os.path.exists(train_annotation_path):
        os.remove(train_annotation_path)

    # val_set   : VOC2007_test
    test_data_path_2007 = os.path.join(vockit_data_root, "VOC2007")
    test_annotation_path = os.path.join(
        str(data_root_annotation), "test_annotation.txt"
    )
    if os.path.exists(test_annotation_path):
        os.remove(test_annotation_path)

    len_train = parse_voc_annotation(
        train_data_path_2007,
        "trainval",
        train_annotation_path,
        use_difficult_bbox=False,
    ) + parse_voc_annotation(
        train_data_path_2012,
        "trainval",
        train_annotation_path,
        use_difficult_bbox=False,
    )
    len_test = parse_voc_annotation(
        test_data_path_2007, "test", test_annotation_path, use_difficult_bbox=False
    )

    print(
        "The number of images for train and test are :train : {0} | test : {1}".format(
            len_train, len_test
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--vockid_path",
        type=str,
        default="/neutrino/datasets/VOCdevkit/",
        help="VOCKIT path",
    )
    parser.add_argument(
        "--annotation_path", type=str, default="../data", help="Annotation data path"
    )
    args = parser.parse_args()

    prepare_data(args.vockid_path, args.annotation_path)
