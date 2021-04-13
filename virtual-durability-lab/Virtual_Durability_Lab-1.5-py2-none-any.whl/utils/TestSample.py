# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:24:06 2020

@author: U550787
"""
import sys

if sys.version_info.major == 3:
    from .Sample import Sample 
    from .DamageModel import DamageModel
else:
    from Sample import Sample 
    from DamageModel import DamageModel
    
    
import numpy as np
from matplotlib import pyplot as plt


class TestSample:
    """
        Realize a virtual failure test for a Sample given.
        
        Parameters
        ----------
        test_type : string
            Choice of the test
            Choices : 'Failure', 'Locati', 'Zero_failure', 'Staircase'
        
        name : string
            The name of your test. (It's use to save an visual representation)
        
        sample : Sample instance
            Acquire the Sample instance to test 
        
        life_objective : scalar (Optional)
            Establish the life objective for each sample tested must respect.
            
        stress_reference : scalar (Optional)
            Default : None
            Define the stress reference in case of the staircase test. For more information about the Staircase go to help(Test.staircase)
        
        stress_increment : scalar (Optional)
            Default : None
            Define the stress increase or decrease after each step of a staircase test
        
        basquin_slope_param : scalar (Optional)
            Default : 8 
        
        save_graph : string (Optional)
            Default : None
            Define the save path of the generated graph.
        
        Raises
        ----------
        ValueError
            Parameter 'sample' is missing or incorrect. Please enter a Sample instance, for further information go to help(Sample).
        
        ValueError
            Parameter 'test_type' is missing or incorrect. Please choose one of these : 'Staircase', 'Locati', 'Zero_failure', 'Failure'.
            
        ValueError
            Parameter 'stress_reference' and/or 'stress_increment' are missing. Please enter correct value to use the staircase test
            
        ValueError
            Parameter 'test_type' is missing or incorrect. Please choose one of these : 'Staircase', 'Locati', 'Zero_failure', 'Failure'.
            
        ValueError
            Parameter 'life_objective' is missing.
            
        Methods
        ----------
        staircase(self)
        locati(self)
        failure_test(self)
        zero_failure_test(self)
        test_visualisation(self)        
        
        Examples
        ----------
        #Test of the sample_1 from the first example of the Sample instance with the zero failure test. 
        test_1 = Test(life_objective=42000,sample=sample_1, test_type="Zero_failure")
        
        #Test of the sample_1 from the first example of the Sample instance with the staircase test.
        test_2 = Test(life_objective=60000,sample=sample_1, test_type="Staircase", stress_reference=300, stress_increment = 50)
    """
    
    def __init__(self, **kwargs):
        
        self.pourcent_success_failure = 0.7
        
        #Necessary arguments to do a stair case and/or a locati
        self.f0 = kwargs.get("stress_reference", None)
        self.d = kwargs.get("stress_increment", None)
        self.b_coeff = kwargs.get("basquin_slope_param", 8)
    
        #Sample assignement and life objective wich is optional 
        self.Sample = kwargs.get("sample", None)
        self.L = kwargs.get("life_objective", None)
        
        #Determine wich test to use
        self.test = kwargs.get("test_type", None)
        
        self.name = kwargs.get("name", None)
        self.save_path = kwargs.get("save_path", None)
        
        if not self.Sample or not isinstance(self.Sample, Sample):
            raise ValueError("Parameter 'sample' is missing or incorrect. Please enter a Sample instance, for further information go to help(Sample).")
            
        if not self.test or self.test not in ["Staircase", "Locati", "Zero_failure", "Failure"]:
            raise ValueError("Parameter 'test_type' is missing or incorrect. Please choose one of these : 'Staircase', 'Locati', 'Zero_failure', 'Failure'.")
    
        if not self.L:
            raise ValueError("Parameter 'life_objective' is missing.")
            
        #After perfom the test we define wich kind of data we have to do some post-traitment
        self.data_type = None
        
        #Test execution
        self.exec_test()
        
    def exec_test(self):
        
        if self.test == "Staircase":
            if not self.f0 and not self.d:
                raise ValueError("Parameter 'stress_reference' and/or 'stress_increment' are missing. Please enter correct value to use the staircase test")
            self.staircase()
            
        elif self.test == "Locati":
            if not self.f0 and not self.d:
                raise ValueError("Parameter 'stress_reference' and/or 'stress_increment' are missing. Please enter correct value to use the locati test")
            
        elif self.test == "Zero_failure":
            self.zero_failure_test()
            
        elif self.test == "Failure":
            self.failure_test()
            
        self.set_data_type()
        
        if self.save_path:
            self.test_visualisation()
    
    
    def staircase(self):
        """
        The staircase is a particular test. The test sollicitation evolve for each piece. 
        Each sample is sequential tested. 
        If there is a failure, the test sollicitation decrement by stress_increment. 
        If there is no failure, the test sollicitation increment by stress_increment. 
        
        The first test sollicitation is represented by the parameter stress_reference.
        To variate the sollicitation test, we use the equivalent damage model of Basquin which determine the life measure equivalent for each sample.
        """
        self.result = []
        
        success = False
        f = self.f0
        dm = DamageModel()
        L_eq = self.L
        
        for i, L_sa in enumerate(self.Sample.sample):
            if i != 0 :
                if success:
                    f += self.d
                else:
                    f -= self.d
            
            L_eq = dm.Basquin(f, self.f0, self.L, self.b_coeff)
            
            if L_sa < L_eq:
                success = False
            else:
                success = True
            
            self.result.append(("OK", L_eq) if success else ("NOK", L_sa))
            
        
        
    def locati(self):
        
        self.result = []
        
        life_step = self.L/3.
        f = 1.2 * self.f0
        L_eq = life_step
        dm = DamageModel()
        
        for L_sa in self.Sample.sample: 
            
            while 1:
                
                if self.locati_mode == "+":
                    f += self.d 
                else:
                    f -= self.d
                    
                L_eq += dm.Basquin(f, self.f0, self.L, self.b_coeff) 
                
                if L_sa > L_eq:
                    L_eq = life_step
                    break
            
            self.result.append(("OK", L_eq))
        
        
    def failure_test(self):
        
        self.result = [ ("NOK", L_sa) for L_sa in self.Sample.sample ]
    
    def zero_failure_test(self):
        
        self.result = [("NOK", L_sa )if L_sa <= self.L else ("OK", self.L) for L_sa in self.Sample.sample]
    
    def set_data_type(self):
        
        if self.result:
            
            res = [r[0] for r in self.result]
            failure = res.count('NOK')
            success = res.count('OK') 
            
            if failure == len(self.result):
                self.data_type = "Complete Data"
                
            elif float(failure)/len(self.result) >= self.pourcent_success_failure:
                self.data_type = "Low Right Censored Data"
                
            elif float(success)/len(self.result) >= self.pourcent_success_failure:
                self.data_type = "Strong Right Censored Data"
          
            else:
                self.data_type = "Censored Data"
                
    def test_visualisation(self, plot_limit=20):
        """
        Show plot with all results data generated
        
        plot_limit need to be a number under or same as the sample size
        """
        
        if plot_limit > self.Sample.size: 
            raise ValueError("Impossible to define plot_limit more than the sample size.")
        
        fig, ax = plt.subplots()
            
        y_label = [r[0] for r in self.result[:plot_limit]]
        y_pos = np.arange(len(self.result[:plot_limit]))
        res = [r[1] for r in self.result[:plot_limit]]
            
        rects = ax.barh(y_pos,height=0.3,tick_label=y_label, alpha=0.8, color=['g' if r[0]=="OK" else 'r' for r in self.result], width=res)
        ax.set_yticks(y_pos)
        ax.set_title("%s test result with %d samples" % (self.test, plot_limit))
        ax.set_xlabel("Quantifiable life measure")
        #Add annotations with the life measurement
        for i,rect in enumerate(rects):
            width = int(rect.get_width())
                
            #Shift the text
            xloc = -45
            # Center the text vertically in the bar
            yloc = rect.get_y() + rect.get_height() / 2
                
            ax.annotate(int(res[i]), xy=(width, yloc), xytext=(xloc, 0),textcoords="offset pixels", va='center',weight='bold', clip_on=True)
            
            
        plt.show()
            
        if self.save_path:
            self.save_path = self.save_path.decode('utf-8')
            name = "%s/%s.png" % (self.name, self.save_path) if self.name else "%s/sample.png" % self.save_path
            fig.savefig(name.decode('utf-8'), format='png', bbox_inches='tight')
            
            
#    def Def_stress_strengh(self,stress_func, strengh_func ,mean1, std_dev1, mean2, std_dev2): 
#        
#        return quad(lambda a: strengh_func.pdf(a, loc=mean1, scale=std_dev1)*stress_func.cdf(a, loc=mean2, scale=std_dev2), 0, stress_func.ppf(0.999))
                
                
class TestTestSample:
    """
        Test for the Test class
    
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
    
    test = TestTestSample()
