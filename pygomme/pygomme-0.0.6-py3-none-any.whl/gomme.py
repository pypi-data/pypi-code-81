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
    def label(self, value):
        if not isinstance(value, str):
            raise TypeError("Label must be a string object.")
        self._label = value
    
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string object.")
        self._title = value
    
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
    
    def cache_clear(self):
        self.data.cache_clear()
        self.average.cache_clear()
        self.deviation.cache_clear()
        
    @lru_cache
    def average(self,n=n_def):
        avg = np.average(self.data(n))
        return avg
      
    @lru_cache
    def deviation(self,n=n_def):
        std = np.std(self.data(n),ddof=1)
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
    
    def data(self, n=None):
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
    def data(self, n=n_def):
        if np.isscalar(self.value) :
            size = (n,)
        else:
            m = len(self.value)
            size = (n,m)
        if self.distribution == np.random.uniform :
            self.__data = np.random.uniform(self.value-self.half_width,
                                            self.value+self.half_width,
                                            size=size)
            pass
        if self.distribution == np.random.normal :
            self.__data = np.random.normal(self.value,
                                           scale=self.scale,
                                           size=size)
            pass
        if self.distribution == np.random.triangular :
            self.__data = np.random.triangular(self.value-self.half_width,
                                                  self.value,
                                                  self.value+self.half_width,
                                                  size=size)
            pass
        return self.__data
    
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
    def data(self, n=n_def):
        self.scale = self.precision_digit + self.precision_relative*self.value
        self.half_width = self.scale/np.sqrt(3)
        self.__data = np.random.uniform(self.value-self.half_width,
                                        self.value+self.half_width,
                                        size=n)
        return self.__data
      
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
    
    @lru_cache
    def data(self,n=n_def):
        if self.partial is None:
            datas = [arg.data(n) for arg in self.argument]
        else :
            datas = [arg.value for arg in self.argument]
            datas[self.partial] = self.argument[self.partial].data(self.n_sim)
        
        self.__data = self.function(*datas) 
        return self.__data
    
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
        data_x = self.x.data(self.n)
        data_y = self.y.data(self.n)
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
            ax_histx.hist(self.x.data(self.n)[:,i],
                          bins='rice',
                          color="blue",
                          )
            ax_histy.hist(self.y.data(self.n)[:,i],
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
 
class CoefficientLinearFit(MeasureB):
    def __init__(self, 
                 a=np.zeros(1),
                 b=np.zeros(1),
                 a_label=" ",
                 b_label=" ",
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

        ax.set_xlabel(r'${la}$'.format(la=self.a_label))
        ax.set_ylabel(r'${la}$'.format(la=self.b_label))
        
        #ax_histx.set_title(self.title)
        
        
        ax.scatter(self.a,self.b,color='blue')
        
        ax_histx.hist(self.a,bins='rice',color="blue",)
        ax_histy.hist(self.b,color="blue",bins='rice',
                          orientation='horizontal')
   
        if file is not None:
            fig.savefig(file)
        else :
            plt.show()
        plt.close()
        return
   
    
    
if __name__ == "__main__":
    pass
    
