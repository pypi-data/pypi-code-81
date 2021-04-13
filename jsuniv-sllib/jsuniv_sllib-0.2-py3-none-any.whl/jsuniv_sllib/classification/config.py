import torch
import torchvision.transforms as transforms

# dict_label = {"airplane": 0, "automobile": 1, "bird": 2, "cat": 3, "deer": 4,"dog": 5,
#               "frog": 6, "horse": 7, "ship": 8, "truck": 9}
# 1.dict_label:类别对应表
# dict_label = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4,"5": 5,
#               "6": 6, "7": 7, "8": 8, "9": 9}  # 如果改了分类目标，这里需要修改
dict_label = None
def define_for_dict_label():
    return dict_label
# 2.batchsize：批次大小
batchsize = 8

# 3.num_epoch：训练轮次，一般默认200
num_epoch = 200

# 学习率
learning_rate = 0.01

# 4.crop_size:裁剪尺寸
crop_size = None

# 5.训练集的图片路径
train_image = None  # r'./major_dataset_repo/major_collected_dataset/train/image'

# 6.验证集的图片路径
val_image = None

# 7.测试集的图片路径
test_image = None

# 8.待转训练、验证和测试集的数据原文件
dataset_image = None # r'./image'

# 9.数据集划分后保存的路径
split_dataset = None  # r'./split_dataset'

# 划分比例

account_for_dataset = (0.8,0.1,0.1)


# 10.模型的保存路径
path_saved_model = "saved_model"
def define_for_path_saved_model():
    return path_saved_model

# 保存间隔
saved_interval = 10

# 11.path_test_model : 测试模型的路径
path_test_model = "models_for_test"

# 12.path_predict_model : predict模型的路径
path_predict_model = "models_for_predict"

# 13.指定设备
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# 14.（norm_mean，norm_std）：数据集的均值和标准差
norm_mean = [0.33424968,0.33424437, 0.33428448]
norm_std = [0.24796878, 0.24796101, 0.24801227]

# 15.model:模型的选择
model = None
def define_for_model():
    return model
# model = ResNet34(num_classes=10, num_linear=512)

# 类别字符串
# classes = ["airplane", "automobile", "bird", "cat", "deer","dog", "frog", "horse", "ship", "truck"]
classes = None
def define_for_classes():
    return classes

# 用于模型的可视化
def define_for_input_size():
    input_size = (3,crop_size[0],crop_size[1])
    return input_size

# 预处理
# 训练数据预处理

def define_for_train_transform():
    train_transform = transforms.Compose([
        transforms.Resize(crop_size),
        transforms.ToTensor(),
        transforms.Normalize(norm_mean, norm_std),
    ])
    return train_transform

# 验证数据预处理

def define_for_valid_transform():
    valid_transform = transforms.Compose([
        transforms.Resize(crop_size),
        transforms.ToTensor(),
        transforms.Normalize(norm_mean, norm_std),
    ])
    return valid_transform

# 推理数据的预处理
def define_for_inference_transform():
    inference_transform = transforms.Compose([
        transforms.Resize(crop_size),
        transforms.ToTensor(),
        transforms.Normalize(norm_mean, norm_std),
    ])
    return inference_transform