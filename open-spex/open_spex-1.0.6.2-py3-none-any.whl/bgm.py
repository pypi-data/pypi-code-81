#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:38:03 2020

@author: Anders Ringbom; Swedish Defence Research Agency (FOI)
         anders.ringbom@foi.se
         
         version 2.0.0: Major revision of algorithm. Only activity matrices calculated. Activity conentrations
                        calculated afterwards. 
                        Non-statistical error now calculated using Monte Carlo. 
                        Error breakdown added. 
                        ValueError now raised if matrix inversion fails. 
                        (2021-03-26)
         version 1.0.4: Corrected minor bug when Lc calculated for gas background (2021-03-05)  
         version 1.0.3: Corrected bug when activities only calculated (2021-01-04)       
         version 1.0.2: Modified handling of input errors
         version 1.0.1: Four metastable interference factors included in matrix.
"""
import numpy as np
import math
from open_spex import const
from scipy.stats import norm
from datetime import datetime
import copy
import time

#THIS IS THE VERSION NUMBER. REMEMBER TO CHANGE WHEN UPDATES ARE MADE
#####################################################################
VERSION = '2.0.0'    #Changed 2021-03-24
#####################################################################

kROI_1=1
kROI_2=2
kROI_3=4
kROI_4=8
kROI_5=16
kROI_6=32
kROI_7=64
kROI_8=128
kROI_9= 256
kROI_10=512 

class bgmHandler:
    """
    A class handling BGM-analysis input and results.  
    Set up the analysis EITHER using a BGSample instance OR by 
    specifying all data with the lists 
    'setup','eff','ratio','scounts', 'gcounts' (optional), and 'dcounts'
    
    Parameters
    ----------
    sample:             A BGSample instance to be analyzed. If this is specified,
                        no other parameters except 'verbose' should be set.
    verbose:            True/False. More printout. Default = 'False'
    setup:              A list with analysis setup data on the following format:
                        [<tau (s) i.e. time difference between sample and gasbk acq start>, 
                        <collection time (s)>, 
                        <process time (s)>, 
                        < sample real acqt (s)>, 
                        < sample live acqt (s)> 
                        < gasbk real acqt (s)>  (optional, set to 'None' if not used)
                        < gasbk live acqt (s)>  (optional, set to 'None' if not used) 
                        < detbk real acqt (s)>, 
                        < detbk live acqt (s)> 
                        < xe vol (ml) >, 
                        < xe vol err (ml) > ]
    eff:                Efficiencies and their errors for ROI 2-10 
                        [eff_2, ... eff_10, eff_err_2, ... eff_err10]
    ratio:              Interference ratios and their errors
                        If metastable inteference ratios not included:
                        [rat_1, ... rat_16, rat_err_1, ... rat_err_16]
                        else:
                        [rat_1, ... rat_18, rat_err_1, ... rat_err_18]
    scounts:            ROI gross counts in sample. [c1, c2, ..., c10]
    gcounts:            ROI gross counts in gasbk. [c1, c2, ..., c10] (optional, set to 'None' if not used)
    dcounts:            ROI gross counts in detbk. [c1, c2, ..., c10]
    """
    def __init__(self, sample = None, verbose = False, setup= [], eff = [], ratio = [],
                  scounts = [], gcounts = [], dcounts = []):
        self.version = VERSION
        self.inputErrors = False
        if sample == None and (len(setup) !=11 or len(eff) != 18 
                               or (len(ratio) != 32 and len(ratio) != 36 and len(ratio) != 40)
                               or len(scounts) != 10 or len(dcounts) != 10):
            print("Error in bgm input: Wrong data format.")
            self.inputErrors = True
            return
        self.verbose = verbose
        # Sample used
        if sample != None:
            if sample.gasbk == None:
                self.gAcqLive = None
                self.gAcqReal = None
                self.gAcqStart = None
                self.gasbkUsed = False
                self.pol_g_ene_chan_gasbk = None
                self.pol_b_ene_chan_gasbk = None
                self.pol_g_ene_fwhm_gasbk = None
                self.pol_b_ene_fwhm_gasbk = None
            else:
                self.gAcqLive = sample.gasbk.acq_livetime
                self.gAcqReal = sample.gasbk.acq_realtime
                self.gAcqStart = sample.gasbk.acq_start
                self.gasbkUsed = True
                self.pol_g_ene_chan_gasbk = sample.gasbk.pol_g_ene_chan
                self.pol_b_ene_chan_gasbk = sample.gasbk.pol_b_ene_chan
                self.pol_g_ene_fwhm_gasbk = sample.gasbk.pol_g_ene_fwhm
                self.pol_b_ene_fwhm_gasbk = sample.gasbk.pol_b_ene_fwhm
            self.activityOnly = True
            if hasattr(sample.sample,"collstart_time"):
                self.activityOnly = False
            if  hasattr(sample.sample,"xe_vol"):
                if sample.sample.xe_vol <= 0:
                    self.activityOnly = True
                    print("Warning in bgm input: xenon volume <=0. Only activites calculated.") 
            if  hasattr(sample,"collTime"):
                if sample.collTime != None:
                    if sample.collTime <= 0:
                        self.activityOnly = True
                        print("Warning in bgm input: collection time <=0. Only activites calculated.")
            self.srid = sample.sample.srid
            self.station = sample.sample.station
            self.detector = sample.sample.detector
            self.sAcqStart = sample.sample.acq_start
            self.dAcqStart = sample.detbk.acq_start
            self.comment = sample.sample.comment
            self.tau =   sample.tau
            if self.tau < 0:
                print("Error in bgm input: Negative tau (%d s)" %self.tau)
                self.inputErrors = True
                return
            self.sAcqReal = sample.sample.acq_realtime
            self.sAcqLive = sample.sample.acq_livetime
            self.dAcqReal = sample.detbk.acq_realtime
            self.dAcqLive = sample.detbk.acq_livetime
            self.tweaked = sample.sample.tweaked
            self.tweakParam = sample.sample.tweakParam
            self.calibrationMethod = sample.sample.calMethod
            self.pol_g_ene_chan_sample = sample.sample.pol_g_ene_chan
            self.pol_b_ene_chan_sample = sample.sample.pol_b_ene_chan
            self.pol_g_ene_fwhm_sample = sample.sample.pol_g_ene_fwhm
            self.pol_b_ene_fwhm_sample = sample.sample.pol_b_ene_fwhm
            self.pol_g_ene_chan_detbk = sample.detbk.pol_g_ene_chan
            self.pol_b_ene_chan_detbk = sample.detbk.pol_b_ene_chan
            self.pol_g_ene_fwhm_detbk = sample.detbk.pol_g_ene_fwhm
            self.pol_b_ene_fwhm_detbk = sample.detbk.pol_b_ene_fwhm
            if not self.activityOnly:
                self.collStart = sample.sample.collstart_time
                self.collStop = sample.sample.collstop_time
                self.collTime = sample.collTime
                self.procTime = sample.procTime
                self.airVol = sample.sample.air_volume
                self.xeVol = sample.sample.xe_vol
                self.xeVolErr = sample.sample.xe_vol_err
                self.xeYield = sample.sample.xe_yield
                self.xeYieldErr = sample.sample.xe_yield_err
                self.V = self.xeVol/const.XE_AIR
                self.dV = self.xeVolErr/const.XE_AIR
                if self.procTime <= 0:
                    print("Error in bgm input: Negative process time (%d s)" %self.procTime)
                    self.inputErrors = True
                    return
                    if self.procTime > 24*3600:
                        print("Warning in bgm input: Process time (%d s) longer than 24 hours." %self.procTime)
            else:
                self.collStart = None
                self.collStop = None
                self.collTime = None
                self.procTime = None
                self.airVol = None
                self.xeVol = None
                self.xeVolErr = None
                self.xeYield = None
                self.xeYieldErr = None
                self.V = None
                self.dV = None
            if len(sample.sample.bg_eff) != 9:
                print("Error in bgm input: b-g eficiencies incomplete.")
                self.inputErrors = True
                return
            if (len(sample.sample.ratio) != 16 and len(sample.sample.ratio) != 18
                and len(sample.sample.ratio) != 20):
                print("Error in bgm input: Interference ratios incomplete.")
                self.inputErrors = True
                return
            self.eff = np.zeros(18)
            i = 0
            for e in sample.sample.bg_eff:
                self.eff[i] = e[2]
                self.eff[i+9] = e[3]
                i += 1
            self.ratio = np.zeros(len(sample.sample.ratio)*2)
            i = 0
            for r in sample.sample.ratio:
                self.ratio[i] = r[3]
                self.ratio[i+len(sample.sample.ratio)] = r[4]
                i += 1
            self.sampleGross = sample.sample.roi_counts
            if (sum(self.sampleGross) == 0):
                print("Error in bgm input: Zero sample gross counts.")
                self.inputErrors = True
                return
            self.detbkGross = sample.detbk.roi_counts
            if (sum(self.detbkGross) == 0):
                print("Error in bgm input: Zero detbk gross counts.")
                self.inputErrors = True
                return
            if self.gasbkUsed:
                self.gasbkGross = sample.gasbk.roi_counts
                if (sum(self.gasbkGross) == 0):
                    print("Error in bgm input: Zero gasbk gross counts.")
                    self.inputErrors = True
                    return
            else:
                self.gasbkGross = None
            self.roiLimits = sample.sample.ROI_limits_chan
        #Data used
        if sample == None and len(setup) == 11:
            self.srid = None
            if setup[5] != None:
                self.gasbkUsed = True
            else: 
                self.gasbkUsed = False
            self.tau = setup[0]
            self.collTime = setup[1]
            self.procTime = setup[2]
            self.sAcqReal = setup[3]
            self.sAcqLive = setup[4]
            self.gAcqReal = setup[5]
            self.gAcqLive = setup[6]
            self.dAcqReal = setup[7]
            self.dAcqLive = setup[8]
            self.xeVol = setup[9]
            self.xeVolErr = setup[10]
            self.eff = eff
            self.ratio = ratio
            self.sampleGross = scounts
            self.detbkGross = dcounts
            if self.gasbkUsed:
                self.gasbkGross = gcounts
            else:
                self.gasbkGross = None
            self.V = self.xeVol/const.XE_AIR
            self.dV = self.xeVolErr/const.XE_AIR
        # No parameters specified. Create empty handler.
        if sample == None and len(setup) == 0:
            self.inputErrors = None
            self.sample = None
            self.comment = None
            self.srid = None
            self.tau = None
            self.collTime = None
            self.procTime = None
            self.sAcqReal = None
            self.sAcqLive = None
            self.gAcqReal = None
            self.gAcqLive = None
            self.dAcqReal = None
            self.dAcqLive = None
            self.gAcqStart = None
            self.sAcqStart = None
            self.dAcqStart = None
            self.gasbkUsed = None
            self.station = None
            self.detector = None
            self.collStart = None
            self.collStop = None
            self.airVol
            self.xeVol = None
            self.xeVolErr = None
            self.xeYield = None
            self.xeYieldErr = None
            self.eff = None
            self.ratio = None
            self.sampleGross = None
            self.detbkGross = None
            self.gasbkGross = None
            self.V = None
            self.dV = None
            self.roiLimits = None
            self.combLCZeroSample = None
            self.combLCZeroGasbk = None
        # result attributes
        self.combined= True
        self.unitscale = None
        self.dimension = None
        self.ingrowth = True
        self.grossCounts = None
        self.grossCountsDBcorr = None 
        self.grossCountsDBcorrErr = None
        self.netCounts = None
        self.netCountsErr = None
        self.netCountsLC = None
        self.netCountsMDC = None
        self.bgrCounts = None
        self.bgrCountsErr = None
        self.bgrCountsBayes = None
        self.ResponseMatrix_A = None
        self.ResponseErrorMatrix_A = None
        self.InvResponseMatrix_A = None
        #self.InvResponseErrorMatrix_A= None
        self.CovMatrix_A = None 
        #self.ResponseMatrix_AC = None
        #self.ResponseErrorMatrix_AC = None
        #self.InvResponseMatrix_AC = None
        #self.InvResponseErrorMatrix_AC= None
        #self.CovMatrix_AC = None 
        self.AC = None
        self.ACErr = None
        self.ACErrNonstat = None
        self.ACDX = None
        self.LC = None
        self.MDC = None
        self.A = None
        self.AErr = None
        self.AErrNonstat = None
        self.ADX = None
        self.LCA = None
        self.MDA = None
        self.AnalysisMethod = None
        self.F = None
        self.dsFact = None
        self.dgFact = None
        self.analysisTime = None
        self.roiBitPattern = 0
        self.xe131mDet = None
        self.xe133mDet = None
        self.xe133Det = None
        self.xe135Det = None
        self.alphaSample = None
        self.Xe133AC = None
        self.Xe133ACErr = None
        self.Xe133ACErrNonStat = None
        self.Xe133ACLC = None
        self.Xe133ACMDC = None
        self.Xe133ACVar0 = None
        self.Xe133A = None
        self.Xe133AErr = None
        self.Xe133AErrNonStat = None
        self.Xe133ALC = None
        self.Xe133AMDA = None
        self.alphaGasbk = None
        self.Xe133ACg = None
        self.Xe133ACErrg = None
        self.Xe133ACErrNonStatg = None
        self.Xe133ACLCg = None
        self.Xe133ACMDCg = None
        self.Xe133ACVar0g = None
        self.Xe133Ag = None
        self.Xe133AErrg = None
        self.Xe133AErrNonStatg = None
        self.Xe133ALCg = None
        self.Xe133AMDAg = None
        self.xi_ac = None
        self.xi_a = None
        self.Xe133A_dx = None
        self.Xe133AC_dx = None
        self.errBreakdown = False
        self.AErrNonstat_rat = None 
        self.AErrNonstat_br = None 
        self.AErrNonstat_eff = None
        self.combLCZeroSample = None
        
    def getXeCategory(self):
        """Returns FOI category"""
        det = self.A >= self.LCA #Detection matrix for all ROI's
        det_133 = self.Xe133AC >= self.Xe133ACLC #Xe-133 is a special case because it uses multiple ROI's
        det_131m = det[4]
        det_133m = det[5]
        det_135 = det[1]
        category = sum([det_133,det_131m,det_133m,det_135])
        return "FOI:G"+str(category)
        
    def report(self):
        """ Returns the analysis report as a string.
            Can only be used if the bgmHandler was created using a 'BGSample'
        """
        if self.srid == None:
            print("Error in report: bgmHandler probably not created using a 'BGSample'")
            return ''
        rep = str()
        if self.inputErrors:
            rep += "\nThere were input errors. No BGM analysis performed.\n"
            return rep
        rep += "\n\n\n#############################################################################################################\n"
        rep += format("BGM analysis report.\nVersion %s\n" %self.version)
        rep += "#############################################################################################################\n\n"
        rep += format('SRID: %s\n' %self.srid)
        rep += format('Analysis time: %s\n' %self.analysisTime)
        rep += format('Station: %s Detector: %s\n' %(self.station, self.detector))
        rep += format('Analysis method: %s\n' %self.analysisMethod)
        rep += format('Calibration method: %s\n' %self.calibrationMethod)
        pol = '['
        for p in self.pol_g_ene_chan_sample:
            pol += str(p) + ','
        pol += ']'
        rep += format('Sample gamma calibration polynom channel(energy): %s\n' %pol)
        pol = '['
        for p in self.pol_b_ene_chan_sample:
            pol += str(p) + ','
        pol += ']'
        rep += format('Sample beta calibration polynom channel(energy): %s\n' %pol)
        if self.tweaked:
            rep += "Calibration tweaked!\n"
            rep += format('Beta offset: %f Beta tweak: %f Gamma offset: %f Gamma tweak: %f\n' 
                          %(self.tweakParam[0], self.tweakParam[1], self.tweakParam[2], self.tweakParam[3]))
        if self.activityOnly:
            rep += "Collection information not complete. Only activies calculated\n"
        else:
            rep += format('Collection Start: %s Collection Stop: %s\n' %(self.collStart, self.collStop))
            rep += format('Collection time: %5.1f s\n' %self.collTime)
            rep += format('Air volume: %3.2f m3\n' %self.airVol)
            rep += format('Processing time: %5.1f s\n' %self.procTime)
            rep += format('Xenon volume: %1.3f +/- %1.3f ml\n' %(self.xeVol, self.xeVolErr))
            rep += format('Xenon yield: %1.3f +/- %1.3f\n' %(self.xeYield, self.xeYieldErr))
        if self.gasbkUsed:
            rep += format('Tau: %5.1f s\n' %self.tau)
        rep += format('Sample acq. start: %s \n' %self.sAcqStart)
        rep += format('Sample acq. Realtime: %s s Livetime: %s s (%3.3f%%)\n' %(self.sAcqReal, self.sAcqLive
                      ,self.sAcqLive/self.sAcqReal*100))
        if self.gasbkUsed:
            rep += format('Gasbk acq. start: %s \n' %self.gAcqStart)
            rep += format('Gasbk acq. Realtime: %s s Livetime: %s s (%3.1f%%)\n' %(self.gAcqReal, self.gAcqLive
                      ,self.gAcqLive/self.gAcqReal*100))
        rep += format('Detbk acq. start: %s \n' %self.dAcqStart)
        rep += format('Detbk acq. Realtime: %s s Livetime: %s s (%3.1f%%)\n\n' %(self.dAcqReal, self.dAcqLive
                      ,self.dAcqLive/self.dAcqReal*100))
        rep += format('Comment: %s\n\n' %self.comment)
        rep += format("ROI detection bitpattern: %s\n" %bin(self.roiBitPattern))
        ROI_4 = self.roiBitPattern & kROI_4 != 0
        ROI_7 = self.roiBitPattern & kROI_7 != 0
        ROI_8 = self.roiBitPattern & kROI_8 != 0
        ROI_9 = self.roiBitPattern & kROI_9 != 0
        ROI_10 = self.roiBitPattern & kROI_10 != 0
        rois = format("ROI:s used for Xe-133 analysis: ")
        rois += "3 "
        if self.combined:
            if ROI_4: rois += "4 "
            if ROI_7: rois += "7 "
            if ROI_8: rois += "8 "
            if ROI_9: rois += "9 "
            if ROI_10: rois += "10 "
        else:
            rois += "4 "
        rois += "\n"
        rep += rois
        rep += format("Correction for Xe-133m->Xe-133 ingrowth applied if Xe-133m detected:")
        if (self.ingrowth):
            rep += " YES\n"
            if not self.activityOnly:
                rep += format("AC ingrowth corr. factor xi (AC_133' = AC_133 - xi*AC_133m) = %f\n" %self.xi_ac)
            rep += format("A ingrowth corr. factor xi (A_133' = A_133 - xi*A_133m) = %f\n" %self.xi_a)
        else:
            rep += " NO\n"
        if self.combLCZeroSample and not self.combined:
            rep += format("WARNING: The ROI 3+4 zero-signal background variance <= 0 for the sample.\n")
            rep += format("The critical limit for the combined ROI 3+4 was set to min(LC_3,LC_4)\n")
        if self.combLCZeroGasbk and not self.combined:
            rep += format("WARNING: The ROI 3+4 zero-signal background variance <= 0 for the gas background.\n")
            rep += format("The critical limit for the combined ROI 3+4 was set to min(LC_8,LC_9)\n")
        
        if self.analysisTime != None:
            if not self.activityOnly:
                ac =  self.AC
                ace =  self.ACErr
                acen =  self.ACErrNonstat
                lc =  self.LC
                mc =  self.MDC
            a =  self.A
            ae =  self.AErr
            aen =  self.AErrNonstat
            l =  self.LCA
            m =  self.MDA
            det = self.A >= self.LCA
            if not self.activityOnly: 
                rep += format('Unit: %s or %s/m3\n\n' %(self.unit, self.unit))
                rep += '{:<10s} {:<7s} {:<7s} {:<7s} {:<7s} {:<7s} {:<7s} {:<7s} {:<7s} {:<7s} {:<7s} {:<7s}\n'.format( 
                          'Isotope','AC','staErr','sysErr','LC','MDC','A','staErr','sysErr','LCA','MDA', 'Detected')
                rep += "----------------------------------------------------------------------------------------------------\n"
                f1 = '{:<10s} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7d}\n'
                det_133 = self.Xe133AC >= self.Xe133ACLC
                rep += f1.format('Xe-133',self.Xe133AC, self.Xe133ACErr, self.Xe133ACErrNonStat, self.Xe133ACLC, self.Xe133ACMDC, 
                                 self.Xe133A, self.Xe133AErr, self.Xe133AErrNonStat, self.Xe133ALC, self.Xe133AMDA, det_133)
                rep += f1.format('Xe-131m',ac[4], ace[4], acen[4], lc[4], mc[4], a[4], ae[4], aen[4], l[4], m[4], det[4])
                rep += f1.format('Xe-133m', ac[5], ace[5], acen[5], lc[5], mc[5], a[5], ae[5], aen[5], l[5], m[5], det[5])
                rep += f1.format('Xe-135', ac[1], ace[1], acen[1], lc[1], mc[1], a[1], ae[1], aen[1], l[1], m[1], det[1])
                rep += "----------------------------------------------------------------------------------------------------\n\n"
                if self.gasbkUsed:
                    rep += "Gas background:\n"
                    rep += "----------------------------------------------------------------------------------------------------\n"
                    f1 = '{:<10s} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7d}\n'
                    det_133g = self.Xe133ACg >= self.Xe133ACLCg
                    rep += f1.format('Xe-133',self.Xe133ACg, self.Xe133ACErrg, self.Xe133ACErrNonStatg, self.Xe133ACLCg, self.Xe133ACMDCg, 
                                     self.Xe133Ag, self.Xe133AErrg, self.Xe133AErrNonStatg, self.Xe133ALCg, self.Xe133AMDAg,det_133g)
                    rep += f1.format('Xe-131m',ac[10], ace[10], acen[10], lc[10], mc[10], a[10], ae[10], aen[10], l[10], m[10],det[10])
                    rep += f1.format('Xe-133m', ac[11], ace[11], acen[11], lc[11], mc[11], a[11], ae[11], aen[11], l[11], m[11], det[11])
                    rep += f1.format('Xe-135', ac[7], ace[7], acen[7], lc[7], mc[7], a[7], ae[7], aen[7], l[7], m[7], det[7])
                    rep += "----------------------------------------------------------------------------------------------------\n\n"
            else:
                rep += format('Unit: %s\n\n' %self.unit)
                rep += '{:<10s} {:<7s} {:<7s} {:<7s} {:<7s} {:<7s} {:<7s}\n'.format( 
                          'Isotope','A','Err','Err nst','LCA','MDA','Detected')
                rep += "----------------------------------------------------------------------------------------------------\n"
                f1 = '{:<10s} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7d}\n'
                det_133 = self.Xe133A >= self.Xe133ALC
                rep += f1.format('Xe-133', self.Xe133A, self.Xe133AErr, self.Xe133AErrNonStat, self.Xe133ALC, self.Xe133AMDA,det_133)
                rep += f1.format('Xe-131m', a[4], ae[4], aen[4], l[4], m[4],det[4])
                rep += f1.format('Xe-133m', a[5], ae[5], aen[5], l[5], m[5], det[5])
                rep += f1.format('Xe-135', a[1], ae[1], aen[1], l[1], m[1], det[1])
                rep += "----------------------------------------------------------------------------------------------------\n\n"
                if self.gasbkUsed:
                    rep += "Gas background:\n"
                    rep += "----------------------------------------------------------------------------------------------------\n"
                    f1 = '{:<10s} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7.3f} {:<7d}\n'
                    det_133g = self.Xe133Ag >= self.Xe133ALCg
                    rep += f1.format('Xe-133', self.Xe133Ag, self.Xe133AErrg, self.Xe133AErrNonStatg, self.Xe133ALCg, self.Xe133AMDAg,det_133g)
                    rep += f1.format('Xe-131m', a[10], ae[10], aen[10], l[10], m[10],det[10])
                    rep += f1.format('Xe-133m', a[11], ae[11], aen[11], l[11], m[11], det[11])
                    rep += f1.format('Xe-135', a[7], ae[7], aen[7], l[7], m[7], det[7])
                    rep += "----------------------------------------------------------------------------------------------------\n\n"
            
            rep += "ROI specific results\n\n"
            if not self.activityOnly:
                rep += "ROI\tAC\tErr\tErr nst\tLC\tMDC\tA\tErr\tErr nst\tLCA\tMDA\tDetected\n"
            else:
                rep += "ROI\tA\tErr\tErr nst\tLCA\tMDA\tDetected\n"
            rep += "----------------------------------------------------------------------------------------------------------\n"
            for i in range(self.dimension):
                if i==6:
                    rep += "----------------------------------------------------------------------------------------------------------\n"
                if not self.activityOnly:
                    rep += format("%d\t%3.3f\t%3.3f\t%3.3f\t%3.3f\t%3.3f\t%3.3f\t%3.3f\t%3.3f\t%3.3f\t%3.3f\t%d\n"
                              %(i+1,ac[i], ace[i], acen[i], lc[i], mc[i], a[i], ae[i], aen[i], l[i], m[i], det[i]))
                else:
                    rep += format("%d\t%3.3f\t%3.3f\t%3.3f\t%3.3f\t%3.3f\t%d\n"
                              %(i+1, a[i], ae[i], aen[i], l[i], m[i], det[i]))
            rep += "----------------------------------------------------------------------------------------------------------\n\n"
            g = self.grossCounts
            gd = self.grossCountsDBcorr
            gde = self.grossCountsDBcorrErr
            n = self.netCounts
            vn = np.multiply(self.netCountsErr,self.netCountsErr) 
            b = self.bgrCounts
            bc = self.bgrCountsBayes
            be = np.multiply(self.bgrCountsErr,self.bgrCountsErr) 
            nl = self.netCountsLC
            rep += "ROI\tGross\tGr-db\tV Gr-db\tNet\tV Net\tBgr\tBgr cor\tV Bgr\tNet LC\n"
            rep += "-----------------------------------------------------------------------------------\n"
            for i in range(self.dimension):
                if i==6:
                    rep += "-----------------------------------------------------------------------------------\n"
                rep += format("%d\t%d\t%3.3f\t%3.3f\t%3.3f\t%3.3f\t%3.3f\t%3.3f\t%3.3f\t%3.3f\n"
                              %(i+1,g[i], gd[i], gde[i], n[i], vn[i], b[i], bc[i], be[i], nl[i]))
            rep += "-----------------------------------------------------------------------------------\n\n"
            
           
            if self.verbose:
                rep += "ROI Limits in channels:\n"
                rep += "ROI\tb_low\tb_high\tg_low\tg_high\n"
                rep += "----------------------------------------------------------\n"
                for r in self.roiLimits:
                    #rep += format("%d\t%3.3f\t%3.3f\t%3.3f\t%3.3f\n" %(r[0], r[1], r[2], r[3], r[4]))
                    rep += format("%d\t%d\t%d\t%d\t%d\n" %(r[0], r[1], r[2], r[3], r[4]))
                rep += "----------------------------------------------------------\n"
                rep += "\nbg-efficiencies\n"
                rep += "---------------\n"
                rep += "ROI\tefficiency\n"
                rep += "-----------------------------\n"
                siz = int(self.eff.size/2)
                for i in range(siz):
                        rep += format("%d\t%f +/- %f\n" %(i+2,self.eff[i], self.eff[i+siz]))
                rep += "-----------------------------\n"
                rep += "\ninterference ratios\n"
                rep += "---------------\n"
                rep += "Index\tratio\n"
                rep += "-----------------------------\n"
                siz = int(self.ratio.size/2)
                for i in range(siz):
                        rep += format("%d\t%f +/- %f\n" %(i+1,self.ratio[i], self.ratio[i+siz]))
                rep += "-----------------------------\n"
        else:
            rep += "No BGM analysis performed\n"
        return rep
        
    def analysisInfo(self):
        """ Returns basic analysis results as a string """
        if self.inputErrors:
            return "\nThere were input errors. No BGM analysis performed.\n"
        if not self.activityOnly: 
            ac =  self.AC
            ace =  self.ACErr
            lc =  self.LC
            mdc = self.MDC
            txt = format("Analysis method: %s, unit: %s\n\n" %(self.analysisMethod, self.unit))
            txt += '{:<10s}{:<17s}{:<7s}{:<7s}{:<7s}\n'.format('','AC',' LC','MDC','Detected') 
            txt += '-----------------------------------------\n'
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7.3f}{:<7d}\n'.format('Xe-133:',self.Xe133AC,'+/-',self.Xe133ACErr, self.Xe133ACLC,self.Xe133ACMDC, self.xe133Det)   
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7.3f}{:<7d}\n'.format('Xe-131m:',ac[4],'+/-',ace[4], lc[4], mdc[4], self.xe133Det)
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7.3f}{:<7d}\n'.format('Xe-133m:',ac[5],'+/-',ace[5], lc[5],mdc[5], self.xe133Det) 
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7.3f}{:<7d}\n'.format('Xe-135:',ac[1],'+/-',ace[1], lc[1],mdc[1], self.xe133Det)
            txt += '-----------------------------------------\n'
        else:
            a =  self.A
            ae =  self.AErr
            lc =  self.LCA
            mda = self.MDA
            txt = format("Analysis method: %s, unit: %s\n\n" %(self.analysisMethod, self.unit))
            txt += '{:<10s}{:<17s}{:<7s}{:<7s}\n'.format('','A',' LC','MDA') 
            txt += '-----------------------------------------\n'
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7.3f}\n'.format('Xe-133:',self.Xe133A,'+/-',self.Xe133AErr, self.Xe133ALC,self.Xe133AMDC)   
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7.3f}\n'.format('Xe-131m:',a[4],'+/-',ae[4], lc[4], mda[4])
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7.3f}\n'.format('Xe-133m:',a[5],'+/-',ae[5], lc[5],mda[5]) 
            txt += '{:<10s}{:<7.3f}{:<4s}{:<7.3f}{:<7.3f}{:<7.3f}\n'.format('Xe-135:',a[1],'+/-',ae[1], lc[1],mda[1])
            txt += '-----------------------------------------\n'
        return txt
    
    def makeROIBitPattern(self):
        """Make the ROI bit pattern to be used when analyzing for Xe-133.
           Result stored as an integer 'self.roiBitPattern'
           Also make detection flags. 
        """
        self.xe131mDet = self.A[4] >= self.LCA[4]
        self.xe133mDet = self.A[5] >= self.LCA[5]
        self.xe133Det = self.Xe133A >= self.Xe133ALC
        self.xe135Det = self.A[1] >= self.LCA[1]
        ROI_4 = not self.xe131mDet and (not self.xe133mDet) 
        ROI_7 = self.xe131mDet
        ROI_8 = self.xe133mDet
        ROI_9 = not self.xe133mDet and self.xe131mDet
        ROI_10 = not self.xe131mDet and self.xe133mDet
        self.roiBitPattern = kROI_3 + ROI_4*kROI_4 + ROI_7*kROI_7 + ROI_8*kROI_8 + ROI_9*kROI_9 +  ROI_10*kROI_10
 
def bgm(h, comb = True, unit = 0.001, ingrowth = True, noBayesCorr = False, useROI3Only = False, errBreakdown = False):
    """
    Perform a BGM- analysis.

    Parameters:
    -----------
    h:          An instance of bgmHandler with sample data.
                h will contain the results when the analysis is done.
    comb:       If 'True', re-analyze using ROI 7-10 if metastable(s)
                detected. Else do original bgm analysis only. Default is 'True'. 
    unit:       1 = Bq or 0.001 = mBq; Default =  0.001
    ingrowth:   If 'True', correct for Xe-133m->Xe-133 ingrowth if Xe-133m detected. 
                Default is'True'.
    noBayesCorr If 'True', do not use the Bayesian correction for decision limits. 
                 Default 'False'. Used for testing only.
    useROI3Only If 'True', reported Xe-133 activity is obtained using ROI3 only
    errBreakdown If 'True', calculate and report the different components of the 
                 systematic error. Takes a bit of extra time. 
    
    Returns:
    --------
                The results are stored as members of the 'bgmHandler' h.
                The following arrays stores ROI-specific data 
                (all have dim = 6 or 12, depending on the use of the gas background):
                    
                AC:             Activity concentrations
                ACErr:          Activity concentration errors (statistical)
                ACErrNonstat    Activity concentration errors (non-statistical)
                LC              AC critical limits
                MDC             MDC:s
                A               Activities
                AErr            Activity errors (statistical)
                AErrNonstat     Activity errors (non-statistical)
                LCA             Activity critical limits
                MDA             MDA:s
                
                The combined Xe-133 results are stored as floats:
                
                Sample:         Xe133AC, Xe133ACErr, Xe133ACErrNonStat
                                Xe133ACLC, Xe133ACMDC
                                Xe133A, Xe133AErr, Xe133AErrNonStat
                                Xe133ALC, Xe133AMDA
                Gasbk:          Xe133ACg, Xe133ACErrg, Xe133ACErrNonStatg
                                Xe133ACLCg, Xe133ACMDCg
                                Xe133Ag, Xe133AErrg, Xe133AErrNonStatg
                                Xe133ALCg, Xe133AMDAg
    """
    if h.inputErrors:
        print("Input errors in bgm, non analysis performed.")
        return
    if unit != 0.001 and unit != 1:
        print("Wrong unit in bgm: %f. No analysis performed." %unit)
        return
    #Set analysis method and unit
    h.ingrowth = ingrowth
    h.combined = comb
    h.noBayesCorr = noBayesCorr
    h.errBreakdown = errBreakdown
    h.useROI3Only = useROI3Only
    h.dsFact = h.sAcqLive/h.dAcqLive
    h.analysisMethod = buildAnalysisMethod(h.combined, h.gasbkUsed, h.ingrowth, h.noBayesCorr, h.useROI3Only)
    if h.gasbkUsed:
        K = 12
        h.dgFact = h.gAcqLive/h.dAcqLive
    else:
        K = 6
    h.unitscale = unit
    if unit==1:
            h.unit = "Bq"
    else:
            h.unit = "mBq"
    if h.verbose:
        print("Starting BGM analysis. Analysis method: %s,  unit: %s\n" %(h.analysisMethod, h.unit))
    #Build data vectors
    d = np.zeros(K)
    dt = np.zeros(K)
    var_dt = np.zeros(K)
    varvar_dt = np.zeros(K)
    y = np.zeros(K)
    for i in range(6): 
         d[i] = h.detbkGross[i]
         if K == 12:
             d[i+6] = h.detbkGross[i]
         dt[i] = h.dsFact*d[i]
         if K == 12:
             dt[i+6] = h.dgFact*d[i+6]
         var_dt[i] = pow(h.dsFact,2)*d[i]
         if  K == 12:
             var_dt[i+6] = pow(h.dgFact,2)*d[i+6]
         varvar_dt[i] = pow(h.dsFact,4)*d[i]
         if K == 12:
             varvar_dt[i+6] = pow(h.dgFact,4)*d[i+6]
    for i in range(6): 
        y[i] = h.sampleGross[i]
        if K == 12:
            y[i+6] = h.gasbkGross[i]
    #Calculate gas background subtraction factors
    F = np.zeros(5)
    if h.gasbkUsed:
        F[0] = calcF(const.XE133_LAM, h.tau, h.sAcqLive, h.sAcqReal, 
                        h.gAcqLive, h.gAcqReal)
        F[1] = calcF(const.XE135_LAM, h.tau, h.sAcqLive, h.sAcqReal, 
                        h.gAcqLive, h.gAcqReal)
        F[2] =  calcF(const.XE131M_LAM, h.tau, h.sAcqLive, h.sAcqReal, 
                        h.gAcqLive, h.gAcqReal)
        F[3] = calcF(const.XE133M_LAM, h.tau, h.sAcqLive, h.sAcqReal, 
                        h.gAcqLive, h.gAcqReal)
        F[4] = calcF(const.RN222_LAM, h.tau, h.sAcqLive, h.sAcqReal, 
                        h.gAcqLive, h.gAcqReal)
    h.F = F
    #Make activity response matrices
    try:
        h.ResponseMatrix_A= ResponseMatrix(h)
        h.ResponseErrorMatrix_A = ResponseErrorMatrix(h)
    except ValueError as e:
        print("ValueError when making response matrices.")
        raise ValueError(e)
    except ZeroDivisionError as e:
        print("ZeroDivisionError when making response matrices.")
        raise ZeroDivisionError(e)
    #Analyze first turn
    #print("Analyzing first turn for activity...")
    try:
        bgm_core(h, y, d, dt, var_dt, varvar_dt, noBayesCorr = h.noBayesCorr)
    except ValueError as e:
        raise ValueError(e)
    #Make ROI bitpattern
    h.makeROIBitPattern()
    ROI_4 = h.roiBitPattern & kROI_4 != 0
    ROI_7 = h.roiBitPattern & kROI_7 != 0
    ROI_8 = h.roiBitPattern & kROI_8 != 0
    ROI_9 = h.roiBitPattern & kROI_9 != 0
    ROI_10 = h.roiBitPattern & kROI_10 != 0
    if h.combined and not ROI_4:
        #Make new response matrices
        try:
            h.ResponseMatrix_A = ResponseMatrix(h, comb=True)
            h.ResponseErrorMatrix_A = ResponseErrorMatrix(h, comb=True)
        except ValueError as e:
            print("ValueError when making response matrices.")
            raise ValueError(e)
        except ZeroDivisionError as e:
            print("ZeroDivisionError when making response matrices.")
            raise ZeroDivisionError(e)
        #update ROI4 data according to ROI pattern
        y[3] = ROI_7*h.sampleGross[6] + ROI_8*h.sampleGross[7] + \
            ROI_9*h.sampleGross[8] + ROI_10*h.sampleGross[9]
        if K == 12:
            y[9] = ROI_7*h.gasbkGross[6] + ROI_8*h.gasbkGross[7] + \
            ROI_9*h.gasbkGross[8] + ROI_10*h.gasbkGross[9]
        d[3] = ROI_7*h.detbkGross[6] + ROI_8*h.detbkGross[7] + \
            ROI_9*h.detbkGross[8] + ROI_10*h.detbkGross[9]
        dt[3] = h.dsFact*d[3]
        var_dt[3] = pow(h.dsFact,2)*d[3]
        varvar_dt[3] = pow(h.dsFact,4)*d[3]
        if K ==12:
            d[9] = d[3]
            dt[9] = h.dgFact*d[9]
            var_dt[9] = pow(h.dgFact,2)*d[9]
            varvar_dt[9] = pow(h.dgFact,4)*d[9]
        try:
            bgm_core(h, y, d, dt, var_dt, varvar_dt, comb = True, noBayesCorr = h.noBayesCorr)
        except ValueError as e:
            raise ValueError(e)
    h.analysisTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #Error breakdown
    try:
        dA_rat = ResponseErrorMatrix(h, h.combined, True, False, False)
        dA_br = ResponseErrorMatrix(h, h.combined, False, True, False)
        dA_eff = ResponseErrorMatrix(h, h.combined, False, False, True)
    except ValueError as e:
        print("ValueError when making response matrices.")
        raise ValueError(e)
    except ZeroDivisionError as e:
        print("ZeroDivisionError when making response matrices.")
        raise ZeroDivisionError(e)
    try:
        h.AErrNonstat, h.AErrNonStatHistData, h.AErrNonStatHistBins = calcErr(h.ResponseMatrix_A, h.ResponseErrorMatrix_A,h.grossCountsDBcorr)
        if h.errBreakdown:
            h.AErrNonstat_rat, h.AErrNonStat_rat_histData, h.AErrNonStat_rat_histBins = calcErr(h.ResponseMatrix_A, dA_rat,h.grossCountsDBcorr)
            h.AErrNonstat_br, h.AErrNonStat_br_histData, h.AErrNonStat_br_histBins = calcErr(h.ResponseMatrix_A, dA_br,h.grossCountsDBcorr)
            h.AErrNonstat_eff, h.AErrNonStat_eff_histData, h.AErrNonStat_eff_histBins = calcErr(h.ResponseMatrix_A, dA_eff,h.grossCountsDBcorr)
    except ValueError as e:
        print("ValueError when performing error estimate using MC.")
        raise ValueError(e)
    #Convert to activity concentration
    if not h.activityOnly:
        calcAC(h)
    if h.verbose:
        print("\nActivity response matrix:\n")
        print(h.ResponseMatrix_A)
        print("\nActivity response error matrix:\n")
        print(h.ResponseErrorMatrix_A)
        print("\nInverted activity response matrix:\n")
        print(h.InvResponseMatrix_A)

def calcAct(z,A):
    """
    Returns activity vector given z and A.
    Used in Monte-Carlo calculation systematic errors in x.   
    """
    try:
         B = np.linalg.inv(A)
    except np.linalg.LinAlgError as e:
            raise ValueError(format("Error in calcAct during matrix inversion:\n %s" %e)) 
    return np.dot(B,z)

def calcErr(AA, dAA, z):
    """MC calculation of systematic errors in x due to errors in the response matrix
       assuming that the matrix uncertainties are normaly distributed.
    """
    np.random.seed(int(time.time()))
    nhistories = 10000
    dim = np.size(AA,0)
    A =  copy.copy(AA)
    dA1 =  copy.copy(dAA)
    dA = np.where(dA1 < 1e-12, 0, dA1)
    ra = np.random.normal(loc = A, scale = dA, size = (nhistories,dim,dim))
    remove = []
    i = 0
    #Remove results where an element differ more that 4 sigma. 
    #This is to remove outliers that might affect the resulting variance unproportionally 
    for r in ra:
        im = -1
        for j in range(dim):
            for k in range(dim):
                if (abs(r[j,k] - A[j,k]) > 4*dA[j,k]) and dA[j,k] > 0 and im == -1:
                    im = i
                    remove.append(i)
        i += 1
    ram = np.delete(ra,remove, axis = 0)
    try:
        xarr = calcAct(z,ram)
    except ValueError as e:
        raise ValueError(e)
    errHistData = []
    errHistBins = []
    for i in range(dim):
        data, bins = np.histogram(xarr[:,i], bins = 'auto')
        errHistData.append(data)
        center = (bins[:-1] + bins[1:]) / 2
        errHistBins.append(center)
    return np.sqrt(np.var(xarr, axis = 0)), errHistData, errHistBins
        
def bgm_core(h, y, d, dt, var_dt, varvar_dt, comb=False, noBayesCorr = False):
    """
    Do the BGM calculation.
    
    Parameters:
    ----------
    h            An instance of bgmHandler containing response matrices.
                 h will be updated with the results.
    y            sample (and gas background, optional) gross counts 
                 [s_0, ..., s_n, g_0,...,g_n]
    d            detector background gross counts [d_0,..., d_n]
    dt           detecor background gross * sample/detbk acq. times
                 [dt_0, ..., dt_n]
    var_dt       variance of dt
                 [var_dt_0, ..., var_dt_n]
    varvar_dt    variance of var_dt
                 [varvar_dt_0, ..., varvar_dt_n]
    comb         ROI 4 is combined from ROI 7-10. Default 'False'.
    noBayesCorr  If 'True', do not use the Byesian correction for decision limits. 
                 Default 'False'.
    """
    A =  copy.copy(h.ResponseMatrix_A)
    try:
        B = np.linalg.inv(A)
    except np.linalg.LinAlgError as e:
            raise ValueError(format("Error in bgm_core during matrix inversion:\n %s" %e)) 
    dim = np.size(A,0)
    z = y-dt
    var_z = y + var_dt
    x = np.dot(B,z)
    COV_x = np.zeros((dim,dim))
    COV_dx = np.zeros((dim,dim))
    var_x = np.empty(dim)
    dx = np.empty(dim)
    for i in range(dim):
        for j in range(dim):
            b_row_i = B[i]
            b_row_j = B[j]
            bi_bj = np.zeros(dim)
            for k in range(dim):
                bi_bj[k] = b_row_i[k]*b_row_j[k]
            COV_x[i,j] = np.dot(bi_bj, var_z)
            COV_dx[i,j] = np.dot(bi_bj, var_dt)
            if not comb:
                COV_x[i,j] += var_z[4]*xi_nij(B,4,i,j) + var_z[5]*xi_nij(B,5,i,j)
                COV_dx[i,j] += var_dt[4]*xi_nij(B,4,i,j) + var_dt[5]*xi_nij(B,5,i,j)
                if dim == 12:
                    COV_x[i,j] += var_z[10]*xi_nij(B,10,i,j) + var_z[11]*xi_nij(B,11,i,j)
                    COV_dx[i,j] += var_dt[10]*xi_nij(B,10,i,j) + var_dt[11]*xi_nij(B,11,i,j)
            else:
                COV_x[i,j] += var_z[4]*xi_nij(B,4,i,j)*(not h.xe131mDet) \
                    + var_z[5]*xi_nij(B,5,i,j)*(not h.xe133mDet)
                COV_dx[i,j] += var_dt[4]*xi_nij(B,4,i,j)*(not h.xe131mDet) \
                    + var_dt[5]*xi_nij(B,5,i,j)*(not h.xe133mDet)
                if dim == 12:
                    COV_x[i,j] += var_z[10]*xi_nij(B,10,i,j)*(not h.xe131mDet) \
                        + var_z[11]*xi_nij(B,11,i,j)*(not h.xe133mDet)
                    COV_dx[i,j] += var_dt[10]*xi_nij(B,10,i,j)*(not h.xe131mDet) \
                        + var_dt[11]*xi_nij(B,11,i,j)*(not h.xe133mDet)
        var_x[i] = COV_x[i,i]
        dx[i] = COV_dx[i,i]
    Ad = np.zeros((dim,dim))
    Adp = np.zeros(dim)
    for i in range(dim):
        Ad[i,i] = A[i,i]
        Adp[i] = A[i,i]
    net = np.dot(Ad,x)
    var_net = np.dot(np.square(Ad),var_x)
    y0 = np.empty(dim)
    var_y0 = np.empty(dim)
    y0B = np.empty(dim)
    yC = np.empty(dim)
    for i in range(dim):
        cA = copy.copy(A)
        a0_row =  cA[i]
        a0_row[i] = 0
        y0[i] = np.dot(a0_row,x) + dt[i]
        var_y0_1 = np.dot(COV_x, a0_row)
        var_y0[i] = np.dot(a0_row,var_y0_1) + var_dt[i]
        phi = 1/math.sqrt(2*math.pi)*math.exp(-y0[i]*y0[i]/2/var_y0[i])
        Z = norm.cdf(y0[i]/math.sqrt(var_y0[i]))
        if noBayesCorr:
            y0B[i] = y0[i]
        else:
            y0B[i] = y0[i] + math.sqrt(var_y0[i])*phi/Z
        try:
            yC[i] = const.K_S*math.sqrt(y0B[i] + var_y0[i])
        except ValueError:
            raise ValueError(format("ValueError in BGM when calculating critical limit. y0B[i] = %f var_y0[i] = %f i = %d" 
                  %(y0B[i], var_y0[i], i)))
    Ks = np.full(dim,const.K_S)
    yD = np.square(Ks) + 2*yC
    h.dimension= dim
    h.grossCounts = y 
    h.grossCountsDBcorr = z 
    h.grossCountsDBcorrErr = np.sqrt(var_z)
    h.netCounts = net
    h.netCountsErr = np.sqrt(var_net)
    h.netCountsLC = yC
    h.netCountsMDC = yD
    h.bgrCounts = y0
    h.bgrCountsErr = np.sqrt(var_y0)
    h.bgrCountsBayes = y0B
    h.InvResponseMatrix_A = B
    h.CovMatrix_A = COV_x
    h.A = x
    h.AErr = np.sqrt(var_x)
    h.ADX = np.sqrt(dx)
    h.LCA = np.divide(yC,Adp)
    h.MDA = np.divide(yD,Adp)
    h.xi_a = xi_act(const.XE133M_LAM, const.XE133_LAM, h.sAcqReal)
    xe133mdet = h.A[5] >= h.LCA[5]
    if h.useROI3Only:
        h.Xe133A = h.A[2] -  xe133mdet*h.ingrowth*h.xi_a*h.A[5]
        h.Xe133AErr = math.sqrt(var_x[2] + xe133mdet*h.ingrowth*pow(h.xi_a,2)*var_x[5])
        h.Xe133ALC = h.LCA[2]
        h.Xe133AMDA = h.MDA[2]
        h.Xe133A_dx = h.ADX[2]
        if dim == 12:
            h.Xe133Ag = h.A[8]
            h.Xe133AErrg = h.AErr[8]
            h.Xe133ALCg = h.LCA[8]
            h.Xe133AMDAg = h.MDA[8]
    else:            
        #Combine ROI 3 and 4
        alpha = (var_x[3] - COV_x[2,3])/(var_x[2] + var_x[3] - 2*COV_x[2,3])
        x23 = alpha*x[2] + (1-alpha)*x[3]
        var_x23 = pow(alpha,2)*var_x[2] + pow(1-alpha,2)*var_x[3] + 2*alpha*(1-alpha)*COV_x[2,3]
        alpha_dx = (dx[3] - COV_dx[2,3])/(dx[2] + dx[3] - 2*COV_dx[2,3])
        dx_x23 = pow(alpha_dx,2)*dx[2] + pow(1-alpha_dx,2)*dx[3] + 2*alpha_dx*(1-alpha_dx)*COV_dx[2,3]
        gamma3 =0
        gamma4 =0
        delta34 =0
        for i in range(dim):
             gamma3 += B[2,i]*B[2,i]*(A[i,2]+ A[i,3]) 
             gamma4 += B[3,i]*B[3,i]*(A[i,2]+ A[i,3]) 
             delta34 += B[2,i]*B[3,i]*(A[i,2]+ A[i,3])
        if not comb:
            gamma3 += (A[4,2] +A[4,3])*xi_nij(B, 4, 2, 2)
            gamma3 += (A[5,2] +A[5,3])*xi_nij(B, 5, 2, 2)
        if dim==12:
             gamma3 += (A[10,2] +A[10,3])*xi_nij(B, 10, 2, 2)
             gamma3 += (A[11,2] +A[11,3])*xi_nij(B, 11, 2, 2)
        if not comb:
            gamma4 += (A[4,2] +A[4,3])*xi_nij(B, 4, 3, 3)
            gamma4 += (A[5,2] +A[5,3])*xi_nij(B, 5, 3, 3)
        if dim == 12:
             gamma4 += (A[10,2] +A[10,3])*xi_nij(B, 10, 3, 3)
             gamma4 += (A[11,2] +A[11,3])*xi_nij(B, 11, 3, 3)
        if not comb:
            delta34 += (A[4,2] +A[4,3])*xi_nij(B, 4, 2, 3)
            delta34 += (A[5,2] +A[5,3])*xi_nij(B, 5, 2, 3) 
        if dim == 12:
             delta34 += (A[10,2] +A[10,3])*xi_nij(B, 10, 2, 3)
             delta34 += (A[11,2] +A[11,3])*xi_nij(B, 11, 2, 3)
        m = pow(alpha,2)*gamma3 + pow(1-alpha,2)*gamma4 + 2*alpha*(1-alpha)*delta34 
        var0 = var_x23 - m*x23
        if var0 < 0:
             var0 = 0
             print("Warning in bgm_core: Combined (ROI 3+4) sample backgrund variance < 0.") 
             print("Xe-133 LC set to min(LC_3,LC_4)")
             h.combLCZeroSample = True
             Xe133LC = min(h.LCA[2], h.LCA[3])
        else:
            h.combLCZeroSample = False
            Xe133LC = const.K_S*math.sqrt(var0) 
        Xe133MDC = m*const.K_S + 2*Xe133LC 
        h.alphaSample = alpha
        xe133mdet = h.A[5] >= h.LCA[5]
        h.Xe133A = x23 -  xe133mdet*h.ingrowth*h.xi_a*h.A[5]
        h.Xe133AErr = math.sqrt(var_x23 + xe133mdet*h.ingrowth*pow(h.xi_a,2)*var_x[5])
        h.Xe133ALC = Xe133LC
        h.Xe133AMDA = Xe133MDC
        h.Xe133A_dx = np.sqrt(dx_x23)
        h.combLCZeroGasbk = False
        h.x23 = x23
        h.var_x23 = var_x23
        if dim == 12:
            alpha = (var_x[9] - COV_x[8,9])/(var_x[8] + var_x[9] - 2*COV_x[8,9])
            x23 = alpha*x[8] + (1-alpha)*x[9]
            var_x23 = pow(alpha,2)*var_x[8] + pow(1-alpha,2)*var_x[9] + 2*alpha*(1-alpha)*COV_x[8,9]
            gamma3 =0
            gamma4 =0
            delta34 =0
            for i in range(dim):
                 gamma3 += B[8,i]*B[8,i]*(A[i,8]+ A[i,9]) 
                 gamma4 += B[9,i]*B[9,i]*(A[i,8]+ A[i,9]) 
                 delta34 += B[8,i]*B[9,i]*(A[i,8]+ A[i,9])
            if not comb:
                gamma3 += (A[4,8] +A[4,9])*xi_nij(B, 4, 8, 8)
                gamma3 += (A[5,8] +A[5,9])*xi_nij(B, 5, 8, 8)
                gamma3 += (A[10,8] +A[10,9])*xi_nij(B, 10, 8, 8)
                gamma3 += (A[11,8] +A[11,9])*xi_nij(B, 11, 8, 8)
                gamma4 += (A[4,8] +A[4,9])*xi_nij(B, 4, 9, 9)
                gamma4 += (A[5,8] +A[5,9])*xi_nij(B, 5, 9, 9)
                gamma4 += (A[10,8] +A[10,9])*xi_nij(B, 10, 9, 9)
                gamma4 += (A[11,8] +A[11,9])*xi_nij(B, 11, 9, 9) 
                delta34 += (A[4,8] +A[4,9])*xi_nij(B, 4, 8, 9)
                delta34 += (A[5,8] +A[5,9])*xi_nij(B, 5, 8, 9) 
                delta34 += (A[10,8] +A[10,9])*xi_nij(B, 10, 8, 9)
                delta34 += (A[11,8] +A[11,9])*xi_nij(B, 11, 8, 9)
            m = pow(alpha,2)*gamma3 + pow(1-alpha,2)*gamma4 + 2*alpha*(1-alpha)*delta34 
            var0 = var_x23 - m*x23
            if var0 < 0:    
                 var0 = 0  
                 print("Warning in bgm_core: Combined (ROI 3+4) sample backgrund variance < 0.\n") 
                 print("Xe-133 LC set to min(LC_3,LC_4)\n")
                 h.combLCZeroGasbk = True
                 Xe133LC = min(h.LCA[8], h.LCA[9])
            else:
                h.combLCZeroGasbk = False
                Xe133LC = const.K_S*math.sqrt(var0) 
            Xe133MDC = m*const.K_S + 2*Xe133LC 
            h.alphaGasbk = alpha;
            h.Xe133Ag = x23
            h.Xe133AErrg = math.sqrt(var_x23)
            h.Xe133ALCg = Xe133LC
            h.Xe133AMDAg = Xe133MDC

def buildAnalysisMethod(comb, useGasbk, ingrowth, noBayesCorr, useROI3Only):
    """Returns the analysis method string"""
    met = "BGM"
    if comb:
        met += "-C"
    if useGasbk:
        met += "-GB"
    if ingrowth:
        met += "-I"
    if noBayesCorr:
        met += "-NOBA"
    if useROI3Only:
        met += "-ROI3"
    met += '-V' + VERSION
    return met

def xi_nij(B, n, i, j):
    """
    Calculate covariance correction terms.
    
    Parameters:
    -----------
    B:        Inverse response matrix
    n:        index n
    i:        index i
    j:        index j
      
    Returns:
    -------
    numeric   The correction factor
    
    """
    ret=0
    if n == 4:
        ret = B[i,3]*B[j,4] + B[i,4]*B[j,3]
    if n == 5:
        ret = B[i,3]*B[j,5] + B[i,5]*B[j,3]
    if n == 10:
        ret = B[i,9]*B[j,10] + B[i,10]*B[j,9]
    if n == 11:
        ret = B[i,9]*B[j,11] + B[i,11]*B[j,9]
    return ret
        
def calcF(Lambda, tao, slive, sreal, glive, greal):
    """
    Calculate gas background subtraction factor.
    
    Parameters
    -----------
    Lambda:    decay constant (1/s)
    tao:       Time between acquisition start of sample and gas background (s)
    slive:     Sample acquisition live time
    sreal:     Sample acquisition real time
    glive:     Gasbk acquisition live time
    greal:     Gasbk acquisition real time
    
    Returns
    ------
    numeric    Subtraction factor
    """
    return (greal/glive)*(slive/sreal)*math.exp(-Lambda*tao) \
            *(1-math.exp(-Lambda*sreal))/(1-math.exp(-Lambda*greal))
            
def xi(lambda1, lambda2, tc, tp, ta):
    """
    Calculate activity concentration ingrowth correction factor according to
    Axelsson and Ringbom, Apl. Rad. Isot. 92 (2014) 12-17; eq. 15
    This takes into account ingrowth during sampling, processing and 
    activity measurement. 
    
    Parameters
    ----------
    lambda1:   Decay constant (1/s) for mother isotope
    lambda2:   Decay constant (1/s) for daughter isotope
    tc:        Collection time (s)
    tp:        Processing time (s)
    ta:        Acquisition time (s)
    
    Returns:
    --------
    numeric    Ingrowth factor
    """         
    fc1=1-math.exp(-lambda1*tc) 
    fp1 = math.exp(-lambda1*tp)
    fa1 = 1-math.exp(-lambda1*ta)
    fc2=1-math.exp(-lambda2*tc)
    fp2 = math.exp(-lambda2*tp)
    fa2 = 1-math.exp(-lambda2*ta)
    return lambda2/(lambda2-lambda1)*(lambda2*lambda2/lambda1/lambda1*fc1*fp1*fa1/fc2/fp2/fa2 - 1)

def xi_act(lambda1, lambda2, ta):
    """
    Calculate activity ingrowth correction factor according to
    Axelsson and Ringbom, Apl. Rad. Isot. 92 (2014) 12-17; eq. 15
    
    Parameters
    ----------
    lambda1:   Decay constant (1/s) for mother isotope
    lambda2:   Decay constant (1/s) for daughter isotope
    ta:        Acquisition time (s)
    
    Returns:
    --------
    numeric    Ingrowth factor
    """ 
    return lambda2/(lambda2-lambda1)*(lambda2/lambda1*(1-math.exp(-lambda1*ta))/(1-math.exp(-lambda2*ta))-1)

def calcAC(h):
    """
    Calculate activity concentration from activity

    Parameters
    ----------
    h:           A bgmHandler.
    """
    f_133 = const.XE133_LAM*h.collTime/h.V/(1-math.exp(-h.collTime*const.XE133_LAM))/math.exp(-h.procTime*const.XE133_LAM)
    f_131m = const.XE131M_LAM*h.collTime/h.V/(1-math.exp(-h.collTime*const.XE131M_LAM))/math.exp(-h.procTime*const.XE131M_LAM)
    f_133m = const.XE133M_LAM*h.collTime/h.V/(1-math.exp(-h.collTime*const.XE133M_LAM))/math.exp(-h.procTime*const.XE133M_LAM)
    f_135 = const.XE135_LAM*h.collTime/h.V/(1-math.exp(-h.collTime*const.XE135_LAM))/math.exp(-h.procTime*const.XE135_LAM)
    f_rn222 = const.RN222_LAM*h.collTime/h.V/(1-math.exp(-h.collTime*const.RN222_LAM))/math.exp(-h.procTime*const.RN222_LAM)
    f = np.empty(h.dimension)
    f[0] = f_rn222
    f[1] = f_135
    f[2], f[3] = f_133, f_133
    f[4] = f_131m
    f[5] = f_133m
    if h.dimension == 12:
        f[6] = f_rn222
        f[7] = f_135
        f[8], f[9] = f_133, f_133
        f[10] = f_131m
        f[11] = f_133m
    h.AC = np.multiply(f,h.A)
    h.ACErr = np.multiply(f,h.AErr)
    relErrActSq = np.divide(np.multiply(h.AErrNonstat,h.AErrNonstat),np.multiply(h.A,h.A))
    v = np.full(h.dimension,h.V)
    dv = np.full(h.dimension,h.dV)
    relErrVsq = np.divide(np.multiply(dv,dv),np.multiply(v,v))
    h.ACErrNonstat = np.multiply(np.absolute(h.AC), np.sqrt(relErrActSq + relErrVsq))
    if h.errBreakdown:
        relErrActSq_rat = np.divide(np.multiply(h.AErrNonstat_rat,h.AErrNonstat_rat),np.multiply(h.A,h.A))
        h.ACErrNonstat_rat  = np.multiply(np.absolute(h.AC), np.sqrt(relErrActSq_rat))
        relErrActSq_eff = np.divide(np.multiply(h.AErrNonstat_eff,h.AErrNonstat_eff),np.multiply(h.A,h.A))
        h.ACErrNonstat_eff  = np.multiply(np.absolute(h.AC), np.sqrt(relErrActSq_eff))
        relErrActSq_br = np.divide(np.multiply(h.AErrNonstat_br,h.AErrNonstat_br),np.multiply(h.A,h.A))
        h.ACErrNonstat_br  = np.multiply(np.absolute(h.AC), np.sqrt(relErrActSq_br))
        h.ACErrNonstat_V  = np.multiply(np.absolute(h.AC), np.sqrt(relErrVsq))
    h.LC = np.multiply(f,h.LCA)
    h.MDC = np.multiply(f,h.MDA)
    h.ACDX = np.multiply(f,h.ADX)
    h.xi_ac = xi(const.XE133M_LAM, const.XE133_LAM, h.collTime, h.procTime, h.sAcqReal)
    xe133mdet = h.A[5] >= h.LCA[5]
    if h.useROI3Only:
        h.combLCZeroSample = False
        h.combLCZeroGasbk = False
        h.Xe133AErrNonStat = h.AErrNonstat[2]
        h.Xe133AC = h.AC[2]
        h.Xe133ACErr = h.ACErr[2]
        h.Xe133ACLC = h.LC[2]
        h.Xe133ACMDC = h.MDC[2]
        h.Xe133ACErrNonStat = h.ACErrNonstat[2]
        if h.errBreakdown:
            h.Xe133AErrNonStat_eff = h.AErrNonstat_eff[2]
            h.Xe133AErrNonStat_rat = h.AErrNonstat_rat[2]
            h.Xe133AErrNonStat_br = h.AErrNonstat_br[2]
            h.Xe133ACErrNonStat_eff = h.ACErrNonstat_eff[2]
            h.Xe133ACErrNonStat_rat = h.ACErrNonstat_rat[2]
            h.Xe133ACErrNonStat_br = h.ACErrNonstat_br[2]
            h.Xe133ACErrNonStat_V = h.ACErrNonstat_V[2]
        if h.gasbkUsed:
            h.Xe133AErrNonStatg = h.AErrNonstat[8]
            h.Xe133ACg = h.AC[8]
            h.Xe133ACErrg = h.ACErr[8]
            h.Xe133ACErrNonStatg = h.ACErrNonstat[8]
            h.Xe133ACLCg =  h.LC[8]
            h.Xe133ACMDCg =  h.MDC[8]
    else:
        x23 = h.x23*f_133
        var_x23 = h.var_x23*f_133*f_133
        h.Xe133AErrNonStat = math.sqrt(pow(h.alphaSample,2)*pow(h.AErrNonstat[2],2) + pow(1-h.alphaSample,2)*pow(h.AErrNonstat[3],2) + 
                                       xe133mdet*h.ingrowth*pow(h.xi_a,2)*pow(h.AErrNonstat[5],2))
        h.Xe133AC = x23 -  xe133mdet*h.ingrowth*h.xi_ac*h.AC[5]
        h.Xe133ACErr = math.sqrt(var_x23 + xe133mdet*h.ingrowth*pow(h.xi_ac,2)*pow(h.ACErr[5],2))
        h.Xe133ACErrNonStat =  abs(h.Xe133AC)*math.sqrt(pow(h.Xe133AErrNonStat,2)/pow(h.Xe133A,2) + pow(h.dV,2)/pow(h.V,2))
        h.Xe133ACLC = h.Xe133ALC*f_133
        h.Xe133ACMDC = h.Xe133AMDA*f_133
        if h.errBreakdown:
            h.Xe133AErrNonStat_eff = math.sqrt(pow(h.alphaSample,2)*pow(h.AErrNonstat_eff[2],2) + pow(1-h.alphaSample,2)*pow(h.AErrNonstat_eff[3],2) + 
                                           xe133mdet*h.ingrowth*pow(h.xi_ac,2)*pow(h.AErrNonstat_eff[5],2))
            h.Xe133AErrNonStat_rat = math.sqrt(pow(h.alphaSample,2)*pow(h.AErrNonstat_rat[2],2) + pow(1-h.alphaSample,2)*pow(h.AErrNonstat_rat[3],2) + 
                                           xe133mdet*h.ingrowth*pow(h.xi_ac,2)*pow(h.AErrNonstat_rat[5],2))
            h.Xe133AErrNonStat_br = math.sqrt(pow(h.alphaSample,2)*pow(h.AErrNonstat_br[2],2) + pow(1-h.alphaSample,2)*pow(h.AErrNonstat_br[3],2) + 
                                           xe133mdet*h.ingrowth*pow(h.xi_ac,2)*pow(h.AErrNonstat_br[5],2))
            h.Xe133ACErrNonStat_eff = abs(h.Xe133AC)*math.sqrt(pow(h.Xe133AErrNonStat_eff,2)/pow(h.Xe133A,2))
            h.Xe133ACErrNonStat_rat = abs(h.Xe133AC)*math.sqrt(pow(h.Xe133AErrNonStat_rat,2)/pow(h.Xe133A,2))
            h.Xe133ACErrNonStat_br = abs(h.Xe133AC)*math.sqrt(pow(h.Xe133AErrNonStat_br,2)/pow(h.Xe133A,2))
            h.Xe133ACErrNonStat_V = abs(h.Xe133AC)*h.dV/h.V
        if h.gasbkUsed:
            h.Xe133AErrNonStatg = math.sqrt(pow(h.alphaGasbk,2)*pow(h.AErrNonstat[8],2) + pow(1-h.alphaGasbk,2)*pow(h.AErrNonstat[9],2))
            h.Xe133ACg = h.Xe133Ag*f_133
            h.Xe133ACErrg = h.Xe133AErrg*f_133
            h.Xe133ACErrNonStatg = math.sqrt(pow(h.alphaGasbk,2)*pow(h.ACErrNonstat[8],2) + pow(1-h.alphaGasbk,2)*pow(h.ACErrNonstat[9],2))
            h.Xe133ACLCg =  h.Xe133ALCg*f_133
            h.Xe133ACMDCg =  h.Xe133AMDAg*f_133
        
def ResponseMatrix(h, comb = False):
    """
    Make a BGM response matrix  (6 or 12 ROIs).'
    Stored in the bgmHandler as 'ResponseErrorMatrix_AC' or 'ResponseErrorMatrix_A'
    
    Parameters
    ----------
    h:           A bgmHandler.
    comb:        Use bitpattern for ROI4 (default 'False')
    
    Returns:
    --------
    numpy matrix
    """
    etas = np.zeros(5)
    dts = h.sAcqReal/h.sAcqLive
    dim = 6
    if h.gasbkUsed:
        etab = np.zeros(5)
        dtg = h.gAcqReal/h.gAcqLive
        dim = 12
    etas[0] = dts*const.XE133_LAM/(1-math.exp(-h.sAcqReal*const.XE133_LAM))
    etas[1] = dts*const.XE135_LAM/(1-math.exp(-h.sAcqReal*const.XE135_LAM))
    etas[2] = dts*const.XE131M_LAM/(1-math.exp(-h.sAcqReal*const.XE131M_LAM))
    etas[3] = dts*const.XE133M_LAM/(1-math.exp(-h.sAcqReal*const.XE133M_LAM))
    etas[4] = dts*const.RN222_LAM/(1-math.exp(-h.sAcqReal*const.RN222_LAM))
    if dim==12:
        etab[0] = dtg*const.XE133_LAM/(1-math.exp(-h.gAcqReal*const.XE133_LAM))
        etab[1] = dtg*const.XE135_LAM/(1-math.exp(-h.gAcqReal*const.XE135_LAM))
        etab[2] = dtg*const.XE131M_LAM/(1-math.exp(-h.gAcqReal*const.XE131M_LAM))
        etab[3] = dtg*const.XE133M_LAM/(1-math.exp(-h.gAcqReal*const.XE133M_LAM))
        etab[4] = dtg*const.RN222_LAM/(1-math.exp(-h.gAcqReal*const.RN222_LAM))
    if comb:
        ROI_7 = h.roiBitPattern & kROI_7 != 0
        ROI_8 = h.roiBitPattern & kROI_8 != 0
        ROI_9 = h.roiBitPattern & kROI_9 != 0
        ROI_10 = h.roiBitPattern & kROI_10 != 0
    a = np.full((dim,dim),1.e-12)  
    if dim==12:
          #--- ROI 1
          a[0,0] = h.eff[0]*const.BG_BR_222RN/etas[4]  # Use Xe-135 h.eff for radon
          a[0,6] = a[0,0]*h.F[4]*etas[4]/etab[4]
		  #---ROI 2
          a[1,1] = h.eff[0]*const.BG_BR_135XE/etas[1]
          a[1,7] = a[1,1]*h.F[1]*etas[1]/etab[1]
          a[1,0] = h.ratio[0]*a[0,0]
          a[1,6] = a[1,0]*h.F[4]*etas[1]/etab[1]
		  #---ROI 3
          a[2,2] = h.eff[1]*const.BG_BR_133XE_80/etas[0]
          a[2,8] = a[2,2]*h.F[0]*etas[0]/etab[0]
          a[2,0] = h.ratio[1]*a[0,0]
          a[2,6] = a[2,0]*h.F[4]*etas[0]/etab[0]
		  #---ROI 4
          if not comb:
              a[3,3] = h.eff[2]*const.BG_BR_133XE_30/etas[0]
              a[3,9] = a[3,3]*h.F[0]*etas[0]/etab[0]
              a[3,0] = h.ratio[2]*a[0,0]
              a[3,2] = h.ratio[9]*a[2,2]
              a[3,6] = a[3,0]*h.F[4]*etas[0]/etab[0]
              a[3,8] = a[3,2]*h.F[0]*etas[0]/etab[0]
              a[3,4] = h.eff[3]*const.BG_BR_131MXE_30/etas[2] # = a[4,4]
              a[3,5] = h.eff[4]*const.BG_BR_133MXE_30/etas[3] # = a[5,5]
              if h.ratio.size >= 38:
                  a[3,4] += h.ratio[18]*h.eff[3]*const.BG_BR_131MXE_30/etas[2]
                  a[3,5] += h.ratio[19]*h.eff[4]*const.BG_BR_133MXE_30/etas[3]
              a[3,10] = a[3,4]*h.F[2]*etas[2]/etab[2]
              a[3,11] = a[3,5]*h.F[3]*etas[3]/etab[3]
          else:
              a[3,3] = (h.eff[5]*ROI_7 + h.eff[6]*ROI_8 + h.eff[7]*ROI_9 + h.eff[8]*ROI_10)*const.BG_BR_133XE_30/etas[0]
              a[3,0] = (h.ratio[5]*ROI_7 + h.ratio[6]*ROI_8 + h.ratio[7]*ROI_9 + h.ratio[8]*ROI_10)*a[0,0]
              a[3,2] = (h.ratio[12]*ROI_7 + h.ratio[13]*ROI_8 + h.ratio[14]*ROI_9 + h.ratio[15]*ROI_10)*a[2,2]
              a[3,9] = a[3,3]*h.F[0]*etas[0]/etab[0]
              a[3,6] = a[3,0]*h.F[4]*etas[0]/etab[0]
              a[3,8] = a[3,2]*h.F[0]*etas[0]/etab[0]
              if h.ratio.size >= 38:
                  a[3,4] = h.ratio[18]*h.eff[3]*const.BG_BR_131MXE_30/etas[2]*(ROI_7 + ROI_10)
                  a[3,5] = h.ratio[19]*h.eff[4]*const.BG_BR_133MXE_30/etas[3]*(ROI_8 + ROI_9)
              a[3,10] = a[3,4]*h.F[2]*etas[2]/etab[2]
              a[3,11] = a[3,5]*h.F[3]*etas[3]/etab[3]
		  #---ROI 5
          a[4,4] = h.eff[3]*const.BG_BR_131MXE_30/etas[2]
          a[4,10] = a[4,4]*h.F[2]*etas[2]/etab[2]
          a[4,0] = h.ratio[3]*a[0,0]
          a[4,2] = h.ratio[10]*a[2,2]
          a[4,6] = a[4,0]*h.F[4]*etas[2]/etab[2]
          a[4,8] = a[4,2]*h.F[0]*etas[2]/etab[2]
          if h.ratio.size >= 36:
              a[4,5] = h.ratio[16]*h.eff[4]*const.BG_BR_133MXE_30/etas[3]  #added 2020-09-14 =a[5,5]
              a[4,11] = a[4,5]*h.F[3]*etas[2]/etab[2]  #Added 2020-09-14
		  #---ROI 6
          a[5,5] = h.eff[4]*const.BG_BR_133MXE_30/etas[3]
          a[5,11] = a[5,5]*h.F[3]*etas[3]/etab[3]
          a[5,0] = h.ratio[4]*a[0,0]
          a[5,2] = h.ratio[11]*a[2,2]
          a[5,6] = a[5,0]*h.F[4]*etas[3]/etab[3]
          a[5,8] = a[5,2]*h.F[0]*etas[3]/etab[3]
          if h.ratio.size >= 36:
               a[5,4] = h.ratio[17]*a[4,4]   #added 2020-09-14
               a[5,10] = a[5,4]*h.F[2]*etas[3]/etab[3] #added 2020-09-14
          #
	 	  #------Gasbk
		  #
		  #---ROI 1
          a[6,6] = h.eff[0]*const.BG_BR_222RN/etab[4]
		  #---ROI 2
          a[7,7] = h.eff[0]*const.BG_BR_135XE/etab[1]
          a[7,6] = h.ratio[0]*a[6,6]
		  #---ROI 3
          a[8,8] = h.eff[1]*const.BG_BR_133XE_80/etab[0]
          a[8,6] = h.ratio[1]*a[6,6]
		  #---ROI 4
          if not comb:
              a[9,9] = h.eff[2]*const.BG_BR_133XE_30/etab[0]
              a[9,6] = h.ratio[2]*a[6,6]
              a[9,8] = h.ratio[9]*a[8,8]
              a[9,10] = h.eff[3]*const.BG_BR_131MXE_30/etab[2] # = a[14,14]
              a[9,11] = h.eff[4]*const.BG_BR_133MXE_30/etab[3] # = a[15,15]
              if h.ratio.size >= 38:
                  a[9,10] += h.ratio[18]*h.eff[3]*const.BG_BR_131MXE_30/etab[2]
                  a[9,11] += h.ratio[19]*h.eff[4]*const.BG_BR_133MXE_30/etab[3]
          else:
              a[9,9] = (h.eff[5]*ROI_7 + h.eff[6]*ROI_8 + h.eff[7]*ROI_9 + h.eff[8]*ROI_10)*const.BG_BR_133XE_30/etab[0]
              a[9,6] = (h.ratio[5]*ROI_7 + h.ratio[6]*ROI_8 + h.ratio[7]*ROI_9 + h.ratio[8]*ROI_10)*a[6,6]
              a[9,8] = (h.ratio[12]*ROI_7 + h.ratio[13]*ROI_8 + h.ratio[14]*ROI_9 + h.ratio[15]*ROI_10)*a[8,8]
              if h.ratio.size >= 38:
                  a[9,10] = h.ratio[18]*h.eff[3]*const.BG_BR_131MXE_30/etab[2]*(ROI_7 + ROI_10)
                  a[9,11] = h.ratio[19]*h.eff[4]*const.BG_BR_133MXE_30/etab[3]*(ROI_8 + ROI_9)
          a[10,10] = h.eff[3]*const.BG_BR_131MXE_30/etab[2]
          a[10,6] = h.ratio[3]*a[6,6]
          a[10,8] = h.ratio[10]*a[8,8]
          if h.ratio.size == 36:
              a[10,11] = h.ratio[16]*h.eff[4]*const.BG_BR_133MXE_30/etab[3]  #added 2020-09-14 =a[11,11]
		  #---ROI 6
          a[11,11] = h.eff[4]*const.BG_BR_133MXE_30/etab[3]
          a[11,6] = h.ratio[4]*a[6,6]
          a[11,8] = h.ratio[11]*a[8,8]
          if h.ratio.size == 36:
              a[11,10] = h.ratio[17]*a[10,10] #added 2020-09-14
    if dim==6:
          #---ROI 1
          a[0,0] = h.eff[0]*const.BG_BR_222RN/etas[4]  # Use Xe-135 h.eff for radon

		  #---ROI 2
          a[1,1] = h.eff[0]*const.BG_BR_135XE/etas[1]
          a[1,0] = h.ratio[0]*a[0,0]
		  #---ROI 3
          a[2,2] = h.eff[1]*const.BG_BR_133XE_80/etas[0]
          a[2,0] = h.ratio[1]*a[0,0]
		  #---ROI 4
          if not comb:
              a[3,3] = h.eff[2]*const.BG_BR_133XE_30/etas[0]
              a[3,0] = h.ratio[2]*a[0,0]
              a[3,2] = h.ratio[9]*a[2,2]
              a[3,4] = h.eff[3]*const.BG_BR_131MXE_30/etas[2] # = a[4,4]
              a[3,5] = h.eff[4]*const.BG_BR_133MXE_30/etas[3] # = a[5,5]
              if h.ratio.size >= 38:
                  a[3,4] += h.ratio[18]*h.eff[3]*const.BG_BR_131MXE_30/etas[2]
                  a[3,5] += h.ratio[19]*h.eff[4]*const.BG_BR_133MXE_30/etas[3]
          else:
              a[3,3] = (h.eff[5]*ROI_7 + h.eff[6]*ROI_8 + h.eff[7]*ROI_9 + h.eff[8]*ROI_10)*const.BG_BR_133XE_30/etas[0]
              a[3,0] = (h.ratio[5]*ROI_7 + h.ratio[6]*ROI_8 + h.ratio[7]*ROI_9 + h.ratio[8]*ROI_10)*a[0,0]
              a[3,2] = (h.ratio[12]*ROI_7 + h.ratio[13]*ROI_8 + h.ratio[14]*ROI_9 + h.ratio[15]*ROI_10)*a[2,2]
              if h.ratio.size >= 38:
                  a[3,4] = h.ratio[18]*h.eff[3]*const.BG_BR_131MXE_30/etas[2]*(ROI_7 + ROI_10)
                  a[3,5] = h.ratio[19]*h.eff[4]*const.BG_BR_133MXE_30/etas[3]*(ROI_8 + ROI_9)
		  #---ROI 5
          a[4,4] = h.eff[3]*const.BG_BR_131MXE_30/etas[2]
          a[4,0] = h.ratio[3]*a[0,0]
          a[4,2] = h.ratio[10]*a[2,2]
          if h.ratio.size >= 36:
              a[4,5] = h.ratio[16]*h.eff[4]*const.BG_BR_133MXE_30/etas[3] #added 2020-09-14 =a[5,5]
		  #---ROI 6
          a[5,5] = h.eff[4]*const.BG_BR_133MXE_30/etas[3]
          a[5,0] = h.ratio[4]*a[0,0]
          a[5,2] = h.ratio[11]*a[2,2]
          if h.ratio.size >= 36:
              a[5,4] = h.ratio[17]*a[4,4] #added 2020-09-14
    return h.unitscale*a

        
def ResponseErrorMatrix(h, comb = False, ratios = True, branch = True, efficiency = True):
    """
    Make a BGM response error matrix from response matrix A.
    The error matrix will have dim = dim(A) and same unit as A.
    Stored in the bgmHandler as 'ResponseErrorMatrix_A'
    
    Parameters:
    ----------
    h           A bgmHandler.
    comb        Use bitpattern for ROI4. Default 'False'
    
    Returns:
    --------
    numpy matrix
    """
    A =  copy.copy(h.ResponseMatrix_A)
    dim = len(A)
    dA= np.full((dim,dim),0.)    
    B = np.zeros(dim)
    B[0] = const.BG_BR_222RN
    B[1] = const.BG_BR_135XE
    B[2] = const.BG_BR_133XE_80 
    B[3] = const.BG_BR_133XE_30 
    B[4] = const.BG_BR_131MXE_30 
    B[5] = const.BG_BR_133MXE_30
    if dim == 12:
        for i in range(6):
            B[i+6] = B[i]
    dB = np.zeros(dim)
    dB[0] = const.BG_BR_222RN_ERR
    dB[1] = const.BG_BR_135XE_ERR
    dB[2] = const.BG_BR_133XE_80_ERR
    dB[3] = const.BG_BR_133XE_30_ERR
    dB[4] = const.BG_BR_131MXE_30_ERR
    dB[5] = const.BG_BR_133MXE_30_ERR
    if dim == 12:
        for i in range(6):
            dB[i+6] = dB[i]
    ef= np.zeros(9)
    for i in range(9):
        if efficiency:
            ef[i] = pow(h.eff[i+9]/h.eff[i],2)
        else:
            ef[i] = 0
    rf= np.zeros(h.ratio.size)
    for i in range(int(h.ratio.size/2)):
        if ratios:
            rf[i] = pow(h.ratio[i+int(h.ratio.size/2)]/h.ratio[i],2)
        else:
            rf[i] = 0
    bf= np.zeros(dim)
    for i in range(dim):
        if branch:
            bf[i] = pow(dB[i]/B[i],2)
        else:
            bf[i] = 0 
    if comb:
        ROI_7 = h.roiBitPattern & kROI_7 != 0
        ROI_8 = h.roiBitPattern & kROI_8 != 0
        ROI_9 = h.roiBitPattern & kROI_9 != 0
        ROI_10 = h.roiBitPattern & kROI_10 != 0
    if dim == 12:
          #
		  #------Sample
		  #
		  #---ROI 1
          dA[0,0] = abs(A[0,0])*math.sqrt(ef[0] + bf[0])
          #dA[0,6] = abs(A[0,6])*math.sqrt(rf[0] + pow(dA[0,0]/A[0,0],2))
          dA[0,6] = abs(A[0,6])*dA[0,0]/A[0,0]   #Changed 2021-03-30
		  #---ROI 2
          dA[1,1] = abs(A[1,1])*math.sqrt(ef[0] + bf[1])
          dA[1,0] = abs(A[1,0])*math.sqrt(rf[0] + pow(dA[0,0]/A[0,0],2))
          dA[1,6] = abs(A[1,6])*dA[1,0]/A[1,0]
          dA[1,7] = abs(A[1,7]*dA[1,1]/A[1,1])
		  #---ROI 3
          dA[2,2] = abs(A[2,2])*math.sqrt(ef[1] + bf[2])
          #dA[2,0] = abs(A[3,0])*math.sqrt(rf[1] + pow(dA[0,0]/A[0,0],2))
          dA[2,0] = abs(A[2,0])*math.sqrt(rf[1] + pow(dA[0,0]/A[0,0],2)) #Changed 2021-03-30
          dA[2,6] = abs(A[2,6])*dA[2,0]/A[2,0]
          dA[2,8] = abs(A[2,8]*dA[2,2]/A[2,2])
		  #---ROI 4
          if not comb:
              dA[3,3] = abs(A[3,3])*math.sqrt(ef[2] + bf[3])
              dA[3,0] = abs(A[3,0])*math.sqrt(rf[2] + pow(dA[0,0]/A[0,0],2))
              dA[3,2] = abs(A[3,2])*math.sqrt(rf[9] + pow(dA[2,2]/A[2,2],2))
              dA[3,4] = abs(A[4,4])*math.sqrt(ef[3] + bf[4]); #= dA[4,4]
              dA[3,5] = abs(A[5,5])*math.sqrt(ef[4] + bf[5]); #= dA[5,5]
              dA[3,6] = abs(A[3,6]*dA[3,0]/A[3,0])
              dA[3,8] = abs(A[3,8]*dA[3,2]/A[3,2])
              dA[3,9] = abs(A[3,9]*dA[3,3]/A[3,3])
              dA[3,10] = abs(A[3,10]*dA[3,4]/A[3,4])
              dA[3,11] = abs(A[3,11]*dA[3,5]/A[3,5])
          else:
              dA[3,3] = abs(A[3,3])*math.sqrt(ef[5]*ROI_7 + ef[6]*ROI_8 + ef[7]*ROI_9 + 
                ef[8]*ROI_10 + bf[3])
              dA[3,0] = abs(A[3,0])*math.sqrt(rf[5]*ROI_7 + rf[6]*ROI_8 + rf[7]*ROI_9 
                + rf[8]*ROI_10 + pow(dA[0,0]/A[0,0],2))
              dA[3,2] = abs(A[3,2])*math.sqrt(rf[12]*ROI_7 + rf[13]*ROI_8 + rf[14]*ROI_9
                + rf[15]*ROI_10 + pow(dA[2,2]/A[2,2],2))
              dA[3,6] = abs(A[3,6])*dA[3,0]/A[3,0]
              dA[3,8] = abs(A[3,8])*dA[3,2]/A[3,2]
              dA[3,9] = abs(A[3,9]*dA[3,3]/A[3,3])
		  #---ROI 5
          dA[4,4] = abs(A[4,4])*math.sqrt(ef[3] + bf[4])
          dA[4,0] = abs(A[4,0])*math.sqrt(rf[3] + pow(dA[0,0]/A[0,0],2))
          dA[4,2] = abs(A[4,2])*math.sqrt(rf[10] + pow(dA[2,2]/A[2,2],2))
          dA[4,6] = abs(A[4,6]*dA[4,0]/A[4,0])
          dA[4,8] = abs(A[4,8]*dA[4,2]/A[4,2])
          dA[4,10] = abs(A[4,10]*dA[4,4]/A[4,4])
          if h.ratio.size == 36:  #Added 2020-09-14
              dA[4,5] = abs(A[4,5])*math.sqrt(rf[16] + pow(A[5,5]*math.sqrt(ef[4] + bf[5])/A[5,5],2))
              dA[4,11] = abs(A[4,11]*dA[4,5]/A[4,5])
		  #---ROI 6
          dA[5,5] = abs(A[5,5])*math.sqrt(ef[4] + bf[5])
          dA[5,0] = abs(A[5,0])*math.sqrt(rf[4] + pow(dA[0,0]/A[0,0],2))
          dA[5,2] = abs(A[5,2])*math.sqrt(rf[11] + pow(dA[2,2]/A[2,2],2))
          dA[5,6] = abs(A[5,6]*dA[5,0]/A[5,0])
          dA[5,8] = abs(A[5,8]*dA[5,2]/A[5,2])
          dA[5,11] = abs(A[5,11]*dA[5,5]/A[5,5])
          if h.ratio.size == 36: #Added 2020-09-14
              dA[5,4] = abs(A[5,4])*math.sqrt(rf[17] + pow(dA[4,4]/A[4,4],2))
              dA[5,10] = abs(A[5,10])*dA[5,4]/A[5,4]
          #
	 	  #------Gasbk
		  #
		  #---ROI 1
          dA[6,6] = abs(A[6,6])*math.sqrt(ef[0] + bf[6])
		  #---ROI 2
          dA[7,7] = abs(A[7,7])*math.sqrt(ef[0] + bf[7])
          dA[7,6] = abs(A[7,6])*math.sqrt(rf[0] + pow(dA[6,6]/A[6,6],2))
		  #---ROI 3
          dA[8,8] = abs(A[8,8])*math.sqrt(ef[1] + bf[8])
          dA[8,6] = abs(A[8,6])*math.sqrt(rf[1] + pow(dA[6,6]/A[6,6],2))
		  #---ROI 4
          if not comb:
              dA[9,9] = abs(A[9,9])*math.sqrt(ef[2] + bf[9])
              dA[9,6] = abs(A[9,6])*math.sqrt(rf[2] + pow(dA[6,6]/A[6,6],2))
              dA[9,8] = abs(A[9,8])*math.sqrt(rf[9] + pow(dA[8,8]/A[8,8],2))
              dA[9,10] = abs(A[6,6])*math.sqrt(ef[3] + bf[10]) # = dA[14,14]
              dA[9,11] = abs(A[11,11])*math.sqrt(ef[4] + bf[11]) # = dA[15,15]
          else:
              dA[9,9] = abs(A[9,9])*math.sqrt(ef[5]*ROI_7 + ef[6]*ROI_8 + ef[7]*ROI_9 + 
                ef[8]*ROI_10 + bf[3])
              dA[9,6] = abs(A[9,6])*math.sqrt(rf[5]*ROI_7 + rf[6]*ROI_8 + rf[7]*ROI_9 
                + rf[8]*ROI_10 + pow(dA[6,6]/A[6,6],2))
              dA[9,8] = abs(A[9,8])*math.sqrt(rf[12]*ROI_7 + rf[13]*ROI_8 + rf[14]*ROI_9
                + rf[15]*ROI_10 + pow(dA[8,8]/A[8,8],2))
		  #---ROI 5
          dA[8,8] = abs(A[10,10])*math.sqrt(ef[3] + bf[10] )
          dA[8,6] = abs(A[10,6])*math.sqrt(rf[3] + pow(dA[6,6]/A[6,6],2))
          dA[10,8] = abs(A[10,8])*math.sqrt(rf[10] + pow(dA[8,8]/A[8,8],2))
          if h.ratio.size == 36: #added 2020-09-14
              dA[10,11] = abs(A[10,11])*math.sqrt(rf[16] + pow(A[11,11]*math.sqrt(ef[4] + bf[11])/A[11,11],2))
		  #---ROI 6
          dA[11,11] = abs(A[11,11])*math.sqrt(ef[4] + bf[11])
          dA[11,6] = abs(A[11,6])*math.sqrt(rf[4] + pow(dA[6,6]/A[6,6],2))
          dA[11,8] = abs(A[11,8])*math.sqrt(rf[11] + pow(dA[8,8]/A[8,8],2))
          if h.ratio.size == 36: #added 2020-09-14
              dA[11,10] = abs(A[11,10])*math.sqrt(rf[17] + pow(dA[10,10]/A[10,10],2))
    if dim == 6:
          #---ROI 1
          dA[0,0] = abs(A[0,0])*math.sqrt(ef[0] + bf[0])
		  #---ROI 2
          dA[1,1] = abs(A[1,1])*math.sqrt(ef[0] + bf[1])
          dA[1,0] = abs(A[1,0])*math.sqrt(rf[0] + pow(dA[0,0]/A[0,0],2))
		  #---ROI 3
          dA[2,2] = abs(A[2,2])*math.sqrt(ef[1] + bf[2])
          #dA[2,0] = abs(A[3,0])*math.sqrt(rf[1] + pow(dA[0,0]/A[0,0],2))
          dA[2,0] = abs(A[2,0])*math.sqrt(rf[1] + pow(dA[0,0]/A[0,0],2))  #Changed 2021-03-30
		  #---ROI 4
          if not comb:
              dA[3,3] = abs(A[3,3])*math.sqrt(ef[2] + bf[3])
              dA[3,0] = abs(A[3,0])*math.sqrt(rf[2] + pow(dA[0,0]/A[0,0],2))
              dA[3,2] = abs(A[3,2])*math.sqrt(rf[9] + pow(dA[2,2]/A[2,2],2))
              dA[3,4] = abs(A[4,4])*math.sqrt(ef[3] + bf[4]) #= dA[4,4]
              dA[3,5] = abs(A[5,5])*math.sqrt(ef[4] + bf[5]) #= dA[5,5]
          else:
              dA[3,3] = abs(A[3,3])*math.sqrt(ef[5]*ROI_7 + ef[6]*ROI_8 + ef[7]*ROI_9 + 
                ef[8]*ROI_10 + bf[3])
              dA[3,0] = abs(A[3,0])*math.sqrt(rf[5]*ROI_7 + rf[6]*ROI_8 + rf[7]*ROI_9 
                + rf[8]*ROI_10 + pow(dA[0,0]/A[0,0],2))
              dA[3,2] = abs(A[3,2])*math.sqrt(rf[12]*ROI_7 + rf[13]*ROI_8 + rf[14]*ROI_9
                + rf[15]*ROI_10 + pow(dA[2,2]/A[2,2],2))
		  #---ROI 5
          dA[4,4] = abs(A[4,4])*math.sqrt(ef[3] + bf[4])
          dA[4,0] = abs(A[4,0])*math.sqrt(rf[3] + pow(dA[0,0]/A[0,0],2))
          dA[4,2] = abs(A[4,2])*math.sqrt(rf[10] + pow(dA[2,2]/A[2,2],2))
          if h.ratio.size == 36: #added 2020-09-14
              dA[4,5] = abs(A[4,5])*math.sqrt(rf[16] + pow(A[5,5]*math.sqrt(ef[4] + bf[5])/A[5,5],2))
		  #---ROI 6
          dA[5,5] = abs(A[5,5])*math.sqrt(ef[4] + bf[5])
          dA[5,0] = abs(A[5,0])*math.sqrt(rf[4] + pow(dA[0,0]/A[0,0],2))
          dA[5,2] = abs(A[5,2])*math.sqrt(rf[11] + pow(dA[2,2]/A[2,2],2))
          if h.ratio.size == 36: #added 2020-09-14
              dA[5,4] = abs(A[5,4])*math.sqrt(rf[17] + pow(dA[4,4]/A[4,4],2))
    for i in range(dim):
        dA[i,i] += 1.e-8 #Add small number to diagonal elements to avoid singularity
    return dA