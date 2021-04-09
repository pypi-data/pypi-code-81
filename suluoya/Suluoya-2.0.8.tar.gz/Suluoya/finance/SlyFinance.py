from sympy import *
import numpy as np


class annuity(object):
    def __init__(self, pv=0, rate=0.0083, nper=48, pmt=-2633.30, fv=0, Type=0):
        '''
        年金问题
                
        ◾ Rate 各期利率。 例如，如果您获得年利率为 10% 的汽车贷款，并且每月还款一次，则每月的利率为 10%/12（即 0.83%）。 您需要在公式中输入 0.1/12（即 0.0083） 作为利率。
        
        ◾ Nper 年金的付款总期数。 例如，如果您获得为期四年的汽车贷款，每月还款一次，则贷款期数为 4*12（即 48）期。 您需要在公式中输入 48 作为 nper。
        
        ◾ Pmt  每期的付款金额，在年金周期内不能更改。 通常，pmt 包括本金和利息，但不含其他费用或税金。 例如，对于金额为 ￥100,000、利率为 12% 的四年期汽车贷款，每月付款为 ￥2633.30。 您需要输入 -2633.30 作为 pmt。
        
        ◾ fv   未来值，或在最后一次付款后希望得到的现金余额。 如果省略 fv，则假定其值为 0（例如，贷款的未来值是 0）。 例如，如果要在 18 年中为支付某个特殊项目而储蓄 ￥500,000，则 ￥500,000 就是未来值。 然后，您可以对利率进行保守的猜测，并确定每月必须储蓄的金额。
        
        ◾ Type  0 或 1，用以指定各期的付款时间是在期初还是期末。默认为0即期末。
        '''
        self.pv = pv
        self.rate = rate
        self.nper = nper
        self.pmt = pmt
        self.fv = fv
        self.Type = Type

    @property
    def PV(self):
        pv = Symbol('pv')
        pv = solve((pv*(1+self.rate)**self.nper)+(self.pmt*(1+self.rate*self.Type)
                                                  * (((1+self.rate)**self.nper-1)/self.rate))+self.fv, pv)[0]
        return pv

    @property
    def Rate(self):
        rate = Symbol('rate')
        rate = solve((self.pv*(1+rate)**self.nper)+(self.pmt*(1+rate *
                                                              self.Type)*(((1+rate)**self.nper-1)/rate))+self.fv, rate)[0]
        return rate

    @property
    def Nper(self):
        nper = Symbol('nper')
        nper = solve((self.pv*(1+self.rate)**nper)+(self.pmt*(1+self.rate *
                                                              self.Type)*(((1+self.rate)**nper-1)/self.rate))+self.fv, nper)[0]
        return nper

    @property
    def Pmt(self):
        pmt = Symbol('pmt')
        pmt = solve((self.pv*(1+self.rate)**self.nper)+(pmt*(1+self.rate*self.Type)
                                                        * (((1+self.rate)**self.nper-1)/self.rate))+self.fv, pmt)[0]
        return pmt

    @property
    def FV(self):
        fv = Symbol('fv')
        fv = solve((self.pv*(1+self.rate)**self.nper)+(self.pmt*(1+self.rate *
                                                                 self.Type)*(((1+self.rate)**self.nper-1)/self.rate))+fv, fv)[0]
        return fv


def NPV(rate=0.1, values=[-10000, 3000, 4200, 6800]):
    '''
    使用贴现率和一系列未来支出（负值）和收益（正值）来计算一项投资的净现值。
    
    ◾ rate   年贴现率
    
    ◾ values 一年前的初期投资和每年的收益。注意要按顺序！！！
    '''
    npv = 0
    n = 1
    for i in values:
        npv += i/(1+rate)**n
        n += 1
    return npv



def IRR(values=[-700000, 120000, 150000, 180000, 210000]):
    '''
    返回净现值等于0的贴现率，即内部贴现率
    
    ◾ values 某项业务的初期成本费用（负数）和每年的净收入。注意要按顺序！！！
    '''
    return np.irr(values)



