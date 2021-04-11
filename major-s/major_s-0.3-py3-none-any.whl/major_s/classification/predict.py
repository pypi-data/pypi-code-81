import os
import time
from PIL import Image
from . import config
import torch
import torchvision.transforms as transforms
from torchsummary import summary
# 标签和类别的映射关系

# 注意事项
# 1.model.eval()
# 2.torch.no_grad()
# 3.数据预处理保持一致
# 4.预测时间的计算

# 设置net为全局变量，避免网络的重复加载，加速模型推断
net = None

def preprocessing(img,transform = None):
    if transforms is None:
        raise Exception("无transform进行预处理")
    img_tensor = transform(img)
    return img_tensor

def get_model(saved_model_path=config.path_saved_model, visual_model=False, input_size=(3, 32, 32)):
    net = config.model
    net.load_state_dict(torch.load(saved_model_path))
    if visual_model:
        summary(net, input_size=input_size, device="cpu")
    return net

def load_model():
    model_path = config.path_saved_model
    global net
    net = get_model(model_path, False, input_size=(3, 32, 32))
    net.to(config.device)
    net.eval()

def predict_for_singleimg(img_path):
    # 1. data
    # 2. model
    # 3.单图predict
    with torch.no_grad():
        # step 1/4 : path --> img
        img_rgb = Image.open(img_path).convert('RGB')

        # step 2/4 : img --> tensor
        img_tensor = preprocessing(img_rgb, config.define_for_inference_transform())
        img_tensor.unsqueeze_(0)
        img_tensor = img_tensor.to(config.device)

        # step 3/4 : tensor --> vector
        time_start = time.time()
        outputs = net(img_tensor)
        time_end = time.time()
        print("所耗时间：", time_end - time_start)

        # step 4/4 : visualization
        print(outputs)
        _, pred_int = torch.max(outputs, 1)
        print(pred_int)
        pred_str = config.classes[int(pred_int.cuda().data.cpu().numpy())]
        print(pred_str)

def predict_for_directory(path):
    # 1. data
    # 2. model
    # 3.多图预测
    with torch.no_grad():
        # step 1/4 : path --> img
        files_list = os.listdir(path)
        file_path_list = [os.path.join(path, img) for img in files_list]
        for i in range(len(file_path_list)):
            img_rgb = Image.open(file_path_list[i]).convert('RGB')

            # step 2/4 : img --> tensor
            img_tensor = preprocessing(img_rgb,config.define_for_inference_transform())
            img_tensor.unsqueeze_(0)
            img_tensor = img_tensor.to(config.device)

            # step 3/4 : tensor --> vector
            time_start = time.time()
            outputs = net(img_tensor)
            time_end = time.time()
            print("所耗时间：", time_end - time_start)

            # step 4/4 : visualization
            print(outputs)
            _, pred_int = torch.max(outputs, 1)
            print(pred_int)
            pred_str = config.classes[int(pred_int.cuda().data.cpu().numpy())]
            print(pred_str)


if __name__ == "__main__":
    # 1. data
    img_path = r"D:\Classification_Demo\major_dataset_repo\split_data\test\0\0_116.png"
    # 2. model
    model_path = config.path_saved_model
    net = get_model(model_path,False,input_size=(3,32,32))
    net.to(config.device)
    net.eval()
    # 3.单图predict
    with torch.no_grad():
        # step 1/4 : path --> img
        img_rgb = Image.open(img_path).convert('RGB')

        # step 2/4 : img --> tensor
        img_tensor = preprocessing(img_rgb,config.inference_transform)
        img_tensor.unsqueeze_(0)
        img_tensor = img_tensor.to(config.device)

        # step 3/4 : tensor --> vector
        time_start = time.time()
        outputs = net(img_tensor)
        time_end = time.time()

        # step 4/4 : visualization
        print(outputs)
        _,pred_int = torch.max(outputs,1)
        print(pred_int)
        pred_str = config.classes[int(pred_int.cuda().data.cpu().numpy())]
        print(pred_str)

    # 4.多图预测
    with torch.no_grad():
        # step 1/4 : path --> img
        path = r"D:\Classification_Demo\major_dataset_repo\split_data\test\0"
        files_list = os.listdir(path)
        file_path_list = [os.path.join(path, img) for img in files_list]

        for i in range(100):
            img_rgb = Image.open(file_path_list[i]).convert('RGB')

            # step 2/4 : img --> tensor
            img_tensor = preprocessing(img_rgb,config.inference_transform)
            img_tensor.unsqueeze_(0)
            img_tensor = img_tensor.to(config.device)

            # step 3/4 : tensor --> vector
            time_start = time.time()
            outputs = net(img_tensor)
            time_end = time.time()
            print("所耗时间：",time_end - time_start)

            # step 4/4 : visualization
            print(outputs)
            _,pred_int = torch.max(outputs,1)
            print(pred_int)
            pred_str = config.classes[int(pred_int.cuda().data.cpu().numpy())]
            print(pred_str)
