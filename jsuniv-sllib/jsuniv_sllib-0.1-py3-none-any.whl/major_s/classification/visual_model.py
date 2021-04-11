from torchsummary import summary

def visual(net,input_size):
    summary(net, input_size=input_size, device="cpu")