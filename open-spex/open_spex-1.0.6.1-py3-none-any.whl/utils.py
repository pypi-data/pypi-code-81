#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 08:53:31 2020

@author: ringbom

This file is part of 'openSpex'
Copyright (c) 2021 Swedish Defence Research Agency (FOI)
"""
import numpy as np
import datetime
import re
import math
import os
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib import pyplot as plt


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class histogram1D(object):
     """ A 1D-histogram where 'data' is in an array with b elements (bins)"""
     def __init__(self, b, data, title = '', xlabel = '', ylabel = '', liveTime = 1):
         self.x = np.arange(0,b,1)
         self.y = np.array(data)
         self.b = b
         self.data, self.bins = np.histogram(self.x,b,weights=self.y)
         self.center = (self.bins[:-1] + self.bins[1:]) / 2
         #self.center = self.bins
         self.title = title
         self.xlabel = xlabel
         self.ylabel = ylabel
         self.liveTime = liveTime
         
     def draw(self, ax, legend = '', useCountrate = False, zoom = [], showTitle = True, showLegend = False):
         """Plot a histogram1D"""
         if zoom != []:
             z = zoom
         else:
             z = [0,len(self.center)]
         if useCountrate:
             data, bins = np.histogram(self.x,self.b,weights=self.y/self.liveTime)
             ax.plot(self.center[z[0]:z[1]],data[z[0]:z[1]],drawstyle="steps",lw = 1, label = legend)
             ylabel = 'counts/bin/s'
             #ax.set_ylabel('counts/bin/s')
         else:
             ax.plot(self.center[z[0]:z[1]],self.data[z[0]:z[1]],drawstyle="steps",lw = 1, label = legend)
             ax.set_ylabel(self.ylabel)
             ylabel = 'counts/bin'
         ax.set_xlabel(self.xlabel)
         if showTitle:
             ax.set_title(self.title)
         if showLegend:
             ax.legend()
         ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
         ax.get_yaxis().get_offset_text().set_visible(False)
         ax_max = max(ax.get_yticks())
         exponent_axis = -np.floor(np.log10(ax_max)).astype(int)
         exp = format(' $\\times$10$^{%i}$' %exponent_axis)
         ylabel += exp
         ax.set_ylabel(ylabel)
         #ax.annotate(r'$\times$10$^{%i}$'%(exponent_axis),
          #   xy=(-.25, .8), xycoords='axes fraction', rotation = 90)
        
     def norm(self, normFactor):
         """Normalize the histogram using normFactor"""
         self.data, self.bins = np.histogram(self.x,self.b,weights=self.y*normFactor)
    
     def rebin(self,fact):
         """Rebin the histogram 'fact' times"""
         self.x = np.arange(0,int(self.b/fact),1)
         yb = []
         for i in np.arange(1,len(self.y),fact):
             yb.append(self.y[i]+self.y[i-1])
         self.y = np.array(yb)
         self.data, self.bins = np.histogram(self.x,int(self.b/fact),weights=self.y)
         self.center = (self.bins[:-1] + self.bins[1:]) / 2
         
class histogram2D(object):
        """ 
        A 2D- beta-gamma histogram with '[binx,biny]' bins and 
        'data' = [(0,0), (0,1),..., (binx-1,biny-1)] 
        """
        def __init__(self, bins, data, title = '', xlabel = '', ylabel = ''):
            self.bins = bins
            self.data = data
            self.title = title
            self.xlabel = xlabel
            self.ylabel = ylabel
            
        def draw(self, fig, ax, roi_data, detBP = None, showBar = True):
            b = []
            g = []
            for i in range(self.bins[1]):
                bi = np.arange(self.bins[0])
                gi = np.full(self.bins[1],i)
                for j in range(len(bi)):
                    b.append(bi[j])
                for j in range(len(gi)):
                    g.append(gi[j])
            ax.set_xlabel(self.xlabel)
            ax.set_ylabel(self.ylabel)
            ax.set_title(self.title)
            im_bg = ax.hist2d(b, g, self.bins, weights = self.data)
            if showBar:
                if fig != None:
                    cb = fig.colorbar(im_bg[3])
                    cb.set_label("Counts")
            self.drawROIs(ax,roi_data,detBP)
        
        def drawROIs(self, ax, roi_data, detBP=None):
            codes = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY,]
            for roi in roi_data:
                verts = []
                verts.append([roi[1],roi[3]])
                verts.append([roi[1],roi[4]])
                verts.append([roi[2],roi[4]])
                verts.append([roi[2],roi[3]])
                verts.append([roi[1],roi[3]])
                path = Path(verts, codes)
                patch = patches.PathPatch(path, facecolor='none', lw=1, edgecolor = 'white')
                ax.add_patch(patch)
            if detBP != None:
                i = 0
                for roi in roi_data:
                    verts = []
                    if pow(2,i) & detBP:
                        verts.append([roi[1],roi[3]])
                        verts.append([roi[1],roi[4]])
                        verts.append([roi[2],roi[4]])
                        verts.append([roi[2],roi[3]])
                        verts.append([roi[1],roi[3]])
                        path = Path(verts, codes)
                        patch = patches.PathPatch(path, facecolor='none', lw=1, edgecolor = 'yellow')
                        ax.add_patch(patch)
                    i += 1

def draw_1D_hist(ax,bins,data,col='blue'):
      """ Draw a 1D- histogram with where 'data' = (0,1,...,bins-1) """
      x = np.arange(0,bins,1)
      y = np.array(data)
      return ax.hist(x,bins,weights=y,color=col,histtype='step')
  
def draw1DHist(ax,data, col='blue'):
         hist,center,width,title = data
         ax.plot(center,hist,drawstyle="steps",lw=0.5,color=col)
         ax.set_xlabel('Energy (chan)')
         ax.set_ylabel('Counts/bin')
         ax.set_title(title)

def make_1D_hist(bins,data,title):
      """ Make a 1D- histogram with where 'data' = (0,1,...,bins-1) """
      x = np.arange(0,bins,1)
      y = np.array(data)
      data,bins = np.histogram(x,bins,weights=y)
      width = 1 * (bins[1] - bins[0])
      center = (bins[:-1] + bins[1:]) / 2
      return data,center,width,title
      
def draw_2D_hist(ax,bins,data):
      """ Draw a 2D- histogram with '[binx,biny]' bins and 
      'data' = [(0,0), (0,1),..., (binx-1,biny-1)] 
      """
      b = []
      g = []
      for i in range(bins[1]):
          bi = np.arange(bins[0])
          gi = np.full(bins[1],i)
          for j in range(len(bi)):
              b.append(bi[j])
          for j in range(len(gi)):
              g.append(gi[j])
      return ax.hist2d(b, g, bins, weights = data)
  
def make_2D_hist(bins,data):
      """ Make a 2D- histogram with '[binx,biny]' bins and 
      'data' = [(0,0), (0,1),..., (binx-1,biny-1)] 
      """
      b = []
      g = []
      for i in range(bins[1]):
          bi = np.arange(bins[0])
          gi = np.full(bins[1],i)
          for j in range(len(bi)):
              b.append(bi[j])
          for j in range(len(gi)):
              g.append(gi[j])
      return np.histogram2d(b, g, bins, weights = data)

def drawROIs(rois, ax, lw= 1, ecolor = 'black', maxroi = 9):
        if ax == None:
            fig,ax = plt.subplots()
            ax.set_xlim(0,256)
            ax.set_ylim(0,256)
        codes = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY,]
        i = 0
        for roi in rois:
            if i < maxroi:
                verts = []
                verts.append([roi[1],roi[3]])
                verts.append([roi[1],roi[4]])
                verts.append([roi[2],roi[4]])
                verts.append([roi[2],roi[3]])
                verts.append([roi[1],roi[3]])
                path = Path(verts, codes)
                patch = patches.PathPatch(path, facecolor='none', lw=lw, edgecolor=ecolor)
                ax.add_patch(patch)
            i += 1
  
def fit_polynom(data, pol_order):
    """Do polynomial fit with order 'pol_order' to data in the form [x,y,y_err] 
       y_err not used at the moment. Minium two data points required. If only
       two data points are supplied, the order of the polynom is set to 1 (linear)
       The result is returned as a 'numpy.poly1d' polynom
    """
    if len(data) < 2:
        print("Error in fit_polynom: Less that two data points")
        return [0]
    if len(data) ==2 and pol_order != 1:
        print("Warning in utils.fit_polynom: Only two data points. Linear fit used.")
        pol_order = 1
    x = []
    y = []
    y_err = []
    for point in data:
        x.append(point[0])
        y.append(point[1])
        y_err.append(point[2])
    x = np.asarray(x) 
    y = np.asarray(y)
    y_err = np.asarray(y_err)
    p = np.poly1d(np.polyfit(x,y,pol_order))
    return p

def calc_pol(x,pol):
    """Calculate a polynom of order n.  
    pol = pol[0]*x^n + pol[1]*x^(n-1) + ...
    """
    ret = 0
    order = len(pol)-1
    for f in pol:
        ret += f*pow(x,order)
        order -= 1
    return ret

def invert_pol(y,pol):
    """
    Get the x value where y = pol(x), where pol is a numpy.poly1d polynom 
    of order 1 (linear) or 2 (quadratic).
    """
    if pol.order == 2:
        x1 = (-pol[1] + math.sqrt(pol[1]*pol[1] - 4*pol[2]*(pol[0]-y)))/2./pol[2]
        x2 = (-pol[1] - math.sqrt(pol[1]*pol[1] - 4*pol[2]*(pol[0]-y)))/2./pol[2]
        return max([x1,x2])
    elif pol.order == 1:
        return (y-pol[0])/pol[1]
    else:
        print("Error in invert_pol: order of polynom not 1 or 2")
        return 0

def chanRes(e, ene_chan_pol, ene_fwhm_pol):
    """
    Get channel and resolution (sigma) in channels at energy e 
    given energy-channel and energy-fwhm polynoms (linear or quadratic)
    """
    c = ene_chan_pol(e)
    de = ene_fwhm_pol(e)/2.35
    if ene_chan_pol.order == 2:
        dc = (ene_chan_pol[1] + 2*ene_chan_pol[2]*e)*de
    else:
        dc = ene_chan_pol[1]*de
    return c,dc 

def readDate(d):
    """Make a datetime object from string with format
    'Y-M-D h:m:s.f' or 'Y/M/D h:m:s.f or 'M/D/Y HH:MM'
    """
    r1 = re.compile('[1-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9] [0-9][0-9]:[0-9][0-9]*')
    r2 = re.compile('[1-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]*')
    dp = d.split('.',1)
    dps = dp[0]
    if r1.match(dps):
        ds = datetime.datetime.strptime(dps, '%Y/%m/%d %H:%M:%S')
    elif r2.match(dps):
        ds = datetime.datetime.strptime(dps, '%Y-%m-%d %H:%M:%S')
    else:
        ds = None
        print("Error in readDate: Wrong time format:",d)
    return ds

def Fieller(x1, dx1, x2, dx2, rho):
    """
    Calculate upper and lower confidence intervals r+ and r- 
    for the ratio r = x2/x1 of two normally distributed variables using Fiellers' theorem.
    Depending on how the eror ellipse intersects any of the axes, 
    different solutions for [r-,r+] are obtained:
        
    Completely unbounded:   ]-inf, inf[
    Exclusive unbounded:    ]-inf, r+]
    Bounded:                [r-,r+]
        
    Parameters
    ==========
    x1          value 1
    dx1         sigma for value 1
    x2          value 2
    dx2         sigma for value 2
    rho         correlation coefficient
    
    Return:    r+,r- if solution is bounded. Otherwize None,None 
    """
    if dx1==0 or dx2==0:
        print("Uncertainty =0, nothing calculated")
        return None,None 
    # calculate error matrix
    c11 = dx1*dx1
    c22 = dx2*dx2
    c12 = rho*dx1*dx2
    #calculate q2 limits 
    q2_exclusive = x1*x1/c11
    q2_complete = (x2*x2*c11 - 2*x1*x2*c12+x1*x1*c22)/(c11*c22-c12*c12)
    if q2_complete <= 1: 
     #   print("Completely unbounded")
        return None, None 
    if q2_exclusive < 1 and q2_complete > 1:
      #  print("Exclusive unbounded")
        return None,None
    r_neg = ((x1*x2-c12) - math.sqrt((x1*x2-c12)*(x1*x2-c12)-(x1*x1-c11)*(x2*x2-c22)))/(x1*x1-c11)
    r_pos = ((x1*x2-c12) + math.sqrt((x1*x2-c12)*(x1*x2-c12)-(x1*x1-c11)*(x2*x2-c22)))/(x1*x1-c11)
    #print(r_neg," ", r_pos)
    return r_neg,r_pos


def get_block(data, block_name):
    """ Returns the block 'block_name' as a list of lines from the string 'data' on PHD-format."""
    block=[]
    start = 0
    for line in data.splitlines():
        if line.startswith(block_name):
            start=1
        if ((line.startswith("#") and block_name not in line) or ('STOP' in line)) and start == 1:
            start=0
            return block
        if start==1:
            block.append(line)
    return block

def getDataType(fileName):
    """Returns DATA_TYPE from a PHD-file"""
    with open(fileName, 'r') as f:
        data = f.read()
        for line in data.splitlines():
            w = line.split()
            if 'DATA_TYPE' in line:
                return w[1]
    print("Error in getDataType: No datatype found.")
    return None

def getMeasurementId(fileName, dataType):
    """
    Get the measurement id from an IMS file. 
    dataType = 'sample', 'detbk', or 'gasbk'
    """
    with open(fileName, 'r') as f:
        data = f.read()
        block = get_block(data,'#Header')
        if len(block) > 0:
            l = 0
            for line in block:
                w = line.split()
                if l == 3:
                    sample_id = w[0]
                    detbk_id = w[1]
                    gasbk_id = w[2]
                l += 1
            if dataType == 'sample':
                return sample_id
            elif dataType == 'detbk':
                return detbk_id
            elif dataType == 'gasbk':
                return gasbk_id
            else:
                print(format("Error in getSampleId: Wrong data type %s" %dataType))
                return None
        else:
            print("Error in getSampleId: No #Header found.")
            return None

def getIMSFiles(path,  dataType):
    """Get a list of IMS files in path for a certain data type.
       the files should have extension '.phd' or '.PHD'
    """
    res = []
    for file in os.listdir(path):
        if file.endswith(".phd") or file.endswith(".PHD"):
            fn = path + "/" + file
            if getDataType(fn) == dataType:
                res.append(fn)
    if len(res) == 0:
        print(format("Warning: No %s files found." %dataType))
    else:
        print("%d files of type %s found" %(len(res), dataType))
    return res