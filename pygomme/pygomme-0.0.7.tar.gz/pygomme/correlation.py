import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.colors as mcolors
from functools import cached_property,lru_cache

from .functions import _histogram_report,_histogram_compare,_gaussian
from .gomme import *

class Correlation_quantity(Quantity):
    def __init__(self,correlation=None,
                 *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.correlation = correlation
        self.correlated_samples = np.zeros(1)
        return 
    
    def samples(self,n=n_def):
        return self.correlated_samples

class Correlation:
    def __init__(self,
                labels=[],
                titles=[],
                keys=[],
                color="gray",
                values=[0,],
                cov=np.zeros((2,2)),
                ):
        self.labels = labels
        self.titles = titles
        self.values = values
        self.keys = keys
        self.cov = cov
        self.color = color
        self.quantity = {}
        for key in keys:
            self.quantity[key] = Correlation_quantity(correlation=self)
        return
    
    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, vals):
        if not isinstance(vals, list):
            raise TypeError("'labels' must be an iterable object.")
        for val in vals:
            if not isinstance(val, str):
                raise TypeError("'label' must be a string object.")
        self._labels = vals
    
    @property
    def titles(self):
        return self._titles

    @titles.setter
    def titles(self, vals):
        if not isinstance(vals, list):
            raise TypeError("'titles' must be an iterable object.")
        for val in vals:
            if not isinstance(val, str):
                raise TypeError("'title' must be a string object.")
        self._titles = vals
    
    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, vals):
        if not isinstance(vals, list):
            raise TypeError("'keys' must be an iterable object.")
        for val in vals:
            if not isinstance(val, str):
                raise TypeError("'key' must be a string object.")
        self._keys = vals
    
    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, vals):
        #self.cache_clear()
        if not isinstance(vals, (list,np.ndarray)):
            raise TypeError("'values' must be an iterable object.")
        for val in vals:
            if not isinstance(val, (int,float,np.float,np.ndarray)):
                raise TypeError("'value' must be a 'float',an 'int' or a 'numpy.ndarray' object.")
        self._values = vals
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise TypeError("Color must be a string object.")
        if value not in {**mcolors.BASE_COLORS,
                         **mcolors.TABLEAU_COLORS,
                         **mcolors.CSS4_COLORS}:
            raise ValueError("""Color must be a valid matplotlib color.
                Visit :
                https://matplotlib.org/stable/gallery/color/named_colors.html
                for more informations.
                """)
        
        self._color = value    
        
    def compute_cov(self):
        l = len(self.keys)
        c = len(self.values[0])
        m = np.zeros((l,c))
        for i in range(l):
            m[i,:] = self.values[i]
        self.cov = np.cov(m,)
        
    def create_samples(self,n=n_def):
        l = len(self.keys)
        c = len(self.values[0])
        means = np.zeros(l)
        for i in range(l):
            means[i] = np.average(self.values[i]) 
        out = np.random.multivariate_normal(means, self.cov,size=n)
        for i in range(l):
            self.quantity[self.keys[i]].correlated_samples = out[:,i]
            
    def scatter(self,x=None,y=None,file=None):
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

        #if self.a_label != "":
            #ax.set_xlabel(r'${la}$'.format(la=self.a_label))
        #if self.b_label != "":    
            #ax.set_ylabel(r'${la}$'.format(la=self.b_label))
        
        #ax_histx.set_title(self.title)
        
        
        ax.scatter(x,y,s=1.5,color='blue')
        
        ax_histx.hist(x,bins='rice',color="blue",)
        ax_histy.hist(y,color="blue",bins='rice',
                          orientation='horizontal')
        
        avg_a = np.average(x)
        std_a = np.std(x)
        avg_b = np.average(y)
        std_b = np.std(y)
        
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
        
