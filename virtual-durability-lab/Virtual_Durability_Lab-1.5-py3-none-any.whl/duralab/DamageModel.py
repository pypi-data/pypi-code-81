# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:24:52 2020

@author: U550787
"""

import math

class DamageModel:
    """
    Determine equivalent life measurement thanks to the Accelerator factor
    """
    def __init__(self):
        
        self.bolztmann_cst = 8.617385*10**-5
        
    def Basquin(self,S1,S2,L2,b):
        """
        Basquin damage model
        
        Parameters
        ----------
        S1 : scalar
            Represent the constraint of the research life measure L1
            
        S2 : scalar
            Represent the reference constraint 
            
        L2 : scalar
            Reprensent the reference quantifiable life measure 

        Return
        ----------
        L1 : scalar
            Represent the quantifiable life measure equivalent
     
        """
        return  L2*(float(S2)/S1)**b
    
    def Arrhenius(self, T1, T2, L2, B, Activation_energy=0):
        """
        Arrhenius damage model (mostly used for thermal stress)
        
        Parameters
        ----------
        T1 : scalar 
            Represent the temperature for the resaerch life measure L1 in °C
            
        T2 : scalar
            Represent the temperature of the accelerated test in °C
        
        L2 : scalar
            Reprensent the quantifiable life measure of the accelerated stress level
        
        B : scalar
            A parameter model determined by the Activation energy
            
        Activation_energy : scalar
            Calculate the B parameter of the model if it mentionned 
            Default = 0 
           
        Return
        ----------
        L1 : scalar
           Reprensent the quantifiable life measure equivalent
        """
        if Activation_energy:
            B = - Activation_energy / self.bolztmann_cst
        
        return L2*math.exp(B/self.Celsius_to_kelvin(T1) - B/self.Celsius_to_kelvin(T2))
    
    def Eyring(self, T1, T2, L2, B, Activation_energy=0):
        """
        Eyring damage model (It's most often used when thermal stress (temperature) is the acceleration variable)
        
        Parameters
        ----------
        T1 : scalar 
            Represent the temperature for the resaerch life measure L1 in °C
            
        T2 : scalar
            Represent the temperature of the accelerated test in °C
        
        L2 : scalar
            Reprensent the quantifiable life measure of the accelerated stres level
        
        B : scalar
            A parameter model determined by the Activation energy
            
        Activation_energy : scalar
            Calculate the B parameter of the model if it mentionned 
            Default = 0 
           
        Return
        ----------
        L1 : scalar
           Reprensent the quantifiable life measure equivalent
        """
        if Activation_energy:
            B = - Activation_energy / self.bolztmann_cst
        
        return L2*(T2/T1)*math.exp(B/self.Celsius_to_kelvin(T1) - B/self.Celsius_to_kelvin(T2))
    
    def Power(self, S1, S2, L2, n):
        """
        Inverse power damage model
        
        Parameters
        ----------
        S1 : scalar
            Represent the use stress level 
            
        S2 : scalar
            Represent the accelerated stress level
        
        L2 : scalar
            Represent the life of accelerated stress level
            
        n : scalar
            Represent the measure of the effect of the stress on the life.
            
        Return
        ----------
        L1 : scalar
            Represent the quatifiable life measure equivalent 
        """
        
        return (float(S2)/S1)**n
    
    def Celsius_to_kelvin(self, T):
        return T + 273.15


class test_Damage_model:
    """
        Damage_model Class Tests
    
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
    
    test = ()