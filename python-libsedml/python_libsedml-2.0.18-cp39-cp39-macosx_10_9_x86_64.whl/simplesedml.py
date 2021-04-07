# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 15:17:23 2021

@author: hsauro
"""

import libsedml


class SimpleSedml:
    
   def __init__(self):
       self.document = libsedml.SedDocument(1, 4)

   def create (self):
       libsedml.writeSedMLToFile(self.document, 'model_sedml.xml') 
           
       
   def addModel (self, source):
       self.model = self.document.createModel()
       self.model.setId("model1")
       self.model.setSource(source)
       self.model.setLanguage("urn:sedml:sbml")
       
   def addTimeCourse (self):
       tc = self.document.createUniformTimeCourse()
       tc.setId("sim1")
       tc.setInitialTime(0.0)
       tc.setOutputStartTime(0.0)
       tc.setOutputEndTime(10.0)
       tc.setNumberOfPoints(100)
       tc.unsetNumberOfPoints()
       tc.setNumberOfSteps(100)
       tc.unsetNumberOfSteps()

       # need to set the correct KISAO Term
       alg = tc.createAlgorithm()
       alg.setKisaoID("KISAO:0000019")   
  
       task = self.document.createTask()
       task.setId("task1")
       task.setModelReference("model1")
       task.setSimulationReference("sim1")
  
       dg = self.document.createDataGenerator()
       dg.setId("time")
       dg.setName("time")
       var = dg.createVariable()
       var.setId("v0")
       var.setName("time")
       var.setTaskReference("task1")
       var.setSymbol("urn:sedml:symbol:time")
       dg.setMath(libsedml.parseFormula("v0"))
       
       dg = self.document.createDataGenerator()
       dg.setId("S1")
       dg.setName("S1")
       var = dg.createVariable()
       var.setId("v1")
       var.setName("S1")
       var.setTaskReference("task1")
       var.setTarget("/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='S1']")
       dg.setMath(libsedml.parseFormula("v1"))
       
       plot = self.document.createPlot2D()
       plot.setId("p1")
       plot.setName("S1 Timecourse")
       curve = plot.createCurve()
       curve.setId("c1")
       curve.setName("S1")
       curve.setLogX(False)
       curve.setLogY(False)
       curve.setXDataReference("time")
       curve.setYDataReference("S1")
  
       report = self.document.createReport()
       report.setId("r1")
       report.setName("report 1")
       set = report.createDataSet()
       set.setId("ds1")
       set.setLabel("time")
       set.setDataReference("time")
       set = report.createDataSet()
       set.setId("ds2")
       set.setLabel("S1")
       set.setDataReference("S1")
    
   def getSedml(self):
       return libsedml.writeSedMLToString(self.document)
    
    
if __name__ == '__main__':
    
   s = SimpleSedml()
   s.addModel ('model_sbml.xml')
   s.addTimeCourse()
   s.create()

   print("done")
