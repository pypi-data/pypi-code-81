# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:58:36 2020

@author: U550787
"""

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import sys
import scipy.stats as s

if float(sys.version[:3])  >= 3.7 :
    from .Sample import Sample 
    from .TestSample import TestSample
    from .DataTreatment import DataTreatment
else:
    from Sample import Sample 
    from TestSample import TestSample
    from DataTreatment import DataTreatment
    
class PlanEfficiency:
    """
        Testing efficience of one test plan by multiple repetitions.
    
        Parameters
        ----------
        
        sample : Sample instance
            Add sample to the test plan
        
        test : TestSample instance
            Add test method to the test plan
        
        data_treatment : Datatreament instance
            Add the data treatment to the test plan    
            
        n : int
            Number of the define plan test (by the sample, test, and data_treatment) repetition. Accuracy will 
        
        
        Raises
        ----------
        ValueError
            Parameter 'sample' is missing or incorrect. Please enter a Sample instance, for further information go to help(Sample).
        
        ValueError
            Parameter 'test' is missing or incorrect. Please enter a TestSample instance, for further information go to help(TestSample).
        
        ValueError
            Parameter 'data_treatment' is missing or incorrect. Please enter a DataTreatment instance, for further information go to help(DataTreatment).
        
            
        Methods
        ----------
        exec_testplan_efficiency(self)
        indicators_calculation(self)
        update(self, result="models")
        efficiency_visualization(self)
        
    """
    
    
    def __init__(self, **kwargs):
        
        self.GRAPH = True 
        
        self.Sample = kwargs.get("sample", None)
        self.TestSample = kwargs.get("test", None)    
        self.DataTreatment = kwargs.get("data_treatment", None)
        
        self.estimate_result = {"Normal": {}, "Lognormal": {}, "Weibull": {}, "Exponential": {}}
        
        self.n = kwargs.get("n", 1)
        
        try:
            if not self.Sample and not isinstance(self.Sample, Sample):
                raise ValueError("Parameter 'sample' is missing or incorrect. Please enter a Sample instance, for further information go to help(Sample).")
        except:
            if not self.Sample and not Sample.__name__ in str(type(Sample)):
                raise ValueError("Parameter 'sample' is missing or incorrect. Please enter a Sample instance, for further information go to help(Sample).")
    
        try:
            if not self.TestSample and not isinstance(self.TestSample, TestSample):
                raise ValueError("Parameter 'test' is missing or incorrect. Please enter a Sample instance, for further information go to help(TestSample).")
        except:
            if not self.TestSample and not self.TestSample.__name__ in str(type(TestSample)):
                raise ValueError("Parameter 'test' is missing or incorrect. Please enter a Sample instance, for further information go to help(TestSample).")
                
        try:
            if not self.DataTreatment and not isinstance(self.DataTreatment, DataTreatment):
                raise ValueError("Parameter 'data_treatment' is missing or incorrect. Please enter a DataTreatment instance, for further information go to help(DataTreatment).")
        except:
            if not self.DataTreatment and not self.DataTreatment.__name__ in str(type(DataTreatment)):
                raise ValueError("Parameter 'data_treatment' is missing or incorrect. Please enter a DataTreatment instance, for further information go to help(DataTreatment).")
    
        self.estimate_result = { key: {} for i, (key, value) in enumerate(self.DataTreatment.estimation_result.items()) if value != {}}
            
        #Desactivate graphical visualization
        self.Sample.GRAPH = False
        self.TestSample.GRAPH = False
        self.DataTreatment.GRAPH = False
        
        self.exec_testplan_efficiency()
        
    def exec_testplan_efficiency(self):
        """
        Main purpose is to repeat the test plan define the first n times, to statistical construe the efficiency of the methods used.
        """
        
        for i in range(1,self.n):
            self.update()
    
            #Need to deepcopy the object to make a new object with a new memory adress reference (if not the values will be the same as the last one)
            for law, law_dict in [ (key, val) for key, val in self.DataTreatment.estimation_result.items() if val != {}]:
            
                for param, data in law_dict.items():
                    
                    if i == 1:
                        self.estimate_result[law][param] = [data]
                    else:
                        self.estimate_result[law][param].append(data)
        
        
        if self.GRAPH:
            self.efficiency_visualization()
    
    
    
    def update(self):
        """
        Generate new randoms value following the define Sample instance, re-run the TestSample instance and calculate the new estimation model
        """
        
        self.Sample.exec_sample()
        self.TestSample.exec_test()
        self.DataTreatment.exec_treatment()
       
        
    def efficiency_visualization(self):
        
        parameters = {"m":"μ",
                      "l":"λ",
                      "s":"σ",
                      "sln":"σ",
                      "mln":"μ",
                      "h":"η", 
                      "b":"β"}
        
        laws = self.estimate_result.keys()
        #Define wich model is define it will be used to split the plot area in rows (Add one to do r values comparaison do to the fact this value is always represented)
        nrow = len(laws) + 1  
        #Define the maximum parameters to split the plot area in colonums -1 for r_value 
        ncols = max([ len(value.keys()) for value in self.estimate_result.values()]) - 1
        
        fig= plt.figure()
        gs = gridspec.GridSpec(nrow, ncols, wspace=0.5, hspace=0.5)
            
        ax_r = fig.add_subplot(gs[0, :])
        ax_r.boxplot([ laws_dict["r_value"] for laws, laws_dict in self.estimate_result.items() if "r_value" in laws_dict.keys() ], 
                     showfliers=False,
                     labels=laws)
        ax_r.set_title("r_value comparaison")
        
        for i, (law, law_dict) in enumerate(self.estimate_result.items()):
            i+=1 
            
            for j, (param, data) in enumerate([(key, value) for key, value in law_dict.items() if key != "r_value"]):
                ax = fig.add_subplot(gs[i, j])
                ax.boxplot(data, 
                           showfliers=False, 
                           labels=list(parameters[param]))
                ax.set_title("{} from {} estimation".format(parameters[param], law))
                
                if law == self.Sample.law_text:
                    
                    input_value = {"Normal": {"s": self.Sample.scale, "m": self.Sample.loc},
                                   "Exponential" : {"l": 1/self.Sample.scale},
                                   "Lognormal" : {"sln": self.Sample.param1, "mln": self.Sample.scale},
                                   "Weibull" : {"b": self.Sample.param1, "h": self.Sample.scale}}
                    
                    ax.plot([0, 1, 2], [ input_value[law][param] for i in range(3)], label="{} input".format(parameters[param]), color="red")
                    ax.legend()
                    ax.annotate('%0.2f' % input_value[law][param], xy=(1, input_value[law][param]), xytext=(8, 0), xycoords=('axes fraction', 'data'), textcoords='offset points')  
        
        #fig.tight_layout() 
        plt.show()

        
class TestPlanEfficiency:
    """
        Test Class tests
        Created to test, debug and integrate the PlanEfficiency
    
        Parameters
        ----------
        
        n : int
            Number of the repetetion wanted to our test plan
        
        Raises
        ----------
 
        Methods
        ----------

    """
    def __init__(self, n):
        
        
        self.n = n 
        self.sample = Sample(name="TestPlanEfficiency",size=10, representation="Random_variates", law="Weibull", scale=19000, param1=1.3)
        self.test =  TestSample(life_objective=20000,sample=self.sample, test_type="Zero_failure")
        self.treatment = DataTreatment(method="Johnson_rank", test_result=self.test)
        
    def functionnal_test_1(self):
        """
        First test with a sample represent by a Weibull law, a zero failure test and a Johnson rank post data treatment
        """
        
        self.test_plan = PlanEfficiency(sample=self.sample, test=self.test, data_treatment=self.treatment, n=self.n)
        #self.test_plan.efficiency_visualization()
    
    
    def dev_efficiency_class_algorithm(self):
        """
        Test the algorithm of the TestingEfficiency Class
        Each times we need to update all the Class and check if the ufond dépdate work correctly
        """
        self.t = {"estimation_result": []}
        
        print(self.sample.sample)
        print(self.test.result)
        print(self.treatment.estimation_result)
        print("----------------\n END FIRST SAMPLES \n----------------")
        self.sample.exec_sample()
        self.test.exec_test()
        self.treatment.exec_treatment()
        print(self.sample.sample)
        print(self.test.result)
        print(self.treatment.estimation_result)
        self.t["estimation_result"].append(deepcopy(self.treatment.estimation_result))
        print("----------------\n END SECOND SAMPLES \n----------------")
        self.sample.exec_sample()
        self.test.exec_test()
        self.treatment.exec_treatment()
        print(self.sample.sample)
        print(self.test.result)
        print(self.treatment.estimation_result)
        print("----------------\n END\n----------------")
        self.t["estimation_result"].append(deepcopy(self.treatment.estimation_result))
        print(self.t)
        
    def dev_boxplot(self):
        
        
        for law_model in [ key for key, value in self.treatment.estimation_result.items() if value != {} ]:
                
            law = {"Normal" : [ s.norm, {"loc" : self.treatment.estimation_result["Normal"]["m"] if "m" in self.treatment.estimation_result["Normal"].keys() else None,
                                         "scale" : self.treatment.estimation_result["Normal"]["s"]if "s" in self.treatment.estimation_result["Normal"].keys() else None}],
                   "Weibull" : [ s.weibull_min,  {"c" : self.treatment.estimation_result["Weibull"]["b"] if "b" in self.treatment.estimation_result["Weibull"].keys() else None,
                                                  "scale" :self.treatment.estimation_result["Weibull"]["h"] if "h" in self.treatment.estimation_result["Weibull"].keys() else None}],
                   "Lognormal" : [s.lognorm, {"s" : self.treatment.estimation_result["Lognormal"]["sln"]  if "sln" in self.treatment.estimation_result["Lognormal"].keys() else None,
                                              "scale" : self.treatment.estimation_result["Lognormal"]["mln"]} if "mln" in self.treatment.estimation_result["Lognormal"].keys() else None], 
                   "Exponential" : [s.expon, {"scale" : 1/self.treatment.estimation_result["Exponential"]["l"]  if "l" in self.treatment.estimation_result["Exponential"].keys() else None}] }[law_model]
                       
            temp =[None, None]
            #Temporary variable to stock law parameters, need two to bound the law thanks to parameters
            temp[0] = law[1].copy()
            temp[1] = law[1].copy()
            #Add bounds with 1 and 99 percentiles of the law
            temp[0].update({"q": 0.01})
            temp[1].update({"q": 0.99})
                
            #Define axe values with bounds 1 and 99 percentiles
            x = np.linspace(law[0].ppf(**temp[0]),law[0].ppf(**temp[1]),100)
            
            #Re define the new temp law with parameters defined
            temp = law[1].copy()
            temp.update({"x": x})
                
            data = law[0].pdf(**temp)    
        
            
            plt.boxplot(data,showfliers=False) 
            
if __name__ == "__main__": 
    
    test = TestPlanEfficiency(20)
