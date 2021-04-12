#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:23:37 2020

@author: ringbom
This file is part of 'openSpex'
Copyright (c) 2021 Swedish Defence Research Agency (FOI)
"""

"""
Physics constants

Radioxenon decay constants and branching ratios are taken from the FOI report
"Improvement of the SAUNA Noble Gas System Calibration Procedures, FOI-R--3451--SE (July 2012)"

Radioxenon NE discrimination line parameters are taken from 
M.B.Kalinowski at al, Discrimination of Nuclear Explosions against Civilian 
Sources Based on Atmospheric XenonIsotopic Activity Ratios, Pure and Applied Geophysics 167 (2010) 517.
"""

K_S = 1.6449
XE133_LAM = 1.52956e-6         #Decay constant for 133Xe(g) (1/s)
XE131M_LAM = 6.72467e-7        #Decay constant for 131Xe(m) (1/s)
XE133M_LAM = 3.66326e-6        #Decay constant for 133Xe(m) (1/s)
XE135_LAM = 2.10657e-5         #Decay constant for 135Xe(g) (1/s)
XE135M_LAM = 7.5556e-4         #Decay constant for 135Xe(m) (1/s)
I133_LAM = 9.26e-6             #Decay constant for 133I(g) (1/s)
I131_LAM = 9.9967e-7           #Decay constant for 131I(g) (1/s)
CE141_LAM = 2.4676e-7          #Decay constant for 141Ce (1/s)
CE137_LAM = 7.3022e-10         #Decay constant for 137Cs (1/s)
BA140_LAM = 6.29085e-7         #Decay constant for 140Ba (1/s)
LA140_LAM = 4.77944e-6         #Decay constant for 140La (1/s)
BG_BR_133XE_80 = 0.37289       #Branching ratio for beta/80 keV gamma decay of 133Xe
BG_BR_133XE_30 = 0.48940       #Branching ratio for beta/30 keV X-ray decay of 133Xe
BG_BR_131MXE_30 = 0.54000      #Branching ratio for EC/30 keV X-ray decay of 131mXe
BG_BR_133MXE_30 = 0.55770      #Branching ratio for EC/30 keV X-ray decay of 133mXe
BG_BR_135XE = 0.90000          #Branching ratio for beta/250 keV gamma decay of 135Xe
BG_BR_133XE_80_ERR = 0.005     #Error for Branching ratio for beta/80 keV gamma decay of 133Xe
BG_BR_133XE_30_ERR = 0.013     #Error for Branching ratio for beta/30 keV X-ray decay of 133Xe
BG_BR_131MXE_30_ERR = 0.02     #Error for Branching ratio for EC/30 keV X-ray decay of 131mXe
BG_BR_133MXE_30_ERR = 0.013    #Error for Branching ratio for EC/30 keV X-ray decay of 133mXe */
BG_BR_135XE_ERR = 0.01         #Error for Branching ratio for beta/250 keV gamma decay of 135Xe */
XE_AIR = 0.087                 #Volume (ml) of Xe per m3 of air */
RN222_LAM = 2.0974e-6          #Radon-222 decay constant (1/s) */
BG_BR_222RN = 0.376            #Radon-222 bg branching ratio for 352 keV gamma energy*/ 
BG_BR_222RN_ERR = 0.01         #Radon-222 bg branching ratio for 352 keV gamma energy TODO: This is a generic value. Change!!! */
KAL_K0 = 1e-6                  #Kalinowski 2010 MIRC discrimination line: Xe135/Xe133 vs Xe133m/Xe131m  separation parameter K */  
KAL_M0 = 4.4388                #Kalinowski 2010 MIRC discrimination line: Xe135/Xe133 vs Xe133m/Xe131m  exp decay slope m */  
KAL_K1 = 2e-2                  #Kalinowski 2010 MIRC discrimination line: Xe133m/Xe133 vs Xe133m/Xe131m  separation parameter K*/  
KAL_M1 = 0.6972                #Kalinowski 2010 MIRC discrimination line: Xe133m/Xe133 vs Xe133m/Xe131m exp decay slope m */  
KAL_K2 = 3.78e-22              #Kalinowski 2010 MIRC discrimination line: Xe135/Xe131m vs Xe133/Xe131m  separation parameter K */  
KAL_M2 = 9.0774                #Kalinowski 2010 MIRC discrimination line: Xe135/Xe131m vs Xe133/Xe131m  exp decay slope m */  
KAL_K3 = 2.0e-1                #Kalinowski 2010 MIRC discrimination line: Xe135/Xe133m vs Xe135/Xe131m  separation parameter K */  
KAL_M3 = 0.7996                #Kalinowski 2010 MIRC discrimination line: Xe135/Xe133m vs Xe135/Xe131m  exp decay slope m */  
KAL_K4 = 3.27e+15              #Kalinowski 2010 MIRC discrimination line: Xe135/Xe133 vs Xe133m/Xe133  separation parameter K */  
KAL_M4 = 9.7847                #Kalinowski 2010 MIRC discrimination line: Xe135/Xe133 vs Xe133m/Xe133 exp decay slope m */ 
GAMMA_ENE_RN222 = 350          #Gamma energy (keV) for Rn222 */   
GAMMA_ENE_XE135 = 249.794      #Gamma energy (keV) for Xe-135 */
GAMMA_ENE_XE133 = 80.9979      #Gamma energy (keV) for Xe-133  */
GAMMA_ENE_XE131M = 163.930     #Gamma energy (keV) for Xe-131m  */
GAMMA_ENE_XE133M = 233.221     #Gamma energy (keV) for Xe-133m  */
XRAY_ENE_XE133 = 31.61         #X-ray energy (keV) for Xe-133  */
XRAY_ENE_XE131M = 30.38        #X-ray energy (keV) for Xe-131m  */
XRAY_ENE_XE133M = 30.38        #X-ray energy (keV) for Xe-133m  */
XRAY_ENE_XE135 = 31.61         #X-ray energy (keV) for Xe-135  */
BETA_ENDPOINT_RN222 = 672          #Beta endpoint energy (keV) for Rn-222 decay in coinc. with 350 keV gamma */
BETA_ENDPOINT_XE133_GAMMA = 346.4  #Beta endpoint energy (keV) for Xe-133 decay in coinc. with 80.99979 keV gamma */
BETA_ENDPOINT_XE133_XRAY = 391.4   #Beta (+CE) endpoint energy (keV) for Xe-133 decay in coinc. with X-ray keV */
BETA_ENDPOINT_XE135 = 915          #Beta endpoint energy (keV) for Xe-135 decay in coinc. with 249.794 keV gamma */
XRAY_ENE_CS137 = 32.86             #Cs-137 K X-ray energy (keV) */
GAMMA1_ENE_CS137 = 661.657         #Cs-137 primary gamma energy (keV) */
XRAY_ENE_EU154 = 43.91             #E-154 K X-ray energy (keV) */
GAMMA1_ENE_EU154 = 123.0706        #E-154 Primary gamma energy (keV) */
GAMMA2_ENE_EU154 = 247.9290        #E-154 Second gamma energy (keV) */
GAMMA3_ENE_EU154 = 591.755         #E-154 Third gamma energy (keV) */
GAMMA4_ENE_EU154 = 692.4205        #E-154 Fourth gamma energy (keV) */
XRAY_ENE_EU152 = 40.96             #E-152 K X-ray energy (keV) */
GAMMA1_ENE_EU152 = 121.7817        #E-152 Primary gamma energy (keV) */
GAMMA2_ENE_EU152 = 344.2785        #E-152 Second gamma energy (keV) */
GAMMA3_ENE_EU152 = 244.6975        #E-152 Third gamma energy (keV) */
GAMMA4_ENE_EU152 = 411.1163        #E-152 Fourth gamma energy (keV) */
XRAY_ENE_AM241 = 13.9              #Am-241 L X-ray energy (keV) */
GAMMA1_ENE_AM241 = 59.5409         #Am-241 Primary gamma energy (keV) */
GAMMA2_ENE_AM241 = 26.3446         #Am-241 Second gamma energy (keV) */
K_CE_ENE_XE131M = 129.37            #K - Conversion electron energy (keV) for Xe-131m  */
L_CE_ENE_XE131M = 158.79            # L - Conversion electron energy (keV) for Xe-131m  */
M_CE_ENE_XE131M = 162.89            #M - Conversion electron energy (keV) for Xe-131m  */
N_CE_ENE_XE131M = 163.74            #N - Conversion electron energy (keV) for Xe-131m  */
O_CE_ENE_XE131M = 163.91            #O - Conversion electron energy (keV) for Xe-131m  */
K_CE_ENE_XE131M_INT = 0.616         #K - Conversion electron intensity for Xe-131m  */
L_CE_ENE_XE131M_INT = 0.288         #L - Conversion electron intensity for Xe-131m  */
M_CE_ENE_XE131M_INT = 0.0659        #M - Conversion electron intensity for Xe-131m  */
N_CE_ENE_XE131M_INT = 0.01342       #N - Conversion electron intensity for Xe-131m  */
O_CE_ENE_XE131M_INT = 0.00147       #O - Conversion electron intensity for Xe-131m  */
K_CE_ENE_XE133M = 198.660           #K - Conversion electron energy (keV) for Xe-133m  */
L_CE_ENE_XE133M = 227.768           #L - Conversion electron energy (keV) for Xe-133m  */
M_CE_ENE_XE133M = 232.079           #M - Conversion electron energy (keV) for Xe-133m  */
N_CE_ENE_XE133M = 233.013           #N - Conversion electron energy (keV) for Xe-133m  */
O_CE_ENE_XE133M = 233.205           #O - Conversion electron energy (keV) for Xe-133m  */
K_CE_ENE_XE133M_INT = 0.629         #K - Conversion electron intensity for Xe-133m  */
L_CE_ENE_XE133M_INT = 0.210         #L - Conversion electron intensity for Xe-133m  */
M_CE_ENE_XE133M_INT = 0.047         #M - Conversion electron intensity for Xe-133m  */
N_CE_ENE_XE133M_INT = 0.0096        #N - Conversion electron intensity for Xe-133m  */
O_CE_ENE_XE133M_INT = 0.00107       #O - Conversion electron intensity for Xe-133m  */