import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.colors as mcolors
from functools import cached_property,lru_cache

from .functions import _histogram_report,_histogram_compare,_gaussian

plt.rcParams['axes.formatter.use_locale'] = True

n_def = int(1e5)

class Quantity:
    
    def __init__(self,
                 label="",
                 title="",
                 color="gray",
                 ):
        self.label = label
        self.title = title
        self.color = color
        return
    
    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, val):
        if not isinstance(val, str):
            raise TypeError("'label' must be a string object.")
        self._label = val
    
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, val):
        if not isinstance(val, str):
            raise TypeError("'title' must be a string object.")
        self._title = val
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, val):
        if not isinstance(val, str):
            raise TypeError("Color must be a string object.")
        if val not in {**mcolors.BASE_COLORS,
                       **mcolors.TABLEAU_COLORS,
                       **mcolors.CSS4_COLORS}:
            raise ValueError("""Color must be a valid matplotlib color.
                Visit :
                https://matplotlib.org/stable/gallery/color/named_colors.html
                for more informations.
                """)
        
        self._color = val
    
    def cache_clear(self):
        self.samples.cache_clear()
        self.average.cache_clear()
        self.deviation.cache_clear()
        
    @lru_cache
    def average(self,n=n_def):
        avg = np.average(self.samples(n))
        return avg
      
    @lru_cache
    def deviation(self,n=n_def):
        std = np.std(self.samples(n),ddof=1)
        return std
    
    def __sub__(self, other):
        z = ((self.average() - other.average())
            / np.sqrt(self.deviation()**2 + other.deviation()**2))
        return np.abs(z)
    
    def __floordiv__(self, other):
        return Compare(A=self,B=other)
    
    def pretty_print(self,n=n_def):
        avg = self.average(n)
        std = self.deviation(n)
        na = np.floor(np.log10(np.abs(avg)))
        if std != 0:
            ns = np.floor(np.log10(std))
            if abs(na) > 2 :
                avg *= 10**(-na)
                std *= 10**(-na)
                wa = int(na-ns +1)
                ws = wa
                pp = r"$({a:.{wa}f} \pm {s:.{ws}f})\times 10^{{{e:}}}$".format(a=avg,s=std,e=int(na),wa=wa,ws=ws)
            else :
                wa = int(-ns +1)
                ws = wa
                pp = "${a:.{wa}f} \pm {s:.{ws}f}$".format(a=avg,s=std,wa=wa,ws=ws)
        else:
            pp = "${a}$".format(a=avg)
        return pp.replace(".","{,}")
    
    def __str__(self):
        n = n_def
        avg = self.average(n)
        std = self.deviation(n)
        na = np.floor(np.log10(np.abs(avg)))
        if std != 0:
            ns = np.floor(np.log10(std))
            if abs(na) > 2 :
                avg *= 10**(-na)
                std *= 10**(-na)
                wa = int(na-ns +1)
                ws = wa
                pp = "({a:.{wa}f} ± {s:.{ws}f})x10^{e:}".format(a=avg,s=std,e=int(na),wa=wa,ws=ws)
            else :
                wa = int(-ns +1)
                ws = wa
                pp = "{a:.{wa}f} ± {s:.{ws}f}".format(a=avg,s=std,wa=wa,ws=ws)
        else:
            pp=str(avg)
        return pp.replace(".",",")
    
    def histogram(self, 
                  n=n_def, file=None,
                  gaussian=False,
                  ):
        plt.clf()
        fig, ax = plt.subplots()
        _histogram_report(ax,self,n,gaussian=gaussian)
 
        if file is not None:
            fig.savefig(file)
        else :
            plt.show()
        plt.close()
        return

