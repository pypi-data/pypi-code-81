import numpy as np
import torch
from models import Darknet
from utils import torch_utils


def test_sparsity(model):

    # --------------------- total sparsity --------------------
    total_zeros = 0
    total_nonzeros = 0

    for name, weight in model.named_parameters():
        if (len(weight.size()) == 4):# and "shortcut" not in name):  # only consider conv layers
            zeros = np.sum(weight.cpu().detach().numpy() == 0)
            total_zeros += zeros
            non_zeros = np.sum(weight.cpu().detach().numpy() != 0)
            total_nonzeros += non_zeros

    comp_ratio = float((total_zeros + total_nonzeros)) / float(total_nonzeros)

    print("ONLY consider CONV layers: ")
    print("total number of zeros: {}, non-zeros: {}, zero sparsity is: {:.4f}".format(
        total_zeros, total_nonzeros, total_zeros / (total_zeros + total_nonzeros)))
    print("only consider conv layers, compression rate is: {:.4f}".format(
        (total_zeros + total_nonzeros) / total_nonzeros))
    print("===========================================================================\n\n")
    return comp_ratio




if __name__ == '__main__':
    print("Check Dense model: ")
    model = Darknet(cfg = 'cfg/csdarknet53s-panet-spp.cfg',img_size=(320,320))
    n_po, macso = torch_utils.model_info(model, verbose=False)
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', type=str, default='weights/best8x-514.pt', help='initial weights path')
    opt = parser.parse_args()

    print("Check 8x prunned model: ")
    state_dict = torch.load('weights/{}'.format(opt.weights))
    model.load_state_dict(state_dict["model"])
    n_p8x, macs8x = model.prunedinfo()
    print("parameters compression rate: %g, flops compression rate: %g" % (n_po/n_p8x, macso/macs8x)) ##flops=2*macs
    test_sparsity(model)
