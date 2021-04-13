import os
import random
from PIL import Image
from torch.utils.data import Dataset
from . import config
random.seed(1)




# 返回所有图片路径和标签
def get_img_label(data_dir):
    # 类别对应表
    dict_label = config.define_for_dict_label()
    img_label_list = list()
    for root, dirs, _ in os.walk(data_dir):
        # 遍历类别
        for sub_dir in dirs:
            img_names = os.listdir(os.path.join(root, sub_dir))
            # img_names = list(filter(lambda x: x.endswith('.png'), img_names))   # 如果改了图片格式，这里需要修改
            # 遍历图片
            for i in range(len(img_names)):
                img_name = img_names[i]
                path_img = os.path.join(root, sub_dir, img_name)
                label = dict_label[sub_dir]
                img_label_list.append((path_img, int(label)))
    return img_label_list

# 主要是用来接受索引返回样本用的
class LoadDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        # 1.获取所有图片的路径、label , 和 2.确定预处理操作
        self.img_label_list = get_img_label(data_dir)  # img_label_list，在DataLoader中通过index读取样本
        self.transform = transform

    #接受一个索引，返回一个样本 ---  img, label
    def __getitem__(self, index):
        path_img, label = self.img_label_list[index]
        img = Image.open(path_img).convert('RGB')     # 0~255
        if self.transform is not None:
            img = self.transform(img)   # 在这里做transform，转为tensor等等
        return img, label

    def __len__(self):
        return len(self.img_label_list)



