#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 21:41:15 2020

@author: ringbom

This file is part of 'openSpex'
Copyright (c) 2021 Swedish Defence Research Agency (FOI)
"""
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import os
import numpy as np

from open_spex import BGMeasurement as bg
from open_spex import bgm as bgm



font = 'Liberation Mono'
if os.name == 'nt':
    font = 'Courier New'

class BGSample:
    """
    A beta-gamma sample with sample, gas background (optional), 
    detector background, and qc (optional).
    Created either by using BGMeasurement objects or filenames.
    
    Parameters
    ----------
    sample: BGMeasurement or filename string
    detbk:  BGMeasurement or filename string 
    gasbk:  BGMeasurement or filename string (optional) 
    qc:     BGMeasurement or filename string (optional) 
    """
    def __init__(self, sample, detbk, gasbk= None, qc = None):
        
        if isinstance(sample, str):
            self.sample = bg.BGMeasurement(sample)
        else:
            self.sample = sample
        if isinstance(detbk, str):
            self.detbk = bg.BGMeasurement(detbk)
        else:
            self.detbk = detbk
        if isinstance(gasbk, str):
            self.gasbk = bg.BGMeasurement(gasbk)
        else:
            self.gasbk = gasbk
        if isinstance(qc, str):
            self.qc = bg.BGMeasurement(qc)
        else:
            self.qc = qc
        if gasbk != None:
            self.tau = (self.sample.acq_start - self.gasbk.acq_start).total_seconds()
        else:
            self.tau = 0
        if hasattr(self.sample,"collstart_time"):
            self.collTime = (self.sample.collstop_time - self.sample.collstart_time).total_seconds()
            self.procTime = (self.sample.acq_start - self.sample.collstop_time).total_seconds()
        else:
            self.collTime = None
            self.procTime = None
            print("Sample has no collection info. Only activities can be calculated.")
        #self.check()
        self.bgmHandler = None
        self.analysisInfo = "Not analyzed"
        self.stationType = self.sample.stationType
        self.makeInfo()
            
    def bgmAnalysis(self, combine = True, verbose = False, ingrowth = True, 
                    unit = 0.001, optROI = False):
        """
        Do a BGM-analysis.
        Parameters:
        ----------
        combine             True (default)/False. Use different combinations of ROI7-10 in the Xe-133 calculation 
                            depending on detection pattern. If 'False', use original BGM. 
        ingrowth            True (default)/False. Correct for Xe-133m->Xe133 ingrowth if Xe133m detected.
        verbose             True/False (default). More printout.
        unit                1 = Bq or 0.001 (default) = mBq
        """
        self.bgmHandler = bgm.bgmHandler(self, verbose)
        bgm.bgm(self.bgmHandler, combine, unit=unit, ingrowth = ingrowth)
        self.makeAnalysisInfo()
    
    def bgmAnalysis3(self, verbose = False, unit = 0.001):
        """This is for testing only. Does a BGM - analysis without using the BGSample object.""" 
        if self.gasbk != None:
            gAcqLive = self.gasbk.acq_livetime
            gAcqReal = self.gasbk.acq_realtime
        else:
            gAcqLive = None
            gAcqReal = None
        tau =   self.tau
        collTime = self.collTime
        procTime = self.procTime
        sAcqReal = self.sample.acq_realtime
        sAcqLive = self.sample.acq_livetime
        dAcqReal = self.detbk.acq_realtime
        dAcqLive = self.detbk.acq_livetime
        xeVol = self.sample.xe_vol
        xeVolErr = self.sample.xe_vol_err
        eff = np.zeros(18)
        i = 0
        for e in self.sample.bg_eff:
            eff[i] = e[2]
            eff[i+9] = e[3]
            i += 1
        ratio = np.zeros(32)
        i = 0
        for r in self.sample.ratio:
            ratio[i] = r[3]
            ratio[i+16] = r[4]
            i += 1
        sampleGross = self.sample.roi_counts
        detbkGross = self.detbk.roi_counts
        if self.gasbk != None:
            gasbkGross = self.gasbk.roi_counts
        else:
            gasbkGross = None
        setup = [tau, collTime, procTime, sAcqReal, sAcqLive, gAcqReal, 
                 gAcqLive, dAcqReal, dAcqLive, xeVol, xeVolErr]
        print("setup = " , setup)
        print("eff = ", eff)
        print("ratio = ", ratio)
        print("sample gross = ", sampleGross)
        print("gasbk gross = ", gasbkGross)
        print("detbk gross = ", detbkGross)
        self.bgmHandler = bgm.bgmHandler(None, verbose, setup, eff, ratio, 
                                    sampleGross, gasbkGross, detbkGross)
        bgm.bgm(self.bgmHandler, unit=unit)
        
    def makeInfo(self):
        """Make a string with some collection information."""
        txt = format("Station: %s\n" % self.sample.station)
        txt = format("Detector: %s\n" % self.sample.detector)
        if hasattr(self.sample, "collstart_time"):
            txt = format("Coll. start: %s\n" % self.sample.collstart_time)
            txt = format("Coll. stop: %s\n" % self.sample.collstop_time)
        self.info = txt
        
    def makeAnalysisInfo(self):
        """Make a string with essential analysis results"""
        if self.bgmHandler.inputErrors:
            self.analysisInfo = "Input errors. No analysis performed."
            return
        txt = format("Analysis method: %s\n\n" %self.bgmHandler.analysisMethod)
        if not self.bgmHandler.activityOnly:
            ac =  self.bgmHandler.AC
            ace =  self.bgmHandler.ACErr
            lc =  self.bgmHandler.LC
            txt += '{:<10s}{:<17s}{:<7s}{:<7s}\n'.format('','AC [mBq/m3]',' LC','Detected') 
            txt += '------------------------------------------\n'
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7d}\n'.format('Xe-133:',self.bgmHandler.Xe133AC,'+/-',
                            self.bgmHandler.Xe133ACErr, self.bgmHandler.Xe133ACLC, self.bgmHandler.xe133Det)   
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7d}\n'.format('Xe-131m:',ac[4],'+/-',ace[4], lc[4], self.bgmHandler.xe131mDet)
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7d}\n'.format('Xe-133m:',ac[5],'+/-',ace[5], lc[5], self.bgmHandler.xe133mDet) 
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7d}\n'.format('Xe-135:',ac[1],'+/-',ace[1], lc[1], self.bgmHandler.xe135Det)     
            txt += '------------------------------------------\n'
        else:
            a =  self.bgmHandler.A
            ae =  self.bgmHandler.AErr
            lc =  self.bgmHandler.LCA
            txt += '{:<10s}{:<17s}{:<7s}{:<7s}\n'.format('','A [mBq]',' LC', 'Detected') 
            txt += '------------------------------------------\n'
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7d}\n'.format('Xe-133:',self.bgmHandler.Xe133A,'+/-',
                            self.bgmHandler.Xe133AErr, self.bgmHandler.Xe133ALC, self.bgmHandler.xe133Det)   
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7d}\n'.format('Xe-131m:',a[4],'+/-',ae[4], lc[4], self.bgmHandler.xe131mDet)
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7d}\n'.format('Xe-133m:',a[5],'+/-',ae[5], lc[5], self.bgmHandler.xe133mDet) 
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7d}\n'.format('Xe-135:',a[1],'+/-',ae[1], lc[1], self.bgmHandler.xe135Det)     
            txt += '------------------------------------------\n'
        self.analysisInfo = txt
        
    def plot(self):
        """Plot sample histograms and analysis info"""
        fig = plt.figure(constrained_layout=True, figsize=[10,9])
        gs = GridSpec(2,2, figure=fig)
        ax1 = fig.add_subplot(gs[0,0])
        ax2 = fig.add_subplot(gs[1,0])
        ax4 = fig.add_subplot(gs[0,1])
        ax3 = fig.add_subplot(gs[1,1])
        self.sample.gamma_hist.draw(ax1)
        self.sample.beta_hist.draw(ax2)
        self.sample.drawBGHist(fig,ax3)
        txt = self.info + "\n" + self.analysisInfo
        font_dict = {'family': font, 'color':'black', 'size':12}
        ax4.axis('off')
        ax4.text(0., 0.95, txt, va='top', fontdict = font_dict)
        plt.show()