#  for major_test
import torch
from . import config
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from .dataset import LoadDataset

def evaluteTop1(model, loader):
    model.eval()

    correct = 0
    total = len(loader.dataset)

    for x, y in loader:
        x, y = x.to(config.device), y.to(config.device)
        with torch.no_grad():
            logits = model(x)
            pred = logits.argmax(dim=1)
            correct += torch.eq(pred, y).sum().float().item()
        # correct += torch.eq(pred, y).sum().item()
    return correct / total


def evaluteTop5(model, loader):
    model.eval()
    correct = 0
    total = len(loader.dataset)
    for x, y in loader:
        x, y = x.to(config.device), y.to(config.device)
        with torch.no_grad():
            logits = model(x)
            maxk = max((1, 5))
            y_resize = y.view(-1, 1)
            _, pred = logits.topk(maxk, 1, True, True)
            correct += torch.eq(pred, y_resize).sum().float().item()
    return correct / total

if __name__ == "__main__":
    # 1.加载测试数据
    # 1.1 预处理
    test_transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize(config.norm_mean, config.norm_std),
    ])
    # 1.2 数据加载
    test_data = LoadDataset(data_dir=config.test_image, transform=test_transform)
    test_loader = DataLoader(dataset=test_data, batch_size=config.batchsize, shuffle=True)  # shuffle训练时打乱样本

    # 2.加载模型
    net = config.model  # 对应修改模型 net = se_resnet50(num_classes=5,pretrained=True)
    path_model_state_dict = config.path_test_model
    net.load_state_dict(torch.load(path_model_state_dict))

    # 3.评测
    evaluteTop1(net,test_loader)
    evaluteTop5(net,test_loader)