class Reference(Quantity):
    def __init__(self,value=0 ,
                 *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.value = value
        return    
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if not isinstance(val, (int,float)):
            raise TypeError("Value must be a float or an int object.")
        self._value = val
    
    def average(self,n=None):
        return self.value
        
    def deviation(self,n=None):
        return 0
    
    def samples(self, n=None):
        return self.value*np.ones(n)
    
class MeasureB(Quantity):
    
    def __init__(self,
                 value=0,
                 half_width=0,
                 scale=0,
                 distribution=None,
                 color="cornflowerblue",
                 *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.value = value
        self.half_width = half_width
        self.scale = scale
        self.distribution = distribution
        self.color = color
        return  
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self.cache_clear()
        if not isinstance(val, (int,float,np.ndarray)):
            raise TypeError("'value' must be a 'float' or an 'int' or 'numpy.array' object.")
        self._value = val
        
    @property
    def half_width(self):
        return self._half_width

    @half_width.setter
    def half_width(self, val):
        self.cache_clear()
        if not isinstance(val, (int,float,np.ndarray)):
            raise TypeError("'half_width' must be a 'float' or an 'int' or 'numpy.array' object. ")
        if isinstance(val, (int,float,)):
            if val <0 :
                raise ValueError("""'half_width' must be positive.
                    {} is not a valid value for a distribution scale.
                    """.format(val))
        if isinstance(val, (np.ndarray,)):
            if val.all() <0 :
                raise ValueError("""'half_width' must be positive.
                    {} is not a valid value for a distribution scale.
                    """.format(val))
        self._half_width = val

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, val):
        self.cache_clear()
        if not isinstance(val, (int,float,np.ndarray)):
            raise TypeError("'scale' must be a 'float' or an 'int' or 'numpy.array' object.")
        if isinstance(val, (int,float,)):
            if val <0 :
                raise ValueError("""'scale' must be positive.
                    {} is not a valid value for a distribution scale.
                    """.format(val))
        if isinstance(val, (np.ndarray,)):
            if val.all() <0 :
                raise ValueError("""'scale' must be positive.
                    {} is not a valid value for a distribution scale.
                    """.format(val))
        self._scale = val

    @property
    def distribution(self):
        return self._distribution

    @distribution.setter
    def distribution(self, val):
        self.cache_clear()
        if (not callable(val)) & (val is not None):
            raise TypeError("""distribution must be either:
                a numpy function
                or set to 'None'""")
        self._distribution = val

    @lru_cache
    def samples(self, n=n_def):
        if np.isscalar(self.value) :
            size = (n,)
        else:
            m = len(self.value)
            size = (n,m)
        if self.distribution == np.random.uniform :
            self.__samples = np.random.uniform(self.value-self.half_width,
                                            self.value+self.half_width,
                                            size=size)
            pass
        if self.distribution == np.random.normal :
            self.__samples = np.random.normal(self.value,
                                           scale=self.scale,
                                           size=size)
            pass
        if self.distribution == np.random.triangular :
            self.__samples = np.random.triangular(self.value-self.half_width,
                                                  self.value,
                                                  self.value+self.half_width,
                                                  size=size)
            pass
        return self.__samples
    
class MeasureA(MeasureB):
    def __init__(self, 
                 experimental_data=np.zeros(1),
                 distribution=np.random.normal,
                 color = "mediumslateblue",
                 *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.experimental_data = experimental_data
        self.distribution = distribution
        self.color = color
        self.compute_parameters()
    
    @property
    def experimental_data(self):
        return self._experimental_data

    @experimental_data.setter
    def experimental_data(self, val):
        self.cache_clear()
        if not isinstance(val, (list,np.ndarray)):
            raise TypeError("'experimental_data' must be a 'numpy.array' object or a list.")
        self._experimental_data = val
        self.compute_parameters()
    
    def compute_parameters(self):
        self.value = np.average(self.experimental_data)
        self.scale = np.std(self.experimental_data,ddof=1)
        self.half_width = self.scale*np.sqrt(3) 
            
    def histogram(self, 
                  n=n_def, file=None,
                  gaussian=False,
                  ):
        fig = plt.figure(figsize=(8.27, 11.69), 
                         dpi=300,
                         tight_layout=True)
        gs = GridSpec(2, 2, figure=fig)
        
        axB = fig.add_subplot(gs[1, :])
        _histogram_report(axB,self,n,gaussian=gaussian)
            
        axT = fig.add_subplot(gs[0, :], sharex=axB)
        _histogram_report(axT,self,n,gaussian=gaussian,experimental=True)
        
       
        fig.align_xlabels()
 
        if file is not None:
            fig.savefig(file)
        else :
            plt.show()
        plt.close()

        
class MeasureMultimeter(Quantity):
    
    def __init__(self,value=0,
                 precision_digit=0,
                 precision_relative=0,
                 *args, **kwargs) :
        super().__init__(*args, **kwargs)
        self.value = value
        self.precision_digit = precision_digit
        self.precision_relative = precision_relative
        self.distribution = np.random.uniform
        self.color = "salmon"
        return    
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self.cache_clear()
        if not isinstance(val, (int,float,np.ndarray)):
            raise TypeError("'value' must be a 'float' or an 'int' or 'numpy.array' object.")
        self._value = val
        
    @property
    def precision_digit(self):
        return self._precision_digit

    @precision_digit.setter
    def precision_digit(self, val):
        self.cache_clear()
        if not isinstance(val, (int,float,np.ndarray)):
            raise TypeError("'precision_digit' must be a 'float' or an 'int' or 'numpy.array' object.")
        if isinstance(val, (int,float,)):
            if val <0 :
                raise ValueError("""'precision_digit' must be positive.
                    {} is not a valid value for a distribution scale.
                    """.format(val))
        if isinstance(val, (np.ndarray,)):
            if val.all() <0 :
                raise ValueError("""'precision_digit' must be positive.
                    {} is not a valid value for a distribution scale.
                    """.format(val))
        self._precision_digit = val   
    
    @property
    def precision_relative(self):
        return self._precision_relative

    @precision_relative.setter
    def precision_relative(self, val):
        
        self.cache_clear()
        if not isinstance(val, (int,float,np.ndarray)):
            raise TypeError("'precision_relative' must be a 'float' or an 'int' or 'numpy.array' object.")
        if isinstance(val, (int,float,)):
            if val <0 :
                raise ValueError("""'precision_relative' must be positive.
                    {} is not a valid value for a distribution scale.
                    """.format(val))
        if isinstance(val, (np.ndarray,)):
            if val.all() <0 :
                raise ValueError("""'precision_relative' must be positive.
                    {} is not a valid value for a distribution scale.
                    """.format(val))
        self._precision_relative = val   
    
    
    
    @lru_cache
    def samples(self, n=n_def):
        self.scale = self.precision_digit + self.precision_relative*self.value
        self.half_width = self.scale/np.sqrt(3)
        self.__samples = np.random.uniform(self.value-self.half_width,
                                        self.value+self.half_width,
                                        size=n)
        return self.__samples
      

class Compare(Quantity):
    
    def __init__(self, A=None, B=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.A = A
        self.B = B
        return   
    
    def report(self,file=None, n=n_def,*args, **kwargs):
        
        fig, ax = plt.subplots(figsize=(8, 6))
        #fig = plt.figure(figsize=(8, 6), 
                         #dpi=300,
                         #tight_layout=True)
        
        
        _histogram_compare(ax, self.A, self.B, n)
        
        if file is not None:
            fig.savefig(file)
        else :
            plt.show()
        plt.close()
        return
    
if __name__ == "__main__":
    pass
    
