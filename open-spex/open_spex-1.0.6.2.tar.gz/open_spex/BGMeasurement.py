#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 12:10:43 2020

@author: ringbom

This file is part of 'openSpex'
Copyright (c) 2021 Swedish Defence Research Agency (FOI)
"""
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import copy

from open_spex import utils as ut

# (1 << k) | n will set bit k in n
MSG_TYPE_ERR = (1 << 0) | 0
MSG_ID_ERR = (1 << 1) | 0
DATA_TYPE_ERR = (1 << 2) | 0 
HEADER_ERR = (1 << 3) | 0
COMMENT_ERR = (1 << 4) | 0
COLL_ERR = (1 << 5) | 0
ACQ_ERR = (1 << 6) | 0
PROC_ERR = (1 << 7) | 0
CAL_ERR = (1 << 8) | 0
G_ENERGY_ERR = (1 << 9) | 0 
B_ENERGY_ERR = (1 << 10) | 0
G_RES_ERR = (1 << 11) | 0
B_RES_ERR = (1 << 12) | 0
G_EFF_ERR = (1 << 13) | 0
ROI_LIM_ERR = (1 << 14) | 0
BG_EFF_ERR = (1 << 15) | 0
RATIO_ERR = (1 << 16) | 0
G_SPECT_ERR = (1 << 17) | 0
B_SPECT_ERR = (1 << 18) | 0
BG_SPECT_ERR = (1 << 19) | 0
ZERO_GROSS = (1 << 21) | 0
ROI_CHAN_LIM_ERR = (1 << 22) | 0
CERTIFICATE_ERR = (1 << 23) | 0

class BGMeasurement(object):
    """ 
    Class handling a beta-gamma measurement.
    Parameters
    ==========
    stationType      'CUBE' or 'SAUNA'
    fileName         filename if data source is a IMS2.0 text file
    verbose          More printout if 'True'. Default is false.
    makeHist         If 'True' (default), make histograms. If 'False', no histograms are made.
                     This can be useful when analysis is done without plotting spectra 
                     (saves time and memory).
    calibrate        'True' (default): calibrate the sample. 
         
    The following histograms are created:
        
    beta_gamma_hist
    gamma_hist
    beta_hist
    beta_coinc_hist 
    gamma_coinc_hist 
    beta350_hist 
    beta250_hist
    beta81_hist 
    beta30_hist 
    
    """
    def __init__(self, stationType, fileName, verbose = False, makeHist = True, calibrate = True):
     
        self.verbose = verbose
        self.status = 0
        self.stationType = stationType
        self.makeHist = makeHist
        self.sampleId = None
        self.fileName = fileName
        if self.verbose:
            print("Parsing PHD-file ",self.fileName)
        with open(self.fileName, 'r') as f:
            data = f.read()
            self.parsePHDData(data)
        self.dataSource = 'FILE'
        if self.msg_type == 'CUBE':
            self.stationType = 'CUBE'
        self.checkStatus()
        if self.errors:
            return
        #self.tweaked = False
        if calibrate:
            self.calibrate()
            #store calibration data to allow changes later
            self.calib_date_orig = copy.deepcopy(self.calib_date)
            self.gEnergy_orig = copy.deepcopy(self.gEnergy)
            self.gResolution_orig = copy.deepcopy(self.gResolution)
            self.bEnergy_orig = copy.deepcopy(self.bEnergy)
            self.bResolution_orig = copy.deepcopy(self.bResolution)
            self.ROI_limits_ene_orig = copy.deepcopy(self.ROI_limits_ene)
            self.ROI_limits_chan_orig = copy.deepcopy(self.ROI_limits_chan)
            self.bg_eff_orig = copy.deepcopy(self.bg_eff)
            self.ratio_orig = copy.deepcopy(self.ratio)
            #self.gEfficiency_orig = self.gEfficiency
        if self.makeHist:
            self.makeInfo()
        self.db = None     
        self.buildIMSFileName()
    
            
    def buildIMSFileName(self):
        """Constructs the file name used to save data in IMS-format"""
        dt = self.data_type.replace('PHD','')
        if hasattr(self,"collstart_time"):
            self.phdFileName = format('%s-%s-%d-%s.PHD'%(self.detector, 
                                  self.collstart_time.strftime("%Y-%m-%d--%H-%M-%S"),
                                  self.acq_realtime, dt))
        else:
            self.phdFileName = format('%s-%s-%d-%s.PHD'%(self.detector, 
                                  self.acq_start.strftime("%Y-%m-%d--%H-%M-%S"),
                                  self.acq_realtime, dt))
        
    def parsePHDData(self,data):
        """
        Parse data in IMS2.0 - format
        
        Parameters
        ----------
        data          text string in IMS2.0 format
        """
        nok1 = 1
        nok2 = 1
        nok3 = 1
        for line in data.splitlines():
            w = line.split()
            if 'MSG_TYPE' in line:
                self.msg_type = w[1]
                nok1 = 0
            if 'MSG_ID' in line:
                self.msg_id = line.replace("MSG_ID ","")
                nok2 = 0
            if 'DATA_TYPE' in line:
                self.data_type = w[1]
                nok3 = 0
        self.status += nok1*MSG_TYPE_ERR + nok2*MSG_ID_ERR + nok3*DATA_TYPE_ERR
        #
        # Header block
        #
        block = ut.get_block(data,'#Header')
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l == 1:
                    self.station = w[0]
                    self.detector = w[1]
                    self.qual = w[4]
                if l == 2:
                    self.srid = w[0]
                if l == 3:
                    self.sample_id = w[0]
                    self.detbk_id = w[1]
                    self.gasbk_id = w[2]
                if l == 4:
                    date = w[0] + " " + w[1]
                    d = ut.readDate(date)
                    if not d:
                        break
                    else:
                        self.transmit_time = d
                l += 1
        else:
            self.status += HEADER_ERR
        #
        # Comment block
        #
        block = ut.get_block(data,'#Comment')
        self.comment = ''
        if len(block) > 0:
            i = 0
            for line in block:
                if i > 0:
                    self.comment += line
                i += 1
        else:
            self.status += COMMENT_ERR
        #
        # Collection block
        #
        if self.data_type == 'SAMPLEPHD' or self.data_type == 'SPIKEPHD' or self.data_type == 'REGENPHD':
            block = ut.get_block(data,'#Collection')
            if len(block) > 0:
                l = 0
                for line in block:
                    w = line.split()
                    if l == 1:
                        date = w[0] + " " +  w[1]
                        d = ut.readDate(date)
                        if not d:
                            break
                        else:
                            self.collstart_time = d
                        date = w[2] + " " + w[3]
                        d = ut.readDate(date)
                        if not d:
                            break
                        else:
                            self.collstop_time = d
                        self.air_volume = float(w[4])
                    l += 1
            else:
                self.status += COLL_ERR
        #
        # Acquisition block
        #
        block = ut.get_block(data,'#Acquisition')
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l == 1:
                    date = w[0] + " " +  w[1]
                    d = ut.readDate(date)
                    if not d:
                        break
                    else:
                        self.acq_start = d
                    self.acq_realtime = float(w[2])
                    self.acq_livetime = float(w[3])
                l += 1
        else:
            self.status += ACQ_ERR
        #
        # Processing block
        #
        if self.data_type == 'SAMPLEPHD' or self.data_type == 'SPIKEPHD'or self.data_type == 'REGENPHD':
            block = ut.get_block(data,'#Processing')
            if len(block) > 0:
                l = 0
                for line in block:
                    w = line.split()
                    if l == 1:
                        self.xe_vol = float(w[0])
                        self.xe_vol_err = float(w[1])
                    if l == 2:
                        self.xe_yield = float(w[0])
                        self.xe_yield_err = float(w[1])
                    if l == 3:
                        self.archive_nbr = w[0]
                    l += 1
            else:
                self.status += PROC_ERR
        #
        # Calibration block
        #
        block = ut.get_block(data,'#Calibration')
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l == 1:
                    date = w[0] + " "  + w[1]
                    d = ut.readDate(date)
                    if not d:
                        break
                    else:
                        self.calib_date = d
                l += 1
        else:
            self.status += CAL_ERR
        #
        # g_Energy block
        #
        block = ut.get_block(data,'#g_Energy')
        self.gEnergy = []
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l > 0:
                    self.gEnergy.append([float(w[0]), float(w[1]), float(w[2])])
                l += 1
        else:
            self.status += G_ENERGY_ERR

        #
        # g_Resolution block
        #
        block = ut.get_block(data,'#g_Resolution')
        self.gResolution = []
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l > 0:
                    self.gResolution.append([float(w[0]), float(w[1]), float(w[2])])
                l += 1
        else:
            self.status += G_RES_ERR
        #
        # b_Energy block
        #
        block = ut.get_block(data,'#b_Energy')
        self.bEnergy = []
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l > 0:
                    self.bEnergy.append([float(w[0]), float(w[2]), float(w[3])])
                l += 1
        else:
            self.status += B_ENERGY_ERR
        #
        # b_Resolution block
        #
        block = ut.get_block(data,'#b_Resolution')
        self.bResolution = []
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l > 0:
                    self.bResolution.append([float(w[0]), float(w[1]), float(w[2])])
                l += 1
        else:
            self.status += B_RES_ERR
        #
        # g_Efficiency block
        #
        block = ut.get_block(data,'#g_Efficiency')
        self.gEfficiency = []
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l > 0:
                    self.gEfficiency.append([float(w[0]), float(w[1]), float(w[2])])
                l += 1
        else:
            self.status += G_EFF_ERR
        #
        # ROI_Limits block
        #
        block = ut.get_block(data,'#ROI_Limits')
        self.ROI_limits_ene = []
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l > 0:
                    self.ROI_limits_ene.append([int(w[0]), float(w[1]), \
                                    float(w[2]), float(w[3]), float(w[4])])
                l += 1
        else:
            self.status += ROI_LIM_ERR
        #
        # ROI_Chan_Limits block (for CUBE only)
        #
        self.ROI_limits_chan = []
        if self.msg_type == 'CUBE':
            block = ut.get_block(data,'#ROI_Chan_Limits')
            #self.ROI_limits_chan = []
            if len(block) > 0:
                l = 0
                for line in block:
                    w = line.split()
                    if l > 0:
                        self.ROI_limits_chan.append([int(float(w[0])), int(float(w[1])), \
                                        int(float(w[2])), int(float(w[3])), int(float(w[4]))])
                    l += 1
            else:
                self.status += ROI_CHAN_LIM_ERR
        #
        # b-gEfficiency block
        #
        block = ut.get_block(data,'#b-gEfficiency')
        self.bg_eff = []
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l > 0:
                    self.bg_eff.append([w[0], int(w[1]), float(w[2]), float(w[3])])
                l += 1
            if len(self.bg_eff) != 9:
                 self.status += BG_EFF_ERR
        else:
            self.status += BG_EFF_ERR
        #
        # Ratios block
        #
        block = ut.get_block(data,'#Ratios')
        self.ratio = []
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l > 0:
                    self.ratio.append([w[0], int(w[1]), int(w[2]), float(w[3]), float(w[4])])
                l += 1
            if (len(self.ratio) != 16 and len(self.ratio) != 18):
                self.status += RATIO_ERR
        else:
            self.status += RATIO_ERR
        #
        # g_Spectrum block
        #
        block = ut.get_block(data,'#g_Spectrum')
        self.gamma = []
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l == 1:
                    self.ngamma_chan = int(w[0])
                    self.gamma_maxenergy = float(w[1])
                if l > 1:
                    i = 0
                    for word in w:
                        if i > 0:
                            self.gamma.append(int(word))
                        i += 1
                l += 1
        else:
            self.status += G_SPECT_ERR
        #
        # b_Spectrum block
        #
        block = ut.get_block(data,'#b_Spectrum')
        self.beta = []
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l == 1:
                    self.nbeta_chan = int(w[0])
                    self.beta_maxenergy = float(w[1])
                if l > 1:
                    i = 0
                    for word in w:
                        if i > 0:
                            self.beta.append(int(word))
                        i += 1
                l += 1
        else:
            self.status += B_SPECT_ERR
        #
        # Histogram block
        #
        block = ut.get_block(data,'#Histogram')
        self.beta_gamma = []
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l == 1:
                    self.nbg_gamma_chan = int(w[0])
                    self.nbg_beta_chan = int(w[1])
                    self.nbg_gamma_maxene = int(w[2])
                    self.nbg_beta_maxene = int(w[3])
                if l > 1:
                    for word in w:
                        self.beta_gamma.append(int(word))
                l += 1
        else:
            self.status += BG_SPECT_ERR
        #
        # Certification block
        #
        block = ut.get_block(data,'#Certificate')
        self.certificate = ''
        if len(block) > 0:
             i = 0
             for line in block:
                 if i > 0: 
                     self.certificate += line
                 i += 1
        else:
            self.status += CERTIFICATE_ERR

    def checkStatus(self):
        """Check status of data parsing"""
        self.warnings = False
        self.errors = False
        if self.status & MSG_TYPE_ERR:
            print("Error in MSG_TYPE")
            self.errors = True
        if self.status & MSG_ID_ERR:
            print("Error in MSG_ID")
            self.errors = True
        if self.status & DATA_TYPE_ERR:
            print("Error in  DATA_TYPE")
            self.errors = True
        if self.status & HEADER_ERR:
            print("Error in  #Header")
            self.errors = True
        if self.status & COMMENT_ERR:
            print("Warning: #Comment not found")
            self.warnings = True
        if self.status & COLL_ERR:
            print("Error in #Collection")
            self.errors = True
        if self.status & ACQ_ERR:
            print("Error in  #Acquisition")
            self.errors = True
        if self.status & PROC_ERR:
            print("Error in  #Processing")
            self.errors = True
        if self.status & CAL_ERR:
            print("Warning: #Calibration not found")
            self.warnings = True
        if self.status & G_ENERGY_ERR:
            print("Warning: #g_Energy not found")
            self.warnings = True
        if self.status & G_RES_ERR:
            print("Warning: #g_Resolution not found")
            self.warnings = True
        if self.status & B_ENERGY_ERR:
            print("Warning: #b_Energy not found in")
            self.warnings = True
        if self.status & B_RES_ERR:
            print("Warning: #b_Resolution not found")
            self.warnings = True
        if self.status & G_EFF_ERR:
            print("Warning: #g_Efficiency not found")
            self.warnings = True
        if self.status & ROI_LIM_ERR:
            print("Warning: #ROI_Limits not found")
            self.warnings = True
        if self.status & ROI_CHAN_LIM_ERR:
            print("Warning: #ROI_Chan_Limits not found")
            self.warnings = True
        if self.status & BG_EFF_ERR:
            print("Warning: #b-gEfficiency incomplete")
            self.warnings = True
        if self.status & RATIO_ERR:
            print("Warning: #Ratios incomplete")
            self.warnings = True
        if self.status & G_SPECT_ERR:
            print("Error in  #g_Spectrum")
            self.errors = True
        if self.status & B_SPECT_ERR:
            print("Error in #b_Spectrum")
            self.errors = True
        if self.status & BG_SPECT_ERR:
            print("Error in #Histogram")
            self.errors = True
        if self.status & CERTIFICATE_ERR:
            #print("Warning: no #Certificate block")
            self.warnings = True
        if self.status & ZERO_GROSS:
            self.errors = True
        # Other errors:
        if self.errors == False:
            if self.acq_realtime == 0 or self.acq_livetime == 0:
                print("Error: acq_livetime =  %f acq_realtime = %f " 
                      %(self.acq_livetime, self.acq_realtime))
                self.status += ACQ_ERR
                self.errors = True
            if sum(self.beta_gamma) == 0:
                print("Error: Beta-gamma histogram is empty.")
                self.status += BG_SPECT_ERR
                self.errors = True
            if self.data_type == 'SAMPLEPHD' or \
                                    self.data_type == 'REGENPHD' or \
                                    self.data_type == 'SPIKEPHD':
                if self.xe_vol <= 0:
                    print("Warning: Xenon volume %6.6f <= 0 " %self.xe_vol)
                    self.status += PROC_ERR
                    self.warnings = True
                if self.xe_vol > 0. and self.xe_vol <= 0.3:
                    print("Warning: Xenon volume= %6.6f" %self.xe_vol)
                    self.warnings = True
                coll_time =  (self.collstop_time - 
                              self.collstart_time).total_seconds()
                if coll_time < 0 or coll_time > 24*3600:
                    print("Error: Collection time = %d" %coll_time)
                    self.status += COLL_ERR
                    self.errors = True
    
      
    def printLoadedCalibration(self):
        """Print calibration data."""
        txt = format("\n\nCalibration for a %s %s measurement with acquisition start %s\n"
                     %(self.stationType, self.data_type, self.acq_start))
        txt += "===========================================================================================\n"
        txt += format("Calibration date: %s\n" %self.calib_date)
        txt += format("\nGamma energy\n")
        for d in self.gEnergy:
            txt += format("%3.3f\t%3.3f\t%3.3f\n" %(d[0], d[1], d[2]))
        txt += format("\nGamma resolution\n")
        for d in self.gResolution:
            txt += format("%3.3f\t%3.3f\t%3.3f\n" %(d[0], d[1], d[2]))
        txt += format("\nElectron energy\n")
        for d in self.bEnergy:
            txt += format("%3.3f\t%3.3f\t%3.3f\n" %(d[0], d[1], d[2]))
        txt += format("\nElectron resolution\n")
        for d in self.bResolution:
            txt += format("%3.3f\t%3.3f\t%3.3f\n" %(d[0], d[1], d[2]))
        txt += format("\nROI limits in keV\n")
        for d in self.ROI_limits_ene:
            txt += format("%d\t%3.3f\t%3.3f\t%3.3f\t%3.3f\n" %(d[0], d[1], d[2], d[3], d[4]))
        if self.stationType == 'CUBE':
            txt += format("\nROI limits in channels\n")
            for d in self.ROI_limits_chan:
                txt += format("%d\t%3.3f\t%3.3f\t%3.3f\t%3.3f\n" %(d[0], d[1], d[2], d[3], d[4]))
        txt += format("\nROI efficiency\n")
        for d in self.bg_eff:
            txt += format("%s\t%d\t%3.3f\t%3.3f\n" %(d[0], d[1], d[2], d[3]))
        txt += format("\nInterference ratios\n")
        for d in self.ratio:
            txt += format("%s\t%d\t%d\t%3.3f\t%3.3f\n" %(d[0], d[1], d[2], d[3], d[4]))
        print(txt)
        
                        
    def calibrate(self, tweakParam = None):
        """
        Calibrates beta- and gamma energy scales. 
        Calculates ROI limits in channels and ROI counts. 
        Makes histograms and calculates countrates
        
        Parameters
        ==========
        tweakParam = [offsetBeta, tweakBeta,offsetGamma,tweakGamma]; default = None
        """
        #Calibrate
        self.calMethod = "Station"
        self.calibrated = False
        if len(self.gEnergy) < 2 or len(self.bEnergy) < 2:
            print("Warning: Calibration data is missing. Cannot calibrate.")
            self.ROI_limits_chan = []
            self.roi_counts = []
            self.calMethod = "Not performed"
            return
        self.pol_g_ene_chan = ut.fit_polynom(self.gEnergy,2)
        self.pol_b_ene_chan = ut.fit_polynom(self.bEnergy,2)
        self.pol_g_ene_fwhm = ut.fit_polynom(self.gResolution,2)
        self.pol_b_ene_fwhm = ut.fit_polynom(self.bResolution,2)
        #if self.stationType == 'CUBE' and self.dataSource != 'FILE':
        #This requires that ROIs are given in at least one of energies and channels:
        if len(self.ROI_limits_ene) == 0:
            self.ROI_limits_ene = []
            for x in self.ROI_limits_chan:
                self.ROI_limits_ene.append([x[0],ut.invert_pol(x[1],self.pol_b_ene_chan), \
                  ut.invert_pol(x[2],self.pol_b_ene_chan), ut.invert_pol(x[3],self.pol_g_ene_chan), \
                  ut.invert_pol(x[4],self.pol_g_ene_chan)])
        if len(self.ROI_limits_chan) == 0:
        #if self.stationType == 'SAUNA' or self.dataSource == 'FILE':
            #Calculate ROI limits in int channels (rounded)
            self.ROI_limits_chan = []
            for x in self.ROI_limits_ene:
                self.ROI_limits_chan.append([x[0],int(self.pol_b_ene_chan(x[1])+0.5), \
                  int(self.pol_b_ene_chan(x[2])+0.5), int(self.pol_g_ene_chan(x[3])+0.5), \
                  int(self.pol_g_ene_chan(x[4])+0.5)])
            self.ROI_limits_chan_orig = copy.deepcopy(self.ROI_limits_chan)
        #Tweak ROIs if tweakParam exists
        if tweakParam != None:
            self.tweaked = True
            self.calMethod = "Tweaked"
            for roi in self.ROI_limits_chan:
                roi[1] = roi[1]*tweakParam[1] + tweakParam[0]
                roi[2] = roi[2]*tweakParam[1] + tweakParam[0]
                roi[3] = roi[3]*tweakParam[3] + tweakParam[2]
                roi[4] = roi[4]*tweakParam[3] + tweakParam[2]
        else:
            self.tweaked = False
        self.tweakParam = tweakParam
        #Calculate ROI counts
        self.roi_counts = np.zeros(len(self.ROI_limits_chan))
        for g in range(self.nbg_gamma_chan):
            for b in range(self.nbg_beta_chan):
                cont = self.beta_gamma[g*self.nbg_beta_chan + b]
                i = 0
                for roi in self.ROI_limits_chan:
                    if b >= roi[1] and b< roi[2] and g >= roi[3] and g < roi[4]: 
                        self.roi_counts[i] += cont
                    i += 1
        if sum(self.roi_counts) == 0:
            print("Error: Zero gross counts")
            self.status += ZERO_GROSS
        #Make histograms
        if self.makeHist:
            self.beta_gamma_hist = ut.histogram2D([self.nbg_gamma_chan, self.nbg_beta_chan], 
                                                  self.beta_gamma, 
                                                  title = 'Beta-Gamma', 
                                                  xlabel = 'Electron energy (chan)', 
                                                  ylabel = 'Gamma energy (chan)')
            self.gamma_hist = ut.histogram1D(self.ngamma_chan,self.gamma,
                                self.data_type + ' ' + "Gamma singles", 'Energy (chan)', 'Counts/bin',
                                liveTime = self.acq_livetime)
            self.gammaSinglesCR = sum(self.gamma_hist.data[0:])
            self.beta_hist = ut.histogram1D(self.nbeta_chan,self.beta,
                                self.data_type + ' ' + "Beta singles", 'Energy (chan)', 'Counts/bin',
                                liveTime = self.acq_livetime)
            self.betaSinglesCR = sum(self.gamma_hist.data[0:])
            self.coincCR = sum(self.beta_gamma[0:])
            beta_350 = np.zeros(self.nbg_beta_chan)
            beta_250 = np.zeros(self.nbg_beta_chan)
            beta_81 = np.zeros(self.nbg_beta_chan)
            beta_30 = np.zeros(self.nbg_beta_chan)
            gamma_coinc = np.zeros(self.nbg_gamma_chan)
            beta_coinc = np.zeros(self.nbg_beta_chan)
            for g in range(self.nbg_gamma_chan):
                for b in range(self.nbg_beta_chan):
                        beta_coinc[b] += self.beta_gamma[g*self.nbg_beta_chan + b]
                if g >= self.ROI_limits_chan[0][3] and g < self.ROI_limits_chan[0][4]: 
                    for b in range(self.nbg_beta_chan):
                        beta_350[b] += self.beta_gamma[g*self.nbg_beta_chan + b]
                if g >= self.ROI_limits_chan[1][3] and g < self.ROI_limits_chan[1][4]: 
                    for b in range(self.nbg_beta_chan):
                        beta_250[b] += self.beta_gamma[g*self.nbg_beta_chan + b]
                if g >= self.ROI_limits_chan[2][3] and g < self.ROI_limits_chan[2][4]: 
                    for b in range(self.nbg_beta_chan):
                        beta_81[b] += self.beta_gamma[g*self.nbg_beta_chan + b]
                if g >= self.ROI_limits_chan[3][3] and g < self.ROI_limits_chan[3][4]: 
                    for b in range(self.nbg_beta_chan):
                        beta_30[b] += self.beta_gamma[g*self.nbg_beta_chan + b]
            for b in range(self.nbg_beta_chan):
                for g in range(self.nbg_gamma_chan):
                    #gamma_coinc[g] += self.beta_gamma[g*self.nbg_beta_chan + b]
                    # Note change back!!!
                    if b > 0 and g > 0: 
                            gamma_coinc[g] += self.beta_gamma[g*self.nbg_beta_chan + b]
            self.beta350_hist = ut.histogram1D(self.nbg_beta_chan,beta_350,
                                        self.data_type + ' ' + "Beta 350 keV gamma", 'Energy (chan)', 'Counts/bin',
                                        liveTime = self.acq_livetime)
            self.beta250_hist = ut.histogram1D(self.nbg_beta_chan,beta_250,
                                        self.data_type + ' ' + "Beta 250 keV gamma", 'Energy (chan)', 'Counts/bin',
                                        liveTime = self.acq_livetime)
            self.beta81_hist = ut.histogram1D(self.nbg_beta_chan,beta_81,
                                        self.data_type + ' ' + "Beta 81 keV gamma", 'Energy (chan)', 'Counts/bin',
                                        liveTime = self.acq_livetime)
            self.beta30_hist = ut.histogram1D(self.nbg_beta_chan,beta_30,
                                        self.data_type + ' ' + "Beta 30 keV gamma", 'Energy (chan)', 'Counts/bin',
                                        liveTime = self.acq_livetime)
            self.beta_coinc_hist = ut.histogram1D(self.nbg_beta_chan,beta_coinc,
                                        self.data_type + ' ' + "Beta total coincidence", 'Energy (chan)', 'Counts/bin',
                                        liveTime = self.acq_livetime)
            self.gamma_coinc_hist = ut.histogram1D(self.nbg_gamma_chan,gamma_coinc,
                                        self.data_type + ' ' + "Gamma total coincidence", 'Energy (chan)', 'Counts/bin',
                                        liveTime = self.acq_livetime)
        self.calibrated = True
        self.makeInfo()
        
    def resetROIs(self):
        """Set ROI limits to original calibration"""
        self.ROI_limits_chan = copy.deepcopy(self.ROI_limits_chan_orig)

    def get1DHistList(self, opt):
        """
        Make a list with the histograms. 
        This can be used in plotting menus etc. 
        
        Parameters
        ----------
        opt          'beta' or 'gamma'
        """
        if opt != 'gamma' and opt != 'beta':
            print("Wrong option in get1DHistList.")
            return
        hl = []
        if opt == 'gamma':
            hl.append(self.gamma_hist)
            hl.append(self.gamma_coinc_hist)
        if opt == 'beta':
            hl.append(self.beta_hist)
            hl.append(self.beta_coinc_hist)
            hl.append(self.beta30_hist)
            hl.append(self.beta81_hist)
            hl.append(self.beta250_hist)
            hl.append(self.beta350_hist)
        return hl
    
    def show_histograms(self):
        """ Show gamma, beta, and beta-gamma histograms """
        fig = plt.figure(constrained_layout=True, figsize=[10,9])
        gs = GridSpec(3,3, figure=fig)
        ax1 = fig.add_subplot(gs[1,-1])
        ax2 = fig.add_subplot(gs[2,-1])
        ax3 = fig.add_subplot(gs[1:,:-1])
        self.gamma_coinc_hist.draw(ax1)
        self.beta_coinc_hist.draw(ax2)
        self.beta_gamma_hist.draw(fig,ax3,self.ROI_limits_chan)
        plt.show()
            
    def makeInfo(self):
        """ Make brief measurement information string"""
        txt = format("Detector: %s\n" % self.detector)
        txt += format("Type: %s Qualifier: %s\n" % (self.data_type, self.qual))
        txt += format("Calibration method: %s\n" % self.calMethod)
       # txt += format("Calibration date: %s\n" % self.calib_date.strftime("%Y-%m-%d %H:%M:%S"))
        if self.data_type == 'SAMPLEPHD' or \
            self.data_type == 'SPIKEPHD' or \
            self.data_type == 'REGENPHD':
                    txt += format("Coll. start: %s\n" % self.collstart_time.strftime("%Y-%m-%d %H:%M:%S"))
                    txt += format("Coll. stop: %s\n" % self.collstop_time.strftime("%Y-%m-%d %H:%M:%S"))
                    txt += format("Air volume: %2.2f m3\n" %self.air_volume)
                    txt += format("Xe Vol: %1.3f +/- %1.3f ml\n" 
                                  %(self.xe_vol, self.xe_vol_err))
                    txt += format("Yield: %1.2f +/- %1.2f\n" 
                                  %(self.xe_yield, self.xe_yield_err))
        txt += format("Acq. start: %s\n" % self.acq_start.strftime("%Y-%m-%d %H:%M:%S"))
        txt += format("Real: %s  Live: %s\n" % (self.acq_realtime, self.acq_livetime))
        if self.makeHist:
            txt += format("Gamma  singles CR: %1.3e\n" % (self.gammaSinglesCR/self.acq_livetime))
            txt += format("Beta  singles CR: %1.3e\n" % (self.betaSinglesCR/self.acq_livetime))
            txt += format("Beta-gamma coinc. CR: %1.3e\n" % (self.coincCR/self.acq_livetime))
        self.info = txt
        
  
            
    def IMSFormat(self):
        """Create data string on IMS format""" 
        #Assign dummy values for data not used by CUBE-systems"
        if self.stationType == 'CUBE':
            self.msg_type = 'CUBE'
            self.msg_id = "1 DUMMY"
            self.qual = 'FULL'
            self.sample_id = "SAMPLE_ID_DUMMY"
            self.detbk_id = "DETBK_ID_DUMMY"
            self.gasbk_id = "GASBK_ID_DUMMY"
            self.archive_nbr = '00'
            self.gamma_maxenergy = 999
            self.beta_maxenergy = 999
            self.nbg_gamma_maxene = 999
            self.nbg_beta_maxene = 999
            self.gEfficiency = []
            if self.data_type != 'SAMPLEPHD':
                self.srid = 'DUMMYSRID'
        #Write buffer
        buf = format("BEGIN IMS2.0\n")
        buf += format("MSG_TYPE %s\n" %self.msg_type)
        buf += format("MSG_ID %s\n" %self.msg_id)
        buf += format("DATA_TYPE %s\n" %self.data_type)
        buf += format("#Header 3\n")
        buf += format("%s %s B GEOMETRY   %s\n" %(self.station, self.detector, self.qual))
        buf += format("%s\n" %self.srid)
        buf += format("%s    %s     %s\n" %(self.sample_id, self.detbk_id, self.gasbk_id))
        date_time = self.transmit_time.strftime("%Y/%m/%d %H:%M:%S.0")
        buf += format("%s\n" %date_time)
        buf += format("#Comment\n")
        buf += format("%s\n" %self.comment)
        if self.data_type == 'SAMPLEPHD':
            buf += format("#Collection\n")
            coll_start = self.collstart_time.strftime("%Y/%m/%d %H:%M:%S.0")
            coll_stop = self.collstop_time.strftime("%Y/%m/%d %H:%M:%S.0")
            buf += format("%s %s %2.6f\n" %(coll_start, coll_stop,self.air_volume))
        buf += format("#Acquisition\n")
        acq_start = self.acq_start.strftime("%Y/%m/%d %H:%M:%S.0")
        buf += format("%s %5.6f %5.6f\n" %(acq_start, self.acq_realtime, self.acq_livetime))
        if self.data_type == 'SAMPLEPHD':
            buf += format("#Processing\n")
            buf += format("%2.5f %2.5f\n" %(self.xe_vol, self.xe_vol_err))
            buf += format("%2.5f %2.5f\n" %(self.xe_yield, self.xe_yield_err))
            buf += format("%s\n" %self.archive_nbr)
        buf += format("#Calibration\n")
        date_time = self.calib_date.strftime("%Y/%m/%d %H:%M:%S.0")
        buf += format("%s\n" %date_time)
        buf += format("#g_Energy\n")
        for e in self.gEnergy:
            buf += format("%2.6f\t%2.6f\t%2.6f\n" %(e[0], e[1], e[2]))
        buf += format("#b_Energy\n")
        for e in self.bEnergy:
            buf += format("%2.6f\tC %2.6f\t%2.6f\n" %(e[0], e[1], e[2]))
        buf += format("#g_Resolution\n")
        for e in self.gResolution:
            buf += format("%2.6f\t%2.6f\t%2.6f\n" %(e[0], e[1], e[2]))
        buf += format("#b_Resolution\n")
        for e in self.bResolution:
            buf += format("%2.6f\t%2.6f\t%2.6f\n" %(e[0], e[1], e[2]))
        buf += format("#g_Efficiency\n")
        for e in self.gEfficiency:
            buf += format("%2.6f\t%1.6f\t%1.6f\n" %(e[0], e[1], e[2]))
        buf += format("#ROI_Limits\n")
        for r in self.ROI_limits_ene:
            buf += format("%d\t%3.5f\t%3.5f\t%3.5f\t%3.5f\n" %(r[0], r[1], r[2], r[3], r[4]))
        #Also write ROIs in channels if this is a CUBE
        if self.stationType == 'CUBE':
            buf += format("#ROI_Chan_Limits\n")
            for r in self.ROI_limits_chan:
                buf += format("%d\t%d\t%d\t%d\t%d\n" %(r[0], r[1], r[2], r[3], r[4]))
        buf += format("#b-gEfficiency\n")
        for e in self.bg_eff:
            buf += format("%s\t%d\t%1.6f\t%1.6f\n" %(e[0], e[1], e[2], e[3]))
        buf += format("#Ratios\n")
        for r in self.ratio:
            buf += format("%s\t%d\t%d\t%1.6f\t%1.6f\n" %(r[0], r[1], r[2], r[3], r[4]))
        buf += format("#g_Spectrum\n")
        buf += format("%d\t%d\n" %(self.ngamma_chan, self.gamma_maxenergy))
        i = 0
        for c in range(self.ngamma_chan):
            if not c % 5: 
                buf += format("%d\t%d\t%d\t%d\t%d\t%d\n" %(i,
                        self.gamma[i], self.gamma[i+1], self.gamma[i+2], 
                        self.gamma[i+3], self.gamma[i+4]))
                
                i += 5
                if (self.ngamma_chan - i) < 5: break
        m = self.ngamma_chan - i
        if m > 0:
            buf += format("%d\t" %i)
            for j in range(m):
                buf += format("%d\t" %self.gamma[i+j])
        buf += '\n'
        buf += format("#b_Spectrum\n")
        buf += format("%d\t%d\n" %(self.nbeta_chan, self.beta_maxenergy))
        i = 0
        for c in range(self.nbeta_chan):
            if not c % 5: 
                buf += format("%d\t%d\t%d\t%d\t%d\t%d\n" %(i,
                        self.beta[i], self.beta[i+1], self.beta[i+2], 
                        self.beta[i+3], self.beta[i+4]))
                
                i += 5
                if (self.nbeta_chan - i) < 5: break
        m = self.nbeta_chan - i
        if m > 0:
            buf += format("%d\t" %i)
            for j in range(m):
                buf += format("%d\t" %self.beta[i+j])
        buf += '\n'
        buf += format("#Histogram\n")
        buf += format("%d\t%d\t%d\t%d\n" %(self.nbg_gamma_chan, 
                                               self.nbg_beta_chan, 
                                               self.nbg_gamma_maxene, 
                                               self.nbg_beta_maxene))
        i = 0
        for c in self.beta_gamma:
            if i > 0 and not (i % self.nbg_beta_chan):
                buf += '\n'
            buf += format("%d " %c)
            i += 1
        if (self.stationType != 'CUBE'):
            if not (self.status & CERTIFICATE_ERR):
                buf += format("#Certificate\n")
                buf += self.certificate
        buf += '\nSTOP'
        return buf  