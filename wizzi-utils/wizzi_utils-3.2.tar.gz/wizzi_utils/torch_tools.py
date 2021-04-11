import torch
import numpy as np
from wizzi_utils import misc_tools as mt  # misc tools


# import torchvision


def cuda_on():
    """ check if cuda available """
    return torch.cuda.is_available()


def set_cuda_scope_and_seed(seed: int, dtype='FloatTensor'):
    """
    :param seed: setting torch seed and default torch if cuda on
    :param dtype:
        https://pytorch.org/docs/stable/tensors.html
        32-bit floating point: torch.cuda.FloatTensor
        64-bit floating point: torch.cuda.DoubleTensor
    :return:
    """
    mt.set_seed(seed)
    if cuda_on():
        def_dtype = 'torch.cuda.' + dtype
        torch.set_default_tensor_type(def_dtype)
        torch.cuda.manual_seed(seed)
        print('working on CUDA. default dtype = {} <=> {}'.format(def_dtype, torch.get_default_dtype()))
    else:
        torch.manual_seed(seed)
        print('working on CPU')
    return


def add_cuda(var: torch.Tensor) -> torch.Tensor:
    """ assigns the variables to GPU if available"""
    if cuda_on() and not is_cuda(var):
        var = var.cuda()
    return var


def is_trainable(var: torch.Tensor) -> bool:
    return var.requires_grad


def is_cuda(var: torch.Tensor) -> bool:
    return var.is_cuda


def size_s(var: torch.Tensor) -> str:
    """
    :param var:
    :return: clean str of tensor size
    e.g. torch.Size([1, 3, 29]) -> [1, 3, 29]
    """
    size_str = str(var.size())
    size_str = size_str[size_str.find("(") + 1:size_str.find(")")]
    return size_str


def total_size(t: torch.Tensor, ignore_first=True) -> int:
    """ e.g. t.size() = (2,3,4).
        if ignore_first True: return 3*4=12
        else                         2*3*4=24
    """
    total = 1
    my_shape = t.shape[1:] if ignore_first else t.shape
    for d in my_shape:
        total *= d
    return total


def torch_to_numpy(var_torch: torch.Tensor) -> np.array:
    if is_trainable(var_torch):
        var_np = var_torch.detach().cpu().numpy()
    else:
        var_np = var_torch.cpu().numpy()
    return var_np


def numpy_to_torch(var_np: np.array, to_double=True, detach: bool = False) -> torch.Tensor:
    """ float is hard coded. if you need double, change the code"""
    if detach:
        if to_double:
            var_torch = add_cuda(torch.from_numpy(var_np).double()).detach()
        else:
            var_torch = add_cuda(torch.from_numpy(var_np).float()).detach()
    else:
        if to_double:
            var_torch = add_cuda(torch.from_numpy(var_np).double())
        else:
            var_torch = add_cuda(torch.from_numpy(var_np).float())
    return var_torch


def to_str(var, title: str, data_chars: int = 100, float_precision: int = 2) -> str:
    """
    :param var: the variable
    :param title: the title (usually variable name)
    :param data_chars: how many char to print.
        -1: none
         0: all
        +0: maximum 'data_chars' (e.g. data_chars=50 and |str(var)|=100 - first 50 chars)
    :param data_chars: how many char to print.
    :param float_precision: round number if possible(float, np array...). 0 for no rounding
    :return: informative string of the variable
    """

    if isinstance(var, torch.Tensor):
        type_s = str(type(var)).replace('<class \'', '').replace('\'>', '')  # clean type name
        string = '{}({},shape={},dtype={},trainable:{},is_cuda:{})'
        string = string.format(title, type_s, size_s(var), var.dtype, is_trainable(var), is_cuda(var))
        if float_precision > 0:
            string += mt.add_data(np.round(var.tolist(), float_precision).tolist(), data_chars, float_precision=0)
        else:
            string += mt.add_data(var.tolist(), data_chars, float_precision=0)
        if len(var.size()) > 0:  # recursive call
            string += '\n\t{}'.format(to_str(var=var[0], title='{}[0]'.format(title), data_chars=data_chars))
    else:  # if it's not Tensor - use the default to_str() from misc_tools
        string = mt.to_str(var, title, data_chars)
    return string


