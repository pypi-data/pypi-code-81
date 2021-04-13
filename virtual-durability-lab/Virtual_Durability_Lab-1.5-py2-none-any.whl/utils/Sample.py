# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:26:39 2020

@author: U550787
"""

import numpy as np
import scipy.stats as s
from matplotlib import pyplot as plt

class Sample:
    """
        Probability definition of a sample. 
        
        Parameters
        ----------
        name : string (Optional)
            Name of the sample
            
        model : string
            Name of the damage model choose for the sample 
            Default : None
        
        representation : string
            Choice the representation of the probability law. 
            Choices : 'Random_Variates', 'Cumulative_distribution', 'Probability_density_mass' 
        
        law : string
            Definition of the probility law of the sample.
            Choices : "Exponential", "Uniform", "Weibull", "Lognormal", "Normal"
            
        parm1 : scalar (Optional)
            Default : None
            Parameter to describe the parameter of the following law : 
                Weibull parameter c : shape
                Lognormal parameter s : shape
        
        loc : scalar (Optional)
            Default : 0
            To shift the law.
            f(x, loc, scale) <=> f(y) with y = (x - loc) / scale.
            
        scale : scalar (Optional)
            Default : 1
            To scale the law.
            f(x, loc, scale) <=> f(y) with y = (x - loc) / scale.
            
        save_path : string (Optional)
            Default : None
            Define the save path of the graph generated.
                
        Raises
        ----------
        ValueError
            Law parameter incorrect. You must choose one of the Binomial, Exponential, Poisson, Weibull, Lognormal, Normal laws.
        
        ValueError
            Parameter 'representation' missing or incorrect. Please choose one of these : 'Random_Variates', 'Cumulative_distribution', 'Probability_density'
            
        ValueError
            Parameter size for the generation of Random_variates missing
        
        ValueError
            Law error. The parameter param1 (β) of the law must be superior to 0.
        
        ValueError
            Law error. The parameter scale (η) of the law must be superior to 0.
            
        ValueError
            Law error. The parameter of the law missing.
            
        ValueError
            Law error.  The parameter param1 (σ) of the law must be superior to 0.
        
        ValueError
            Law error. The parameter of the law missing.
        
        ValueError
            Law error. The parameter scale (1/λ) must be superior to O.
        
        ValueError
            Law error.\tThis law isn't available
            
        Methods
        ----------
        sample_definition(self, **kwargs)
        sample_visualization(self, **kwargs)
        param_title_graph(self, **kwargs)
        
        Examples
        ----------
        #Creation of 100 random values for stress sample represented by a Normal law with mean and standard deviation : μ=49000, σ=8000. (Use to define samples)
        sample_1 = Sample(representation="Random_variates", name="Stress", law="Normal", scale=8000, loc=49000, size=7) 
        
        #Creation of the probabilty density function for a Weibull law with beta : β=1.3 . (Use to see theorical representation of pdf)
        sample_2 = Sample(representation="Probability_density", name="Weibull pdf", law="Weibull", param1=1.3)
        
        #Creation of the cumulative distribution for a Lognormal law with. (Use to see theorical representation of cdf)
        sample_3 = Sample(representation="Cumulative_distribution", name="Lognormal cdf", law="Lognormal", param1=1.2)
        
    """
    def __init__(self, **kwargs):
        
        
        self.GRAPH = True
       
        #Population damage model not implemented yet
        self.model = kwargs.get("model", None)
        #Size of the sample
        self.size = kwargs.get("size", None)
        
        self.representation = kwargs.get("representation", None)
        
        law = kwargs.get("law", None)
        self.name = kwargs.get("name", law)
        param1 = kwargs.get("param1", None)
        self.loc = kwargs.get("loc", 0)
        self.scale = kwargs.get("scale", 1)
        
        #Boolean which add Allan PLait Weibull representation when Weibull sample representation is choosen (random variates)
        self.Allan_Plait_representation = False
        
        self.save_path = kwargs.get("save_path", None)
        
        if law not in ["Uniform", "Exponential", "Weibull", "Lognormal", "Normal"]:
            raise ValueError("Law parameter incorrect. You must choose one of the Exponential, Weibull, Uniform, Lognormal, Normal laws.")

        if self.representation not in ['Random_variates', 'Cumulative_distribution', 'Probability_density']:
            raise ValueError("Parameter 'representation' missing or incorrect. Please choose one of these : 'Random_Variates', 'Cumulative_distribution', 'Probability_density'")
        
        if self.representation == 'Random_variates' and not self.size:
            raise ValueError("Parameter size for the generation of Random_variates missing")

        self.law = {"Exponential" : s.expon, "Uniform" : s.uniform, "Weibull" : s.weibull_min, "Lognormal" : s.lognorm, "Normal" : s.norm}[law]
        
        
    
        
        if(law == "Weibull"):
        
            if(param1>0 and self.scale>0):
                
                if (self.loc == 0):
                    self.Allan_Plait_representation = True
    
                self.x = np.linspace(self.law.ppf(0.01, param1, loc=self.loc, scale=self.scale), self.law.ppf(0.99, param1, loc=self.loc, scale=self.scale), 100)
                
                if self.representation == "Random_variates":
                    self.sample_definition(c=param1, loc=self.loc, scale=self.scale, size=self.size)
                else:
                    self.sample_definition(x=self.x, c=param1, loc=self.loc, scale=self.scale)  
                    
                    
            elif(param1<=0):
                raise ValueError(u"Law error. The parameter param1 (β) of the law must be superior to 0.")
            
            elif(self.scale<=0):
                raise ValueError(u"Law error. The parameter scale (η) of the law must be superior to 0.")
            
            else:
                raise ValueError(u"Law error. The parameter of the law missing.")
        
        elif(law == "Lognormal"):
            
            if (param1>0):
                self.x = np.linspace(self.law.ppf(0.01, param1, loc=self.loc, scale=self.scale), self.law.ppf(0.99, param1, loc=self.loc, scale=self.scale), 100)

                if self.representation == "Random_variates":
                    self.sample_definition(s=param1, loc=self.loc, scale=self.scale, size=self.size) 
                else:
                    self.sample_definition(x=self.x, s=param1, loc=self.loc, scale=self.scale) 
            elif (param1<=0):
                raise ValueError("Law error.  The parameter param1 (σ) of the law must be superior to 0.")
            else:
                 raise ValueError("Law error. The parameter of the law missing.")    
            
        elif(law == "Uniform"):
               
            self.x = np.linspace(self.law.ppf(0.01, loc=self.loc, scale=self.scale), self.law.ppf(0.99,loc=self.loc, scale=self.scale), 100)
            if self.representation == "Random_variates":
                self.sample_definition(loc=self.loc, scale=self.scale, size=self.size)
            else:
                self.sample_definition(x=self.x,loc=self.loc, scale=self.scale)
            
        elif(law == "Exponential"):
            
            if(self.scale>0):
                self.x = np.linspace(self.law.ppf(0.01, loc=self.loc, scale=self.scale), self.law.ppf(0.99,loc=self.loc, scale=self.scale), 100)
                if self.representation == "Random_variates":
                    self.sample_definition(loc=self.loc, scale=self.scale, size=self.size)
                else:
                    self.sample_definition(x=self.x,loc=self.loc, scale=self.scale)
            else:
                raise ValueError("Law error. The parameter scale (1/λ) must be superior to O.")
                
        elif(law == "Normal"):
                
            self.x = np.linspace(self.law.ppf(0.01, loc=self.loc, scale=self.scale), self.law.ppf(0.99,loc=self.loc, scale=self.scale), 100)
            if self.representation == "Random_variates":
                self.sample_definition(loc=self.loc, scale=self.scale, size=self.size)
            else:
                self.sample_definition(x=self.x,loc=self.loc, scale=self.scale)
            
        else:
            raise ValueError("Law error.\tThis law isn't available")

    def sample_definition(self, **kwargs):
        
        if self.representation == "Probability_density":
        
            self.sample = self.law.pdf(**kwargs)
        
        elif self.representation == "Cumulative_distribution":
            self.sample = self.law.cdf(**kwargs)    
        
        elif self.representation == "Random_variates":
            self.sample = self.law.rvs(**kwargs)
            
            kwargs.pop("size")
            kwargs["x"]=self.x
            
            self.theorical = self.law.pmf(**kwargs) if kwargs.get("mu",0) or kwargs.get("p",0) else self.law.pdf(**kwargs)
            
        if self.save_path or self.GRAPH: 
                self.sample_visualization(**kwargs)
            
            
    def sample_visualization(self, **kwargs):
        
        self.fig, self.ax = plt.subplots(2, 1) if self.Allan_Plait_representation else plt.subplots(1,1)
        
        if self.representation == "Probability_density":
            
            self.ax.plot(self.x, self.sample, 'r-', lw=2, alpha=0.6, label=str(self.name)+" pdf")
        
        elif self.representation == "Cumulative_distribution":
            self.ax.plot(self.x, self.sample, 'b-', lw=2, alpha=0.6, label=str(self.name)+" cdf")
        
        elif self.representation == "Random_variates":
            
            ax = self.ax[0] if self.Allan_Plait_representation else self.ax 
            ax1 = ax.twinx()
            
            ax.hist(self.sample, histtype='stepfilled', alpha=0.2)
            ax1.plot(self.x, self.theorical, 'r-', lw=2, alpha=0.6, label=str(self.name)+" pdf")
            
            ax1.set_ylabel("Probability density")
            ax.set_ylabel("Occurence number")
            ax.set_xlabel("Quantifiable life measure")
            
            ax.set_title("%s probability density with %s" % (self.name, self.param_title_graph(**kwargs)))
            
            if self.Allan_Plait_representation:
                self.ax[1].plot(np.log(self.x), np.log(-np.log(1 - self.law.cdf(**kwargs))), 'r-', lw=2, alpha=0.6, label="Allan plait weibull representation")
                self.ax[1].set_ylabel("log( -log(1 - F(t)) )")
                self.ax[1].set_xlabel("log(t)")
                self.ax[1].set_yscale('log')
                self.ax[1].set_xscale('log')
                self.ax[1].set_title('Allan Plait representation')

                
        if self.GRAPH:
            plt.tight_layout()
            plt.show()
        
        if self.save_path:
            
            name = "%s\%s.png" % (self.save_path,self.name) if self.name else "%s\sample.png" % self.save_path
            
            self.fig.savefig(name.decode('utf-8'), format='png',bbox_inches='tight')
            
        
    
    def param_title_graph(self, **kwargs):
    
        if self.law == s.expon :
            r = u"λ = %.2f, ϒ = %.2f" %(1/kwargs['scale'], kwargs["loc"])
        elif self.law == s.norm:
            r = u"μ = %.2f, σ = %.2f." % (kwargs["loc"], kwargs["scale"])
        elif self.law == s.lognorm:
            r = u"μ = %.2f, σ = %.2f" % (kwargs["scale"], kwargs["s"])
        elif self.law == s.weibull_min:
            r = u"β = %.2f, η = %.2f, ϒ = %.2f" % (kwargs["c"], kwargs["scale"], kwargs["loc"])
        elif self.law == s.uniform:
            r = u"intervall of [%.2f; %.2f]" % (kwargs["loc"], kwargs["loc"]+kwargs["scale"])

        return r 
    
class TestSample:
    """
        Sample Class tests
    
        Parameters
        ----------
        
        Raises
        ----------
 
        Methods
        ----------

    """
    def __init__(self):
        return
    
    
if __name__ == "__main__": 
    
    test = TestSample()#Sample(representation="Random_variates", name="Weibull sample", law="Weibull", param1=1.5, scale=8000, size=7)