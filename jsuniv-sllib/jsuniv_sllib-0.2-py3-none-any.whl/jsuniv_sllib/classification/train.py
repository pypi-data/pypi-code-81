# ============================ 导入工具包包 ============================
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torch.optim as optim
from matplotlib import pyplot as plt
from .utils import set_seed
from . import config
from .dataset import LoadDataset
import os
# ============================ 辅助函数 ============================
set_seed() # 设置随机种子
# ============================ step 0/5 参数设置 ============================
MAX_EPOCH = config.num_epoch
BATCH_SIZE = config.batchsize
LR = config.learning_rate
log_interval = 10
val_interval = 1

train_curve = list()
valid_curve = list()

def makedir(new_dir):
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

# ============================ step 1/5 数据 ============================
def define_for_train_loader():
    # 构建训练集的Dataset和DataLoader
    train_dataset = LoadDataset(data_dir=config.train_image, transform=config.define_for_train_transform())
    train_loader = DataLoader(dataset=train_dataset, batch_size=BATCH_SIZE, shuffle=True)  # shuffle训练时打乱样本
    return train_loader

def define_for_valid_loader():
    # 构建验证集的Dataset和DataLoader
    valid_dataset = LoadDataset(data_dir=config.val_image, transform=config.define_for_valid_transform())
    valid_loader = DataLoader(dataset=valid_dataset, batch_size=BATCH_SIZE)
    return valid_loader

# ============================ step 2/5 模型 ============================
def define_for_net():
    net = config.model  # 对应修改模型 net = se_resnet50(num_classes=5,pretrained=True)
    return net

# ============================ step 3/5 损失函数 ============================
def define_for_criterion():
    criterion = nn.CrossEntropyLoss()                                                   # 选择损失函数
    return criterion

# ============================ step 4/5 优化器 ============================
def define_for_optimizer():
    optimizer = optim.SGD(define_for_net().parameters(), lr=LR, momentum=0.9)                        # 选择优化器
    return optimizer

def define_for_scheduler():
    scheduler = torch.optim.lr_scheduler.StepLR(define_for_optimizer(), step_size=10, gamma=0.1)     # 设置学习率下降策略，每过step_size个epoch，做一次更新
    return scheduler

# ============================ step 5/5 训练 ============================
def run():
    net = define_for_net()
    optimizer = define_for_optimizer()
    train_loader = define_for_train_loader()
    criterion = define_for_criterion()
    scheduler =define_for_scheduler()
    valid_loader =define_for_valid_loader()

    for epoch in range(MAX_EPOCH):
        loss_mean = 0.
        correct = 0.
        total = 0.
        # incorrect=0.
        net.train()

        # 打印当前学习率
        print(optimizer.state_dict()['param_groups'][0]['lr'])
        for i, data in enumerate(train_loader):# 获取数据
            # forward
            inputs, labels = data
            outputs = net(inputs)
            # backward
            optimizer.zero_grad()  # 梯度置零,设置在loss之前
            loss = criterion(outputs, labels)  # 一个batch的loss
            loss.backward()  # loss反向传播
            # update weights
            optimizer.step()  # 更新所有的参数
            # 统计分类情况
            _, predicted = torch.max(outputs.data, 1)  # 1 返回索引的意思
            total += labels.size(0)
            correct += (predicted == labels).squeeze().sum().numpy()  # 计算一共正确的个数
            loss_mean += loss.item()  # 计算一共的loss
            train_curve.append(loss.item())  # 训练曲线，用于显示

            if (i+1) % 10 == 0:   # log_interval=10 表示每迭代10次，打印一次训练信息,在这里bachsize=16 迭代10次就是160张图片，即total=160
                loss_mean = loss_mean / log_interval  # 取平均loss
                print("Training:Epoch[{:0>3}/{:0>3}] Iteration[{:0>3}/{:0>3}] Loss: {:.4f} Acc:{:.2%}".format(
                    epoch, MAX_EPOCH, i+1, len(train_loader), loss_mean, correct / total))
                correct=correct
                total=total   # total=160
                # 保存训练信息，即写日志
                f = open("log_training.txt", 'a')  # 若文件不存在，系统自动创建。'a'表示可连续写入到文件，保留原内容，在原
                # 内容之后写入。可修改该模式（'w+','w','wb'等）
                f.write("Training:Epoch[{:0>3}/{:0>3}] Iteration[{:0>3}/{:0>3}] Loss: {:.4f} Acc:{:.2%}".format(
                    epoch, MAX_EPOCH, i+1, len(train_loader), loss_mean, correct / total))  # 将字符串写入文件中
                f.write("\n")  # 换行
                f.close()
                loss_mean = 0.  # 每次需要清0

        scheduler.step()  # 更新学习率


        # validate the model
        if (epoch+1) % 2 == 0:  # val_interval=1 表示每一个epoch打印一次验证信息
            # 验证一次，保存一次模型
            path_model_state_dict = config.path_saved_model
            makedir(os.path.split(path_model_state_dict)[0])
            torch.save(net.state_dict(), path_model_state_dict)


            correct_val = 0. #  正确值
            total_val = 0.  # 一共的
            loss_val = 0.  # 损失
            net.eval()  # 模型保持静止，不进行更新，从而来验证
            with torch.no_grad():  # 不保存梯度,减少内存消耗，提高运行速度
                for j, data in enumerate(valid_loader):
                    inputs, labels = data
                    outputs = net(inputs)
                    loss = criterion(outputs, labels)
                    _, predicted = torch.max(outputs.data, 1)
                    total_val += labels.size(0)
                    correct_val += (predicted == labels).squeeze().sum().numpy()
                    loss_val += loss.item()
                valid_curve.append(loss_val/valid_loader.__len__())
                print("Valid:\t Epoch[{:0>3}/{:0>3}] Iteration[{:0>3}/{:0>3}] Loss: {:.4f} Acc:{:.2%}".format(
                    epoch, MAX_EPOCH, j+1, len(valid_loader), loss_val, correct_val / total_val))
                f = open("log_training.txt", 'a')  # 若文件不存在，系统自动创建。'a'表示可连续写入到文件，保留原内容，在原
                # 内容之后写入。可修改该模式（'w+','w','wb'等）
                f.write("Valid:\t Epoch[{:0>3}/{:0>3}] Iteration[{:0>3}/{:0>3}] Loss: {:.4f} Acc:{:.2%}".format(
                    epoch, MAX_EPOCH, j+1, len(valid_loader), loss_val, correct_val / total_val))  # 将字符串写入文件中
                f.write("\n")  # 换行
                f.close()

    train_x = range(len(train_curve))
    train_y = train_curve

    train_iters = len(train_loader)
    valid_x = np.arange(1, len(valid_curve)+1) * train_iters*val_interval # 由于valid中记录的是epochloss，需要对记录点进行转换到iterations
    valid_y = valid_curve

    plt.plot(train_x, train_y, label='Train')
    plt.plot(valid_x, valid_y, label='Valid')

    plt.legend(loc='upper right')
    plt.ylabel('loss value')
    plt.xlabel('Iteration')
    plt.show()



