import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.colors as mcolors
from functools import cached_property,lru_cache

from .functions import _histogram_report,_histogram_compare,_gaussian
from .gomme import *
from .propagation import *

class LinearFit():
    
    def __init__(self, x=None, y=None, n=n_def,
                 *args, **kwargs):
        self.x = x
        self.y = y
        self.n = n
        self.fit()
        return
    
    def fit(self):
        m = len(self.x.value)
        data_x = self.x.samples(self.n)
        data_y = self.y.samples(self.n)
        a = np.empty(self.n)
        b = np.empty(self.n)
        for i in range(self.n):
            serie = np.polynomial.Polynomial.fit(data_x[i,:], 
                                                 data_y[i,:],
                                                 1, 
                                                 domain=None, rcond=None, 
                                                 full=False, w=None, window=None)
            a[i] = serie.convert().coef[1]
            b[i] = serie.convert().coef[0]
            
        self.a = MeasureA(experimental_data=a,
                          color="deepskyblue",
                          distribution=np.random.uniform
                          )
        self.b = MeasureA(experimental_data=b,
                          color="deepskyblue",
                          distribution=np.random.uniform
                          )
        
        self.ab = CoefficientLinearFit(a=a,b=b)
        
    def __str__(self):
        pp = "a={} | b={}".format(str(self.a),str(self.b))
        return pp
    
    def report(self,file=None):
        fig = plt.figure(figsize=(11.69, 8.27))
        gs = fig.add_gridspec(2, 2,  width_ratios=(7, 2), 
                              height_ratios=(2, 7),
                              left=0.1, right=0.9, bottom=0.1, top=0.9,
                              wspace=0.05, hspace=0.05)
        
        ax = fig.add_subplot(gs[1, 0])
        ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
        ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)
        ax_histx.tick_params(axis="x", labelbottom=False)
        ax_histy.tick_params(axis="y", labelleft=False)

        ax.set_xlabel(r'${la}$'.format(la=self.x.label))
        ax.set_ylabel(r'${la}$'.format(la=self.y.label))
        
        ax_histx.set_title(self.x.title)
        ax_histy.set_title(self.y.title)
        
        ax.errorbar(self.x.value,self.y.value,
                    xerr=self.x.scale,yerr=self.y.scale,
                    fmt='+',color='blue')
        left, right = ax.get_xlim()
        down,up = ax.get_ylim()
        x = np.linspace(left,right,2)
        ax.plot(x, self.a.average()*x + self.b.average(),color="red")
        
        a_max = self.a.average() + self.a.deviation()
        a_min = self.a.average() - self.a.deviation()
        b_max = self.b.average() + self.b.deviation()
        b_min = self.b.average() - self.b.deviation()
        ax.fill_between(x, a_max*x + b_max,
                        a_min*x + b_min,
                        alpha=0.2)
        props = dict(boxstyle='square', facecolor='palegreen', alpha=0.9)
        ax.text(0.05, 0.95, 
                "y=ax+b\na={}\nb={}".format(self.a.pretty_print(),self.b.pretty_print()), 
                transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)
        ax.set_xlim([left,right])
        ax.set_ylim([down,up])
        
        for i in range(len(self.x.value)):
            ax_histx.hist(self.x.samples(self.n)[:,i],
                          bins='rice',
                          color="blue",
                          )
            ax_histy.hist(self.y.samples(self.n)[:,i],
                          color="blue",
                          bins='rice',
                          orientation='horizontal',
                          )
        #ax_histy.hist(self.y.data(self.n), bins=n_def)
        
        if file is not None:
            fig.savefig(file)
        else :
            plt.show()
        plt.close()
        return
    
    def report_full(self):
        return
 
class CoefficientLinearFit(Quantity):
    def __init__(self, 
                 a=np.zeros(1),
                 b=np.zeros(1),
                 a_label="",
                 b_label="",
                 distribution=np.random.normal,
                 color = "green",
                 *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.a = a
        self.b = b
        self.a_label = a_label
        self.b_label = b_label
        self.color = color
        
    def scatter(self,file=None):
        fig = plt.figure(figsize=(11.69, 8.27))
        gs = fig.add_gridspec(2, 2,  width_ratios=(7, 2), 
                              height_ratios=(2, 7),
                              left=0.1, right=0.9, bottom=0.1, top=0.9,
                              wspace=0.05, hspace=0.05)
        
        ax = fig.add_subplot(gs[1, 0])
        ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
        ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)
        ax_histx.tick_params(axis="x", labelbottom=False)
        ax_histy.tick_params(axis="y", labelleft=False)

        if self.a_label != "":
            ax.set_xlabel(r'${la}$'.format(la=self.a_label))
        if self.b_label != "":    
            ax.set_ylabel(r'${la}$'.format(la=self.b_label))
        
        #ax_histx.set_title(self.title)
        
        
        ax.scatter(self.a,self.b,s=1.5,color='blue')
        
        ax_histx.hist(self.a,bins='rice',color="blue",)
        ax_histy.hist(self.b,color="blue",bins='rice',
                          orientation='horizontal')
        
        avg_a = np.average(self.a)
        std_a = np.std(self.a)
        avg_b = np.average(self.b)
        std_b = np.std(self.b)
        
        ax.axvline(x=avg_a, color="black", linestyle="--")
        ax.axvline(x=avg_a+std_a, color="blue", linestyle="--")
        ax.axvline(x=avg_a-std_a, color="blue", linestyle="--")
        
        ax_histx.axvline(x=avg_a, color="black", linestyle="--")
        ax_histx.axvline(x=avg_a+std_a, color="blue", linestyle="--")
        ax_histx.axvline(x=avg_a-std_a, color="blue", linestyle="--")
        
        ax.axhline(y=avg_b, color="black", linestyle="--")
        ax.axhline(y=avg_b+std_b, color="blue", linestyle="--")
        ax.axhline(y=avg_b-std_b, color="blue", linestyle="--")
        
        ax_histy.axhline(y=avg_b, color="black", linestyle="--")
        ax_histy.axhline(y=avg_b+std_b, color="blue", linestyle="--")
        ax_histy.axhline(y=avg_b-std_b, color="blue", linestyle="--")
        
        if file is not None:
            fig.savefig(file)
        else :
            plt.show()
        plt.close()
        return
   
    
