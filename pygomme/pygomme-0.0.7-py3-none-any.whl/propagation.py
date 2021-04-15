import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.colors as mcolors
from functools import cached_property,lru_cache

from .functions import _histogram_report,_histogram_compare,_gaussian
from .gomme import *


class Propagation(Quantity):
    
    def __init__(self, function=None,
                 argument=None,
                 n_sim = n_def,
                 partial=None,
                 color = "goldenrod",
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.function = function
        self.argument = argument
        self.n_sim = n_sim
        self.color = color
        self.partial = partial
        return   
    
    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, val):
        if not callable(val):
            raise TypeError("""'function' must be either:
                a numpy function
                or set to 'None'""")
        self._function = val
    
    @property
    def argument(self):
        return self._argument

    @argument.setter
    def argument(self, val):
        self._argument = val
        
    @property
    def n_sim(self):
        return self._n_sim

    @n_sim.setter
    def n_sim(self, val):
        if not isinstance(val,int):
            raise TypeError("'n_sim' must be an 'integer'.")
        if val<=0:
            raise ValueError("'n_sim' must be positive.")
        self._n_sim = val
    
    @property
    def partial(self):
        return self._partial

    @partial.setter
    def partial(self, val):
        #if not isinstance(val,int):
            #raise TypeError("'partial' must be an 'integer'.")
        #if val<=0:
            #raise ValueError("'partial' must be positive.")
        self._partial = val
    
    @lru_cache
    def samples(self,n=n_def):
        if self.partial is None:
            s = [arg.samples(n) for arg in self.argument]
        else :
            s = [arg.value for arg in self.argument]
            s[self.partial] = self.argument[self.partial].samples(self.n_sim)
        
        self.__samples = self.function(*s) 
        return self.__samples
    
    def report(self,file=None,gaussian=False):
        fig = plt.figure(figsize=(8.27, 11.69), 
                         dpi=300,
                         tight_layout=True)
        n_arg = len(self.argument)
        
        gs = GridSpec((n_arg+1)//2+1, 2, figure=fig)
        
        for i,arg in enumerate(self.argument) :
            axT = fig.add_subplot(gs[i//2, i%2])
            _histogram_report(axT,arg,self.n_sim,gaussian=gaussian)
            
        axF = fig.add_subplot(gs[-1, :])
        _histogram_report(axF,self,self.n_sim,gaussian=gaussian)
        
        if file is not None:
            fig.savefig(file)
        else :
            plt.show()
        plt.close()
        return
    
    def report_partial(self,file=None,gaussian=False):
        fig = plt.figure(figsize=(8.27, 11.69), 
                         dpi=300,
                         tight_layout=True)
        n_arg = len(self.argument)
        
        gs = GridSpec(n_arg+1, 2, figure=fig)
        
        axT = fig.add_subplot(gs[-1, :])
        _histogram_report(axT, self, self.n_sim, gaussian=gaussian)
        
        ax = []
     
        for i,arg in enumerate(self.argument) :
            Q = Propagation(label=self.label,
                    title="{} -> {}".format(self.argument[i].title, self.title),
                    function=self.function,
                    argument=self.argument,
                    n_sim=self.n_sim,
                    partial=i,
                    color="mediumseagreen")
            ax.append(fig.add_subplot(gs[i, :], sharex=axT))
            _histogram_report(ax[i], Q, self.n_sim, gaussian=gaussian)
            
        fig.align_xlabels(ax)

        if file is not None:
            fig.savefig(file)
        else :
            plt.show()
        plt.close()
        return   
    
    def histogram(self, 
                  file=None,
                  gaussian=False,
                  ):
        plt.clf()
        fig, ax = plt.subplots()
        _histogram_report(ax,self,self.n_sim,gaussian=gaussian)
 
        if file is not None:
            fig.savefig(file)
        else :
            plt.show()
        plt.close()
        return
    