def save_tensor(t, path: str, ack_print: bool = True, tabs: int = 0):
    """
    t: dict or a tensor

    e.g. saving and loading tensor:
        a = torch.ones(size=(2, 3, 29))
        print(to_str(a, 'a'))
        save_tensor(a, path='./a.pt')
        a2 = load_tensor('./a.pt')
        print(to_str(a2, 'a2'))

    e.g. saving and loading tensors dict:
        b = torch.ones(size=(2, 3, 29))
        c = torch.ones(size=(2, 3, 29))
        b_c = {'b': b, 'c': c}
        print(to_str(b_c, 'b_c'))
        save_tensor(b_c, path='./b_c.pt')
        b_c2 = load_tensor('./b_c.pt')
        print(to_str(b_c2, 'b_c2'))
        print(to_str(b_c2['b'], "b_c2['b']"))
        print(to_str(b_c2['c'], "b_c2['c']"))
    """
    torch.save(t, path)
    if ack_print:
        print('{}Saved to: {}'.format(tabs * '\t', path))
    return


def load_tensor(path: str, ack_print: bool = True, tabs: int = 0):
    """ t: dict or a tensor """
    dst_allocation = None if cuda_on() else 'cpu'
    t = torch.load(path, map_location=dst_allocation)
    if ack_print:
        print('{}Loaded: {}'.format(tabs * '\t', path))
    return t


def torch_uniform(shape: tuple, range_low: float, range_high: float) -> torch.Tensor:
    ret = torch.empty(shape).uniform_(range_low, range_high)
    return ret


def torch_normal(shape: tuple, miu: float, std: float) -> torch.Tensor:
    ret = torch.empty(shape).normal_(miu, std)
    return ret


def opt_to_str(optimizer: torch.optim) -> str:
    opt_s = str(optimizer).replace('\n', '').replace('    ', ' ')
    return opt_s


def get_lr(optimizer: torch.optim) -> float:
    lr = None
    if "lr" in optimizer.param_groups[0]:
        lr = optimizer.param_groups[0]['lr']
    return lr


def set_lr(optimizer: torch.optim, new_lr: float) -> None:
    optimizer.param_groups[0]['lr'] = new_lr
    return


def get_opt_by_name(opt_d: dict, params: list) -> torch.optim:
    """
    :param params: trainable params
    :param opt_d: has keys:
        e.g. options:
        {'name'= 'ADAM', 'lr': 0.001, 'weight_decay': 0}
        {'name': 'ADAM', 'lr': 0.001, 'weight_decay': 0.0001}  # L2 regularization
        {'name': 'SGD', 'lr': 0.001, 'momentum': 0.9, 'weight_decay': 0}
        {'name': 'SGD', 'lr': 0.001, 'momentum': 0.9, 'weight_decay': 0.0001} # L2 regularization
    :return:
    """
    opt = None
    if opt_d['name'] == 'ADAM':
        opt = torch.optim.Adam(params, lr=opt_d['lr'], weight_decay=opt_d['weight_decay'])
    elif opt_d['name'] == 'SGD':
        opt = torch.optim.SGD(params, lr=opt_d['lr'], momentum=opt_d['momentum'], weight_decay=opt_d['weight_decay'])
    return opt


class OptimizerHandler:
    """
    example:
    optimizer = torch.optim.Adam(model.parameters(), lr=0.1)
    optimizer = OptimizerHandler(optimizer, factor=0.5, patience=15, min_lr=0.0005)

    for epoch in range(1, n_epochs + 1):
        for x,y in batches:
            y_tag = model(y)
            loss = loss_func(y, y_tag)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        optimizer.update_lr()  # <- this counts the epochs and tries to change the lr
        # update_lr add +1 to counter. if counter >= patience: counter = 0 and new_lr= max(old_lr * factor, min_lr)

    """

    def __init__(self, optimizer: torch.optim, factor: float, patience: int, min_lr: float):
        self.optimizer = optimizer
        self.factor = factor
        self.patience = patience
        self.min_lr = min_lr
        self.epochs_passed = 0

    def step(self):
        self.optimizer.step()
        return

    def lr(self):
        return self.optimizer.param_groups[0]['lr']

    def set_lr(self, new_lr: float):
        self.optimizer.param_groups[0]['lr'] = new_lr
        return

    def zero_grad(self):
        self.optimizer.zero_grad()
        return

    def update_lr(self):
        self.epochs_passed += 1
        if self.epochs_passed >= self.patience:
            self.epochs_passed = 0
            old_lr = self.lr()
            new_lr = max(old_lr * self.factor, self.min_lr)
            self.set_lr(new_lr)
            # print('new lr changed to {}'.format(self.lr()))
        return


class EarlyStopping:
    def __init__(self, patience: int):
        self.patience = patience
        self.counter = 0
        self.best = None
        return

    def should_early_stop(self, loss: float):
        should_stop = False
        if self.best is None:
            self.best = loss
        elif loss < self.best:
            self.best = loss
            self.counter = 0
        else:
            self.counter += 1
            # print('\t\tpatience {}/{}'.format(self.counter, self.patience))
            if self.counter >= self.patience:
                should_stop = True
        return should_stop


