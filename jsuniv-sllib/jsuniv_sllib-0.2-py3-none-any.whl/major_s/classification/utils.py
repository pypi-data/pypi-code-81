import random
import numpy as np
import torch
from torchsummary import summary
def set_seed(seed=1):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)


def vis_model(model,inputSize):
    summary(model,input_size=inputSize,device="cpu")

