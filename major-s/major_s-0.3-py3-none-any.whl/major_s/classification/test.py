from torchsummary import summary
from .config import model,input_size
summary(model,input_size=input_size,device="cpu")