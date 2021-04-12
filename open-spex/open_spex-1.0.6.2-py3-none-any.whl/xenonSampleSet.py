#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 15:59:24 2020

@author: ringbom

This file is part of 'openSpex'
Copyright (c) 2021 Swedish Defence Research Agency (FOI)
"""

from matplotlib.figure import Figure
import wx
import numpy as np
import pickle
from os import path
import os
import shutil

from open_spex import const
from open_spex import utils as ut
from open_spex import BGMeasurement as bg
from open_spex import BGSample as bgs

class station:
    """
    A radioxenon measurement station
    Parameters
    ==========
    statType       Station type ('SAUNA' or 'CUBE')
    station        Station code
    site           Site name
    country        Country where site is
    lat            Station lat
    lon            Station lon
    network        Name of network (IMS, SCA, ...)
    """
    def __init__(self, statType, station, site=None, country=None, 
                 lat=None, lon=None, network = None):
        self.station = station
        self.stationType = station
        self.site = site
        self.country = country
        self.lat = lat
        self.lon = lon
        self.statType = statType
        self.network = network

class xenonSample:
    """
    Holds selected data from an analyzed BGSample
    """
    def __init__(self, bgs):
        if bgs.bgmHandler == None:
            print("Sample not analyzed. xenonSampe not created.")
            return
        self.isoPassed = ['XE-133','XE-131M','XE-133M','XE-135','RN-222']
        self.plotIndex = []
        self.marked = False
        self.dataSource = bgs.sample.dataSource
        self.resultPath = None
        self.stationType = bgs.sample.stationType
        self.sampleID = bgs.sample.sampleId
        """
        self.acqID = bgs.sample.aID
        self.detbkAcqId = bgs.detbk.aID
        if bgs.gasbk != None:
            self.gasbkAcqId = bgs.gasbk.aID
        else:
            self.gasbkAcqId = None
        """
        self.station = station(bgs.stationType, bgs.sample.station)
        self.detector = bgs.sample.detector
        self.srid = bgs.sample.srid        
        self.collstart_time = bgs.sample.collstart_time
        self.collstop_time = bgs.sample.collstop_time
        self.collTime = bgs.collTime
        self.acq_start = bgs.sample.acq_start
        self.airVol = bgs.sample.air_volume
        self.xeVol = bgs.sample.xe_vol
        self.xeVolErr = bgs.sample.xe_vol_err
        self.xeYield = bgs.sample.xe_yield
        self.xeYieldErr = bgs.sample.xe_yield_err
        self.unitscale = bgs.bgmHandler.unitscale
        self.unit = bgs.bgmHandler.unit
        self.AnalysisMethod = bgs.bgmHandler.analysisMethod
        self.roiBP = bgs.bgmHandler.roiBitPattern
        self.grossCounts = bgs.bgmHandler.grossCounts
        self.netCounts = bgs.bgmHandler.netCounts
        self.roiLimits = bgs.bgmHandler.roiLimits
        self.tau = bgs.bgmHandler.tau
        self.collTime = bgs.bgmHandler.collTime
        self.procTime = bgs.bgmHandler.procTime
        self.sAcqReal = bgs.bgmHandler.sAcqReal
        self.sAcqLive = bgs.bgmHandler.sAcqLive
        self.gAcqReal = bgs.bgmHandler.gAcqReal
        self.gAcqLive = bgs.bgmHandler.gAcqLive
        self.dAcqReal = bgs.bgmHandler.dAcqReal
        self.dAcqLive = bgs.bgmHandler.dAcqLive
        self.sampleGross = bgs.bgmHandler.sampleGross
        self.gasbkGross = bgs.bgmHandler.gasbkGross
        self.detbkGross = bgs.bgmHandler.detbkGross
        self.gasbkUsed = bgs.bgmHandler.gasbkUsed
        self.eff = bgs.bgmHandler.eff
        self.ratio = bgs.bgmHandler.ratio
        
        self.AC = bgs.bgmHandler.AC
        self.ACErr = bgs.bgmHandler.ACErr
        self.LC = bgs.bgmHandler.LC
        self.MDC = bgs.bgmHandler.MDC
        self.A = bgs.bgmHandler.A
        self.AErr = bgs.bgmHandler.AErr
        self.LCA = bgs.bgmHandler.LCA
        self.MDA = bgs.bgmHandler.MDA
        
        self.AC_Rn = bgs.bgmHandler.AC[0]
        self.ACErr_Rn = bgs.bgmHandler.ACErr[0]
        self.ACErrNonstat_Rn = bgs.bgmHandler.ACErrNonstat[0]
        self.LC_Rn = bgs.bgmHandler.LC[0]
#        self.LC_Rn_nc = bgs.bgmHandler.LC_ncorr[0] 
        self.MDC_Rn = bgs.bgmHandler.MDC[0]
        self.A_Rn = bgs.bgmHandler.A[0]
        self.AErr_Rn = bgs.bgmHandler.AErr[0]
        self.AErrNonstat_Rn = bgs.bgmHandler.AErrNonstat[0]
        self.LCA_Rn = bgs.bgmHandler.LCA[0]
        self.MDA_Rn = bgs.bgmHandler.MDA[0]
        
        self.AC_135 = bgs.bgmHandler.AC[1]
        self.ACErr_135 = bgs.bgmHandler.ACErr[1]
        self.ACErrNonstat_135 = bgs.bgmHandler.ACErrNonstat[1]
        self.LC_135 = bgs.bgmHandler.LC[1]
 #       self.LC_135_nc = bgs.bgmHandler.LC_ncorr[1]
        self.MDC_135 = bgs.bgmHandler.MDC[1]
        self.A_135 = bgs.bgmHandler.A[1]
        self.AErr_135 = bgs.bgmHandler.AErr[1]
        self.AErrNonstat_135 = bgs.bgmHandler.AErrNonstat[1]
        self.LCA_135 = bgs.bgmHandler.LCA[1]
        self.MDA_135 = bgs.bgmHandler.MDA[1]
        self.AC_133 = bgs.bgmHandler.Xe133AC
        self.ACErr_133 = bgs.bgmHandler.Xe133ACErr
        self.ACErrNonstat_133 = bgs.bgmHandler.Xe133ACErrNonStat
        self.LC_133 = bgs.bgmHandler.Xe133ACLC
   #         self.LC_133_nc = bgs.bgmHandler.Xe133ACLC
        self.MDC_133 = bgs.bgmHandler.Xe133ACMDC
        self.A_133 = bgs.bgmHandler.Xe133A
        self.AErr_133 = bgs.bgmHandler.Xe133AErr
        self.AErrNonstat_133 = bgs.bgmHandler.Xe133AErrNonStat
        self.LCA_133 = bgs.bgmHandler.Xe133ALC
        self.MDA_133 = bgs.bgmHandler.Xe133AMDA
        
        self.AC_131m = bgs.bgmHandler.AC[4]
        self.ACErr_131m = bgs.bgmHandler.ACErr[4]
        self.ACErrNonstat_131m = bgs.bgmHandler.ACErrNonstat[4]
        self.LC_131m = bgs.bgmHandler.LC[4]
    #    self.LC_131m_nc = bgs.bgmHandler.LC_ncorr[m1]
        self.MDC_131m = bgs.bgmHandler.MDC[4]
        self.A_131m = bgs.bgmHandler.A[4]
        self.AErr_131m = bgs.bgmHandler.AErr[4]
        self.AErrNonstat_131m = bgs.bgmHandler.AErrNonstat[4]
        self.LCA_131m = bgs.bgmHandler.LCA[4]
        self.MDA_131m = bgs.bgmHandler.MDA[4]
        
        self.AC_133m = bgs.bgmHandler.AC[5]
        self.ACErr_133m = bgs.bgmHandler.ACErr[5]
        self.ACErrNonstat_133m = bgs.bgmHandler.ACErrNonstat[5]
        self.LC_133m = bgs.bgmHandler.LC[5]
     #   self.LC_133m_nc = bgs.bgmHandler.LC_ncorr[m2]
        self.MDC_133m = bgs.bgmHandler.MDC[5]
        self.A_133m = bgs.bgmHandler.A[5]
        self.AErr_133m = bgs.bgmHandler.AErr[5]
        self.AErrNonstat_133m = bgs.bgmHandler.AErrNonstat[5]
        self.LCA_133m = bgs.bgmHandler.LCA[5]
        self.MDA_133m = bgs.bgmHandler.MDA[5]
        self.makeInfo()
      
    def detected(self,opt,iso):
        """
        Check if isotope 'iso' is detected in the sample. 
        opt = 'LC' or  'LC99'
        Returns 'True' or 'False'
        """
        if opt =='LC':
            if iso == 'XE-133':
                return self.AC_133 >= self.LC_133
            elif iso == 'XE-131M':
                return self.AC_131m >= self.LC_131m
            elif iso == 'XE-133M':
                return self.AC_133m >= self.LC_133m
            elif iso == 'XE-135':
                return self.AC_135 >= self.LC_135
            elif iso == 'RN-222':
                return self.AC_Rn >= self.LC_Rn
            else:
                print("Unknown isotope")
        elif opt == 'LC99':
            if iso == 'XE-133':
                return self.AC_133 >= self.LC_133*2.326/1.645
            elif iso == 'XE-131M':
                return self.AC_131m >= self.LC_131m*2.326/1.645
            elif iso == 'XE-133M':
                return self.AC_133m >= self.LC_133m*2.326/1.645
            elif iso == 'XE-135':
                return self.AC_135 >= self.LC_135*2.326/1.645
            elif iso == 'RN-222':
                return self.AC_Rn >= self.LC_Rn*2.326/1.645
            else:
                print("Unknown isotope")
        else:
            print("Unknown option.")
            
    def getDetectionBP(self,opt):
        """
        Get the detection bit pattern. 
        opt = 'LC', 'LC99' or LC_nc (no Bayesian correction)
        Returns the bitpattern bit [1,2,3,4] = 
        ['XE-133','XE-131M','XE-133M','XE-135'] 
        """
        iso = ['XE-133','XE-131M','XE-133M','XE-135']
        bp = 0
        ni = 0
        for i in iso:
            if self.detected(opt,i):
                bp += (1 << ni) | 0
            ni += 1
        return bp
    
    def makeInfo(self):
       """String with info on a xenonSample"""
       txt = "Sample\n"
       txt += "===========\n"
       #txt += format("Sample Id: %d Acquisition Id: %d\n" %(self.sampleID, self.acqID))
       txt += format("Detector: %s\n" %self.detector)
       txt += format("Coll. start: %s\n" % self.collstart_time.strftime("%Y-%m-%d %H:%M:%S"))
       txt += format("Coll. stop: %s\n" % self.collstop_time.strftime("%Y-%m-%d %H:%M:%S"))
       txt += format("Air volume: %2.2f m3\n" %self.airVol)
       txt += format("Xe Vol: %1.3f +/- %1.3f ml\n" %(self.xeVol, self.xeVolErr))
       txt += format("Yield: %1.2f +/- %1.2f\n" %(self.xeYield, self.xeYieldErr))
       txt += format("Analysis method: %s\n" %self.AnalysisMethod)
       txt += format("ROI detection bitpattern: %s\n" %bin(self.roiBP))
       txt += '{:<10s}{:<17s}{:<7s}\n'.format('','AC [mBq/m3]',' LC')
       txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}\n'.format('Xe-133:',self.AC_133,'+/-',self.ACErr_133, self.LC_133) 
       txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}\n'.format('Xe-131m:',self.AC_131m,'+/-',self.ACErr_131m, self.LC_131m)
       txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}\n'.format('Xe-133m:',self.AC_133m,'+/-',self.ACErr_133m, self.LC_133m)
       txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}\n'.format('Xe-135:',self.AC_135,'+/-',self.ACErr_135, self.LC_135) 
       self.info = txt
       return txt
   
    def csvLine(self):
        line = ''
        if self.resultPath != None:
            line += self.resultPath + ','
        else:
            line += ','
        line += self.station.station + ',' + self.detector + ',' + self.srid + ','
        line += self.collstart_time.strftime("%Y-%m-%d %H:%M:%S") + ',' + self.collstop_time.strftime("%Y-%m-%d %H:%M:%S") + ',' + self.acq_start.strftime("%Y-%m-%d %H:%M:%S") + ','
        line += format("%2.2f,%3.3f,%3.3f,%3.3f,%3.3f," %(self.airVol, self.xeVol,self.xeVolErr, self.xeYield, self.xeYieldErr))
        line += self.AnalysisMethod + ','
        line += format("%3.3f, %3.3f,%3.3f,%3.3f,%3f," %(self.AC_133, self.ACErr_133, self.ACErrNonstat_133, self.LC_133, self.MDC_133))
        line += format("%3.3f, %3.3f,%3.3f,%3.3f,%3f," %(self.AC_131m, self.ACErr_131m, self.ACErrNonstat_131m, self.LC_131m, self.MDC_131m))
        line += format("%3.3f, %3.3f,%3.3f,%3.3f,%3f," %(self.AC_133m, self.ACErr_133m, self.ACErrNonstat_133m, self.LC_133, self.MDC_133m))
        line += format("%3.3f, %3.3f,%3.3f,%3.3f,%3f," %(self.AC_135, self.ACErr_135, self.ACErrNonstat_135, self.LC_135, self.MDC_135))
        line += format("%3.3f, %3.3f,%3.3f,%3.3f,%3f," %(self.AC_Rn, self.ACErr_Rn, self.ACErrNonstat_Rn, self.LC_Rn, self.MDC_Rn))
        line += format("%3.3f, %3.3f,%3.3f,%3.3f,%3f," %(self.A_133, self.AErr_133, self.AErrNonstat_133, self.LCA_133, self.MDA_133))
        line += format("%3.3f, %3.3f,%3.3f,%3.3f,%3f," %(self.A_131m, self.AErr_131m, self.AErrNonstat_131m, self.LCA_131m, self.MDA_131m))
        line += format("%3.3f, %3.3f,%3.3f,%3.3f,%3f," %(self.A_133m, self.AErr_133m, self.AErrNonstat_133m, self.LCA_133, self.MDA_133m))
        line += format("%3.3f, %3.3f,%3.3f,%3.3f,%3f," %(self.A_135, self.AErr_135, self.AErrNonstat_135, self.LCA_135, self.MDA_135))
        line += format("%3.3f, %3.3f,%3.3f,%3.3f,%3f" %(self.A_Rn, self.AErr_Rn, self.AErrNonstat_Rn, self.LCA_Rn, self.MDA_Rn))
        line += '\n'
        return line
    
    def drawROIs(self, ax=None, lw= 1, ecolor = 'black', maxroi = 9):
        ut.drawROIs(self.roiLimits, ax, lw = lw, ecolor = ecolor, maxroi = maxroi)

class xenonSampleSet:
    """
    A set of 'xenonSample':s
    """
    def __init__(self, samplePath, detbkPath, resultPath = None, combine =True, use_gasbk = True,
                     prog = False, verbose = False, newCal = None, useIngrowth = True, writeResults = False,
                     moveDataFiles = False):
        self.set = []
        self.resultPath = resultPath
        self.writeResults = writeResults
        #
        #Analysis from files
        #
        sampleFiles = ut.getIMSFiles(samplePath, 'SAMPLEPHD')
        if use_gasbk:
            gasbkFiles = ut.getIMSFiles(samplePath, 'GASBKPHD')
        detbkFiles= ut.getIMSFiles(detbkPath, 'DETBKPHD')
        aid = 1
        if len(sampleFiles) > 0 and len(detbkFiles) > 0:
            if prog:
               progdia = wx.ProgressDialog("Calculating Measurement Set...", "Time remaining", 
                                len(sampleFiles),style=wx.PD_AUTO_HIDE 
                                | wx.PD_CAN_ABORT
                                | wx.PD_ELAPSED_TIME 
                                | wx.PD_REMAINING_TIME 
                                | wx.PD_SMOOTH)
               c = 0
               cancelled = False
            analyzedfiles = []
            for sf in sampleFiles:
               sample = bg.BGMeasurement('SAUNA', fileName = sf, verbose = verbose)
               sample.aID = aid
               sample.sampleId = aid
               gasbk = None
               detbk = None
               if use_gasbk:
                   for gf in gasbkFiles:
                      if sample.gasbk_id == ut.getMeasurementId(gf, 'sample'):
                          gasbk = bg.BGMeasurement('SAUNA', fileName = gf, verbose = verbose)
                          gasbkf = gf
                          break
               for df in detbkFiles:
                   if sample.detbk_id == ut.getMeasurementId(df, 'sample'):
                          detbk = bg.BGMeasurement('SAUNA', fileName = df, verbose = verbose)
                          break
               if sample != None and detbk != None:
                   if not sample.errors and not detbk.errors and not (sample.status & bg.ZERO_GROSS): 
                       bgsample = bgs.BGSample(sample, detbk,  gasbk = gasbk)
                       analyzedfiles.append((sf, bgsample.sample.station))
                       if newCal != None:
                           bgsample.sample.loadCalibration(newCal)
                           bgsample.detbk.loadCalibration(newCal)
                           if gasbk != None:
                               bgsample.gasbk.loadCalibration(newCal)
                       if gasbk != None:
                           if (gasbkf, bgsample.sample.station) not in analyzedfiles:
                            analyzedfiles.append((gasbkf, bgsample.sample.station))
                   #try:
                       bgsample.bgmAnalysis(combine, verbose, useIngrowth)
                       xs = xenonSample(bgsample)
                       if resultPath != None and writeResults:
                           self.writeResultFiles(bgsample, xs)
                       self.set.append(xs)
                   #except:
                       #print("Error in BGM for ID %d with coll. start %s" %(r[0], 
                           #bgsample.sample.collstart_time.strftime("%Y-%m-%d %H:%M:%S")))
                   else:
                       print("Errors in sample data for SRID %s." %sample.srid)
               else:
                   print("Errors in sample data for SRID %s." %sample.srid)
               aid += 1
               if prog:
                   goOn = progdia.Update(c)
                   if not goOn[0]:
                       progdia.Destroy()
                       cancelled = True
                       break
                   c += 1
            if resultPath != None and moveDataFiles:
                self.moveFiles(analyzedfiles)
            if prog and not cancelled:
               progdia.Destroy()
        else:
            print("Error when making Measurement Set.\nCould not find enough files""")
     
        if len(self.set) > 0:
            self.makeStationList()
            print("Created a Measurement Set with %d samples" %len(self.set))
            self.makeReport()
        else:
            print("Warning: Measurement Set is empty")
            
    def writeResultFiles(self, bgsample, xs):
        """
        Save sample .pkl-files.
        Sort data into station folders.
        """
        main_rp = path.join(self.resultPath, "results")
        if not path.exists(main_rp):
            os.mkdir(main_rp)
        rp = path.join(main_rp, bgsample.sample.station)
        if not path.exists(rp):
            os.mkdir(rp)
        sampleFileName = format("%s-%s-%d.pkl" 
            %(bgsample.sample.detector,
              bgsample.sample.collstart_time.strftime("%Y-%m-%d--%H-%M-%S"),bgsample.sample.acq_realtime))
        sampleFile = path.join(rp, sampleFileName)
        try:
           with open(sampleFile, 'wb') as file:
                pickle.dump(bgsample, file)
                print("Saving sample as %s" %sampleFile)
           xs.resultPath = sampleFile
        except IOError as e:
            print(e)
            print("Cannot save sample as %s" %sampleFile)
            
    def moveFiles(self,files):
        """Move files to the result directory"""
        main_dp = path.join(self.resultPath,"data")
        if not path.exists(main_dp):
            os.mkdir(main_dp)
        for f in files:
            try:
                shutil.move(f[0], main_dp)
                print("Moving %s to %s" %(f[0],main_dp))
            except IOError as e:
                print(e)
                print("File not moved.")

    @classmethod
    def emptySet(cls):
        """Alternative constructor for an empty set"""
        return cls('','','',None)
       
    def makeStationList(self):
        """Make list of station codes belonging to the set"""
        self.stationList = []
        for s in self.set:
            if s.station.station not in self.stationList:
                self.stationList.append(s.station.station)
                
    def getNSamples(self,station = ''):
        """Get nuber of samples in the set. 
        If station not empty string, only samples belonging to
        station code is counted.
        """
        n = 0
        for s in self.set:
            if station != '':
                if s.station.station == station:
                    n += 1
            else:
                n += 1
        return n
        
    def appendSet(self, anotherSet):
        """Append another set.
           Can contain data from another station.
        """
        for m in anotherSet.set:
            self.set.append(m)
        self.makeStationList() 
    
    def appendSample(self,s):
        """Append a sample to the set.
           Can be from another station.
        """
        self.set.append(s)
        self.makeStationList()
        
    def getPlottedSample(self,i,line_ind):
        """
        Get the sample plotted in line 'line_ind' with  index 'i'
        All lines plotted must have unique 'line_ind'
        """
        for s in self.set:
            for p in s.plotIndex:
                if p[0] == i and p[1] == line_ind:
                    return s
        return None

    def removeMarkers(self):
        """Un-mark all samples"""
        for s in self.set:
            s.marked = False
            
            
    def getFirstLastCollTime(self):
        """Get the first and last collection start times in the set"""
        i = 0
        for s in self.set:
            if i == 0:
                first = s.collstart_time
                last = s.collstart_time
            else:
                if s.collstart_time < first:
                     first = s.collstart_time
                if s.collstart_time > last:
                     last = s.collstart_time
            i += 1
        return first,last
        
    def plotQuantity(self, quant, useErr = False):
        """
        Plot a timeseries (uing coll start time) of one ror several quantities given by 
        the list of strings 'quant'
        Posible arguments are 'xeVol', 'airVol', 'xeYield'
        If useErr = True, show error bars if applicable.
        """
        if len(self.set) == 0:
            print("Measurement set empty. No plot is made.")
            return
        col = ['b','g','c','m','k']
        fig = Figure()
        ax = fig.add_subplot()
        ax.set(xlabel='Coll. Start')
        i = 0
        for q in quant:
            time = []
            y = []
            ye = []
            popt = 'o' + col[i]
            if q == 'xeVol':
                unit = 'ml'
            elif q == 'xeYield':
                unit = ''
            elif q == 'airVol':
                unit = 'm3'
            else:
                print("Wrong option in 'plotQuantity'.")
                return
            for s in self.set:
                time.append(s.collstart_time)
                if q == 'xeVol':
                     y.append(s.xeVol)
                     ye.append(s.xeVolErr)
                if q == 'xeYield':
                     y.append(s.xeYield)
                     ye.append(s.xeYieldErr)
                if q == 'airVol':
                     y.append(s.airVol)
            if len(y)>0:
                leg = q + ' [' + unit + ']'
                if useErr and q != 'airVol':
                    ax.errorbar(time, y, yerr = ye, fmt = popt, label = leg)
                else:
                    ax.plot(time, y, popt, label = leg)
            i += 1
        ax.legend()
        return fig
        
    def plotACTimeSeries(self, opt, iso = ['Xe-133','Xe-131m','Xe-133m','Xe-135'], hideMarked = False):
        """
        Plot timeseries with activity concentrations and related quantities.
        Parameters
        ==========
        opt        List with plot option strings. Possible quantities to plot are
                   'AC', 'LC', 'MDC', 'A', 'LCA', and 'MDA'.
                   Additional options:
                   'E': include errors
                   'L': connect 'AC' or 'A' with a line
                   'P': 'LC', 'MDC', 'LCA', and 'MDA' at dots (else lines) 
                   'G': include legend
        iso        List with isotopes to plot. Default:
                   ['Xe-133','Xe-131m','Xe-133m','Xe-135']
                   
        hideMarked (True/False). If True, marked samples are not plotted. 
        
        """
        if len(self.set) == 0:
            print("Measurement set empty. No plot is made.")
            return
        if ('AC' in opt) or ('LC' in opt) or ('MDC' in opt):
            unit = "$" + self.set[0].unit + "/m^3$"
            timeLabel = "Collection start"
        else:
            unit = "$" + self.set[0].unit + "$"
            timeLabel = "Acquisition start"
        col = ['b','g','c','m','k']
        fig = Figure(figsize=[9,3*len(iso)])
        ax = []
        for i in range(len(iso)):
            ax.append(fig.add_subplot(len(iso),1,i+1))
            ax[-1].set_ylabel(unit)
            ax[-1].set_xlabel(timeLabel, x = 0.95)
            ax[-1].set_title(iso[i])
        si = 0
        line_id = 0
        for s in self.set:
            s.plotIndex = []
        for st in self.stationList:
            for p in opt:
               if p == 'E' or p == 'L' or p == 'G' or p == 'P':
                   continue
               ii = 0
               for ui in iso:
                   #Reset plot data
                   i = ui.upper()
                   y = []
                   ye = []
                   time = []
                   popt = ''
                   if p == 'A' or p == 'AC':
                       lid = line_id + 100
                   else:
                       lid = line_id
                   if p == 'AC':
                       if 'L' in opt:
                           popt = '-' + col[si]
                       else:
                           popt = 'o' + col[si]
                       plot_ind = 0
                       for s in self.set:
                            if s.station.station == st and not (hideMarked and s.marked):
                                plotted = False
                                if i == 'XE-133' and 'XE-133' in s.isoPassed:
                                    y.append(s.AC_133)
                                    ye.append(s.ACErr_133)
                                    plotted = True
                                if i == 'XE-131M'and 'XE-131M' in s.isoPassed:
                                    y.append(s.AC_131m)
                                    ye.append(s.ACErr_131m)
                                    plotted = True
                                if i == 'XE-133M'and 'XE-133M' in s.isoPassed:
                                    y.append(s.AC_133m)
                                    ye.append(s.ACErr_133m)
                                    plotted = True
                                if i == 'XE-135' and 'XE-135' in s.isoPassed:
                                    y.append(s.AC_135)
                                    ye.append(s.ACErr_135)
                                    plotted = True
                                if i == 'RN-222' and 'RN-222' in s.isoPassed:
                                    y.append(s.AC_Rn)
                                    ye.append(s.ACErr_Rn)
                                    plotted = True
                                if plotted:
                                    s.plotIndex.append([plot_ind,lid])
                                    plot_ind += 1
                                    if ('AC' or 'LC' or 'MDC') in opt:
                                         time.append(s.collstart_time)
                                    else:
                                         time.append(s.acq_start)
                   if p == 'LC':
                       if 'P' in opt:
                           popt = 'o' + col[si]
                       else:
                           popt = '-' + col[si]
                       plot_ind = 0
                       for s in self.set:
                            if s.station.station == st and not (hideMarked and s.marked):
                                plotted = False
                                if i == 'XE-133' and 'XE-133' in s.isoPassed:
                                    y.append(s.LC_133)
                                    ye.append(0)
                                    plotted = True
                                if i == 'XE-131M' and 'XE-131M' in s.isoPassed:
                                    y.append(s.LC_131m)
                                    ye.append(0)
                                    plotted = True
                                if i == 'XE-133M'and 'XE-133M' in s.isoPassed:
                                    y.append(s.LC_133m)
                                    ye.append(0)
                                    plotted = True
                                if i == 'XE-135' and 'XE-135' in s.isoPassed:
                                    y.append(s.LC_135)
                                    ye.append(0)
                                    plotted = True
                                if i == 'RN-222' and 'RN-222' in s.isoPassed:
                                    y.append(s.LC_Rn)
                                    ye.append(0)
                                    plotted = True
                                if plotted:    
                                    s.plotIndex.append([plot_ind,lid])
                                    plot_ind += 1
                                    if ('AC' or 'LC' or 'MDC') in opt:
                                         time.append(s.collstart_time)
                                    else:
                                         time.append(s.acq_start)

                   if p == 'MDC':
                       if 'P' in opt:
                           popt = 'o' + col[si]
                       else:
                           popt = '--' + col[si]
                       plot_ind = 0
                       for s in self.set:
                            if s.station.station == st and not (hideMarked and s.marked):
                                plotted = False
                                if i == 'XE-133' and 'XE-133' in s.isoPassed:
                                    y.append(s.MDC_133)
                                    ye.append(0)
                                    plotted = True
                                if i == 'XE-131M' and 'XE-131M' in s.isoPassed:
                                    y.append(s.MDC_131m)
                                    ye.append(0)
                                    plotted = True
                                if i == 'XE-133M' and 'XE-133M' in s.isoPassed:
                                    y.append(s.MDC_133m)
                                    ye.append(0)
                                    plotted = True
                                if i == 'XE-135' and 'XE-135' in s.isoPassed:
                                    y.append(s.MDC_135)
                                    ye.append(0)
                                    plotted = True
                                if i == 'RN-222' and 'RN-222' in s.isoPassed:
                                    y.append(s.MDC_Rn)
                                    ye.append(0)
                                    plotted = True
                                if plotted:
                                    s.plotIndex.append([plot_ind,lid])
                                    plot_ind += 1
                                    if ('AC' or 'LC' or 'MDC') in opt:
                                         time.append(s.collstart_time)
                                    else:
                                         time.append(s.acq_start)
                               
                   if p == 'A':
                       if 'L' in opt:
                           popt = '-' + col[si]
                       else:
                           popt = 'o' + col[si]
                       plot_ind = 0
                       for s in self.set:
                            if s.station.station == st and not (hideMarked and s.marked):
                                plotted = False
                                if i == 'XE-133' and 'XE-133' in s.isoPassed:
                                    y.append(s.A_133)
                                    ye.append(s.AErr_133)
                                    plotted = True
                                if i == 'XE-131M' and 'XE-131M' in s.isoPassed:
                                    y.append(s.A_131m)
                                    ye.append(s.AErr_131m)
                                    plotted = True
                                if i == 'XE-133M' and 'XE-133M' in s.isoPassed:
                                    y.append(s.A_133m)
                                    ye.append(s.AErr_133m)
                                    plotted = True
                                if i == 'XE-135' and 'XE-135' in s.isoPassed:
                                    y.append(s.A_135)
                                    ye.append(s.AErr_135)
                                    plotted = True
                                if i == 'RN-222' and 'RN-222' in s.isoPassed:
                                    y.append(s.A_Rn)
                                    ye.append(s.AErr_Rn)
                                    plotted = True
                                if plotted:
                                    s.plotIndex.append([plot_ind,lid])
                                    plot_ind += 1
                                    if ('AC' or 'LC' or 'MDC') in opt:
                                         time.append(s.collstart_time)
                                    else:
                                         time.append(s.acq_start)

                   if p == 'LCA':
                       if 'P' in opt:
                           popt = 'o' + col[si]
                       else:
                           popt = '-' + col[si]
                       plot_ind = 0
                       for s in self.set:
                            if s.station.station == st and not (hideMarked and s.marked):
                                plotted = False
                                if i == 'XE-133' and 'XE-133' in s.isoPassed:
                                    y.append(s.LCA_133)
                                    ye.append(0)
                                    plotted = True
                                if i == 'XE-131M' and 'XE-131M' in s.isoPassed:
                                    y.append(s.LCA_131m)
                                    ye.append(0)
                                    plotted = True
                                if i == 'XE-133M' and 'XE-133M' in s.isoPassed:
                                    y.append(s.LCA_133m)
                                    ye.append(0)
                                    plotted = True
                                if i == 'XE-135' and 'XE-135' in s.isoPassed:
                                    y.append(s.LCA_135)
                                    ye.append(0)
                                    plotted = True
                                if i == 'RN-222' and 'RN-222' in s.isoPassed:
                                    y.append(s.LCA_Rn)
                                    ye.append(0)
                                    plotted = True
                                if plotted:
                                    s.plotIndex.append([plot_ind,lid])
                                    plot_ind += 1
                                    if ('AC' or 'LC' or 'MDC') in opt:
                                         time.append(s.collstart_time)
                                    else:
                                         time.append(s.acq_start)

                   if p == 'MDA':
                       if 'P' in opt:
                           popt = 'o' + col[si]
                       else:
                           popt = '--' + col[si]
                       plot_ind = 0
                       for s in self.set:
                            if s.station.station == st and not (hideMarked and s.marked):
                                plotted = False
                                if i == 'XE-133' and 'XE-133' in s.isoPassed:
                                    y.append(s.MDA_133)
                                    ye.append(0)
                                    plotted = True
                                if i == 'XE-131M' and 'XE-131M' in s.isoPassed:
                                    y.append(s.MDA_131m)
                                    ye.append(0)
                                    plotted = True
                                if i == 'XE-133M' and 'XE-133M' in s.isoPassed:
                                    y.append(s.MDA_133m)
                                    ye.append(0)
                                    plotted = True
                                if i == 'XE-135' and 'XE-135' in s.isoPassed:
                                    y.append(s.MDA_135)
                                    ye.append(0)
                                    plotted = True
                                if i == 'RN-222' and 'RN-222' in s.isoPassed:
                                    y.append(s.MDA_Rn)
                                    ye.append(0)
                                    plotted = True
                                if plotted:
                                    s.plotIndex.append([plot_ind,lid])
                                    plot_ind += 1
                                    if ('AC' or 'LC' or 'MDC') in opt:
                                         time.append(s.collstart_time)
                                    else:
                                         time.append(s.acq_start)
                   if 'E' in opt:
                       if len(y)>0:
                           ax[ii].errorbar(time,y,fmt = popt,yerr = ye, 
                          label = p + ' ' + st, gid = lid)
                   else:
                       if len(y) > 0:
                           ax[ii].plot(time,y,popt,label = p + ' ' + st, gid = lid)
                   ii += 1
                   if  not( p == 'E' or p == 'L' or p == 'G'): line_id += 1 
            si += 1
        if not hideMarked:
            self.drawMarkers(fig)
        if 'G' in opt:
            ax[0].legend()
        fig.tight_layout()
        return fig
    
    def activityRatioTimeSeries(self, nominator, denominator, showUnc, hideMarked = False):
        if len(self.set) == 0:
            print("Measurement set empty. No plot is made.")
            return
        nom = nominator.upper()
        denom = denominator.upper()
        col = ['b','g','c','m','k']
        fig = Figure(figsize=[9,9])
        ax = fig.add_subplot()
        sta = 0
        for s in self.set:
            s.plotIndex = []
        lid = 100
        for st in self.stationList:
           form = 'o' + col[sta] 
           y = []
           ye_pos = []
           ye_neg = []
           time = []
           plot_ind = 0
           for s in self.set:
                if s.station.station == st and not (hideMarked and s.marked):
                    if nom in s.isoPassed and denom in s.isoPassed:
                        if nom == 'XE-133':
                            nomv = s.A_133
                            nomve = s.AErr_133
                        elif nom == 'XE-131M':
                            nomv = s.A_131m
                            nomve = s.AErr_131m
                        elif nom == 'XE-133M':
                            nomv = s.A_133m
                            nomve = s.AErr_133m
                        elif nom == 'XE-135':
                            nomv = s.A_135
                            nomve = s.AErr_135
                        else:
                            print("Error: Nominator %s not supported." %nom)
                            return
                        if denom == 'XE-133':
                            denomv = s.A_133
                            denomve = s.AErr_133
                        elif denom == 'XE-131M':
                            denomv = s.A_131m
                            denomve = s.AErr_131m
                        elif denom == 'XE-133M':
                            denomv = s.A_133m
                            denomve = s.AErr_133m
                        elif denom == 'XE-135':
                            denomv = s.A_135
                            denomve = s.AErr_135
                        else:
                            print("Error: Denominator %s not supported." %denom)
                            return
                        if nomv > 0 and denomv > 0:
                            r = nomv/denomv
                            r_neg, r_pos = ut.Fieller(denomv,denomve, nomv,nomve,0)
                            time.append(s.acq_start)
                            y.append(r)
                            s.plotIndex.append([plot_ind,lid])
                            plot_ind += 1
                            if r_neg != None and r_pos != None:  
                                ye_neg.append(r - r_neg)
                                ye_pos.append(r_pos - r)
                            else:
                                ye_neg.append(0)
                                ye_pos.append(0)    
           if len(y) > 0:
               if showUnc:
                   dy = [ye_neg,ye_pos]
                   ax.errorbar(time, y, yerr = dy, fmt = form, label = st, gid = lid)
               else:
                   ax.plot(time,y,form, label = st, gid = lid)
           sta += 1
           lid += 1
        ylabel = format("%s / %s" %(nominator,denominator))
        ax.set_xlabel('Acquisition start')
        ax.set_ylabel(ylabel)
        ax.legend()
        ax.set_yscale('log')
        ax.set_ylim([1e-3,1e+3])
        if not hideMarked:
            self.drawMarkers(fig)
        fig.tight_layout()
        return fig
    
    def frequencyDistr(self, opt, isotopes = ['XE-133','XE-131M','XE-133M','XE-135']):
        """Plot frequency histograms for selected isotopes"""
        if len(self.set) == 0:
            print("Measurement set empty. No plot is made.")
            return
        xlabel = ''
        if ('AC' or 'LC' or 'MDC') in opt:
            xlabel = opt[0] + " [" + "$" + self.set[0].unit + "/m^3$ ]"
        else:
            xlabel = opt[0] + " [" + "$" + self.set[0].unit + "$ ]"
        fig = Figure(figsize=[9,9])
        ax = []
        for i in range(len(isotopes)):
            ax.append(fig.add_subplot(3,2,i+1))
            ax[-1].set_xlabel(xlabel)
            ax[-1].set_ylabel('Number of samples')
            ax[-1].set_title(isotopes[i])
        i = 0
        for isot in isotopes:
            iso = isot.upper()
            data = []
            if opt[0] == 'AC':
               for s in self.set:
                    if iso == 'XE-133' and iso in s.isoPassed:
                        data.append(s.AC_133)
                    if iso == 'XE-131M'and iso in s.isoPassed:
                        data.append(s.AC_131m)
                    if iso == 'XE-133M'and iso in s.isoPassed:
                        data.append(s.AC_133m)
                    if iso == 'XE-135' and iso in s.isoPassed:
                        data.append(s.AC_135)
                    if iso == 'RN-222' and iso in s.isoPassed:
                        data.append(s.AC_Rn)
            if opt[0] == 'LC':
               for s in self.set:
                    if iso == 'XE-133' and iso in s.isoPassed:
                        data.append(s.LC_133)
                    if iso == 'XE-131M'and iso in s.isoPassed:
                        data.append(s.LC_131m)
                    if iso == 'XE-133M'and iso in s.isoPassed:
                        data.append(s.LC_133m)
                    if iso == 'XE-135' and iso in s.isoPassed:
                        data.append(s.LC_135)
                    if iso == 'RN-222' and iso in s.isoPassed:
                        data.append(s.LC_Rn)
            if opt[0] == 'MDC':
               for s in self.set:
                    if iso == 'XE-133' and iso in s.isoPassed:
                        data.append(s.MDC_133)
                    if iso == 'XE-131M'and iso in s.isoPassed:
                        data.append(s.MDC_131m)
                    if iso == 'XE-133M'and iso in s.isoPassed:
                        data.append(s.MDC_133m)
                    if iso == 'XE-135' and iso in s.isoPassed:
                        data.append(s.MDC_135)
                    if iso == 'RN-222' and iso in s.isoPassed:
                        data.append(s.MDC_Rn)
            if opt[0] == 'A':
               for s in self.set:
                    if iso == 'XE-133' and iso in s.isoPassed:
                        data.append(s.A_133)
                    if iso == 'XE-131M'and iso in s.isoPassed:
                        data.append(s.A_131m)
                    if iso == 'XE-133M'and iso in s.isoPassed:
                        data.append(s.A_133m)
                    if iso == 'XE-135' and iso in s.isoPassed:
                        data.append(s.A_135)
                    if iso == 'RN-222' and iso in s.isoPassed:
                        data.append(s.A_Rn)
            if opt[0] == 'LCA':
               for s in self.set:
                    if iso == 'XE-133' and iso in s.isoPassed:
                        data.append(s.LCA_133)
                    if iso == 'XE-131M'and iso in s.isoPassed:
                        data.append(s.LCA_131m)
                    if iso == 'XE-133M'and iso in s.isoPassed:
                        data.append(s.LCA_133m)
                    if iso == 'XE-135' and iso in s.isoPassed:
                        data.append(s.LCA_135)
                    if iso == 'RN-222' and iso in s.isoPassed:
                        data.append(s.LCA_Rn)
            if opt[0] == 'MDA':
               for s in self.set:
                    if iso == 'XE-133' and iso in s.isoPassed:
                        data.append(s.MDA_133)
                    if iso == 'XE-131M'and iso in s.isoPassed:
                        data.append(s.MDA_131m)
                    if iso == 'XE-133M'and iso in s.isoPassed:
                        data.append(s.MDA_133m)
                    if iso == 'XE-135' and iso in s.isoPassed:
                        data.append(s.MDA_135)
                    if iso == 'RN-222' and iso in s.isoPassed:
                        data.append(s.MDA_Rn)
            if len(data)>2:
                bins = 100
                ra = [np.min(data)-0.5, np.max(data) + 0.5]
                ax[i].hist(data,bins,ra,color='b',histtype = 'step')
                bbox = dict(boxstyle='round', fc='0.8')
                txt = format('mean: %1.3f \nmedian: %1.3f \nstd: %1.3f \np95: %3.2f' 
                             %(np.mean(data), np.median(data), np.std(data),np.percentile(data,95)))
                ax[i].text(0.75,0.95,txt,ha='left',va='top',
                  transform = ax[i].transAxes, bbox=bbox)
            else:
                print("Warning: Too few data points. No plotting.")
            i += 1
        fig.tight_layout()
        return fig
    
    def MIRC(self,opt, hideMarked = False):
        """Make a MIRC-plot."""
        if len(self.set) == 0:
            print("Measurement set empty. No plotting.")
            return
        if opt !=3 and opt !=4:
            print("Wrong option in MIRC.")
            return
        if opt == 4:
            xlabel = '$^{133m}Xe/^{131m}Xe$'
            ylabel = '$^{135}Xe/^{133}Xe$'
        if opt == 3:
            xlabel = '$^{133m}Xe/^{133}Xe$'
            ylabel = '$^{135}Xe/^{133}Xe$'
        fig = Figure(figsize=[9,9])
        ax = fig.subplots()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title('MIRC'+str(opt))
        x = []
        y = []
        dx_neg = []
        dx_pos = []
        dy_neg = []
        dy_pos = []
        for s in self.set:
            s.plotIndex = []
        plot_ind = 0
        for s in self.set:
                if opt == 4:
                    if s.A_133 > 0 and s.A_135 and s.A_131m > 0 and s.A_133m > 0 and not (hideMarked and s.marked):
                        rx = s.A_133m/s.A_131m
                        ry = s.A_135/s.A_133
                        y.append(ry)
                        x.append(rx)
                        rx_neg, rx_pos = ut.Fieller(s.A_131m,s.AErr_131m, s.A_133m,s.AErr_133m,0)
                        ry_neg, ry_pos = ut.Fieller(s.A_133,s.AErr_133, s.A_135,s.AErr_135,0)
                        if rx_neg != None and rx_pos != None and ry_neg != None and ry_pos != None:
                            dx_neg.append(rx - rx_neg)
                            dx_pos.append(rx_pos - rx)
                            dy_neg.append(ry - ry_neg)
                            dy_pos.append(ry_pos - ry)
                        else:
                            dx_neg.append(0)
                            dx_pos.append(0)
                            dy_neg.append(0)
                            dy_pos.append(0)
                        s.plotIndex.append([plot_ind,100])
                        plot_ind += 1
                if opt == 3:
                    if s.A_133 > 0 and s.A_135 and s.A_133m > 0:
                        rx = s.A_133m/s.A_133
                        ry = s.A_135/s.A_133
                        y.append(ry)
                        x.append(rx)
                        rx_neg, rx_pos = ut.Fieller(s.A_133,s.AErr_133, s.A_133m,s.AErr_133m,0)
                        ry_neg, ry_pos = ut.Fieller(s.A_133,s.AErr_133, s.A_135,s.AErr_135,0)
                        if rx_neg != None and rx_pos != None and ry_neg != None and ry_pos != None:
                            dx_neg.append(rx -rx_neg)
                            dx_pos.append(rx_pos - rx)
                            dy_neg.append(ry - ry_neg)
                            dy_pos.append(ry_pos - ry)
                        else:
                            dx_neg.append(0)
                            dx_pos.append(0)
                            dy_neg.append(0)
                            dy_pos.append(0)
                        s.plotIndex.append([plot_ind,100])
                        plot_ind += 1
        if len(x) > 0:
            dx = [dx_neg,dx_pos]
            dy = [dy_neg,dy_pos]
            ax.errorbar(x,y, xerr = dx, yerr = dy, fmt = 'ob', gid = 100)
            ax.set_xlim([1e-4,1e+4])
            ax.set_ylim([1e-4,1e+4])
            ax.set_xscale('log')
            ax.set_yscale('log')
            kx = np.linspace(1e-4,1e+4,100)
            y3 = const.KAL_K4*kx**const.KAL_M4
            y4 = const.KAL_K0*kx**const.KAL_M0
            if opt == 3:
                ax.plot(kx,y3,'r', gid = 1)
            if opt == 4:
                ax.plot(kx,y4,'r', gid = 1)
            if not hideMarked:
                self.drawMarkers(fig)
        else:
            print("Warning: Too few data points. No plotting.")
        fig.tight_layout()
        return fig
    
    def drawMarkers(self,fig):
        """
        Draw a circular marker around all marked samples in a plot."""
        for ax in fig.axes:
            mlines = []
            rlines = []
            #remove old markers
            for i in range(len(ax.lines)):
                if ax.lines[i].get_gid() == 99:
                    rlines.append(i)
                else:
                    mlines.append(i)
            j = 0
            for i in rlines:
                ax.lines[i-j].remove()
                j += 1
            #draw new markers
            for l in mlines:
                if ax.lines[l].get_gid() >= 100:
                    x,y = ax.lines[l].get_data()
                    xm = []
                    ym = []
                    for i in range(len(x)):
                        s = self.getPlottedSample(i,ax.lines[l].get_gid())
                        if s != None:
                            if s.marked:
                                xm.append(x[i])
                                ym.append(y[i])
                    msize = ax.lines[l].get_markersize()
                    ax.plot(xm, ym, 'o', markeredgecolor = 'r', markerfacecolor = 'none', 
                            markeredgewidth = 2, markersize = msize*3, gid = 99)
        fig.canvas.draw()
        fig.canvas.flush_events()
    
    def statQuant(self,quantity,isotope,statq, p = 95):
        """
        Calculate statistcial qantity 'statq' with
        possible values (only one):
        'mean', 'median', 'max', 'min', 'var', 'percentile', 'std'.
        'p' is used when calculating the p:th percentile 
        for 'quantity' with possible values (only one):
        AC, LC, MDC, A, LCA, MDA for 'isotope'
        sXeVol; 'isotope' ignored in this case. 
        """
        q = np.array([])
        iso = isotope.upper()
        for s in self.set:
            if quantity == 'AC':
                if iso == 'XE-133' and 'XE-133' in s.isoPassed:
                    q = np.append(q,s.AC_133)
                if iso == 'XE-131M' and 'XE-131M' in s.isoPassed:
                    q = np.append(q,s.AC_131m)
                if iso == 'XE-133M' and 'XE-133M' in s.isoPassed:
                    q = np.append(q,s.AC_133m)
                if iso == 'XE-135' and 'XE-135' in s.isoPassed:
                    q = np.append(q,s.AC_135)
                if iso == 'RN-222' and 'RN-222' in s.isoPassed:
                    q = np.append(q,s.AC_Rn)
            if quantity == 'LC':
                if iso == 'XE-133' and 'XE-133' in s.isoPassed:
                    q = np.append(q,s.LC_133)
                if iso == 'XE-131M' and 'XE-131M' in s.isoPassed:
                    q = np.append(q,s.LC_131m)
                if iso == 'XE-133M' and 'XE-133M' in s.isoPassed:
                    q = np.append(q,s.LC_133m)
                if iso == 'XE-135' and 'XE-135' in s.isoPassed:
                    q = np.append(q,s.LC_135)
                if iso == 'RN-222' and 'RN-222' in s.isoPassed:
                    q = np.append(q,s.LC_Rn)
            if quantity == 'LC_nc':
                if iso == 'XE-133' and 'XE-133' in s.isoPassed:
                    if s.LC_133_nc > 0:
                        q = np.append(q,s.LC_133_nc)
                if iso == 'XE-131M' and 'XE-131M' in s.isoPassed:
                    if s.LC_131m_nc > 0:
                        q = np.append(q,s.LC_131m_nc)
                if iso == 'XE-133M' and 'XE-133M' in s.isoPassed:
                    if s.LC_133m_nc > 0:
                        q = np.append(q,s.LC_133m_nc)
                if iso == 'XE-135' and 'XE-135' in s.isoPassed:
                    if s.LC_135_nc > 0:
                        q = np.append(q,s.LC_135_nc)
                if iso == 'RN-222' and 'RN-222' in s.isoPassed:
                    if s.LC_Rn_nc > 0:
                        q = np.append(q,s.LC_Rn_nc)
            if quantity == 'MDC':
                if iso == 'XE-133' and 'XE-133' in s.isoPassed:
                    q = np.append(q,s.MDC_133)
                if iso == 'XE-131M' and 'XE-131M' in s.isoPassed:
                    q = np.append(q,s.MDC_131m)
                if iso == 'XE-133M' and 'XE-133M' in s.isoPassed:
                    q = np.append(q,s.MDC_133m)
                if iso == 'XE-135' and 'XE-135' in s.isoPassed:
                    q = np.append(q,s.MDC_135)
                if iso == 'RN-222' and 'RN-222' in s.isoPassed:
                    q = np.append(q,s.MDC_Rn)
            if quantity == 'A':
                if iso == 'XE-133' and 'XE-133' in s.isoPassed:
                    q = np.append(q,s.A_133)
                if iso == 'XE-131M' and 'XE-131M' in s.isoPassed:
                    q = np.append(q,s.A_131m)
                if iso == 'XE-133M' and 'XE-133M' in s.isoPassed:
                    q = np.append(q,s.A_133m)
                if iso == 'XE-135' and 'XE-135' in s.isoPassed:
                    q = np.append(q,s.A_135)
                if iso == 'RN-222' and 'RN-222' in s.isoPassed:
                    q = np.append(q,s.A_Rn)
            if quantity == 'LCA':
                if iso == 'XE-133' and 'XE-133' in s.isoPassed:
                    q = np.append(q,s.LCA_133)
                if iso == 'XE-131M' and 'XE-131M' in s.isoPassed:
                    q = np.append(q,s.LCA_131m)
                if iso == 'XE-133M' and 'XE-133M' in s.isoPassed:
                    q = np.append(q,s.LCA_133m)
                if iso == 'XE-135'and 'XE-135' in s.isoPassed:
                    q = np.append(q,s.LCA_135)
                if iso == 'RN-222' and 'RN-222' in s.isoPassed:
                    q = np.append(q,s.LCA_Rn)
            if quantity == 'MDA':
                if iso == 'XE-133' and 'XE-133' in s.isoPassed:
                    q = np.append(q,s.MDA_133)
                if iso == 'XE-131M' and 'XE-131M' in s.isoPassed:
                    q = np.append(q,s.MDA_131m)
                if iso == 'XE-133M' and 'XE-133M' in s.isoPassed:
                    q = np.append(q,s.MDA_133m)
                if iso == 'XE-135'and 'XE-135' in s.isoPassed:
                    q = np.append(q,s.MDA_135)
                if iso == 'RN-222' and 'RN-222' in s.isoPassed:
                    q = np.append(q,s.MDA_Rn)
            if quantity == 'sXeVol':
                q = np.append(q,s.xeVol)
        if len(q) < 2:
            print("Warning: Too few samples to calculate statistics. returning -99")
            return -99
        if statq == 'mean':
            return np.mean(q)
        elif statq == 'min':
            return np.min(q)
        elif statq == 'max':
            return np.max(q)
        elif statq == 'median':
            return np.median(q)
        elif statq == 'var':
            return np.var(q)
        elif statq == 'std':
            return np.std(q)
        elif statq == 'percentile':
            return np.percentile(q,p)
        else:
            print("'statq' option not recognized")
            
    def getDetections(self,opt,isotope):
        """ 
        Calculate detection rate using opt = 'LC', 'LC99' or 'LC_nc'
        for 'isotope'. 
        Returns <number of detections>,<fraction detected>
        """
        iso = isotope.upper()
        n = 0
        if opt == 'LC' or opt == 'LC99':
            for s in self.set:
                if s.detected(opt,iso) and iso in s.isoPassed:
                    n += 1
            ns = self.getNSamples()
            if ns > 0:
                return n, float(n)/float(ns)
            else:
                print("Warning: no detections found.")
                return 0,0
        if opt == 'LC_nc':
            nNan = 0
            for s in self.set:
                det, nan = s.detected(opt,iso) 
                if det and not nan and iso in s.isoPassed:
                    n += 1
                if nan:
                    nNan += 1
            ns = self.getNSamples()
            if ns > 0:
                return n, float(n)/float(ns), nNan
            else:
                print("Warning: no detections found.")
                return 0,0        

    def getIsotopeCombinations(self,opt):
        """
           Get number of samples for different combinations
           of detected isotopes. opt = 'LC' or 'LC99'
        """
        comb = np.zeros((16),int)
        for s in self.set:
            bp = s.getDetectionBP(opt)
            for i in range(16):
                if bp == i:
                    comb[i] += 1
        return comb
    
    def makeReport(self):
        """Make a measurement set report string"""
        cmin,cmax = self.getFirstLastCollTime()
        sta = ''
        for st in self.stationList:
            sta += st + ' (' + str(self.getNSamples(st)) +') '
        txt = '\n\nMeasurement Set report\n'
        txt += '----------------------\n'
        txt += '{:<30s}{:<4d}\n'.format('Total number of samples:', len(self.set))
        txt += '{:<30s}{:<20s}\n'.format('Stations (samples):', sta)
        txt += '{:<30s}{:<15s}\n'.format('First collection start:', cmin.strftime("%Y-%m-%d %H:%M:%S"))
        txt += '{:<30s}{:<15s}\n'.format('Last collection start:', cmax.strftime("%Y-%m-%d %H:%M:%S"))
        txt += self.printStatistics('sXeVol')
        txt += self.printStatistics('AC')
        txt += self.printStatistics('LC')
        txt += self.printStatistics('MDC')
        #txt += self.printStatistics('LC_nc')
        txt += self.printDetectionStatistics()
        txt += self.printDetectionPattern('LC')
        #txt += self.printDetectionPattern('LC99')
        #txt += self.printDetectionPattern('LC_nc')
        self.report = txt
        
    def printStatistics(self, opt):
        """
        Print statistics for a selected quantity. 
        See documentation for 'statQuant' for options.
        """
        txt = ''
        txt += '\n\nStatistics for ' + opt + '\n\n'
        if opt == 'sXeVol':
            txt += '{:<8s}{:<8s}{:<8s}{:<8s}{:<8s}{:<8s}\n'.format(
                   'Max','Min','Mean','Median','Var','95th_p')
            txt += '--------------------------------------------------------\n'
            txt += '{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}\n'.format(
                self.statQuant(opt,'','max'),
                self.statQuant(opt,'','min'),
                self.statQuant(opt,'','mean'),
                self.statQuant(opt,'','median'),
                self.statQuant(opt,'','var'),
                self.statQuant(opt,'','percentile',95))
            txt += '--------------------------------------------------------\n'
        else:   
            txt += '{:<10s}{:<8s}{:<8s}{:<8s}{:<8s}{:<8s}{:<8s}\n'.format(
                    'Isotope','Max','Min','Mean','Median','Var','95th_p')
            txt += '--------------------------------------------------------\n'
            txt += '{:<10s}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}\n'.format(
                    'Xe-133',
                    self.statQuant(opt,'Xe-133','max'),
                    self.statQuant(opt,'Xe-133','min'),
                    self.statQuant(opt,'Xe-133','mean'),
                    self.statQuant(opt,'Xe-133','median'),
                    self.statQuant(opt,'Xe-133','var'),
                    self.statQuant(opt,'Xe-133','percentile',95))
            txt += '{:<10s}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}\n'.format(
                    'Xe-131m',
                    self.statQuant(opt,'Xe-131m','max'),
                    self.statQuant(opt,'Xe-131m','min'),
                    self.statQuant(opt,'Xe-131m','mean'),
                    self.statQuant(opt,'Xe-131m','median'),
                    self.statQuant(opt,'Xe-131m','var'),
                    self.statQuant(opt,'Xe-131m','percentile',95))
            txt += '{:<10s}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}\n'.format(
                    'Xe-133m',
                    self.statQuant(opt,'Xe-133m','max'),
                    self.statQuant(opt,'Xe-133m','min'),
                    self.statQuant(opt,'Xe-133m','mean'),
                    self.statQuant(opt,'Xe-133m','median'),
                    self.statQuant(opt,'Xe-133m','var'),
                    self.statQuant(opt,'Xe-133m','percentile',95))
            txt += '{:<10s}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}\n'.format(
                    'Xe-135',
                    self.statQuant(opt,'Xe-135','max'),
                    self.statQuant(opt,'Xe-135','min'),
                    self.statQuant(opt,'Xe-135','mean'),
                    self.statQuant(opt,'Xe-135','median'),
                    self.statQuant(opt,'Xe-135','var'),
                    self.statQuant(opt,'Xe-135','percentile',95))
            txt += '{:<10s}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}{:<8.3f}\n'.format(
                    'Rn-222',
                    self.statQuant(opt,'Rn-222','max'),
                    self.statQuant(opt,'Rn-222','min'),
                    self.statQuant(opt,'Rn-222','mean'),
                    self.statQuant(opt,'Rn-222','median'),
                    self.statQuant(opt,'Rn-222','var'),
                    self.statQuant(opt,'Rn-222','percentile',95))
            txt += '--------------------------------------------------------\n'
        return txt
    
    def printDetectionStatistics(self):
        """Print detection statistics for the set"""
        
        n_133_lc,f_133_lc = self.getDetections('LC','Xe-133')
        n_131m_lc,f_131m_lc = self.getDetections('LC','Xe-131m')
        n_133m_lc,f_133m_lc = self.getDetections('LC','Xe-133m')
        n_135_lc,f_135_lc = self.getDetections('LC','Xe-135')
        n_rn_lc,f_rn_lc = self.getDetections('LC','Rn-222')
        n_133_lc99,f_133_lc99 = self.getDetections('LC99','Xe-133')
        n_131m_lc99,f_131m_lc99 = self.getDetections('LC99','Xe-131m')
        n_133m_lc99,f_133m_lc99 = self.getDetections('LC99','Xe-133m')
        n_135_lc99,f_135_lc99 = self.getDetections('LC99','Xe-135')
        n_rn_lc99,f_rn_lc99 = self.getDetections('LC99','Rn-222')
        txt = ''
        txt += '\n\nDetection Statistics\n\n'
        txt += '{:<10s}{:<10s}{:<10s}{:<10s}{:<10s}\n'.format(
                'Isotope','LC_samp','LC_frac','LC99_samp','LC99_frac')
        txt += '-----------------------------------------------------\n'
        txt += '{:<10s}{:<10d}{:<10.3f}{:<10d}{:<10.3f}\n'.format(
                'Xe-133', n_133_lc, f_133_lc, n_133_lc99, f_133_lc99)
        txt += '{:<10s}{:<10d}{:<10.3f}{:<10d}{:<10.3f}\n'.format(
                'Xe-131m', n_131m_lc, f_131m_lc, n_131m_lc99, f_131m_lc99)
        txt += '{:<10s}{:<10d}{:<10.3f}{:<10d}{:<10.3f}\n'.format(
                'Xe-133m', n_133m_lc, f_133m_lc, n_133m_lc99, f_133m_lc99)
        txt += '{:<10s}{:<10d}{:<10.3f}{:<10d}{:<10.3f}\n'.format(
                'Xe-135', n_135_lc, f_135_lc, n_135_lc99, f_135_lc99)
        txt += '{:<10s}{:<10d}{:<10.3f}{:<10d}{:<10.3f}\n'.format(
                'Rn-222', n_rn_lc, f_rn_lc, n_rn_lc99, f_rn_lc99)
        txt += '------------------------------------------------------\n'
        return txt
    
    def printDetectionPattern(self,opt):
        txt = ''
        comb = self.getIsotopeCombinations(opt)
        if sum(comb) > 0:
            txt += '\n{:<30s}{:<6s}\n'.format('Isotope detection pattern for',opt)
            txt += '{:<50s}\n'.format('Bit (1,2,3,4) = (Xe-133,Xe-131m,Xe-133m,Xe-135)')
            txt += '--------------------------------\n'
            i = 0
            for c in comb:
                txt += '{:<15s}{:<10d}{:<3.3f}\n'.format(bin(i),c,float(c)/float(sum(comb)))
                i += 1
            txt += '{:<15s}{:<10d}{:<3.3f}\n'.format('Sum:', sum(comb),1)
            txt += '--------------------------------\n'
        else:
            print("Warning: no detections found.")
            txt += 'No detections in bitpattern using ' + opt + '\n'
        return txt
    
    def csv(self):
        """Return string with data for all samples on CSV format"""
        acUnit = self.set[0].unit + "/m3"
        aUnit = self.set[0].unit
        header = "Sample file    , Station, Detector   , SRID, Coll. Start, Coll. Stop, Acq. Start.,"
        header += "Air Volume (m3), XeVol (ml), XeVol Err (ml), Yield, Yield Err, Analysis Method,"
        header += format("AC_133 (%s), ACErr_133 (%s),  ACErrNonStat_133 (%s),  LC_133 (%s),  MDC_133 (%s)," %(acUnit, acUnit, acUnit, acUnit, acUnit))      
        header += format("AC_131m (%s), ACErr_131m (%s),  ACErrNonStat_131m (%s),  LC_131m (%s),  MDC_131m (%s)," %(acUnit, acUnit, acUnit, acUnit, acUnit))      
        header += format("AC_133m (%s), ACErr_133m (%s),  ACErrNonStat_133m (%s),  LC_133m (%s),  MDC_133m (%s)," %(acUnit, acUnit, acUnit, acUnit, acUnit))      
        header += format("AC_135 (%s), ACErr_135 (%s),  ACErrNonStat_135 (%s),  LC_135 (%s),  MDC_135 (%s)," %(acUnit, acUnit, acUnit, acUnit, acUnit))
        header += format("AC_Rn (%s), ACErr_Rn (%s),  ACErrNonStat_Rn (%s),  LC_Rn (%s),  MDC_Rn (%s)," %(acUnit, acUnit, acUnit, acUnit, acUnit))
        header += format("A_133 (%s), AErr_133 (%s),  AErrNonStat_133 (%s),  LCA_133 (%s),  MDA_133 (%s)," %(aUnit, aUnit, aUnit, aUnit, aUnit))      
        header += format("A_131m (%s), AErr_131m (%s),  AErrNonStat_131m (%s),  LCA_131m (%s),  MDA_131m (%s)," %(aUnit, aUnit, aUnit, aUnit, aUnit))      
        header += format("A_133m (%s), AErr_133m (%s),  AErrNonStat_133m (%s),  LCA_133m (%s),  MDA_133m (%s)," %(aUnit, aUnit, aUnit, aUnit, aUnit))      
        header += format("A_135 (%s), AErr_135 (%s),  AErrNonStat_135 (%s),  LCA_135 (%s),  MDA_135 (%s)," %(aUnit, aUnit, aUnit, aUnit, aUnit))  
        header += format("A_Rn (%s), AErr_Rn (%s),  AErrNonStat_Rn (%s),  LCA_Rn (%s),  MDA_Rn (%s)\n" %(aUnit, aUnit, aUnit, aUnit, aUnit))
        data = header
        for s in self.set:
            data += s.csvLine()
        return data
    