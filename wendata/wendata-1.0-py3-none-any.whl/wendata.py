import numpy as np

class wendata():

    def cal_ret_an(self, ret_da):
        array_ret = np.array(ret_da)
        return array_ret.sum() / len(array_ret) * 360

    def cal_std_an(self, ret_da):
        array_ret = np.array(ret_da)
        return array_ret.std() * (360 ** (1/2))

    def cal_sharp_an(self,ret_da):
        return self.cal_ret_an(ret_da)/self.cal_std_an(ret_da)