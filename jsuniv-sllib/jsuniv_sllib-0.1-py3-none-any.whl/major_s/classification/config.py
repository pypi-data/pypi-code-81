import torch

# dict_label = {"airplane": 0, "automobile": 1, "bird": 2, "cat": 3, "deer": 4,"dog": 5,
#               "frog": 6, "horse": 7, "ship": 8, "truck": 9}
# 1.dict_label:类别对应表
dict_label = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4,"5": 5,
              "6": 6, "7": 7, "8": 8, "9": 9}  # 如果改了分类目标，这里需要修改

# 2.batchsize：批次大小
batchsize = 8

# 3.num_epoch：训练轮次，一般默认200
num_epoch = 200

# 学习率
learning_rate = 0.01

# 4.crop_size:裁剪尺寸
crop_size = (32, 32)

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
path_saved_model = None


# 保存间隔
saved_interval = 10

# 11.path_test_model : 测试模型的路径
path_test_model = None

# 12.path_predict_model : predict模型的路径
path_predict_model = None

# 13.指定设备
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

# 14.（norm_mean，norm_std）：数据集的均值和标准差
norm_mean = [0.33424968,0.33424437, 0.33428448]
norm_std = [0.24796878, 0.24796101, 0.24801227]

# 15.model:模型的选择
model = None
# model = ResNet34(num_classes=10, num_linear=512)

# 类别字符串
classes = ["airplane", "automobile", "bird", "cat", "deer","dog", "frog", "horse", "ship", "truck"]

# 用于模型的可视化
input_size = (3,32,32)