def subset_init(c_size: int, A: torch.Tensor, trainable: bool = True) -> torch.Tensor:
    """
        given c_size <= |A|, initialize a tensor C with a random subset of A
    """
    assert c_size <= A.shape[0], 'size cant exceed |A|'
    n = A.shape[0]
    perm = np.random.permutation(n)
    idx = perm[:c_size]
    if A.dtype == 'torch.float64':
        C = A[idx].clone().double()
    elif A.dtype == 'torch.float32':
        C = A[idx].clone().float()
    else:
        C = A[idx].clone()
    C.requires_grad_(trainable)
    return C


def augment_x_y_torch(X: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    """ creates A=X|y """
    assert X.shape[0] == y.shape[0], 'row count must be the same'
    if len(X.shape) == 1:  # change x size()=[n,] to size()=[n,1]
        X = X.view(X.shape[0], 1)
    if len(y.shape) == 1:  # change y size()=[n,] to size()=[n,1]
        y = y.view(y.shape[0], 1)
    A = torch.cat((X, y), 1)
    return A


def de_augment_torch(A: torch.Tensor) -> (torch.Tensor, torch.Tensor):
    """ creates X|y=A """
    assert 0 < len(A.shape) <= 2, 'supports 2d only'
    if len(A.shape) == 1:  # A is 1 point. change from size (n) to size (1,n)
        A = A.view(1, A.shape[0])
    X, y = A[:, :-1], A[:, -1]
    if len(X.shape) == 1:  # change x size()=[n,] to size()=[n,1]
        X = X.view(X.shape[0], 1)
    if len(y.shape) == 1:  # change y size()=[n,] to size()=[n,1]
        y = y.view(y.shape[0], 1)
    return X, y


def split_tensor(Q: torch.Tensor, p: float = 0.9) -> (torch.Tensor, torch.Tensor):
    partition = int(p * Q.shape[0])
    Q_1 = Q[:partition]
    Q_2 = Q[partition:]
    return Q_1, Q_2


def shuffle_tensor(arr: torch.Tensor) -> torch.Tensor:
    """ shuffles an array """
    if isinstance(arr, torch.Tensor):
        arr = arr[torch.randperm(arr.shape[0])]
    return arr


def count_keys(y):
    """
    @:param y: nx1 array (torch, list, numpy)
    e.g.
        from torchvision import datasets
        # data_root = path to the data else download
        dataset = datasets.MNIST(root=data_root, train=False, download=False)
        count_keys(dataset.targets)
    """
    from collections import Counter
    if hasattr(y, "shape"):
        y_shape = y.shape
    else:
        y_shape = len(y)
    print('Count classes: (y shape {})'.format(y_shape))
    cnt = Counter()
    for value in y:
        ind = value.item() if isinstance(y, torch.Tensor) else value
        cnt[ind] += 1
    cnt = sorted(cnt.items())
    for item in cnt:
        print('\tClass {}: {} samples'.format(item[0], item[1]))
    return


def get_torch_version() -> str:
    string = '* PyTorch Version {}'.format(torch.__version__)
    return string


def main():
    a = torch.ones(size=(100, 3))
    a[0][0] = 10000.121215
    print(to_str(a, 'a', data_chars=100, float_precision=3))
    return


if __name__ == '__main__':
    main()

# def data_set_size_to_str(ds: torchvision.datasets) -> str:
#     ds_len = len(ds)
#
#     x = ds.data[0]  # load 1st sample as data loader will load
#     X_size_post_tr = (ds_len,)
#     for d in x.shape:
#         X_size_post_tr += (d,)
#
#     y_size = (len(ds.targets),)  # real data
#     res = '|X|={}, |y|={}'.format(X_size_post_tr, y_size)
#     return res
#
#
# import torch.nn as nn
#
#
# def model_params_print(model: nn.Module, print_values: bool = False, max_samples: int = 2):
#     """
#     :param model: nn model with self.title member
#     :param print_values: print vars values as a list
#     :param max_samples: if print_values: prints first 'max_samples' as a list
#     :return:
#     """
#     print('{}:'.format(model.title))
#     msg = '\t{:15s}: {:10s} ({:7} params), trainable:{}, is_cuda:{}'
#     sum_params = 0
#     for name, param in model.named_parameters():
#         layer_params = 1
#         for d in param.shape:
#             layer_params *= d
#         sum_params += layer_params
#         print(msg.format(name, size_s(param), layer_params, is_trainable(param), is_cuda(param)))
#         if print_values:
#             print('\t\tvalues: {}'.format(param[min(max_samples, param.shape[0])].tolist()))
#     print('\tTotal {:,.0f} params'.format(sum_params))
#     return
#
#
# def model_summary_to_string(model: nn.Module, input_size: tuple, batch_size: int) -> str:
#     """
#         get model info to string
#         e.g.
#             m = MnistModel()
#             print(utils.model_summary_to_string(m, (1, 28, 28), 64))
#     """
#     from torchsummary import summary
#     a, b = redirect_std_start()
#     summary(model, input_size, batch_size)
#     return redirect_std_finish(a, b)
#
#
# def model_params_count(model: nn.Module) -> int:
#     total_parameters = 0
#     for p in list(model.parameters()):
#         total_parameters += tensor_total_size(p, False)
#     return total_parameters
#
#
# def save_model(model: nn.Module, ack_print: bool = True, tabs: int = 0):
#     """ nn model with self.title and self.path members """
#     torch.save(model.state_dict(), model.path)
#     if ack_print:
#         print('{}{} saved to {}'.format(tabs * '\t', model.title, model.path))
#     return
#
#
# def load_model(model: nn.Module, ack_print: bool = True, tabs: int = 0):
#     """ nn model with self.title and self.path members """
#     dst_allocation = None if cuda_on() else 'cpu'
#     model.load_state_dict(torch.load(model.path, map_location=dst_allocation))
#     model.eval()
#     if ack_print:
#         print('{}{} loaded from {}'.format(tabs * '\t', model.title, model.path))
#     return
#
#
# def set_model_status(model: nn.Module, status: bool, status_print: bool = False):
#     """ set model parameters trainable status to 'status' """
#     for param in model.parameters():
#         param.requires_grad_(status)
#     if status_print:
#         print(model_status_str(model))
#     return
#
#
# def model_status_str(model: nn.Module) -> str:
#     """
#     3 options: model fully trainable, fully frozen, both
#     model has self.title
#     """
#     saw_trainable, saw_frozen = 0, 0
#     for param in model.parameters():
#         if is_trainable(param):
#             saw_trainable = 1
#         else:
#             saw_frozen = 1
#     ans = saw_trainable + saw_frozen
#     if ans == 2:
#         msg = '{} is part trainable and part frozen'.format(model.title)
#     elif saw_trainable == 1:
#         msg = '{} is fully trainable'.format(model.title)
#     else:
#         msg = '{} is fully frozen'.format(model.title)
#     return msg
#
#
# def copy_models(model_source: nn.Module, model_target: nn.Module, dont_copy_layers: list, ack: bool = False):
#     """
#     :param model_source: copy from
#     :param model_target: copy to
#     :param dont_copy_layers: list of exact names as appear in model.named_parameters()[0]
#            make sure before coping that dst and target tensors are in the same size
#     :param ack: prints copy\not
#     :return:
#     """
#     print('Copying model {} to model {} except {}:'.format(model_source.title, model_target.title, dont_copy_layers))
#     for name, param in model_source.named_parameters():
#         if name in dont_copy_layers:
#             if ack:
#                 print('\tNOT copied Layer {}'.format(name))
#         else:
#             if ack:
#                 print('\tCopied Layer {}'.format(name))
#             model_target.state_dict()[name].copy_(param)
#             # print('\t\tvalues orig   : {}'.format(param.tolist()))
#             # print('\t\tvalues coreset: {}'.format(model_coreset.state_dict()[name].tolist()))
#             # print('\t\tvalues coreset: {}'.format(model_coreset.state_dict()[name].tolist()))
#     return
#
#
# def freeze_layers(model: nn.Module, trainable_layers: list):
#     """
#     trainable_layers: list of exact names as appear in model.named_parameters()[0]
#     all params that are in trainable_layers -> trainable = True
#     else -> trainable = False
#     """
#     print('Model {}: freezing all except {}:'.format(model.title, trainable_layers))
#     for name, param in model.named_parameters():
#         if name in trainable_layers:
#             param.requires_grad_(True)
#             # print('alive {}'.format(name))
#         else:
#             param.requires_grad_(False)
#             # print('frozen {}'.format(name))
#     return
#
#
# def clone_model(model: nn.Module):
#     import copy
#     model_clone = copy.deepcopy(model)
#     return model_clone
#
#
# def shuffle_ds(ds: torchvision.datasets):
#     """
#     by ref
#     :param ds:
#     :return:
#     """
#     n = ds.targets.shape[0]
#     perm = torch.randperm(n)
#     ds.targets = ds.targets[perm]
#     ds.data = ds.data[perm]
#     return
