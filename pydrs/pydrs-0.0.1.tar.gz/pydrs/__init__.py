#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 26/04/2016
Versão 1.0
@author: Ricieri (ELP)
Python 3.4.4
"""

import struct
import glob
import serial
import time
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import os

from datetime import datetime

__author__ = ""
__version__ = "0.0.1"

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
======================================================================
                    Listas de Entidades BSMP
        A posição da entidade na lista corresponde ao seu ID BSMP
======================================================================
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

UDC_FIRMWARE_VERSION = "0.41 2020-09-11"

ListVar = ['iLoad1','iLoad2','iMod1','iMod2','iMod3','iMod4','vLoad',
           'vDCMod1','vDCMod2','vDCMod3','vDCMod4','vOutMod1','vOutMod2',
           'vOutMod3','vOutMod4','temp1','temp2','temp3','temp4','ps_OnOff',
           'ps_OpMode','ps_Remote','ps_OpenLoop','ps_SoftInterlocks',
           'ps_HardInterlocks','iRef','wfmRef_Gain','wfmRef_Offset','sigGen_Enable','sigGen_Type',
           'sigGen_Ncycles','sigGenPhaseStart','sigGen_PhaseEnd','sigGen_Freq',
           'sigGen_Amplitude','sigGen_Offset','sigGen_Aux','dp_ID','dp_Class','dp_Coeffs','ps_Model',
           'wfmRef_PtrBufferStart','wfmRef_PtrBufferEnd','wfmRef_PtrBufferK','wfmRef_SyncMode']
           
ListCurv = ['wfmRef_Curve','sigGen_SweepAmp','samplesBuffer','fullwfmRef_Curve','wfmRef_Blocks','samplesBuffer_blocks']

ListFunc = ['TurnOn','TurnOff','OpenLoop','ClosedLoop','OpMode','RemoteInterface',
            'SetISlowRef','ConfigWfmRef','ConfigSigGen', 'EnableSigGen',
            'DisableSigGen','ConfigDPModule','WfmRefUpdate','ResetInterlocks','ConfigPSModel',
            'ConfigHRADC','ConfigHRADCOpMode','EnableHRADCSampling','DisableHRADCSampling','ResetWfmRef',
            'SetRSAddress','EnableSamplesBuffer','DisableSamplesBuffer','SetISlowRefx4','SelectHRADCBoard','SelectTestSource',
            'ResetHRADCBoards','Config_nHRADC','ReadHRADC_UFM','WriteHRADC_UFM','EraseHRADC_UFM','ReadHRADC_BoardData']
            
ListTestFunc = ['UdcIoExpanderTest', 'UdcLedTest', 'UdcBuzzerTest', 'UdcEepromTest', 'UdcFlashTest', 'UdcRamTest',
                'UdcRtcTest', 'UdcSensorTempTest', 'UdcIsoPlaneTest', 'UdcAdcTest', 'UdcUartTest', 'UdcLoopBackTest',
                'UdcComTest', 'UdcI2cIsoTest']
                
ListHRADCInputType = ['Vin_bipolar','Vin_unipolar_p','Vin_unipolar_n','Iin_bipolar','Iin_unipolar_p',
                      'Iin_unipolar_n','Vref_bipolar_p','Vref_bipolar_n','GND','Vref_unipolar_p',
                      'Vref_unipolar_n','GND_unipolar','Temp','Reserved0','Reserved1','Reserved2']

ListPSModels = ['FBP_100kHz', 'FBP_Parallel_100kHz', 'FAC_ACDC_10kHz', 'FAC_DCDC_20kHz',
                'FAC_Full_ACDC_10kHz', 'FAC_Full_DCDC_20kHz', 'FAP_ACDC',
                'FAP_DCDC_20kHz', 'TEST_HRPWM', 'TEST_HRADC', 'JIGA_HRADC',
                'FAP_DCDC_15kHz_225A', 'FBPx4_100kHz', 'FAP_6U_DCDC_20kHz',
                'JIGA_BASTIDOR']

ListPSModels_v2_1 = ['Empty','FBP','FBP_DCLink','FAC_ACDC','FAC_DCDC',
                     'FAC_2S_ACDC','FAC_2S_DCDC','FAC_2P4S_ACDC','FAC_2P4S_DCDC',
                     'FAP','FAP_4P','FAC_DCDC_EMA','FAP_2P2S','FAP_IMAS',
                     'FAC_2P_ACDC_IMAS','FAC_2P_DCDC_IMAS','Invalid','Invalid',
                     'Invalid','Invalid','Invalid','Invalid','Invalid','Invalid',
                     'Invalid','Invalid','Invalid','Invalid','Invalid','Invalid',
                     'Invalid','Uninitialized']

ListVar_v2_1 = ['ps_status','ps_setpoint','ps_reference','firmware_version',
                'counter_set_slowref','counter_sync_pulse','siggen_enable',
                'siggen_type','siggen_num_cycles','siggen_n','siggen_freq',
                'siggen_amplitude','siggen_offset','siggen_aux_param',
                'wfmref_selected','wfmref_sync_mode','wfmref_gain',
                'wfmref_offset','p_wfmref_start','p_wfmref_end','p_wfmref_idx']
                
#ListCurv_v2_1 = ['wfmref','buf_samples_ctom','buf_samples_mtoc']
ListCurv_v2_1 = ['wfmref_data_0','wfmref_data_1','buf_samples_ctom']

ListFunc_v2_1 = ['turn_on','turn_off','open_loop','closed_loop','select_op_mode',
                 'reset_interlocks','set_command_interface',
                 'set_serial_termination','unlock_udc','lock_udc',
                 'cfg_source_scope','cfg_freq_scope','cfg_duration_scope',
                 'enable_scope','disable_scope','sync_pulse','set_slowref',
                 'set_slowref_fbp','set_slowref_readback_mon',
                 'set_slowref_fbp_readback_mon','set_slowref_readback_ref',
                 'set_slowref_fbp_readback_ref','reset_counters','cfg_wfmref',
                 'select_wfmref','get_wfmref_size','reset_wfmref','cfg_siggen',
                 'set_siggen','enable_siggen','disable_siggen','set_param','get_param',
                 'save_param_eeprom','load_param_eeprom', 'save_param_bank',
                 'load_param_bank','set_dsp_coeffs','get_dsp_coeff',
                 'save_dsp_coeffs_eeprom', 'load_dsp_coeffs_eeprom',
                 'save_dsp_modules_eeprom', 'load_dsp_modules_eeprom','reset_udc']

ListOpMode_v2_1 = ['Off','Interlock','Initializing','SlowRef','SlowRefSync',
                   'Cycle','RmpWfm','MigWfm','FastRef']
                   
ListSigGenTypes_v2_1 = ['Sine','DampedSine','Trapezoidal','DampedSquaredSine',
                        'Square']

ListParameters = ['PS_Name','PS_Model','Num_PS_Modules','Command_Interface',
                  'RS485_Baudrate','RS485_Address','RS485_Termination',
                  'UDCNet_Address','Ethernet_IP','Ethernet_Subnet_Mask', 
                  'Buzzer_Volume','Freq_ISR_Controller','Freq_TimeSlicer',
                  'Control_Loop_State','Max_Ref','Min_Ref','Max_Ref_OpenLoop',
                  'Min_Ref_OpenLoop',
                  'PWM_Freq','PWM_DeadTime','PWM_Max_Duty','PWM_Min_Duty',
                  'PWM_Max_Duty_OpenLoop','PWM_Min_Duty_OpenLoop',
                  'PWM_Lim_Duty_Share','HRADC_Num_Boards','HRADC_Freq_SPICLK',
                  'HRADC_Freq_Sampling','HRADC_Enable_Heater',
                  'HRADC_Enable_Monitor','HRADC_Type_Transducer',
                  'HRADC_Gain_Transducer','HRADC_Offset_Transducer','SigGen_Type',
                  'SigGen_Num_Cycles','SigGen_Freq','SigGen_Amplitude',
                  'SigGen_Offset','SigGen_Aux_Param','WfmRef_ID_WfmRef',
                  'WfmRef_SyncMode','WfmRef_Frequency','WfmRef_Gain',
                  'WfmRef_Offset','Analog_Var_Max','Analog_Var_Min',
                  'Hard_Interlocks_Debounce_Time','Hard_Interlocks_Reset_Time',
                  'Soft_Interlocks_Debounce_Time','Soft_Interlocks_Reset_Time',
                  'Scope_Sampling_Frequency','Scope_Source','','','','','','',
                  '','','','','Password','Enable_Onboard_EEPROM']

ListBCBFunc = ['ClearPof', 'SetPof', 'ReadPof', 'EnableBuzzer', 'DisableBuzzer',
                'SendUartData', 'GetUartData', 'SendCanData', 'GetCanData',
                'GetI2cData']

typeFormat = {'uint8_t': 'BBHBB', 'uint16_t': 'BBHHB', 'uint32_t': 'BBHIB', 
              'float': 'BBHfB'}
              
bytesFormat = {'Uint16': 'H', 'Uint32': 'L', 'Uint64': 'Q', 'float': 'f'}

typeSize   = {'uint8_t': 6, 'uint16_t': 7, 'uint32_t': 9, 'float': 9}

num_blocks_curves_fbp = [4, 4, 4]
num_blocks_curves_fax = [16, 16, 16]
size_curve_block = [1024, 1024, 1024]

ufmOffset = {'serial': 0, 'calibdate': 4, 'variant': 9, 'rburden': 10,
             'calibtemp': 12, 'vin_gain': 14, 'vin_offset': 16,
             'iin_gain': 18, 'iin_offset': 20, 'vref_p': 22, 'vref_n': 24,
             'gnd': 26}
             
hradcVariant = ['HRADC-FBP','HRADC-FAX-A','HRADC-FAX-B','HRADC-FAX-C','HRADC-FAX-D']

hradcInputTypes = ['GND', 'Vref_bipolar_p', 'Vref_bipolar_n', 'Temp',
                       'Vin_bipolar_p', 'Vin_bipolar_n', 'Iin_bipolar_p','Iin_bipolar_n']

NUM_MAX_COEFFS_DSP = 12
num_dsp_classes = 7                       
num_dsp_modules = [4, 4, 4, 6, 8, 4, 2, 2]
num_coeffs_dsp_modules = [0, 1, 1, 4, 8, 16, 2]
dsp_classes_names = ["DSP_Error", "DSP_SRLim", "DSP_LPF","DSP_PI", 
                     "DSP_IIR_2P2Z", "DSP_IIR_3P3Z", "DSP_VdcLink_FeedForward",
                     "DSP_Vect_Product"]

# FBP
list_fbp_soft_interlocks = ['Heat-Sink Overtemperature']
                           
list_fbp_hard_interlocks = ['Load Overcurrent',
                            'Load Overvoltage',
                            'DCLink Overvoltage',
                            'DCLink Undervoltage',
                            'DCLink Relay Fault',
                            'DCLink Fuse Fault',
                            'MOSFETs Driver Fault',
                            'Welded Relay Fault']

# FBP DC-Link
list_fbp_dclink_hard_interlocks = ['Power_Module_1_Fault',
                                   'Power_Module_2_Fault',
                                   'Power_Module_3_Fault',
                                   'Total_Output_Overvoltage',
                                   'Power_Module_1_Overvoltage',
                                   'Power_Module_2_Overvoltage',
                                   'Power_Module_3_Overvoltage',
                                   'Total_Output_Undervoltage',
                                   'Power_Module_1_Undervoltage',
                                   'Power_Module_2_Undervoltage',
                                   'Power_Module_3_Undervoltage',
                                   'Smoke_Detector','External_Interlock']

# FAC ACDC
list_fac_acdc_soft_interlocks = []

list_fac_acdc_hard_interlocks = ['CapBank Overvoltage',
                                 'Rectifier Overvoltage',
                                 'Rectifier Undervoltage',
                                 'Rectifier Overcurrent',
                                 'Welded Contactor Fault',
                                 'Opened Contactor Fault',
                                 'IIB Input Stage Interlock',
                                 'IIB Command Interlock']

list_fac_acdc_iib_is_interlocks = ['Rectifier Overvoltage',
                                   'Input Overcurrent',
                                   'IGBT Overtemperature',
                                   'IGBT Overtemperature HW',
                                   'Driver Overvoltage',
                                   'Driver Overcurrent',
                                   'Top Driver Error',
                                   'Bottom Driver Error',
                                   'Inductors Overtemperature',
                                   'Heat-Sink Overtemperature',
                                   'Board IIB Overtemperature',
                                   'Module Overhumidity']

list_fac_acdc_iib_is_alarms = ['Rectifier Overvoltage',
                               'Input Overcurrent',
                               'IGBT Overtemperature',
                               'Driver Overvoltage',
                               'Driver Overcurrent',
                               'Inductors Overtemperature',
                               'Heat-Sink Overtemperature',
                               'Board IIB Overtemperature',
                               'Module Overhumidity']

list_fac_acdc_iib_cmd_interlocks = ['Capbank Overvoltage',
                                    'Output Overvoltage',
                                    'External Boards Overvoltage',
                                    'Auxiliary Board Overcurrent',
                                    'IDB Board Overcurrent',
                                    'Rectifier Inductor Overtemperature',
                                    'Rectifier Heat-Sink Overtemperature',
                                    'AC Mains Overcurrent',
                                    'Emergency Button',
                                    'AC Mains Undervoltage',
                                    'AC Mains Overvoltage',
                                    'Ground Leakage Overcurrent',
                                    'Board IIB Overtemperature',
                                    'Module Overhumidity']

list_fac_acdc_iib_cmd_alarms = ['Capbank Overvoltage',
                                'Output Overvoltage',
                                'External Boards Overvoltage',
                                'Auxiliary Board Overcurrent',
                                'IDB Board Overcurrent',
                                'Rectifier Inductor Overtemperature',
                                'Rectifier Heat-Sink Overtemperature',
                                'Ground Leakage Overcurrent',
                                'Board IIB Overtemperature',
                                'Module Overhumidity']

# FAC DCDC
list_fac_dcdc_soft_interlocks = ['DCCT 1 Fault',
                                 'DCCT 2 Fault',
                                 'DCCT High Difference',
                                 'Load Feedback 1 Fault',
                                 'Load Feedback 2 Fault']
                            
list_fac_dcdc_hard_interlocks = ['Load Overcurrent',
                                 'CapBank Overvoltage',
                                 'CapBank Undervoltage',
                                 'IIB Interlock',
                                 'External Interlock',
                                 'Rack Interlock']

list_fac_dcdc_iib_interlocks = ['Input Overvoltage',
                                'Input Overcurrent',
                                'Output Overcurrent',
                                'IGBT 1 Overtemperature',
                                'IGBT 1 Overtemperature HW',
                                'IGBT 2 Overtemperature',
                                'IGBT 2 Overtemperature HW',
                                'Driver Overvoltage',
                                'Driver 1 Overcurrent',
                                'Driver 2 Overcurrent',
                                'Top Driver 1 Error',
                                'Bottom Driver 1 Error',
                                'Top Driver 2 Error',
                                'Bottom Driver 2 Error',
                                'Inductors Overtemperature',
                                'Heat-Sink Overtemperature',
                                'Ground Leakage Overcurrent',
                                'Board IIB Overtemperature',
                                'Module Overhumidity']
                                
list_fac_dcdc_iib_alarms = ['Input Overvoltage',
                            'Input Overcurrent',
                            'Output Overcurrent',
                            'IGBT 1 Overtemperature',
                            'IGBT 2 Overtemperature',
                            'Driver Overvoltage',
                            'Driver 1 Overcurrent',
                            'Driver 2 Overcurrent',
                            'Inductors Overtemperature',
                            'Heat-Sink Overtemperature',
                            'Ground Leakage Overcurrent',
                            'Board IIB Overtemperature',
                            'Module Overhumidity']

# FAC-2S AC/DC
list_fac_2s_acdc_hard_interlocks = ['CapBank Overvoltage',
                                    'Rectifier Overvoltage',
                                    'Rectifier Undervoltage',
                                    'Rectifier Overcurrent',
                                    'Welded Contactor Fault',
                                    'Opened Contactor Fault',
                                    'IIB Input Stage Interlock',
                                    'IIB Command Interlock']

list_fac_2s_acdc_iib_is_interlocks = list_fac_acdc_iib_is_interlocks
list_fac_2s_acdc_iib_cmd_interlocks = list_fac_acdc_iib_cmd_interlocks
list_fac_2s_acdc_iib_is_alarms = list_fac_acdc_iib_is_alarms
list_fac_2s_acdc_iib_cmd_alarms = list_fac_acdc_iib_cmd_alarms

# FAC-2S DC/DC
list_fac_2s_dcdc_soft_interlocks = ['DCCT 1 Fault',
                                    'DCCT 2 Fault',
                                    'DCCT High Difference',
                                    'Load Feedback 1 Fault',
                                    'Load Feedback 2 Fault']
                            
list_fac_2s_dcdc_hard_interlocks = ['Load Overcurrent',
                                    'Module 1 CapBank Overvoltage',
                                    'Module 2 CapBank Overvoltage',
                                    'Module 1 CapBank Undervoltage',
                                    'Module 2 CapBank Undervoltage',
                                    'IIB Mod 1 Itlk',
                                    'IIB Mod 2 Itlk',
                                    'External Interlock',
                                    'Rack Interlock']
  
list_fac_2s_dcdc_iib_interlocks = list_fac_dcdc_iib_interlocks
list_fac_2s_dcdc_iib_alarms = list_fac_dcdc_iib_alarms

# FAC-2P4S AC/DC
list_fac_2p4s_acdc_hard_interlocks = ['CapBank Overvoltage',
                                      'Rectifier Overvoltage',
                                      'Rectifier Undervoltage',
                                      'Rectifier Overcurrent',
                                      'Welded Contactor Fault',
                                      'Opened Contactor Fault',
                                      'IIB Input Stage Interlock',
                                      'IIB Command Interlock']

list_fac_2p4s_acdc_iib_is_interlocks = list_fac_acdc_iib_is_interlocks
list_fac_2p4s_acdc_iib_cmd_interlocks = list_fac_acdc_iib_cmd_interlocks
list_fac_2p4s_acdc_iib_is_alarms = list_fac_acdc_iib_is_alarms
list_fac_2p4s_acdc_iib_cmd_alarms = list_fac_acdc_iib_cmd_alarms

# FAC-2P4S DC/DC
list_fac_2p4s_dcdc_soft_interlocks = ['DCCT 1 Fault',
                                      'DCCT 2 Fault',
                                      'DCCT High Difference',
                                      'Load Feedback 1 Fault',
                                      'Load Feedback 2 Fault',
                                      'Arm 1 Overcurrent',
                                      'Arm 2 Overcurrent',
                                      'Arms High Difference',
                                      'Complementary PS Interlock']
                            
list_fac_2p4s_dcdc_hard_interlocks = ['Load Overcurrent',
                                      'Module 1 CapBank Overvoltage',
                                      'Module 2 CapBank Overvoltage',
                                      'Module 3 CapBank Overvoltage',
                                      'Module 4 CapBank Overvoltage',
                                      'Module 5 CapBank Overvoltage',
                                      'Module 6 CapBank Overvoltage',
                                      'Module 7 CapBank Overvoltage',
                                      'Module 8 CapBank Overvoltage',
                                      'Module 1 CapBank Undervoltage',
                                      'Module 2 CapBank Undervoltage',
                                      'Module 3 CapBank Undervoltage',
                                      'Module 4 CapBank Undervoltage',
                                      'Module 5 CapBank Undervoltage',
                                      'Module 6 CapBank Undervoltage',
                                      'Module 7 CapBank Undervoltage',
                                      'Module 8 CapBank Undervoltage',
                                      'IIB 1 Itlk',
                                      'IIB 2 Itlk',
                                      'IIB 3 Itlk',
                                      'IIB 4 Itlk',
                                      'IIB 5 Itlk',
                                      'IIB 6 Itlk',
                                      'IIB 7 Itlk',
                                      'IIB 8 Itlk']
                                      
list_fac_2p4s_dcdc_iib_interlocks = list_fac_dcdc_iib_interlocks
list_fac_2p4s_dcdc_iib_alarms = list_fac_dcdc_iib_alarms

# FAP                                 
list_fap_soft_interlocks = ['DCCT 1 Fault',
                            'DCCT 2 Fault',
                            'DCCT High Difference',
                            'Load Feedback 1 Fault',
                            'Load Feedback 2 Fault',
                            'IGBTs Current High Difference']
                            
list_fap_hard_interlocks = ['Load Overcurrent',
                            'Load Overvoltage',
                            'DCLink Overvoltage',
                            'DCLink Undervoltage',
                            'Welded Contactor Fault',
                            'Opened Contactor Fault',
                            'IGBT 1 Overcurrent',
                            'IGBT 2 Overcurrent',
                            'IIB Itlk']
                            
list_fap_iib_interlocks = ['Input Overvoltage',
                           'Output Overvoltage',
                           'IGBT 1 Overcurrent',
                           'IGBT 2 Overcurrent',
                           'IGBT 1 Overtemperature',
                           'IGBT 2 Overtemperature',
                           'Driver Overvoltage',
                           'Driver 1 Overcurrent',
                           'Driver 2 Overcurrent',
                           'Driver 1 Error',
                           'Driver 2 Error',
                           'Inductors Overtemperature',
                           'Heat-Sink Overtemperature',
                           'DCLink Contactor Fault',
                           'Contact Sticking of Contactor',
                           'External Interlock',
                           'Rack Interlock',
                           'High Leakage Current',
                           'Board IIB Overtemperature',
                           'Module Overhumidity']
                            
list_fap_iib_alarms = ['Input Overvoltage',
                       'Output Overvoltage',
                       'IGBT 1 Overcurrent',
                       'IGBT 2 Overcurrent',
                       'IGBT 1 Overtemperature',
                       'IGBT 2 Overtemperature',
                       'Driver Overvoltage',
                       'Driver 1 Overcurrent',
                       'Driver 2 Overcurrent',
                       'Inductors Overtemperature',
                       'Heat-Sink Overtemperature',
                       'High Leakage Current',
                       'Board IIB Overtemperature',
                       'Module Overhumidity']

# FAP-4P                                 
list_fap_4p_soft_interlocks = ['DCCT 1 Fault',
                               'DCCT 2 Fault',
                               'DCCT High Difference',
                               'Load Feedback 1 Fault',
                               'Load Feedback 2 Fault',
                               'IGBTs Current High Difference']
                            
list_fap_4p_hard_interlocks = ['Load Overcurrent',
                               'Load Overvoltage',
                               'IGBT 1 Mod 1 Overcurrent',
                               'IGBT 2 Mod 1 Overcurrent',
                               'IGBT 1 Mod 2 Overcurrent',
                               'IGBT 2 Mod 2 Overcurrent',
                               'IGBT 1 Mod 3 Overcurrent',
                               'IGBT 2 Mod 3 Overcurrent',
                               'IGBT 1 Mod 4 Overcurrent',
                               'IGBT 2 Mod 4 Overcurrent',
                               'Welded Contactor Mod 1 Fault',
                               'Welded Contactor Mod 2 Fault',
                               'Welded Contactor Mod 3 Fault',
                               'Welded Contactor Mod 4 Fault',
                               'Opened Contactor Mod 1 Fault',
                               'Opened Contactor Mod 2 Fault',
                               'Opened Contactor Mod 3 Fault',
                               'Opened Contactor Mod 4 Fault',
                               'DCLink Mod 1 Overvoltage',
                               'DCLink Mod 2 Overvoltage',
                               'DCLink Mod 3 Overvoltage',
                               'DCLink Mod 4 Overvoltage',
                               'DCLink Mod 1 Undervoltage',
                               'DCLink Mod 2 Undervoltage',
                               'DCLink Mod 3 Undervoltage',
                               'DCLink Mod 4 Undervoltage',
                               'IIB Mod 1 Itlk',
                               'IIB Mod 2 Itlk',
                               'IIB Mod 3 Itlk',
                               'IIB Mod 4 Itlk']
                               
list_fap_4p_iib_interlocks = list_fap_iib_interlocks
list_fap_4p_iib_alarms = list_fap_iib_alarms
                              
# FAC DCDC EMA
list_fac_dcdc_ema_soft_interlocks = ['DCCT Fault',
                                     'Load Feedback Fault']
                            
list_fac_dcdc_ema_hard_interlocks = ['Load Overcurrent',
                                     'CapBank Overvoltage',
                                     'CapBank Undervoltage',
                                     'Emergency Button',
                                     'Load Waterflow',
                                     'Load Overtemperature',
                                     'IIB Itlk']
 
# FAP-2P2S                                 
list_fap_2p2s_soft_interlocks = ['DCCT 1 Fault',
                               'DCCT 2 Fault',
                               'DCCT High Difference',
                               'Load Feedback 1 Fault',
                               'Load Feedback 2 Fault',
                               'Arms High Difference',
                               'IGBTs Current High Difference',
                               'Complementary PS Interlock']
                            
list_fap_2p2s_hard_interlocks = ['Load Overcurrent',
                               'IGBT 1 Mod 1 Overcurrent',
                               'IGBT 2 Mod 1 Overcurrent',
                               'IGBT 1 Mod 2 Overcurrent',
                               'IGBT 2 Mod 2 Overcurrent',
                               'IGBT 1 Mod 3 Overcurrent',
                               'IGBT 2 Mod 3 Overcurrent',
                               'IGBT 1 Mod 4 Overcurrent',
                               'IGBT 2 Mod 4 Overcurrent',
                               'Welded Contactor Mod 1 Fault',
                               'Welded Contactor Mod 2 Fault',
                               'Welded Contactor Mod 3 Fault',
                               'Welded Contactor Mod 4 Fault',
                               'Opened Contactor Mod 1 Fault',
                               'Opened Contactor Mod 2 Fault',
                               'Opened Contactor Mod 3 Fault',
                               'Opened Contactor Mod 4 Fault',
                               'DCLink Mod 1 Overvoltage',
                               'DCLink Mod 2 Overvoltage',
                               'DCLink Mod 3 Overvoltage',
                               'DCLink Mod 4 Overvoltage',
                               'DCLink Mod 1 Undervoltage',
                               'DCLink Mod 2 Undervoltage',
                               'DCLink Mod 3 Undervoltage',
                               'DCLink Mod 4 Undervoltage',
                               'IIB Mod 1 Itlk',
                               'IIB Mod 2 Itlk',
                               'IIB Mod 3 Itlk',
                               'IIB Mod 4 Itlk',
                               'Arm 1 Overcurrent',
                               'Arm 2 Overcurrent']
                               
list_fap_2p2s_iib_interlocks = list_fap_iib_interlocks
list_fap_2p2s_iib_alarms = list_fap_iib_alarms

 
# FAP 225A
list_fap_225A_soft_interlocks = ['IGBTs Current High Difference']

list_fap_225A_hard_interlocks = ['Load Overcurrent',
                                 'DCLink Contactor Fault', 
                                 'IGBT 1 Overcurrent',
                                 'IGBT 2 Overcurrent']

# FAC-2P ACDC
list_fac_2p_acdc_imas_soft_interlocks = []                              

list_fac_2p_acdc_imas_hard_interlocks = ['CapBank Overvoltage',
                                         'Rectifier Overcurrent',
                                         'AC Mains Contactor Fault',
                                         'Module A Interlock',
                                         'Module B Interlock',
                                         'DCDC Interlock']

# FAC-2P DCDC
list_fac_2p_dcdc_imas_soft_interlocks = []                              

list_fac_2p_dcdc_imas_hard_interlocks = ['Load Overcurrent',
                                         'Module 1 CapBank_Overvoltage',
                                         'Module 2 CapBank_Overvoltage',
                                         'Module 1 CapBank_Undervoltage',
                                         'Module 2 CapBank_Undervoltage',
                                         'Arm 1 Overcurrent',
                                         'Arm 2 Overcurrent',
                                         'Arms High_Difference',
                                         'ACDC Interlock']

class SerialDRS(object):

    ser = serial.Serial()

    def __init__(self):
        #self.ser=serial.Serial()
        self.MasterAdd              = '\x00'
        self.SlaveAdd               = '\x01'
        self.BCastAdd               = '\xFF'
        self.ComWriteVar            = '\x20'
        self.WriteFloatSizePayload  = '\x00\x05'
        self.WriteDoubleSizePayload = '\x00\x03'
        self.ComReadVar             = '\x10\x00\x01'
        self.ComRequestCurve        = '\x40'
        self.ComSendWfmRef          = '\x41'
        self.ComFunction            = '\x50'

        self.DP_MODULE_MAX_COEFF    = 16

        self.ListDPClass = ['ELP_Error','ELP_SRLim','ELP_LPF','ELP_PI_dawu','ELP_IIR_2P2Z','ELP_IIR_3P3Z',
                            'DCL_PID','DCL_PI','DCL_DF13','DCL_DF22','DCL_23']
        self.ListHardInterlocks = ['Sobrecorrente', 'Interlock Externo', 'Falha AC',
                               'Falha ACDC', 'Falha DCDC','Sobretensao','Falha Resistor Precarga','Falha Carga Capacitores Saída',
                               'Botão de Emergência', 'OUT_OVERVOLTAGE', 'IN_OVERVOLTAGE','ARM1_OVERCURRENT','ARM2_OVERCURRENT',
                                'IN_OVERCURRENT','DRIVER1_FAULT','DRIVER2_FAULT','OUT1_OVERCURRENT','OUT2_OVERCURRENT','OUT1_OVERVOLTAGE',
                                'OUT2_OVERVOLTAGE','LEAKAGE_OVERCURRENT','AC_OVERCURRENT']
        self.ListSoftInterlocks = ['IGBT1_OVERTEMP','IGBT2_OVERTEMP','L1_OVERTEMP','L2_OVERTEMP','HEATSINK_OVERTEMP','WATER_OVERTEMP',
                                   'RECTFIER1_OVERTEMP','RECTFIER2_OVERTEMP','AC_TRANSF_OVERTEMP','WATER_FLUX_FAULT','OVER_HUMIDITY_FAULT']

        print("\n pyDRS - compatible UDC firmware version: " + UDC_FIRMWARE_VERSION + "\n")
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ======================================================================
                    Funções Internas da Classe
    ======================================================================
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Converte float para hexadecimal
    def float_to_hex(self, value):
        hex_value = struct.pack('f', value)
        return hex_value.decode('ISO-8859-1')

    # Converte lista de float  para hexadecimal
    def float_list_to_hex(self, value_list):
        hex_list = b''
        for value in value_list:
            hex_list = hex_list + struct.pack('f', value)
        return hex_list.decode('ISO-8859-1')

    def format_list_size(self, in_list, max_size):
        out_list = in_list[0:max_size]
        if max_size > len(in_list):
            for i in range(max_size - len(in_list)):
                out_list.append(0)
        return out_list

    # Converte double para hexadecimal
    def double_to_hex(self,value):
        hex_value = struct.pack('H',value)
        return hex_value.decode('ISO-8859-1')

    # Converte unsigned int para hexadecimal 
    def uint32_to_hex(self,value):
        hex_value = struct.pack('I',value)
        return hex_value.decode('ISO-8859-1')

    # Converte indice para hexadecimal
    def index_to_hex(self,value):
        hex_value = struct.pack('B',value)
        return hex_value.decode('ISO-8859-1')

    # Converte payload_size para hexadecimal
    def size_to_hex(self,value):
        hex_value = struct.pack('>H',value)
        return hex_value.decode('ISO-8859-1')

    # Função Checksum
    def checksum(self, packet):
        b=bytearray(packet.encode('ISO-8859-1'))
        csum =(256-sum(b))%256
        hcsum = struct.pack('B',csum)
        send_msg = packet + hcsum.decode(encoding='ISO-8859-1')
        return send_msg

    # Função de leitura de variável
    def read_var(self,var_id):
        send_msg = self.checksum(self.SlaveAdd+self.ComReadVar+var_id)
        self.ser.reset_input_buffer()
        self.ser.write(send_msg.encode('ISO-8859-1'))

    def is_open(self):
        return self.ser.isOpen()

    def _convertToUint16List(self, val, format):
        val_16 = []
        val_b = struct.pack(bytesFormat[format],val)
        print(val_b)
        for i in range(0,len(val_b),2):
            val_16.append(struct.unpack('H',val_b[i:i+2])[0])
        print(val_16)
        return val_16

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ======================================================================
                Métodos de Chamada de Entidades Funções BSMP
            O retorno do método são os bytes de retorno da mensagem
    ======================================================================
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def TurnOn_FAx(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('TurnOn'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def TurnOn(self,ps_modules):
        payload_size = self.size_to_hex(1+2) #Payload: ID + ps_modules
        hex_modules  = self.double_to_hex(ps_modules)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('TurnOn'))+hex_modules
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def turn_on(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('turn_on'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def TurnOff_FAx(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('TurnOff'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def TurnOff(self,ps_modules):
        payload_size = self.size_to_hex(1+2) #Payload: ID + ps_modules
        hex_modules  = self.double_to_hex(ps_modules)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('TurnOff'))+hex_modules
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def turn_off(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('turn_off'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def open_loop(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('open_loop'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def closed_loop(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('closed_loop'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def OpenLoop(self,ps_modules):
        payload_size = self.size_to_hex(1+2) #Payload: ID + ps_modules
        hex_modules  = self.double_to_hex(ps_modules)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('OpenLoop'))+hex_modules
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def ClosedLoop(self,ps_modules):
        payload_size = self.size_to_hex(1+2) #Payload: ID + ps_modules
        hex_modules  = self.double_to_hex(ps_modules)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('ClosedLoop'))+hex_modules
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)
        
    def OpenLoop_FAx(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('OpenLoop'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def ClosedLoop_FAx(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('ClosedLoop'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def OpMode(self,op_mode):
        payload_size = self.size_to_hex(1+2) #Payload: ID + ps_opmode
        hex_opmode   = self.double_to_hex(op_mode)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('OpMode'))+hex_opmode
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def RemoteInterface(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('RemoteInterface'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def SetISlowRef(self,setpoint):
        payload_size   = self.size_to_hex(1+4) #Payload: ID + iSlowRef
        hex_setpoint   = self.float_to_hex(setpoint)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('SetISlowRef'))+hex_setpoint
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def ConfigWfmRef(self,gain,offset):
        payload_size = self.size_to_hex(1+4+4) #Payload: ID + gain + offset
        hex_gain     = self.float_to_hex(gain)
        hex_offset   = self.float_to_hex(offset)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('ConfigWfmRef'))+hex_gain+hex_offset
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def ConfigSigGen(self,sigType,nCycles,phaseStart,phaseEnd):
        payload_size   = self.size_to_hex(1+2+2+4+4) #Payload: ID + type + nCycles + phaseStart + phaseEnd
        hex_sigType    = self.double_to_hex(sigType)
        hex_nCycles    = self.double_to_hex(nCycles)
        hex_phaseStart = self.float_to_hex(phaseStart)
        hex_phaseEnd   = self.float_to_hex(phaseEnd)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('ConfigSigGen'))+hex_sigType+hex_nCycles+hex_phaseStart+hex_phaseEnd
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def EnableSigGen(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('EnableSigGen'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def DisableSigGen(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('DisableSigGen'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def ConfigDPModule(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('ConfigDPModule'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def ConfigDPModuleFull(self,dp_id,dp_class,dp_coeffs):
        self.Write_dp_ID(dp_id)
        self.Write_dp_Class(dp_class)
        self.Write_dp_Coeffs(dp_coeffs)
        self.ConfigDPModule()

    def WfmRefUpdate(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('WfmRefUpdate'))
        send_msg     = self.checksum(self.BCastAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))

    def ResetInterlocks(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('ResetInterlocks'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def reset_interlocks(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('reset_interlocks'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def ConfigPSModel(self,ps_model):
        payload_size = self.size_to_hex(1+2) #Payload: ID + ps_Model
        hex_model    = self.double_to_hex(ps_model)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('ConfigPSModel'))+hex_model
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def ConfigHRADC(self,hradcID,freqSampling,inputType,enableHeater,enableMonitor):
        payload_size   = self.size_to_hex(1+2+4+2+2+2) #Payload: ID + hradcID + freqSampling + inputType + enableHeater + enableMonitor
        hex_hradcID    = self.double_to_hex(hradcID)
        hex_freq       = self.float_to_hex(freqSampling)
        hex_type       = self.double_to_hex(ListHRADCInputType.index(inputType))
        hex_enHeater   = self.double_to_hex(enableHeater)
        hex_enMonitor  = self.double_to_hex(enableMonitor)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('ConfigHRADC'))+hex_hradcID+hex_freq+hex_type+hex_enHeater+hex_enMonitor
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def ConfigHRADCOpMode(self,hradcID,opMode):
        payload_size   = self.size_to_hex(1+2+2) #Payload: ID + hradcID + opMode
        hex_hradcID    = self.double_to_hex(hradcID)
        hex_opMode     = self.double_to_hex(opMode)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('ConfigHRADCOpMode'))+hex_hradcID+hex_opMode
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def EnableHRADCSampling(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('EnableHRADCSampling'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def DisableHRADCSampling(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('DisableHRADCSampling'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def ResetWfmRef(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('ResetWfmRef'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def SetRSAddress(self,rs_address):
        payload_size = self.size_to_hex(1+2) #Payload: ID + rs_address
        hex_add = self.double_to_hex(rs_address)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('SetRSAddress'))+hex_add
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def EnableSamplesBuffer(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('EnableSamplesBuffer'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def DisableSamplesBuffer(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('DisableSamplesBuffer'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def SelectHRADCBoard(self,hradcID):
        payload_size   = self.size_to_hex(1+2) #Payload: ID
        hex_hradcID    = self.double_to_hex(hradcID)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('SelectHRADCBoard'))+hex_hradcID
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def SelectTestSource(self,inputType):
        payload_size   = self.size_to_hex(1+2) #Payload: inputType
        hex_type       = self.double_to_hex(ListHRADCInputType.index(inputType))
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('SelectTestSource'))+hex_type
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def ResetHRADCBoards(self, enable):
        payload_size   = self.size_to_hex(1+2) #Payload: ID+enable(2)
        hex_enable     = self.double_to_hex(enable)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('ResetHRADCBoards'))+hex_enable
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def Config_nHRADC(self,nHRADC):
        payload_size   = self.size_to_hex(1+2) #Payload: nHRADC
        hex_nhradc     = self.double_to_hex(nHRADC)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('Config_nHRADC'))+hex_nhradc
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def ReadHRADC_UFM(self,hradcID,ufmadd):
        payload_size   = self.size_to_hex(1+2+2) #Payload: ID + hradcID + ufmadd
        hex_hradcID    = self.double_to_hex(hradcID)
        hex_ufmadd    = self.double_to_hex(ufmadd)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('ReadHRADC_UFM'))+hex_hradcID+hex_ufmadd
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def WriteHRADC_UFM(self,hradcID,ufmadd,ufmdata):
        payload_size   = self.size_to_hex(1+2+2+2) #Payload: ID + hradcID + ufmadd + ufmdata
        hex_hradcID    = self.double_to_hex(hradcID)
        hex_ufmadd    = self.double_to_hex(ufmadd)
        hex_ufmdata    = self.double_to_hex(ufmdata)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('WriteHRADC_UFM'))+hex_hradcID+hex_ufmadd+hex_ufmdata
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def EraseHRADC_UFM(self,hradcID):
        payload_size   = self.size_to_hex(1+2) #Payload: ID + hradcID
        hex_hradcID    = self.double_to_hex(hradcID)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('EraseHRADC_UFM'))+hex_hradcID
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def InitHRADC_BoardData(self, serial = 12345678, day = 1, mon = 1,
                            year = 2017, hour = 12, minutes = 30,
                            variant = 'HRADC-FBP', rburden = 20, calibtemp = 40,
                            vin_gain = 1, vin_offset = 0, iin_gain = 1,
                            iin_offset = 0, vref_p = 5, vref_n = -5, gnd = 0):
        boardData = {'serial': serial, 'variant': variant, 'rburden': rburden,
                     'tm_mday': day, 'tm_mon': mon, 'tm_year': year,
                     'tm_hour': hour, 'tm_min': minutes, 'calibtemp': calibtemp,
                     'vin_gain': vin_gain, 'vin_offset': vin_offset,
                     'iin_gain': iin_gain, 'iin_offset': iin_offset,
                     'vref_p': vref_p, 'vref_n': vref_n, 'gnd': gnd}
        return boardData

    def WriteHRADC_BoardData(self,hradcID,boardData):
        print('Configurando placa em UFM mode...')
        self.ConfigHRADCOpMode(hradcID,1)
        time.sleep(0.5)

        print('\nEnviando serial number...')
        ufmdata_16 = self._convertToUint16List(boardData['serial'],'Uint64')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['serial'],ufmdata_16[i])
            time.sleep(0.1)

        print('\nEnviando variante...')
        ufmdata_16 = self._convertToUint16List(hradcVariant.index(boardData['variant']),'Uint16')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['variant'],ufmdata_16[i])
            time.sleep(0.1)

        print('\nEnviando rburden...')
        ufmdata_16 = self._convertToUint16List(boardData['rburden'],'float')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['rburden'],ufmdata_16[i])
            time.sleep(0.1)

        print('\nEnviando calibdate...')
        ufmdata_16 = self._convertToUint16List(boardData['tm_mday'],'Uint16')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['calibdate'],ufmdata_16[i])
            time.sleep(0.1)
        # Month
        ufmdata_16 = self._convertToUint16List(boardData['tm_mon'],'Uint16')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['calibdate']+1,ufmdata_16[i])
            time.sleep(0.1)
        # Year
        ufmdata_16 = self._convertToUint16List(boardData['tm_year'],'Uint16')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['calibdate']+2,ufmdata_16[i])
            time.sleep(0.1)
        # Hour
        ufmdata_16 = self._convertToUint16List(boardData['tm_hour'],'Uint16')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['calibdate']+3,ufmdata_16[i])
            time.sleep(0.1)
        # Minutes
        ufmdata_16 = self._convertToUint16List(boardData['tm_min'],'Uint16')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['calibdate']+4,ufmdata_16[i])
            time.sleep(0.1)

        print('\nEnviando calibtemp...')
        ufmdata_16 = self._convertToUint16List(boardData['calibtemp'],'float')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['calibtemp'],ufmdata_16[i])
            time.sleep(0.1)

        print('\nEnviando vin_gain...')
        ufmdata_16 = self._convertToUint16List(boardData['vin_gain'],'float')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['vin_gain'],ufmdata_16[i])
            time.sleep(0.1)

        print('\nEnviando vin_offset...')
        ufmdata_16 = self._convertToUint16List(boardData['vin_offset'],'float')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['vin_offset'],ufmdata_16[i])
            time.sleep(0.1)

        print('\nEnviando iin_gain...')
        ufmdata_16 = self._convertToUint16List(boardData['iin_gain'],'float')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['iin_gain'],ufmdata_16[i])
            time.sleep(0.1)

        print('\nEnviando iin_offset...')
        ufmdata_16 = self._convertToUint16List(boardData['iin_offset'],'float')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['iin_offset'],ufmdata_16[i])
            time.sleep(0.1)

        print('\nEnviando vref_p...')
        ufmdata_16 = self._convertToUint16List(boardData['vref_p'],'float')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['vref_p'],ufmdata_16[i])
            time.sleep(0.1)

        print('\nEnviando vref_n...')
        ufmdata_16 = self._convertToUint16List(boardData['vref_n'],'float')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['vref_n'],ufmdata_16[i])
            time.sleep(0.1)

        print('\nEnviando gnd...')
        ufmdata_16 = self._convertToUint16List(boardData['gnd'],'float')
        for i in range(len(ufmdata_16)):
            self.WriteHRADC_UFM(hradcID,i+ufmOffset['gnd'],ufmdata_16[i])
            time.sleep(0.1)

        print('Colocando a placa em Sampling mode...')
        self.ConfigHRADCOpMode(hradcID,0)

    def ReadHRADC_BoardData(self,hradcID):
        print('Configurando placa em UFM mode...')
        print(self.ConfigHRADCOpMode(hradcID,1))
        time.sleep(0.5)

        print('Extraindo dados da placa...')
        payload_size   = self.size_to_hex(1+2) #Payload: ID + hradcID
        hex_hradcID    = self.double_to_hex(hradcID)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('ReadHRADC_BoardData'))+hex_hradcID
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        print(self.ser.read(6))

        print('Lendo dados da placa...')
        self.read_var(self.index_to_hex(50+hradcID))
        reply_msg = self.ser.read(1+1+2+56+1)
        print(reply_msg)
        print(len(reply_msg))
        val = struct.unpack('BBHLLHHHHHHfffffffffB',reply_msg)
        try:
            boardData = self.InitHRADC_BoardData(val[3]+val[4]*pow(2,32),val[5],
                                                val[6],val[7],val[8],val[9],
                                                hradcVariant[val[10]],val[11],
                                                val[12],val[13],val[14],val[15],
                                                val[16],val[17],val[18],val[19])
        except:
            print('\n### Placa não inicializada ###\n')
            boardData = self.InitHRADC_BoardData(serial = int(input('Digite o S/N: ')))
            print('\n')

        print('Colocando a placa em Sampling mode...')
        print(self.ConfigHRADCOpMode(hradcID,0))
        time.sleep(0.5)

        return boardData

    def UpdateHRADC_BoardData(self,hradcID):
        variant = len(hradcVariant)
        while variant >= len(hradcVariant) or variant < 0:
            variant = int(input("Enter HRADC variant number:\n  0: HRADC-FBP\n  1: HRADC-FAX-A\n  2: HRADC-FAX-B\n  3: HRADC-FAX-C\n  4: HRADC-FAX-D\n\n>>> "))
        variant = hradcVariant[variant]
        
        boardData = self.ReadHRADC_BoardData(hradcID)
        boardData['variant'] = variant
        boardData['vin_offset'] = np.float32(0)
        boardData['iin_offset'] = np.float32(0)
        
        if variant == 'HRADC-FBP':
            boardData['rburden'] = np.float32(20)
            boardData['vin_gain'] = np.float32(1)
            boardData['iin_gain'] = np.float32(1)
            print(boardData['vin_gain'])
            print(boardData['variant'])
        
        elif variant == 'HRADC-FAX-A':
            boardData['rburden'] = np.float32(0)
            boardData['vin_gain'] = np.float32(6.0/5.0)
            boardData['iin_gain'] = np.float32(6.0/5.0)
            print(boardData['vin_gain'])
            print(boardData['variant'])
            
        elif variant == 'HRADC-FAX-B':
            boardData['rburden'] = np.float32(0)
            boardData['vin_gain'] = np.float32(1)
            boardData['iin_gain'] = np.float32(1)
            print(boardData['vin_gain'])
            print(boardData['variant'])

        elif variant == 'HRADC-FAX-C':
            boardData['rburden'] = np.float32(5)
            boardData['vin_gain'] = np.float32(1)
            boardData['iin_gain'] = np.float32(1)
            print(boardData['vin_gain'])
            print(boardData['variant'])
            
        elif variant == 'HRADC-FAX-D':
            boardData['rburden'] = np.float32(1)
            boardData['vin_gain'] = np.float32(1)
            boardData['iin_gain'] = np.float32(1)
            print(boardData['vin_gain'])
            print(boardData['variant'])
            
        print('\n\nBoard data from HRADC of slot #' + str(hradcID) + ' is about to be overwritten by the following data:')
        print(boardData)
        
        i = input('\n Do you want to proceed? [y/n]: ')
        
        if i is 'Y' or i is 'y':
            self.ConfigHRADCOpMode(hradcID,1)
            time.sleep(0.1)
            self.EraseHRADC_UFM(hradcID)
            time.sleep(0.5)
            self.ResetHRADCBoards(1)
            time.sleep(0.5)
            self.ResetHRADCBoards(0)
            time.sleep(1.5)
            self.WriteHRADC_BoardData(hradcID,boardData)
            boardData_new = self.ReadHRADC_BoardData(hradcID)
            print(boardData_new)
            print(boardData)
            if boardData_new == boardData:
                print('\n\n ### Operation was successful !!! ### \n\n')
            else:
                print('\n\n ### Operation failed !!! ### \n\n')
                
        return [boardData, boardData_new]
    
    def GetHRADCs_BoardData(self,numHRADC):
        boardData_list = []
        for i in range(numHRADC):
            boardData_list.append(self.ReadHRADC_BoardData(i))
        return boardData_list

    def UdcEepromTest(self, rw, data=None):
        if data is not None:
            payload_size    = self.size_to_hex(12)
            hex_rw          = self.double_to_hex(rw)
            hex_byte_0      = self.double_to_hex(data[0])
            hex_byte_1      = self.double_to_hex(data[1])
            hex_byte_2      = self.double_to_hex(data[2])
            hex_byte_3      = self.double_to_hex(data[3])
            hex_byte_4      = self.double_to_hex(data[4])
            hex_byte_5      = self.double_to_hex(data[5])
            hex_byte_6      = self.double_to_hex(data[6])
            hex_byte_7      = self.double_to_hex(data[7])
            hex_byte_8      = self.double_to_hex(data[8])
            hex_byte_9      = self.double_to_hex(data[9])
            send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcEepromTest'))+hex_rw[0]+ \
                                hex_byte_0[0] + hex_byte_1[0] + hex_byte_2[0] + hex_byte_3[0] + hex_byte_4[0] + hex_byte_5[0]+ \
                                hex_byte_6[0] + hex_byte_7[0] + hex_byte_8[0] + hex_byte_9[0]

            print(send_packet.encode('ISO-8859-1'))
            self.ser.write(send_packet.encode('ISO-8859-1'))
            return self.ser.read(15)

    def UdcFlashTest(self, rw):
        payload_size    = self.size_to_hex(2)
        hex_rw          = self.double_to_hex(rw)
        send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcFlashTest'))+hex_rw[0]
        self.ser.write(send_packet.encode('ISO-8859-1'))
        return self.ser.read(6)

    def UdcRamTest(self, rw):
        payload_size    = self.size_to_hex(2)
        hex_rw          = self.double_to_hex(rw)
        send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcRamTest'))+hex_rw[0]
        self.ser.write(send_packet.encode('ISO-8859-1'))
        return self.ser.read(6)

    def UdcAdcTest(self, rw, channel):
        payload_size    = self.size_to_hex(3)
        hex_rw          = self.double_to_hex(rw)
        hex_channel     = self.double_to_hex(channel)
        send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcAdcTest'))+hex_rw[0]+hex_channel[0]
        self.ser.write(send_packet.encode('ISO-8859-1'))
        return self.ser.read(6)

    def UdcSensorTempTest(self, rw):
        payload_size    = self.size_to_hex(2)
        hex_rw          = self.double_to_hex(rw)
        send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcSensorTempTest'))+hex_rw[0]
        self.ser.write(send_packet.encode('ISO-8859-1'))
        return self.ser.read(6)

    def UdcRtcTest(self, rw):
        payload_size    = self.size_to_hex(2)
        hex_rw          = self.double_to_hex(rw)
        send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcRtcTest'))+hex_rw[0]
        self.ser.write(send_packet.encode('ISO-8859-1'))
        return self.ser.read(6)

    def UdcUartTest(self, rw):
        payload_size    = self.size_to_hex(2)
        hex_rw          = self.double_to_hex(rw)
        send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcUartTest'))+hex_rw[0]
        self.ser.write(send_packet.encode('ISO-8859-1'))
        return self.ser.read(6)

    def UdcIoExpanderTest(self, rw):
        payload_size    = self.size_to_hex(2)
        hex_rw          = self.double_to_hex(rw)
        send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcIoExpanderTest'))+hex_rw[0]
        self.ser.write(send_packet.encode('ISO-8859-1'))
        return self.ser.read(6)

#    def UdcEthernetTest(self, rw):
#        payload_size    = self.size_to_hex(2)
#        hex_rw          = self.double_to_hex(rw)
#        send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcEthernetTest'))+hex_rw
#        self.ser.write(send_packet.encode('ISO-8859-1'))
#        return self.ser.read()

    def UdcIsoPlaneTest(self, rw):
        payload_size    = self.size_to_hex(2)
        hex_rw          = self.double_to_hex(rw)
        send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcIsoPlaneTest'))+hex_rw[0]
        self.ser.write(send_packet.encode('ISO-8859-1'))
        return self.ser.read(6)

    def UdcLoopBackTest(self, rw, channel):
        payload_size    = self.size_to_hex(3)
        hex_rw          = self.double_to_hex(rw)
        hex_channel     = self.double_to_hex(channel)
        send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcLoopBackTest'))+hex_rw[0]+hex_channel[0]
        self.ser.write(send_packet.encode('ISO-8859-1'))
        return self.ser.read(6)

    def UdcLedTest(self, rw):
        payload_size    = self.size_to_hex(2)
        hex_rw          = self.double_to_hex(rw)
        send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcLedTest'))+hex_rw[0]
        self.ser.write(send_packet.encode('ISO-8859-1'))
        return self.ser.read(6)

    def UdcBuzzerTest(self, rw):
        payload_size    = self.size_to_hex(2)
        hex_rw          = self.double_to_hex(rw)
        send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcBuzzerTest'))+hex_rw[0]
        self.ser.write(send_packet.encode('ISO-8859-1'))
        return self.ser.read(6)

    def UdcComTest(self, rw, val):
        payload_size    = self.size_to_hex(3)
        hex_rw          = self.double_to_hex(rw)
        hex_value       = self.double_to_hex(val)
        send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcComTest'))+hex_rw[0]+hex_value[0]
        self.ser.write(send_packet.encode('ISO-8859-1'))
        time.sleep(0.2)
        return self.ser.read(6)

    def UdcI2cIsoTest(self, rw, val):
        payload_size    = self.size_to_hex(3)
        hex_rw          = self.double_to_hex(rw)
        hex_value       = self.double_to_hex(val)
        send_packet     = self.ComFunction+payload_size+self.index_to_hex(ListTestFunc.index('UdcI2cIsoTest'))+hex_rw[0]+hex_value[0]
        self.ser.write(send_packet.encode('ISO-8859-1'))
        return self.ser.read(6)

    def SetISlowRefx4(self, iRef1 = 0, iRef2 = 0, iRef3 = 0, iRef4 = 0):
        payload_size = self.size_to_hex(1+4*4) #Payload: ID + 4*iRef
        hex_iRef1    = self.float_to_hex(iRef1)
        hex_iRef2    = self.float_to_hex(iRef2)
        hex_iRef3    = self.float_to_hex(iRef3)
        hex_iRef4    = self.float_to_hex(iRef4)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc.index('SetISlowRefx4'))+hex_iRef1+hex_iRef2+hex_iRef3+hex_iRef4
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def SetPof(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListBCBFunc.index('SetPof'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def ClearPof(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListBCBFunc.index('ClearPof'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def ReadPof(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListBCBFunc.index('ReadPof'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def EnableBuzzer(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListBCBFunc.index('EnableBuzzer'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def DisableBuzzer(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListBCBFunc.index('DisableBuzzer'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def SendUartData(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListBCBFunc.index('SendUartData'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def GetUartData(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListBCBFunc.index('GetUartData'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def SendCanData(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListBCBFunc.index('SendCanData'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def GetCanData(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListBCBFunc.index('GetCanData'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def GetI2cData(self):
        payload_size   = self.size_to_hex(1) #Payload: ID
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListBCBFunc.index('GetI2cData'))
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def read_ps_status(self):
        self.read_var(self.index_to_hex(ListVar_v2_1.index('ps_status')))
        reply_msg = self.ser.read(7)
        val = struct.unpack('BBHHB',reply_msg)
        status = {}
        status['state'] =     ListOpMode_v2_1[(val[3] & 0b0000000000001111)]
        status['open_loop'] = (val[3] & 0b0000000000010000) >> 4
        status['interface'] = (val[3] & 0b0000000001100000) >> 5
        status['active'] =    (val[3] & 0b0000000010000000) >> 7
        status['model'] =     ListPSModels_v2_1[(val[3] & 0b0001111100000000) >> 8]
        status['unlocked'] =  (val[3] & 0b0010000000000000) >> 13
        #print(status)
        return status

    def set_ps_name(self,ps_name):
        if type(ps_name) == str:
            for n in range(len(ps_name)):
                self.set_param('PS_Name', n, float(ord(ps_name[n])))
            for i in range(n+1,64):
                self.set_param('PS_Name', i, float(ord(" ")))

    def get_ps_name(self):
        ps_name = ""
        for n in range(64):
            ps_name = ps_name + chr(int(self.get_param('PS_Name', n)))
            if ps_name[-3:] == '   ':
                ps_name = ps_name[:n-2]
                break
        return ps_name
                
    def set_slowref(self,setpoint):
        payload_size   = self.size_to_hex(1+4) #Payload: ID + iSlowRef
        hex_setpoint   = self.float_to_hex(setpoint)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('set_slowref'))+hex_setpoint
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def set_slowref_fbp(self, iRef1 = 0, iRef2 = 0, iRef3 = 0, iRef4 = 0):
        payload_size = self.size_to_hex(1+4*4) #Payload: ID + 4*iRef
        hex_iRef1    = self.float_to_hex(iRef1)
        hex_iRef2    = self.float_to_hex(iRef2)
        hex_iRef3    = self.float_to_hex(iRef3)
        hex_iRef4    = self.float_to_hex(iRef4)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('set_slowref_fbp'))+hex_iRef1+hex_iRef2+hex_iRef3+hex_iRef4
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def set_slowref_readback_mon(self,setpoint):
        payload_size   = self.size_to_hex(1+4) #Payload: ID + iSlowRef
        hex_setpoint   = self.float_to_hex(setpoint)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('set_slowref_readback_mon'))+hex_setpoint
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def set_slowref_fbp_readback_mon(self, iRef1 = 0, iRef2 = 0, iRef3 = 0, iRef4 = 0):
        payload_size = self.size_to_hex(1+4*4) #Payload: ID + 4*iRef
        hex_iRef1    = self.float_to_hex(iRef1)
        hex_iRef2    = self.float_to_hex(iRef2)
        hex_iRef3    = self.float_to_hex(iRef3)
        hex_iRef4    = self.float_to_hex(iRef4)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('set_slowref_fbp_readback_mon'))+hex_iRef1+hex_iRef2+hex_iRef3+hex_iRef4
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        reply_msg = self.ser.read(21)
        if(len(reply_msg) == 6):
            return reply_msg
        else:
            val = struct.unpack('BBHffffB',reply_msg)
            return [val[3],val[4],val[5],val[6]]
            
    def set_slowref_readback_ref(self,setpoint):
        payload_size   = self.size_to_hex(1+4) #Payload: ID + iSlowRef
        hex_setpoint   = self.float_to_hex(setpoint)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('set_slowref_readback_ref'))+hex_setpoint
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def set_slowref_fbp_readback_ref(self, iRef1 = 0, iRef2 = 0, iRef3 = 0, iRef4 = 0):
        payload_size = self.size_to_hex(1+4*4) #Payload: ID + 4*iRef
        hex_iRef1    = self.float_to_hex(iRef1)
        hex_iRef2    = self.float_to_hex(iRef2)
        hex_iRef3    = self.float_to_hex(iRef3)
        hex_iRef4    = self.float_to_hex(iRef4)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('set_slowref_fbp_readback_ref'))+hex_iRef1+hex_iRef2+hex_iRef3+hex_iRef4
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        reply_msg = self.ser.read(21)
        if(len(reply_msg) == 6):
            return reply_msg
        else:
            val = struct.unpack('BBHffffB',reply_msg)
            return [val[3],val[4],val[5],val[6]]

    def set_param(self, param_id, n, value):
        payload_size = self.size_to_hex(1+2+2+4) #Payload: ID + param id + [n] + value
        if type(param_id) == str:
            hex_id       = self.double_to_hex(ListParameters.index(param_id))
        if type(param_id) == int:
            hex_id       = self.double_to_hex(param_id)
        hex_n        = self.double_to_hex(n)
        hex_value    = self.float_to_hex(value)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('set_param'))+hex_id+hex_n+hex_value
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        reply_msg = self.ser.read(6)
        if reply_msg[4] == 8:
            print('Invalid parameter')
        return reply_msg

    def get_param(self, param_id, n = 0):
        payload_size = self.size_to_hex(1+2+2) #Payload: ID + param id + [n]
        if type(param_id) == str:
            hex_id       = self.double_to_hex(ListParameters.index(param_id))
        if type(param_id) == int:
            hex_id       = self.double_to_hex(param_id)
        hex_n        = self.double_to_hex(n)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('get_param'))+hex_id+hex_n
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.reset_input_buffer()
        self.ser.write(send_msg.encode('ISO-8859-1'))
        reply_msg = self.ser.read(9)
        if len(reply_msg) == 9:
            val = struct.unpack('BBHfB',reply_msg)
            return val[3]
        else:
            #print('Invalid parameter')
            return float('nan')

    def save_param_eeprom(self, param_id, n = 0, type_memory = 2):
        payload_size = self.size_to_hex(1+2+2+2) #Payload: ID + param id + [n] + memory type
        if type(param_id) == str:
            hex_id       = self.double_to_hex(ListParameters.index(param_id))
        if type(param_id) == int:
            hex_id       = self.double_to_hex(param_id)
        hex_n        = self.double_to_hex(n)
        hex_type        = self.double_to_hex(type_memory)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('save_param_eeprom'))+hex_id+hex_n+hex_type
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        reply_msg = self.ser.read(6)
        if reply_msg[4] == 8:
            print('Invalid parameter')
        return reply_msg

    def load_param_eeprom(self, param_id, n = 0, type_memory = 2):
        payload_size = self.size_to_hex(1+2+2+2) #Payload: ID + param id + [n] + memory type
        if type(param_id) == str:
            hex_id       = self.double_to_hex(ListParameters.index(param_id))
        if type(param_id) == int:
            hex_id       = self.double_to_hex(param_id)
        hex_n        = self.double_to_hex(n)
        hex_type        = self.double_to_hex(type_memory)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('load_param_eeprom'))+hex_id+hex_n+hex_type
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        reply_msg = self.ser.read(6)
        if reply_msg[4] == 8:
            print('Invalid parameter')
        return reply_msg

    def save_param_bank(self, type_memory = 2):
        payload_size   = self.size_to_hex(1+2) #Payload: ID + memory type
        hex_type        = self.double_to_hex(type_memory)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('save_param_bank'))+hex_type
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def load_param_bank(self, type_memory = 2):
        payload_size   = self.size_to_hex(1+2) #Payload: ID + memory type
        hex_type        = self.double_to_hex(type_memory)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('load_param_bank'))+hex_type
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def set_param_bank(self, param_file):
        fbp_param_list = []
        with open(param_file,newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                fbp_param_list.append(row)

        for param in fbp_param_list:
            if str(param[0]) == 'PS_Name':
                print(str(param[0]) + "[0]: " + str(param[1]))
                print(self.set_ps_name(str(param[1])))
            else:
                for n in range(64):
                    try:
                        print(str(param[0]) + "["+ str(n) + "]: " + str(param[n+1]))
                        print(self.set_param(str(param[0]),n,float(param[n+1])))
                    except:
                        break
        #self.save_param_bank()
        
    def get_param_bank(self, list_param = ListParameters, timeout = 0.5, print_modules = True):
        timeout_old = self.ser.timeout
        #self.ser.timeout = 0.05
        param_bank = []
        
        for param_name in list_param:
        
            param_row = [param_name]
            
            for n in range(64):
                if param_name == 'PS_Name':
                
                    p = self.get_ps_name()
                    param_row.append(p)
                    #if(print_modules):
                        #print('PS_Name: ' + p)                
                    self.ser.timeout = timeout
                    break
                    
                else:
                    p = self.get_param(param_name,n)
                    if math.isnan(p):
                        break
                    param_row.append(p)
                    #if(print_modules):
                        #print(param_name + "[" + str(n) + "]: " + str(p))
                        
            if(print_modules):
                print(param_row)
                
            param_bank.append(param_row)
                
        self.ser.timeout = timeout_old
        
        return param_bank

    def store_param_bank_csv(self, bank):
        filename = input('Digite o nome do arquivo: ')
        with open( filename + '.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            for param_row in bank:
                writer.writerow(param_row)

    def enable_onboard_eeprom(self):
        self.set_param('Enable_Onboard_EEPROM',0,0)
        self.save_param_eeprom('Enable_Onboard_EEPROM',0,2)
    
    def disable_onboard_eeprom(self):
        self.set_param('Enable_Onboard_EEPROM',0,1)
        self.save_param_eeprom('Enable_Onboard_EEPROM',0,2)
    
    def set_dsp_coeffs(self, dsp_class, dsp_id, coeffs_list = [0,0,0,0,0,0,0,0,0,0,0,0]):
        coeffs_list_full = self.format_list_size(coeffs_list, NUM_MAX_COEFFS_DSP)
        payload_size = self.size_to_hex(1+2+2+4*NUM_MAX_COEFFS_DSP)
        hex_dsp_class= self.double_to_hex(dsp_class)
        hex_dsp_id   = self.double_to_hex(dsp_id)
        hex_coeffs    = self.float_list_to_hex(coeffs_list_full)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('set_dsp_coeffs'))+hex_dsp_class+hex_dsp_id+hex_coeffs
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def get_dsp_coeff(self, dsp_class, dsp_id, coeff):
        payload_size = self.size_to_hex(1+2+2+2)
        hex_dsp_class= self.double_to_hex(dsp_class)
        hex_dsp_id   = self.double_to_hex(dsp_id)
        hex_coeff    = self.double_to_hex(coeff)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('get_dsp_coeff'))+hex_dsp_class+hex_dsp_id+hex_coeff
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.reset_input_buffer()
        self.ser.write(send_msg.encode('ISO-8859-1'))
        reply_msg = self.ser.read(9)
        #print(reply_msg)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def save_dsp_coeffs_eeprom(self, dsp_class, dsp_id, type_memory = 2):
        payload_size = self.size_to_hex(1+2+2+2)
        hex_dsp_class= self.double_to_hex(dsp_class)
        hex_dsp_id   = self.double_to_hex(dsp_id)
        hex_type        = self.double_to_hex(type_memory)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('save_dsp_coeffs_eeprom'))+hex_dsp_class+hex_dsp_id+hex_type
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def load_dsp_coeffs_eeprom(self, dsp_class, dsp_id, type_memory = 2):
        payload_size = self.size_to_hex(1+2+2+2)
        hex_dsp_class= self.double_to_hex(dsp_class)
        hex_dsp_id   = self.double_to_hex(dsp_id)
        hex_type        = self.double_to_hex(type_memory)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('load_dsp_coeffs_eeprom'))+hex_dsp_class+hex_dsp_id+hex_type
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def save_dsp_modules_eeprom(self, type_memory = 2):
        payload_size   = self.size_to_hex(1+2) #Payload: ID + memory type
        hex_type        = self.double_to_hex(type_memory)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('save_dsp_modules_eeprom'))+hex_type
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def load_dsp_modules_eeprom(self, type_memory = 2):
        payload_size   = self.size_to_hex(1+2) #Payload: ID + memory type
        hex_type        = self.double_to_hex(type_memory)
        send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('load_dsp_modules_eeprom'))+hex_type
        send_msg       = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def reset_udc(self):
        reply = input('\nEste comando realiza o reset do firmware da placa UDC, e por isso, so e executado caso a fonte esteja desligada. \nCaso deseje apenas resetar interlocks, utilize o comando reset_interlocks(). \n\nTem certeza que deseja prosseguir? [Y/N]: ')
        if reply == 'Y' or reply == 'y':
            payload_size   = self.size_to_hex(1) #Payload: ID
            send_packet    = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('reset_udc'))
            send_msg       = self.checksum(self.SlaveAdd+send_packet)
            self.ser.write(send_msg.encode('ISO-8859-1'))

    def run_bsmp_func(self,id_func,print_msg = 0):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(id_func)
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        reply_msg = self.ser.read(6)
        if print_msg:
            print(reply_msg)
        return reply_msg

    def run_bsmp_func_all_ps(self,p_func,add_list,arg = None,delay = 0.5, print_reply = 1):
        old_add = self.GetSlaveAdd()
        for add in add_list:
            self.SetSlaveAdd(add)
            if arg == None:
                r = p_func()
            else:
                r = p_func(arg)
            if print_reply:
                print('\n Add ' + str(add))
                print(r)
            time.sleep(delay)
        self.SetSlaveAdd(old_add)

    def cfg_source_scope(self,p_source):
        payload_size = self.size_to_hex(1+4) #Payload: ID + p_source
        hex_op_mode  = self.uint32_to_hex(p_source)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('cfg_source_scope'))+hex_op_mode
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def cfg_freq_scope(self,freq):
        payload_size = self.size_to_hex(1+4) #Payload: ID + freq
        hex_op_mode  = self.float_to_hex(freq)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('cfg_freq_scope'))+hex_op_mode
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def cfg_duration_scope(self,duration):
        payload_size = self.size_to_hex(1+4) #Payload: ID + duration
        hex_op_mode  = self.float_to_hex(duration)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('cfg_duration_scope'))+hex_op_mode
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def enable_scope(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('enable_scope'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)
    
    def disable_scope(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('disable_scope'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def get_scope_vars(self):
        print('\n### Scope Variables ###\n')
        print('Frequency: ' + str((self.read_bsmp_variable(25,'float'))))
        print('Duration: ' + str((self.read_bsmp_variable(26,'float'))))
        print('Source Data: ' + str((self.read_bsmp_variable(27,'uint32_t'))))

        
    def sync_pulse(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('sync_pulse'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def select_op_mode(self,op_mode):
        payload_size = self.size_to_hex(1+2) #Payload: ID + enable
        hex_op_mode  = self.double_to_hex(ListOpMode_v2_1.index(op_mode))
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('select_op_mode'))+hex_op_mode
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def set_serial_termination(self,term_enable):
        payload_size = self.size_to_hex(1+2) #Payload: ID + enable
        hex_enable  = self.double_to_hex(term_enable)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('set_serial_termination'))+hex_enable
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)
        
    def set_command_interface(self,interface):
        payload_size = self.size_to_hex(1+2) #Payload: ID + enable
        hex_interface  = self.double_to_hex(interface)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('set_command_interface'))+hex_interface
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)
    
    def unlock_udc(self,password):
        payload_size = self.size_to_hex(1+2) #Payload: ID + password
        hex_password  = self.double_to_hex(password)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('unlock_udc'))+hex_password
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)
        
    def lock_udc(self,password):
        payload_size = self.size_to_hex(1+2) #Payload: ID + password
        hex_password  = self.double_to_hex(password)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('lock_udc'))+hex_password
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def reset_counters(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('reset_counters'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)
        
    def cfg_siggen(self,sig_type,num_cycles,freq,amplitude,offset,aux0,aux1,aux2,aux3):
        payload_size   = self.size_to_hex(1+2+2+4+4+4+4*4)
        hex_sig_type   = self.double_to_hex(ListSigGenTypes_v2_1.index(sig_type))
        hex_num_cycles = self.double_to_hex(num_cycles)
        hex_freq       = self.float_to_hex(freq)
        hex_amplitude  = self.float_to_hex(amplitude)
        hex_offset     = self.float_to_hex(offset)
        hex_aux0       = self.float_to_hex(aux0)
        hex_aux1       = self.float_to_hex(aux1)
        hex_aux2       = self.float_to_hex(aux2)
        hex_aux3       = self.float_to_hex(aux3)
        send_packet    = self.ComFunction + payload_size + self.index_to_hex(ListFunc_v2_1.index('cfg_siggen')) + hex_sig_type + hex_num_cycles + hex_freq + hex_amplitude + hex_offset + hex_aux0 + hex_aux1 + hex_aux2 + hex_aux3
        send_msg      = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def set_siggen(self,freq,amplitude,offset):
        payload_size   = self.size_to_hex(1+4+4+4)
        hex_freq       = self.float_to_hex(freq)
        hex_amplitude  = self.float_to_hex(amplitude)
        hex_offset     = self.float_to_hex(offset)
        send_packet    = self.ComFunction + payload_size + self.index_to_hex(ListFunc_v2_1.index('set_siggen')) + hex_freq + hex_amplitude + hex_offset
        send_msg      = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def enable_siggen(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size + self.index_to_hex(ListFunc_v2_1.index('enable_siggen'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def disable_siggen(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size + self.index_to_hex(ListFunc_v2_1.index('disable_siggen'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)

    def cfg_wfmref(self, idx, sync_mode, frequency, gain = 1, offset = 0):
        payload_size = self.size_to_hex(1+2+2+4+4+4) #Payload: ID + idx + sync_mode + frequency + gain + offset
        hex_idx  = self.double_to_hex(idx)
        hex_mode  = self.double_to_hex(sync_mode)
        hex_freq    = self.float_to_hex(frequency)
        hex_gain    = self.float_to_hex(gain)
        hex_offset    = self.float_to_hex(offset)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('cfg_wfmref'))+hex_idx+hex_mode+hex_freq+hex_gain+hex_offset
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)
        
    def select_wfmref(self,idx):
        payload_size = self.size_to_hex(1+2) #Payload: ID + idx
        hex_idx  = self.double_to_hex(idx)
        send_packet  = self.ComFunction+payload_size+self.index_to_hex(ListFunc_v2_1.index('select_wfmref'))+hex_idx
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)
        
    def reset_wfmref(self):
        payload_size = self.size_to_hex(1) #Payload: ID
        send_packet  = self.ComFunction+payload_size + self.index_to_hex(ListFunc_v2_1.index('reset_wfmref'))
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(6)
    
    def get_wfmref_vars(self,curve_id):
        print('\n### WfmRef ' + str(curve_id) + ' Variables ###\n')
        print('Length: ' + str((self.read_bsmp_variable(20+curve_id*3,'uint32_t')-self.read_bsmp_variable(19+curve_id*3,'uint32_t'))/2+1))
        print('Index: ' + str((self.read_bsmp_variable(21+curve_id*3,'uint32_t')-self.read_bsmp_variable(19+curve_id*3,'uint32_t'))/2+1))
        print('WfmRef Selected: ' + str(self.read_bsmp_variable(14,'uint16_t')))
        print('Sync Mode: ' + str(self.read_bsmp_variable(15,'uint16_t')))
        print('Frequency: ' + str(self.read_bsmp_variable(16,'float')) + " Hz")
        print('Gain: ' + str(self.read_bsmp_variable(17,'float')))
        print('Offset: ' + str(self.read_bsmp_variable(18,'float')))
        
    def read_csv_file(self,filename, type = 'float'):
        csv_list = []
        with open(filename, newline = '') as f:
            reader = csv.reader(f)
            for row in reader:
                if type == 'float':
                    row_converted = float(row[0])
                elif type == 'string' or type == 'str':
                    row_converted = str(row[0])
                csv_list.append(row_converted)
        print('Length of list: ' + str(len(csv_list)) + '\n')
        return csv_list
        
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ======================================================================
                Métodos de Leitura de Valores das Variáveis BSMP
    O retorno do método são os valores double/float da respectiva variavel
    ======================================================================
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def read_bsmp_variable(self,id_var,type_var,print_msg = 0):
        self.read_var(self.index_to_hex(id_var))
        reply_msg = self.ser.read(typeSize[type_var])
        if print_msg:
            print(reply_msg)
        val = struct.unpack(typeFormat[type_var],reply_msg)
        return val[3]

    def read_bsmp_variable_gen(self,id_var,size_bytes,print_msg = 0):
        self.read_var(self.index_to_hex(id_var))
        reply_msg = self.ser.read(size_bytes+5)
        if print_msg:
            print(reply_msg)
        return reply_msg

    def read_udc_arm_version(self):
        self.read_var(self.index_to_hex(3))
        reply_msg = self.ser.read(133)
        val = struct.unpack('16s',reply_msg[4:20])
        return val[0].decode('utf-8')

    def read_udc_c28_version(self):
        self.read_var(self.index_to_hex(3))
        reply_msg = self.ser.read(133)
        val = struct.unpack('16s',reply_msg[20:36])
        return val[0].decode('utf-8')
    
    def read_udc_version(self):
        print('\n ARM: ' + self.read_udc_arm_version())
        print(' C28: ' + self.read_udc_c28_version())

    def Read_iLoad1(self):
        self.read_var(self.index_to_hex(ListVar.index('iLoad1')))
        reply_msg = self.ser.read(9)
        print(reply_msg)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_iLoad2(self):
        self.read_var(self.index_to_hex(ListVar.index('iLoad2')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_iMod1(self):
        self.read_var(self.index_to_hex(ListVar.index('iMod1')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_iMod2(self):
        self.read_var(self.index_to_hex(ListVar.index('iMod2')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_iMod3(self):
        self.read_var(self.index_to_hex(ListVar.index('iMod3')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_iMod4(self):
        self.read_var(self.index_to_hex(ListVar.index('iMod4')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_vLoad(self):
        self.read_var(self.index_to_hex(ListVar.index('vLoad')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_vDCMod1(self):
        self.read_var(self.index_to_hex(ListVar.index('vDCMod1')))
        reply_msg = self.ser.read(9)
        print(reply_msg)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_vDCMod2(self):
        self.read_var(self.index_to_hex(ListVar.index('vDCMod2')))
        reply_msg = self.ser.read(9)
        print(reply_msg)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_vDCMod3(self):
        self.read_var(self.index_to_hex(ListVar.index('vDCMod3')))
        reply_msg = self.ser.read(9)
        print(reply_msg)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_vDCMod4(self):
        self.read_var(self.index_to_hex(ListVar.index('vDCMod4')))
        reply_msg = self.ser.read(9)
        print(reply_msg)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_vOutMod1(self):
        self.read_var(self.index_to_hex(ListVar.index('vOutMod1')))
        reply_msg = self.ser.read(9)
        print(reply_msg)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_vOutMod2(self):
        self.read_var(self.index_to_hex(ListVar.index('vOutMod2')))
        reply_msg = self.ser.read(9)
        print(reply_msg)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_vOutMod3(self):
        self.read_var(self.index_to_hex(ListVar.index('vOutMod3')))
        reply_msg = self.ser.read(9)
        print(reply_msg)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_vOutMod4(self):
        self.read_var(self.index_to_hex(ListVar.index('vOutMod4')))
        reply_msg = self.ser.read(9)
        print(reply_msg)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_temp1(self):
        self.read_var(self.index_to_hex(ListVar.index('temp1')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_temp2(self):
        self.read_var(self.index_to_hex(ListVar.index('temp2')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_temp3(self):
        self.read_var(self.index_to_hex(ListVar.index('temp3')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_temp4(self):
        self.read_var(self.index_to_hex(ListVar.index('temp4')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_ps_OnOff(self):
        self.read_var(self.index_to_hex(ListVar.index('ps_OnOff')))
        reply_msg = self.ser.read(7)
        val = struct.unpack('BBHHB',reply_msg)
        return val[3]

    def Read_ps_OpMode(self):
        self.read_var(self.index_to_hex(ListVar.index('ps_OpMode')))
        reply_msg = self.ser.read(7)
        val = struct.unpack('BBHHB',reply_msg)
        return val[3]

    def Read_ps_Remote(self):
        self.read_var(self.index_to_hex(ListVar.index('ps_Remote')))
        reply_msg = self.ser.read(7)
        val = struct.unpack('BBHHB',reply_msg)
        return val[3]

    def Read_ps_OpenLoop(self):
        self.read_var(self.index_to_hex(ListVar.index('ps_OpenLoop')))
        reply_msg = self.ser.read(7)
        val = struct.unpack('BBHHB',reply_msg)
        return val[3]

    def Read_ps_SoftInterlocks(self):
        op_bin = 1
        ActiveSoftInterlocks = []

        SoftInterlocksList = ['N/A', 'Sobre-tensao na carga 1', 'N/A',\
                             'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A',\
                             'Sobre-tensao na carga 2', 'N/A',        \
                             'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A',\
                             'Sobre-tensao na carga 3', 'N/A',        \
                             'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A',\
                             'Sobre-tensao na carga 4', 'N/A',        \
                             'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']

        self.read_var(self.index_to_hex(ListVar.index('ps_SoftInterlocks')))
        reply_msg = self.ser.read(9)
        print(reply_msg)
        val = struct.unpack('BBHIB',reply_msg)

        print('Soft Interlocks ativos:')
        for i in range(len('{0:b}'.format(val[3]))):
            if (val[3] & (op_bin << i)) == 2**i:
                ActiveSoftInterlocks.append(SoftInterlocksList[i])
                print(SoftInterlocksList[i])
        print('---------------------------------------------------------------')
        return val[3]

    def Read_ps_HardInterlocks(self):
        op_bin = 1
        ActiveHardInterlocks = []

        HardInterlocksList = ['Sobre-corrente na carga 1', 'N/A',                  \
                             'Sobre-tensao no DC-Link do modulo 1',                \
                             'Sub-tensao no DC-Link do modulo 1',                  \
                             'Falha no rele de entrada do DC-Link do modulo 1',    \
                             'Falha no fusivel de entrada do DC-Link do modulo 1', \
                             'Falha nos drivers do modulo 1',                      \
                             'Sobre-temperatura no modulo 1',                      \
                             'Sobre-corrente na carga 2', 'N/A',                   \
                             'Sobre-tensao no DC-Link do modulo 2',                \
                             'Sub-tensao no DC-Link do modulo 2',                  \
                             'Falha no rele de entrada do DC-Link do modulo 2',    \
                             'Falha no fusivel de entrada do DC-Link do modulo 2', \
                             'Falha nos drivers do modulo 2',                      \
                             'Sobre-temperatura no modulo 2',                      \
                             'Sobre-corrente na carga 3', 'N\A',                   \
                             'Sobre-tensao no DC-Link do modulo 3',                \
                             'Sub-tensao no DC-Link do modulo 3',                  \
                             'Falha no rele de entrada no DC-Link do modulo 3',    \
                             'Falha no fusivel de entrada do DC-Link do modulo 3', \
                             'Falha nos drivers do modulo 3',                      \
                             'Sobre-temperatura no modulo 3',                      \
                             'Sobre-corrente na carga 4', 'N/A',                   \
                             'Sobre-tensao no DC-Link do modulo 4',                \
                             'Sub-tensao no DC-Link do modulo 4',                  \
                             'Falha no rele de entrada do DC-Link do modulo 4',    \
                             'Falha no fusivel de entrada do DC-Link do modulo 4', \
                             'Falha nos drivers do modulo 4',                      \
                             'Sobre-temperatura no modulo 4']

        self.read_var(self.index_to_hex(ListVar.index('ps_HardInterlocks')))
        reply_msg = self.ser.read(9)
        print(reply_msg)
        val = struct.unpack('BBHIB',reply_msg)

        print('Hard Interlocks ativos:')
        for i in range(len('{0:b}'.format(val[3]))):
            if (val[3] & (op_bin << i)) == 2**i:
                ActiveHardInterlocks.append(HardInterlocksList[i])
                print(HardInterlocksList[i])
        print('---------------------------------------------------------------')
        return val[3]

    def Read_iRef(self):
        self.read_var(self.index_to_hex(ListVar.index('iRef')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_wfmRef_Gain(self):
        self.read_var(self.index_to_hex(ListVar.index('wfmRef_Gain')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_wfmRef_Offset(self):
        self.read_var(self.index_to_hex(ListVar.index('wfmRef_Offset')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_sigGen_Enable(self):
        self.read_var(self.index_to_hex(ListVar.index('sigGen_Enable')))
        reply_msg = self.ser.read(7)
        val = struct.unpack('BBHHB',reply_msg)
        return val[3]

    def Read_sigGen_Type(self):
        self.read_var(self.index_to_hex(ListVar.index('sigGen_Type')))
        reply_msg = self.ser.read(7)
        val = struct.unpack('BBHHB',reply_msg)
        return val[3]

    def Read_sigGen_Ncycles(self):
        self.read_var(self.index_to_hex(ListVar.index('sigGen_Ncycles')))
        reply_msg = self.ser.read(7)
        val = struct.unpack('BBHHB',reply_msg)
        return val[3]

    def Read_sigGen_PhaseStart(self):
        self.read_var(self.index_to_hex(ListVar.index('sigGen_PhaseStart')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_sigGen_PhaseEnd(self):
        self.read_var(self.index_to_hex(ListVar.index('sigGen_PhaseEnd')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_sigGen_Freq(self):
        self.read_var(self.index_to_hex(ListVar.index('sigGen_Freq')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_sigGen_Amplitude(self):
        self.read_var(self.index_to_hex(ListVar.index('sigGen_Amplitude')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_sigGen_Offset(self):
        self.read_var(self.index_to_hex(ListVar.index('sigGen_Offset')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_sigGen_Aux(self):
        self.read_var(self.index_to_hex(ListVar.index('sigGen_Aux')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_dp_ID(self):
        self.read_var(self.index_to_hex(ListVar.index('dp_ID')))
        reply_msg = self.ser.read(7)
        val = struct.unpack('BBHHB',reply_msg)
        return val[3]

    def Read_dp_Class(self):
        self.read_var(self.index_to_hex(ListVar.index('dp_Class')))
        reply_msg = self.ser.read(7)
        val = struct.unpack('BBHHB',reply_msg)
        return val[3]

    def Read_dp_Coeffs(self):
        self.read_var(self.index_to_hex(ListVar.index('dp_Coeffs')))
        reply_msg = self.ser.read(69)
        val = struct.unpack('BBHffffffffffffffffB',reply_msg)
        return [val[3],val[4],val[5],val[6],val[7],val[8],val[9],val[10],val[11],val[12],val[13],val[14],val[15],val[16],val[17],val[18]]

    def Read_ps_Model(self):
        self.read_var(self.index_to_hex(ListVar.index('ps_Model')))
        reply_msg = self.ser.read(7)
        val = struct.unpack('BBHHB',reply_msg)
        return val

    def read_ps_model(self):
        reply_msg = self.Read_ps_Model()
        return ListPSModels[reply_msg[3]]

    def Read_wfmRef_PtrBufferStart(self):
        self.read_var(self.index_to_hex(ListVar.index('wfmRef_PtrBufferStart')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHIB',reply_msg)
        return val[3]

    def Read_wfmRef_PtrBufferEnd(self):
        self.read_var(self.index_to_hex(ListVar.index('wfmRef_PtrBufferEnd')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHIB',reply_msg)
        return val[3]

    def Read_wfmRef_PtrBufferK(self):
        self.read_var(self.index_to_hex(ListVar.index('wfmRef_PtrBufferK')))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHIB',reply_msg)
        return val[3]

    def Read_wfmRef_SyncMode(self):
        self.read_var(self.index_to_hex(ListVar.index('wfmRef_SyncMode')))
        reply_msg = self.ser.read(7)
        val = struct.unpack('BBHHB',reply_msg)
        return val[3]

    def Read_iRef1(self):
        self.read_var(self.index_to_hex(45))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_iRef2(self):
        self.read_var(self.index_to_hex(46))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_iRef3(self):
        self.read_var(self.index_to_hex(47))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_iRef4(self):
        self.read_var(self.index_to_hex(48))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    def Read_counterSetISlowRefx4(self):
        self.read_var(self.index_to_hex(49))
        reply_msg = self.ser.read(9)
        val = struct.unpack('BBHfB',reply_msg)
        return val[3]

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ======================================================================
                Métodos de Escrita de Valores das Variáveis BSMP
            O retorno do método são os bytes de retorno da mensagem
    ======================================================================
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def Write_sigGen_Freq(self,float_value):
        hex_float    = self.float_to_hex(float_value)
        send_packet  = self.ComWriteVar+self.WriteFloatSizePayload+self.index_to_hex(ListVar.index('sigGen_Freq'))+hex_float
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(5)

    def Write_sigGen_Amplitude(self,float_value):
        hex_float    = self.float_to_hex(float_value)
        send_packet  = self.ComWriteVar+self.WriteFloatSizePayload+self.index_to_hex(ListVar.index('sigGen_Amplitude'))+hex_float
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(5)

    def Write_sigGen_Offset(self,float_value):
        hex_float    = self.float_to_hex(float_value)
        send_packet  = self.ComWriteVar+self.WriteFloatSizePayload+self.index_to_hex(ListVar.index('sigGen_Offset'))+hex_float
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(5)

    def Write_sigGen_Aux(self,float_value):
        hex_float    = self.float_to_hex(float_value)
        send_packet  = self.ComWriteVar+self.WriteFloatSizePayload+self.index_to_hex(ListVar.index('sigGen_Aux'))+hex_float
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(5)

    def Write_dp_ID(self,double_value):
        hex_double   = self.double_to_hex(double_value)
        send_packet  = self.ComWriteVar+self.WriteDoubleSizePayload+self.index_to_hex(ListVar.index('dp_ID'))+hex_double
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(5)

    def Write_dp_Class(self,double_value):
        hex_double   = self.double_to_hex(double_value)
        send_packet  = self.ComWriteVar+self.WriteDoubleSizePayload+self.index_to_hex(ListVar.index('dp_Class'))+hex_double
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(5)

    def Write_dp_Coeffs(self,list_float):

        hex_float_list = []
        #list_full = list_float[:]

        #while(len(list_full) < self.DP_MODULE_MAX_COEFF):
        #    list_full.append(0)

        list_full = [0 for i in range(self.DP_MODULE_MAX_COEFF)]
        list_full[:len(list_float)] = list_float[:]

        for float_value in list_full:
            hex_float = self.float_to_hex(float(float_value))
            hex_float_list.append(hex_float)
        str_float_list = ''.join(hex_float_list)
        payload_size = self.size_to_hex(1+4*self.DP_MODULE_MAX_COEFF) #Payload: ID + 16floats
        send_packet  = self.ComWriteVar+payload_size+self.index_to_hex(ListVar.index('dp_Coeffs'))+str_float_list
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(5)

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ======================================================================
                     Métodos de Escrita de Curvas BSMP
            O retorno do método são os bytes de retorno da mensagem
    ======================================================================
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    def Send_wfmRef_Curve(self,block_idx,data):
        block_hex = struct.pack('>H',block_idx).decode('ISO-8859-1')
        val   = []
        for k in range(0,len(data)):
           val.append(self.float_to_hex(float(data[k])))
        payload_size  = struct.pack('>H', (len(val)*4)+3).decode('ISO-8859-1')
        curva_hex     = ''.join(val)
        send_packet   = self.ComSendWfmRef+payload_size+self.index_to_hex(ListCurv.index('wfmRef_Curve'))+block_hex+curva_hex
        send_msg      = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(5)

    def Recv_wfmRef_Curve(self,block_idx):
        block_hex    = struct.pack('>H',block_idx).decode('ISO-8859-1')
        payload_size = self.size_to_hex(1+2) #Payload: ID+Block_index
        send_packet  = self.ComRequestCurve+payload_size+self.index_to_hex(ListCurv.index('wfmRef_Curve'))+block_hex
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        recv_msg = self.ser.read(1+1+2+1+2+8192+1) #Address+Command+Size+ID+Block_idx+data+checksum
        val = []
        for k in range(7,len(recv_msg)-1,4):
            val.append(struct.unpack('f',recv_msg[k:k+4]))
        return val

    def Recv_samplesBuffer(self):
        block_hex    = struct.pack('>H',0).decode('ISO-8859-1')
        payload_size = self.size_to_hex(1+2) #Payload: ID+Block_index
        send_packet  = self.ComRequestCurve+payload_size+self.index_to_hex(ListCurv.index('samplesBuffer'))+block_hex
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        recv_msg = self.ser.read(1+1+2+1+2+16384+1) #Address+Command+Size+ID+Block_idx+data+checksum
        val = []
        try:
            for k in range(7,len(recv_msg)-1,4):
                val.extend(struct.unpack('f',recv_msg[k:k+4]))
        except:
            pass
        return val

    def Send_fullwfmRef_Curve(self,block_idx,data):
        block_hex = struct.pack('>H',block_idx).decode('ISO-8859-1')
        val   = []
        for k in range(0,len(data)):
           val.append(self.float_to_hex(float(data[k])))
        payload_size  = struct.pack('>H', (len(val)*4)+3).decode('ISO-8859-1')
        curva_hex     = ''.join(val)
        send_packet   = self.ComSendWfmRef+payload_size+self.index_to_hex(ListCurv.index('fullwfmRef_Curve'))+block_hex+curva_hex
        send_msg      = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(5)

    def Recv_fullwfmRef_Curve(self,block_idx):
        block_hex    = struct.pack('>H',block_idx).decode('ISO-8859-1')
        payload_size = self.size_to_hex(1+2) #Payload: ID+Block_index
        send_packet  = self.ComRequestCurve+payload_size+self.index_to_hex(ListCurv.index('fullwfmRef_Curve'))+block_hex
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        recv_msg = self.ser.read(1+1+2+1+2+16384+1) #Address+Command+Size+ID+Block_idx+data+checksum
        val = []
        for k in range(7,len(recv_msg)-1,4):
            val.append(struct.unpack('f',recv_msg[k:k+4]))
        return val

    def Recv_samplesBuffer_blocks(self,block_idx):
        block_hex    = struct.pack('>H',block_idx).decode('ISO-8859-1')
        payload_size = self.size_to_hex(1+2) #Payload: ID+Block_index
        send_packet  = self.ComRequestCurve+payload_size+self.index_to_hex(ListCurv.index('samplesBuffer_blocks'))+block_hex
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        #t0 = time.time()
        self.ser.write(send_msg.encode('ISO-8859-1'))
        recv_msg = self.ser.read(1+1+2+1+2+1024+1) #Address+Command+Size+ID+Block_idx+data+checksum
        #print(time.time()-t0)
        #print(recv_msg)
        val = []
        for k in range(7,len(recv_msg)-1,4):
            val.extend(struct.unpack('f',recv_msg[k:k+4]))
        return val

    def Recv_samplesBuffer_allblocks(self):
        buff = []
        #self.DisableSamplesBuffer()
        for i in range(0,16):
            #t0 = time.time()
            buff.extend(self.Recv_samplesBuffer_blocks(i))
            #print(time.time()-t0)
        #self.EnableSamplesBuffer()
        return buff

    def read_curve_block(self,curve_id,block_id):
        block_hex    = struct.pack('>H',block_id).decode('ISO-8859-1')
        payload_size = self.size_to_hex(1+2) #Payload: curve_id + block_id
        send_packet  = self.ComRequestCurve+payload_size+self.index_to_hex(curve_id)+block_hex
        send_msg     = self.checksum(self.SlaveAdd+send_packet)
        #t0 = time.time()
        self.ser.reset_input_buffer()
        self.ser.write(send_msg.encode('ISO-8859-1'))
        recv_msg = self.ser.read(1+1+2+1+2+size_curve_block[curve_id]+1) #Address+Command+Size+ID+Block_idx+data+checksum
        #print(time.time()-t0)
        #print(recv_msg)
        val = []
        for k in range(7,len(recv_msg)-1,4):
            val.extend(struct.unpack('f',recv_msg[k:k+4]))
        return val
        
    def write_curve_block(self,curve_id,block_id,data):
        block_hex = struct.pack('>H',block_id).decode('ISO-8859-1')
        val   = []
        for k in range(0,len(data)):
           val.append(self.float_to_hex(float(data[k])))
        payload_size  = struct.pack('>H', (len(val)*4)+3).decode('ISO-8859-1')
        curva_hex     = ''.join(val)
        send_packet   = self.ComSendWfmRef+payload_size+self.index_to_hex(curve_id)+block_hex+curva_hex
        send_msg      = self.checksum(self.SlaveAdd+send_packet)
        self.ser.write(send_msg.encode('ISO-8859-1'))
        return self.ser.read(5)
    
    def write_wfmref(self,curve,data):
        #curve = ListCurv_v2_1.index('wfmref')
        block_size = int(size_curve_block[curve]/4)
        print(block_size)
        
        blocks = [data[x:x+block_size] for x in range(0, len(data), block_size)]
        
        ps_status = self.read_ps_status()
        
        wfmref_selected = self.read_bsmp_variable(14,'uint16_t')
        
        if( (wfmref_selected == curve) and (ps_status['state'] == 'RmpWfm' or ps_status['state'] == 'MigWfm') ): 
            print("\n The specified curve ID is currently selected and PS is on " + ps_status['state'] + " state. Choose a different curve ID to proceed.\n")

        else:
            for block_id in range(len(blocks)):
                self.write_curve_block(curve, block_id, blocks[block_id])
                print(blocks[block_id])

    def read_buf_samples_ctom(self):
        buf = []
        curve_id = ListCurv_v2_1.index('buf_samples_ctom')
        
        ps_status = self.read_ps_status()
        if ps_status['model'] == 'FBP':
            for i in range(num_blocks_curves_fbp[curve_id]):
                buf.extend(self.read_curve_block(curve_id,i))
        else:
            for i in range(num_blocks_curves_fax[curve_id]):
                buf.extend(self.read_curve_block(curve_id,i))
            
        return buf
        

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ======================================================================
                            Funções Serial
    ======================================================================
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def Connect(self,port='COM2',baud=6000000):
        try:
            SerialDRS.ser = serial.Serial(port,baud,timeout=1) #port format should be 'COM'+number
            return True
        except:
            return False

    def Disconnect(self):
        if (self.ser.isOpen()):
            try:
                self.ser.close()
                return True
            except:
                return False

    def SetSlaveAdd(self,address):
        self.SlaveAdd = struct.pack('B',address).decode('ISO-8859-1')

    def GetSlaveAdd(self):
        return struct.unpack('B',self.SlaveAdd.encode())[0]

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ======================================================================
                      Funções auxiliares
    ======================================================================
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    def read_vars_common(self, print_all = False):
    
        loop_state = ["Closed Loop","Open Loop"]
        
        ps_status = self.read_ps_status()
        if ps_status['open_loop'] == 0:
            if (ps_status['model'] == 'FAC_ACDC') or (ps_status['model'] == 'FAC_2S_ACDC') or (ps_status['model'] == 'FAC_2P4S_ACDC'):
                setpoint_unit = " V"
            else:
                setpoint_unit = " A"
        else:
            setpoint_unit = " %"
            
        print("\nPS Model: " + ps_status['model'])
        print("State: " + ps_status['state'])
        print("Loop State: " + loop_state[ps_status['open_loop']])
        
        print("\nSetpoint: " + str(self.read_bsmp_variable(1,'float')) + setpoint_unit)
        print("Reference: " + str(self.read_bsmp_variable(2,'float')) + setpoint_unit)
        
        if print_all:
            print(self.read_ps_status())
            
            print("\nCounter set_slowref: " + str(self.read_bsmp_variable(4,'uint32_t')))
            print("Counter sync pulse: " + str(self.read_bsmp_variable(5,'uint32_t')))
            
            self.get_siggen_vars()
            self.get_wfmref_vars(0)
            self.get_wfmref_vars(1)
            self.get_scope_vars()
        
    def decode_interlocks(self,reg_interlocks,list_interlocks):
        active_interlocks = []
        
        for i in range(32):
            if(reg_interlocks & (1 << i)):
                active_interlocks.append(list_interlocks[i])
                print('\t' + list_interlocks[i])
        return active_interlocks
    
    def read_vars_fbp(self, n = 1, dt = 0.5):
    
        try:
            for i in range(n):
            
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                self.read_vars_common()
                
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fbp_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fbp_hard_interlocks)
                
                print("\nLoad Current: " + str(self.read_bsmp_variable(33,'float')) + " A")
                print("Load Voltage: " + str(self.read_bsmp_variable(34,'float')) + " V")
                print("Load Resistance: " + str( self.read_bsmp_variable(34,'float') / self.read_bsmp_variable(33,'float')) + " Ohm")
                print("Load Power: " + str( self.read_bsmp_variable(34,'float') * self.read_bsmp_variable(33,'float')) + " W")
                print("DC-Link Voltage: " + str(self.read_bsmp_variable(35,'float')) + " V")
                print("Heat-Sink Temp: " + str(self.read_bsmp_variable(36,'float')) + " ºC")
                print("Duty-Cycle: " + str(self.read_bsmp_variable(37,'float')) + " %")
                
                time.sleep(dt)
                
        except:
            pass
    
    def read_vars_fbp_dclink(self, n = 1, dt = 0.5):
    
        try:
            for i in range(n):
            
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                self.read_vars_common()
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("\nHard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fbp_dclink_hard_interlocks)
                
                print("\nModules status: " + str(self.read_bsmp_variable(33,'uint32_t')))
                print("DC-Link Voltage: " + str(self.read_bsmp_variable(34,'float')) + " V")
                print("PS1 Voltage: " + str(self.read_bsmp_variable(35,'float')) + " V")
                print("PS2 Voltage: " + str(self.read_bsmp_variable(36,'float')) + " V")
                print("PS3 Voltage: " + str(self.read_bsmp_variable(37,'float')) + " V")
                print("Dig Pot Tap: " + str(self.read_bsmp_variable(38,'uint8_t')))
                
                time.sleep(dt)
                
        except:
            pass

    def read_vars_fac_acdc(self, n = 1, dt = 0.5, iib = 1):
    
        #try:
        for i in range(n):
        
            print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
            self.read_vars_common()
    
            soft_itlks = self.read_bsmp_variable(31,'uint32_t')
            print("\nSoft Interlocks: " + str(soft_itlks))
            if(soft_itlks):
                self.decode_interlocks(soft_itlks, list_fac_acdc_soft_interlocks)
                print('')
            
            hard_itlks = self.read_bsmp_variable(32,'uint32_t')
            print("Hard Interlocks: " + str(hard_itlks))
            if(hard_itlks):
                self.decode_interlocks(hard_itlks, list_fac_acdc_hard_interlocks)
                
            iib_is_itlks = self.read_bsmp_variable(45,'uint32_t')
            print("\nIIB IS Interlocks: " + str(iib_is_itlks))
            if(iib_is_itlks):
                self.decode_interlocks(iib_is_itlks, list_fac_acdc_iib_is_interlocks)
                
            iib_is_alarms = self.read_bsmp_variable(46,'uint32_t')
            print("IIB IS Alarms: " + str(iib_is_alarms))
            if(iib_is_alarms):
                self.decode_interlocks(iib_is_alarms, list_fac_acdc_iib_is_alarms)

            iib_cmd_itlks = self.read_bsmp_variable(57,'uint32_t')
            print("\nIIB Cmd Interlocks: " + str(iib_cmd_itlks))
            if(iib_cmd_itlks):
                self.decode_interlocks(iib_cmd_itlks, list_fac_acdc_iib_cmd_interlocks)
                
            iib_cmd_alarms = self.read_bsmp_variable(58,'uint32_t')
            print("IIB Cmd Alarms: " + str(iib_cmd_alarms))
            if(iib_cmd_alarms):
                self.decode_interlocks(iib_cmd_alarms, list_fac_acdc_iib_cmd_alarms)
                
            print("\nCapBank Voltage: " + str(self.read_bsmp_variable(33,'float')) + " V")
            print("Rectifier Current: " + str(self.read_bsmp_variable(34,'float')) + " A")
            
            print("Duty-Cycle: " + str(self.read_bsmp_variable(35,'float')) + " %")
            
            if(iib):
                print("\nIIB IS Input Current: " + str(self.read_bsmp_variable(36,'float')) + " A")
                print("IIB IS Input Voltage: " + str(self.read_bsmp_variable(37,'float')) + " V")
                print("IIB IS IGBT Temp: " + str(self.read_bsmp_variable(38,'float')) + " ºC")
                print("IIB IS Driver Voltage: " + str(self.read_bsmp_variable(39,'float')) + " V")
                print("IIB IS Driver Current: " + str(self.read_bsmp_variable(40,'float')) + " A")
                print("IIB IS Inductor Temp: " + str(self.read_bsmp_variable(41,'float')) + " ºC")
                print("IIB IS Heat-Sink Temp: " + str(self.read_bsmp_variable(42,'float')) + " ºC")
                print("IIB IS Board Temp: " + str(self.read_bsmp_variable(43,'float')) + " ºC")
                print("IIB IS Board RH: " + str(self.read_bsmp_variable(44,'float')) + " %")
                print("IIB IS Interlocks: " + str(self.read_bsmp_variable(45,'uint32_t')))
                print("IIB IS Alarms: " + str(self.read_bsmp_variable(46,'uint32_t')))
                
                print("\nIIB Cmd Load Voltage: " + str(self.read_bsmp_variable(47,'float')) + " V")
                print("IIB Cmd CapBank Voltage: " + str(self.read_bsmp_variable(48,'float')) + " V")
                print("IIB Cmd Rectifier Inductor Temp: " + str(self.read_bsmp_variable(49,'float')) + " ºC")
                print("IIB Cmd Rectifier Heat-Sink Temp: " + str(self.read_bsmp_variable(50,'float')) + " ºC")
                print("IIB Cmd External Boards Voltage: " + str(self.read_bsmp_variable(51,'float')) + " V")
                print("IIB Cmd Auxiliary Board Current: " + str(self.read_bsmp_variable(52,'float')) + " A")
                print("IIB Cmd IDB Board Current: " + str(self.read_bsmp_variable(53,'float')) + " A")
                print("IIB Cmd Ground Leakage Current: " + str(self.read_bsmp_variable(54,'float')) + " A")
                print("IIB Cmd Board Temp: " + str(self.read_bsmp_variable(55,'float')) + " ºC")
                print("IIB Cmd Board RH: " + str(self.read_bsmp_variable(56,'float')) + " %")
                print("IIB Cmd Interlocks: " + str(self.read_bsmp_variable(57,'uint32_t')))
                print("IIB Cmd Alarms: " + str(self.read_bsmp_variable(58,'uint32_t')))
            
            time.sleep(dt)
                
        #except:
        #    pass
        
    def read_vars_fac_dcdc(self, n = 1, dt = 0.5, iib = 1):
    
        try:
            for i in range(n):
            
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                self.read_vars_common()
        
                print("\nSync Pulse Counter: " + str(self.read_bsmp_variable(5,'uint32_t')))
                print("WfmRef Index: " + str( (self.read_bsmp_variable(20,'uint32_t') - self.read_bsmp_variable(18,'uint32_t'))/2 + 1))
                
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fac_dcdc_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fac_dcdc_hard_interlocks)
                    
                iib_itlks = self.read_bsmp_variable(51,'uint32_t')
                print("\nIIB Interlocks: " + str(iib_itlks))
                if(iib_itlks):
                    self.decode_interlocks(iib_itlks, list_fac_dcdc_iib_interlocks)
                    
                iib_alarms = self.read_bsmp_variable(52,'uint32_t')
                print("IIB Alarms: " + str(iib_alarms))
                if(iib_alarms):
                    self.decode_interlocks(iib_alarms, list_fac_dcdc_iib_alarms)
        
                print("\nLoad Current: " + str(self.read_bsmp_variable(33,'float')) + " A")
                print("Load Current DCCT 1: " + str(self.read_bsmp_variable(34,'float')) + " A")
                print("Load Current DCCT 2: " + str(self.read_bsmp_variable(35,'float')) + " A")
                
                print("\nCapBank Voltage: " + str(self.read_bsmp_variable(36,'float')) + " V")
                
                print("\nDuty-Cycle: " + str(self.read_bsmp_variable(37,'float')) + " %")
                
                if(iib):
                    print("\nIIB CapBank Voltage: " + str(self.read_bsmp_variable(38,'float')) + " V")
                    print("IIB Input Current: " + str(self.read_bsmp_variable(39,'float')) + " A")
                    print("IIB Output Current: " + str(self.read_bsmp_variable(40,'float')) + " A")
                    print("IIB IGBT Leg 1 Temp: " + str(self.read_bsmp_variable(41,'float')) + " ºC")
                    print("IIB IGBT Leg 2 Temp: " + str(self.read_bsmp_variable(42,'float')) + " ºC")
                    print("IIB Inductor Temp: " + str(self.read_bsmp_variable(43,'float')) + " ºC")
                    print("IIB Heat-Sink Temp: " + str(self.read_bsmp_variable(44,'float')) + " ºC")
                    print("IIB Driver Voltage: " + str(self.read_bsmp_variable(45,'float')) + " V")
                    print("IIB Driver Current 1: " + str(self.read_bsmp_variable(46,'float')) + " A")
                    print("IIB Driver Current 2: " + str(self.read_bsmp_variable(47,'float')) + " A")
                    print("IIB Ground Leakage Current: " + str(self.read_bsmp_variable(48,'float')) + " A")
                    print("IIB Board Temp: " + str(self.read_bsmp_variable(49,'float')) + " ºC")
                    print("IIB Board RH: " + str(self.read_bsmp_variable(50,'float')) + " %")
                    print("IIB Interlocks: " + str(self.read_bsmp_variable(51,'uint32_t')))
                    print("IIB Alarms: " + str(self.read_bsmp_variable(52,'uint32_t')))
                    
                time.sleep(dt)
                
        except:
            pass
            
    def read_vars_fac_dcdc_ema(self, n = 1, dt = 0.5, iib = 0):
    
        try:
            for i in range(n):
            
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                self.read_vars_common()
                
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fac_dcdc_ema_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fac_dcdc_ema_hard_interlocks)
                    
                iib_itlks = self.read_bsmp_variable(39,'uint32_t')
                print("IIB Interlocks: " + str(iib_itlks))
                if(iib_itlks):
                    self.decode_interlocks(iib_itlks, list_fac_dcdc_iib_interlocks)
        
                print("\nLoad Current: " + str(self.read_bsmp_variable(33,'float')))
                print("CapBank Voltage: " + str(self.read_bsmp_variable(34,'float')))
                print("\nDuty-Cycle: " + str(self.read_bsmp_variable(35,'float')))
                
                if(iib):
                    print("\nIIB Input Current: " + str(self.read_bsmp_variable(36,'float')) + " A")
                    print("IIB Output Current: " + str(self.read_bsmp_variable(37,'float')) + " A")
                    print("IIB CapBank Voltage: " + str(self.read_bsmp_variable(38,'float')) + " V")
                    print("IIB IGBT Leg 1 Temp: " + str(self.read_bsmp_variable(39,'float')) + " ºC")
                    print("IIB IGBT Leg 2 Temp: " + str(self.read_bsmp_variable(40,'float')) + " ºC")
                    print("IIB Inductor Temp: " + str(self.read_bsmp_variable(41,'float')) + " ºC")
                    print("IIB Heat-Sink Temp: " + str(self.read_bsmp_variable(42,'float')) + " ºC")
                    print("IIB Driver 1 Error: " + str(self.read_bsmp_variable(43,'float')))
                    print("IIB Driver 2 Error: " + str(self.read_bsmp_variable(44,'float')))
                    
                time.sleep(dt)
                
        except:
            pass

    def read_vars_fac_2s_acdc(self, n = 1, add_mod_a = 2, dt = 0.5, iib = 0):
    
        old_add = self.GetSlaveAdd()
        
        try:
            for i in range(n):
            
                self.SetSlaveAdd(add_mod_a)
            
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                self.read_vars_common()
    
                print('\n *** MODULE A ***')
    
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fac_2s_acdc_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fac_2s_acdc_hard_interlocks)
                    
                iib_is_itlks = self.read_bsmp_variable(45,'uint32_t')
                print("\nIIB IS Interlocks: " + str(iib_is_itlks))
                if(iib_is_itlks):
                    self.decode_interlocks(iib_is_itlks, list_fac_2s_acdc_iib_is_interlocks)
                    
                iib_is_alarms = self.read_bsmp_variable(46,'uint32_t')
                print("IIB IS Alarms: " + str(iib_is_alarms))
                if(iib_is_alarms):
                    self.decode_interlocks(iib_is_alarms, list_fac_2s_acdc_iib_is_alarms)

                iib_cmd_itlks = self.read_bsmp_variable(57,'uint32_t')
                print("\nIIB Cmd Interlocks: " + str(iib_cmd_itlks))
                if(iib_cmd_itlks):
                    self.decode_interlocks(iib_cmd_itlks, list_fac_2s_acdc_iib_cmd_interlocks)
                    
                iib_cmd_alarms = self.read_bsmp_variable(58,'uint32_t')
                print("IIB Cmd Alarms: " + str(iib_cmd_alarms))
                if(iib_cmd_alarms):
                    self.decode_interlocks(iib_cmd_alarms, list_fac_2s_acdc_iib_cmd_alarms)
                
                print("\nCapBank Voltage: " + str(self.read_bsmp_variable(33,'float')) + " V")
                print("Rectifier Current: " + str(self.read_bsmp_variable(34,'float')) + " A")
                print("Duty-Cycle: " + str(self.read_bsmp_variable(35,'float')) + " %")
                
                if(iib):
                    print("\nIIB IS Input Current: " + str(self.read_bsmp_variable(36,'float')) + " A")
                    print("IIB IS Input Voltage: " + str(self.read_bsmp_variable(37,'float')) + " V")
                    print("IIB IS IGBT Temp: " + str(self.read_bsmp_variable(38,'float')) + " ºC")
                    print("IIB IS Driver Voltage: " + str(self.read_bsmp_variable(39,'float')) + " V")
                    print("IIB IS Driver Current: " + str(self.read_bsmp_variable(40,'float')) + " A")
                    print("IIB IS Inductor Temp: " + str(self.read_bsmp_variable(41,'float')) + " ºC")
                    print("IIB IS Heat-Sink Temp: " + str(self.read_bsmp_variable(42,'float')) + " ºC")
                    print("IIB IS Board Temp: " + str(self.read_bsmp_variable(43,'float')) + " ºC")
                    print("IIB IS Board RH: " + str(self.read_bsmp_variable(44,'float')) + " %")
                    print("IIB IS Interlocks: " + str(self.read_bsmp_variable(45,'uint32_t')))
                    print("IIB IS Alarms: " + str(self.read_bsmp_variable(46,'uint32_t')))
                    
                    print("\nIIB Cmd Load Voltage: " + str(self.read_bsmp_variable(47,'float')) + " V")
                    print("IIB Cmd CapBank Voltage: " + str(self.read_bsmp_variable(48,'float')) + " V")
                    print("IIB Cmd Rectifier Inductor Temp: " + str(self.read_bsmp_variable(49,'float')) + " ºC")
                    print("IIB Cmd Rectifier Heat-Sink Temp: " + str(self.read_bsmp_variable(50,'float')) + " ºC")
                    print("IIB Cmd External Boards Voltage: " + str(self.read_bsmp_variable(51,'float')) + " V")
                    print("IIB Cmd Auxiliary Board Current: " + str(self.read_bsmp_variable(52,'float')) + " A")
                    print("IIB Cmd IDB Board Current: " + str(self.read_bsmp_variable(53,'float')) + " A")
                    print("IIB Cmd Ground Leakage Current: " + str(self.read_bsmp_variable(54,'float')) + " A")
                    print("IIB Cmd Board Temp: " + str(self.read_bsmp_variable(55,'float')) + " ºC")
                    print("IIB Cmd Board RH: " + str(self.read_bsmp_variable(56,'float')) + " %")
                    print("IIB Cmd Interlocks: " + str(self.read_bsmp_variable(57,'uint32_t')))
                    print("IIB Cmd Alarms: " + str(self.read_bsmp_variable(58,'uint32_t')))
                        
                self.SetSlaveAdd(add_mod_a+1)
                
                print('\n *** MODULE B ***')
                
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fac_2s_acdc_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fac_2s_acdc_hard_interlocks)
        
                iib_is_itlks = self.read_bsmp_variable(45,'uint32_t')
                print("\nIIB IS Interlocks: " + str(iib_is_itlks))
                if(iib_is_itlks):
                    self.decode_interlocks(iib_is_itlks, list_fac_2s_acdc_iib_is_interlocks)
                    
                iib_is_alarms = self.read_bsmp_variable(46,'uint32_t')
                print("IIB IS Alarms: " + str(iib_is_alarms))
                if(iib_is_alarms):
                    self.decode_interlocks(iib_is_alarms, list_fac_2s_acdc_iib_is_alarms)

                iib_cmd_itlks = self.read_bsmp_variable(57,'uint32_t')
                print("\nIIB Cmd Interlocks: " + str(iib_cmd_itlks))
                if(iib_cmd_itlks):
                    self.decode_interlocks(iib_cmd_itlks, list_fac_2s_acdc_iib_cmd_interlocks)
                    
                iib_cmd_alarms = self.read_bsmp_variable(58,'uint32_t')
                print("IIB Cmd Alarms: " + str(iib_cmd_alarms))
                if(iib_cmd_alarms):
                    self.decode_interlocks(iib_cmd_alarms, list_fac_2s_acdc_iib_cmd_alarms)
                
                print("\nCapBank Voltage: " + str(self.read_bsmp_variable(33,'float')) + " V")
                print("Rectifier Current: " + str(self.read_bsmp_variable(34,'float')) + " A")
                print("Duty-Cycle: " + str(self.read_bsmp_variable(35,'float')) + " %")
                
                if(iib):
                    print("\nIIB IS Input Current: " + str(self.read_bsmp_variable(36,'float')) + " A")
                    print("IIB IS Input Voltage: " + str(self.read_bsmp_variable(37,'float')) + " V")
                    print("IIB IS IGBT Temp: " + str(self.read_bsmp_variable(38,'float')) + " ºC")
                    print("IIB IS Driver Voltage: " + str(self.read_bsmp_variable(39,'float')) + " V")
                    print("IIB IS Driver Current: " + str(self.read_bsmp_variable(40,'float')) + " A")
                    print("IIB IS Inductor Temp: " + str(self.read_bsmp_variable(41,'float')) + " ºC")
                    print("IIB IS Heat-Sink Temp: " + str(self.read_bsmp_variable(42,'float')) + " ºC")
                    print("IIB IS Board Temp: " + str(self.read_bsmp_variable(43,'float')) + " ºC")
                    print("IIB IS Board RH: " + str(self.read_bsmp_variable(44,'float')) + " %")
                    print("IIB IS Interlocks: " + str(self.read_bsmp_variable(45,'uint32_t')))
                    print("IIB IS Alarms: " + str(self.read_bsmp_variable(46,'uint32_t')))
                    
                    print("\nIIB Cmd Load Voltage: " + str(self.read_bsmp_variable(47,'float')) + " V")
                    print("IIB Cmd CapBank Voltage: " + str(self.read_bsmp_variable(48,'float')) + " V")
                    print("IIB Cmd Rectifier Inductor Temp: " + str(self.read_bsmp_variable(49,'float')) + " ºC")
                    print("IIB Cmd Rectifier Heat-Sink Temp: " + str(self.read_bsmp_variable(50,'float')) + " ºC")
                    print("IIB Cmd External Boards Voltage: " + str(self.read_bsmp_variable(51,'float')) + " V")
                    print("IIB Cmd Auxiliary Board Current: " + str(self.read_bsmp_variable(52,'float')) + " A")
                    print("IIB Cmd IDB Board Current: " + str(self.read_bsmp_variable(53,'float')) + " A")
                    print("IIB Cmd Ground Leakage Current: " + str(self.read_bsmp_variable(54,'float')) + " A")
                    print("IIB Cmd Board Temp: " + str(self.read_bsmp_variable(55,'float')) + " ºC")
                    print("IIB Cmd Board RH: " + str(self.read_bsmp_variable(56,'float')) + " %")
                    print("IIB Cmd Interlocks: " + str(self.read_bsmp_variable(57,'uint32_t')))
                    print("IIB Cmd Alarms: " + str(self.read_bsmp_variable(58,'uint32_t')))
                        
                time.sleep(dt)
                
            self.SetSlaveAdd(old_add)
        except:
            self.SetSlaveAdd(old_add)
            
    def read_vars_fac_2s_dcdc(self, n = 1, com_add = 1, dt = 0.5, iib = 0):
    
        old_add = self.GetSlaveAdd()
        iib_offset = 14*(iib-1)
        
        try:
            for i in range(n):
    
                self.SetSlaveAdd(com_add)
            
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                
                self.read_vars_common()
                
                print("\nSync Pulse Counter: " + str(self.read_bsmp_variable(5,'uint32_t')))
                                
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fac_2s_dcdc_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fac_2s_dcdc_hard_interlocks)
                
                print("\nLoad Current: " + str(self.read_bsmp_variable(33,'float')) + " A")
                print("Load Current DCCT 1: " + str(self.read_bsmp_variable(34,'float')) + " A")
                print("Load Current DCCT 2: " + str(self.read_bsmp_variable(35,'float')) + " A")
                
                print("\nCapBank Voltage 1: " + str(self.read_bsmp_variable(36,'float')) + " V")
                print("CapBank Voltage 2: " + str(self.read_bsmp_variable(37,'float')) + " V")
                
                print("\nDuty-Cycle 1: " + str(self.read_bsmp_variable(38,'float')) + " %")
                print("Duty-Cycle 2: " + str(self.read_bsmp_variable(39,'float')) + " %")
                
                if(iib):
                    print("\nIIB CapBank Voltage: " + str(self.read_bsmp_variable(40 + iib_offset,'float')) + " V")
                    print("IIB Input Current: " + str(self.read_bsmp_variable(41 + iib_offset,'float')) + " A")
                    print("IIB Output Current: " + str(self.read_bsmp_variable(42 + iib_offset,'float')) + " A")
                    print("IIB IGBT Leg 1 Temp: " + str(self.read_bsmp_variable(43 + iib_offset,'float')) + " ºC")
                    print("IIB IGBT Leg 2 Temp: " + str(self.read_bsmp_variable(44 + iib_offset,'float')) + " ºC")
                    print("IIB Inductor Temp: " + str(self.read_bsmp_variable(45 + iib_offset,'float')) + " ºC")
                    print("IIB Heat-Sink Temp: " + str(self.read_bsmp_variable(46 + iib_offset,'float')) + " ºC")
                    print("IIB Driver Voltage: " + str(self.read_bsmp_variable(47 + iib_offset,'float')) + " V")
                    print("IIB Driver Current 1: " + str(self.read_bsmp_variable(48 + iib_offset,'float')) + " A")
                    print("IIB Driver Current 2: " + str(self.read_bsmp_variable(49 + iib_offset,'float')) + " A")
                    print("IIB Board Temp: " + str(self.read_bsmp_variable(50 + iib_offset,'float')) + " ºC")
                    print("IIB Board RH: " + str(self.read_bsmp_variable(51 + iib_offset,'float')) + " %")
                    
                    iib_itlks = self.read_bsmp_variable(52 + iib_offset,'uint32_t')
                    print("\nIIB Interlocks: " + str(iib_itlks))
                    if(iib_itlks):
                        self.decode_interlocks(iib_itlks, list_fac_2s_dcdc_iib_interlocks)
                        
                    iib_alarms = self.read_bsmp_variable(53 + iib_offset,'uint32_t')
                    print("IIB Alarms: " + str(iib_alarms))
                    if(iib_alarms):
                        self.decode_interlocks(iib_alarms, list_fac_2s_dcdc_iib_alarms)

                time.sleep(dt)
                
            self.SetSlaveAdd(old_add)
        except:
            self.SetSlaveAdd(old_add)

    def read_vars_fac_2p4s_acdc(self, n = 1, add_mod_a = 1, dt = 0.5, iib = 0):
        self.read_vars_fac_2s_acdc(n, add_mod_a, dt, iib)
            
    def read_vars_fac_2p4s_dcdc(self, n = 1, com_add = 1, dt = 0.5, iib = 0):
    
        old_add = self.GetSlaveAdd()
        
        try:
            for i in range(n):
    
                self.SetSlaveAdd(com_add)
            
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                
                self.read_vars_common()
                
                print("\nSync Pulse Counter: " + str(self.read_bsmp_variable(5,'uint32_t')))
                                
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fac_2p4s_dcdc_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fac_2p4s_dcdc_hard_interlocks)
                
                print("\nLoad Current: " + str(self.read_bsmp_variable(33,'float')))
                print("Load Current DCCT 1: " + str(self.read_bsmp_variable(34,'float')))
                print("Load Current DCCT 2: " + str(self.read_bsmp_variable(35,'float')))
                
                print("\nArm Current 1: " + str(self.read_bsmp_variable(36,'float')))
                print("Arm Current 2: " + str(self.read_bsmp_variable(37,'float')))
                
                print("\nCapBank Voltage 1: " + str(self.read_bsmp_variable(38,'float')))
                print("CapBank Voltage 2: " + str(self.read_bsmp_variable(39,'float')))
                print("CapBank Voltage 3: " + str(self.read_bsmp_variable(40,'float')))
                print("CapBank Voltage 4: " + str(self.read_bsmp_variable(41,'float')))
                print("CapBank Voltage 5: " + str(self.read_bsmp_variable(42,'float')))
                print("CapBank Voltage 6: " + str(self.read_bsmp_variable(43,'float')))
                print("CapBank Voltage 7: " + str(self.read_bsmp_variable(44,'float')))
                print("CapBank Voltage 8: " + str(self.read_bsmp_variable(45,'float')))
                
                print("\nDuty-Cycle 1: " + str(self.read_bsmp_variable(46,'float')))
                print("Duty-Cycle 2: " + str(self.read_bsmp_variable(47,'float')))
                print("Duty-Cycle 3: " + str(self.read_bsmp_variable(48,'float')))
                print("Duty-Cycle 4: " + str(self.read_bsmp_variable(49,'float')))
                print("Duty-Cycle 5: " + str(self.read_bsmp_variable(50,'float')))
                print("Duty-Cycle 6: " + str(self.read_bsmp_variable(51,'float')))
                print("Duty-Cycle 7: " + str(self.read_bsmp_variable(52,'float')))
                print("Duty-Cycle 8: " + str(self.read_bsmp_variable(53,'float')))   

                if(iib):

                    print("\nIIB CapBank Voltage: " + str(self.read_bsmp_variable(54,'float')) + " V")
                    print("IIB Input Current: " + str(self.read_bsmp_variable(55, 'float')) + " A")
                    print("IIB Output Current: " + str(self.read_bsmp_variable(56,'float')) + " A")
                    print("IIB IGBT Leg 1 Temp: " + str(self.read_bsmp_variable(57,'float')) + " ºC")
                    print("IIB IGBT Leg 2 Temp: " + str(self.read_bsmp_variable(58,'float')) + " ºC")
                    print("IIB Inductor Temp: " + str(self.read_bsmp_variable(59,'float')) + " ºC")
                    print("IIB Heat-Sink Temp: " + str(self.read_bsmp_variable(60,'float')) + " ºC")
                    print("IIB Driver Voltage: " + str(self.read_bsmp_variable(61,'float')) + " V")
                    print("IIB Driver Current 1: " + str(self.read_bsmp_variable(62,'float')) + " A")
                    print("IIB Driver Current 2: " + str(self.read_bsmp_variable(63,'float')) + " A")
                    print("IIB Board Temp: " + str(self.read_bsmp_variable(64,'float')) + " ºC")
                    print("IIB Board RH: " + str(self.read_bsmp_variable(65,'float')) + " %")
                    
                    iib_itlks = self.read_bsmp_variable(66,'uint32_t')
                    print("\nIIB Interlocks: " + str(iib_itlks))
                    if(iib_itlks):
                        self.decode_interlocks(iib_itlks, list_fac_2p4s_dcdc_iib_interlocks)
                        
                    iib_alarms = self.read_bsmp_variable(67,'uint32_t')
                    print("IIB Alarms: " + str(iib_alarms))
                    if(iib_alarms):
                        self.decode_interlocks(iib_alarms, list_fac_2p4s_dcdc_iib_alarms)    

                    print("\nIIB CapBank Voltage: " + str(self.read_bsmp_variable(68,'float')) + " V")
                    print("IIB Input Current: " + str(self.read_bsmp_variable(69,'float')) + " A")
                    print("IIB Output Current: " + str(self.read_bsmp_variable(70,'float')) + " A")
                    print("IIB IGBT Leg 1 Temp: " + str(self.read_bsmp_variable(71,'float')) + " ºC")
                    print("IIB IGBT Leg 2 Temp: " + str(self.read_bsmp_variable(72,'float')) + " ºC")
                    print("IIB Inductor Temp: " + str(self.read_bsmp_variable(73,'float')) + " ºC")
                    print("IIB Heat-Sink Temp: " + str(self.read_bsmp_variable(74,'float')) + " ºC")
                    print("IIB Driver Voltage: " + str(self.read_bsmp_variable(75,'float')) + " V")
                    print("IIB Driver Current 1: " + str(self.read_bsmp_variable(76,'float')) + " A")
                    print("IIB Driver Current 2: " + str(self.read_bsmp_variable(77,'float')) + " A")
                    print("IIB Board Temp: " + str(self.read_bsmp_variable(78,'float')) + " ºC")
                    print("IIB Board RH: " + str(self.read_bsmp_variable(79,'float')) + " %")
                    
                    iib_itlks = self.read_bsmp_variable(80,'uint32_t')
                    print("\nIIB Interlocks: " + str(iib_itlks))
                    if(iib_itlks):
                        self.decode_interlocks(iib_itlks, list_fac_2p4s_dcdc_iib_interlocks)
                        
                    iib_alarms = self.read_bsmp_variable(81,'uint32_t')
                    print("IIB Alarms: " + str(iib_alarms))
                    if(iib_alarms):
                        self.decode_interlocks(iib_alarms, list_fac_2p4s_dcdc_iib_alarms)                        
        
                time.sleep(dt)
                
            self.SetSlaveAdd(old_add)
        except:
            self.SetSlaveAdd(old_add)
    
    def read_vars_fap(self, n = 1, com_add = 1, dt = 0.5, iib = 1):
    
        old_add = self.GetSlaveAdd()
        
        try:
            for i in range(n):
            
                self.SetSlaveAdd(com_add)
            
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                self.read_vars_common()
    
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fap_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fap_hard_interlocks)
                    
                iib_itlks = self.read_bsmp_variable(56,'uint32_t')
                print("\nIIB Interlocks: " + str(iib_itlks))
                if(iib_itlks):
                    self.decode_interlocks(iib_itlks, list_fap_iib_interlocks)
                    
                iib_alarms = self.read_bsmp_variable(57,'uint32_t')
                print("\nIIB Alarms: " + str(iib_alarms))
                if(iib_alarms):
                    self.decode_interlocks(iib_alarms, list_fap_iib_alarms)

                iload = self.read_bsmp_variable(33,'float')
                
                print("\nLoad Current: " + str(iload) + " A")
                print("Load Current DCCT 1: " + str(self.read_bsmp_variable(34,'float')) + " A")
                print("Load Current DCCT 2: " + str(self.read_bsmp_variable(35,'float')) + " A")
                
                if not iload == 0:
                    print("\nLoad Resistance: " + str( abs(self.read_bsmp_variable(43,'float')) / iload ) + " Ohm")
                else:
                    print("\nLoad Resistance: 0 Ohm")
                print("Load Power: " + str( self.read_bsmp_variable(43,'float') * self.read_bsmp_variable(33,'float')) + " W")
                
                print("\nDC-Link Voltage: " + str(self.read_bsmp_variable(36,'float')) + " V")
                print("\nIGBT 1 Current: " + str(self.read_bsmp_variable(37,'float')) + " A")
                print("IGBT 2 Current: " + str(self.read_bsmp_variable(38,'float')) + " A")
                print("\nIGBT 1 Duty-Cycle: " + str(self.read_bsmp_variable(39,'float')) + " %")
                print("IGBT 2 Duty-Cycle: " + str(self.read_bsmp_variable(40,'float')) + " %")
                print("Differential Duty-Cycle: " + str(self.read_bsmp_variable(41,'float')) + " %")
                
                if(iib):
                    print("\nIIB Input Voltage: " + str(self.read_bsmp_variable(42,'float')) + " V")
                    print("IIB Output Voltage: " + str(self.read_bsmp_variable(43,'float')) + " V")
                    print("IIB IGBT 1 Current: " + str(self.read_bsmp_variable(44,'float')) + " A")
                    print("IIB IGBT 2 Current: " + str(self.read_bsmp_variable(45,'float')) + " A")
                    print("IIB IGBT 1 Temp: " + str(self.read_bsmp_variable(46,'float')) + " ºC")
                    print("IIB IGBT 2 Temp: " + str(self.read_bsmp_variable(47,'float')) + " ºC")
                    print("IIB Driver Voltage: " + str(self.read_bsmp_variable(48,'float')) + " V")
                    print("IIB Driver Current 1: " + str(self.read_bsmp_variable(49,'float')) + " A")
                    print("IIB Driver Current 2: " + str(self.read_bsmp_variable(50,'float')) + " A")
                    print("IIB Inductor Temp: " + str(self.read_bsmp_variable(51,'float')) + " ºC")
                    print("IIB Heat-Sink Temp: " + str(self.read_bsmp_variable(52,'float')) + " ºC")
                    print("IIB Ground Leakage Current: " + str(self.read_bsmp_variable(53,'float')) + " A")
                    print("IIB Board Temp: " + str(self.read_bsmp_variable(54,'float')) + " ºC")
                    print("IIB Board RH: " + str(self.read_bsmp_variable(55,'float')) + " %")
                    print("IIB Interlocks: " + str(self.read_bsmp_variable(56,'uint32_t')))
                    print("IIB Alarms: " + str(self.read_bsmp_variable(57,'uint32_t')))
                time.sleep(dt)
                
            self.SetSlaveAdd(old_add)
        except:
            self.SetSlaveAdd(old_add)
            
    def read_vars_fap_4p(self, n = 1, com_add = 1, dt = 0.5, iib = 0):
    
        old_add = self.GetSlaveAdd()
        iib_offset = 16*(iib-1)
        
        try:
            for i in range(n):
            
                self.SetSlaveAdd(com_add)
            
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                self.read_vars_common()
    
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fap_4p_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fap_4p_hard_interlocks)
                    
                for j in range(4):
                    iib_itlks = self.read_bsmp_variable(72 + j*16,'uint32_t')
                    print("\nIIB " + str(j+1) + " Interlocks: " + str(iib_itlks))
                    if(iib_itlks):
                        self.decode_interlocks(iib_itlks, list_fap_4p_iib_interlocks)
                        
                    iib_alarms = self.read_bsmp_variable(73 + j*16,'uint32_t')
                    print("IIB " + str(j+1) + " Alarms: " + str(iib_alarms))
                    if(iib_alarms):
                        self.decode_interlocks(iib_alarms, list_fap_4p_iib_alarms)
        
                print("\n Mean Load Current: " + str(self.read_bsmp_variable(33,'float')) + " A")
                print("Load Current 1: " + str(self.read_bsmp_variable(34,'float')) + " A")
                print("Load Current 2: " + str(self.read_bsmp_variable(35,'float')) + " A")
                
                print("Load Voltage: " + str(self.read_bsmp_variable(36,'float')) + " V")
                
                print("\nIGBT 1 Current Mod 1: " + str(self.read_bsmp_variable(37,'float')) + " A")
                print("IGBT 2 Current Mod 1: " + str(self.read_bsmp_variable(38,'float')) + " A")
                print("IGBT 1 Current Mod 2: " + str(self.read_bsmp_variable(39,'float')) + " A")
                print("IGBT 2 Current Mod 2: " + str(self.read_bsmp_variable(40,'float')) + " A")
                print("IGBT 1 Current Mod 3: " + str(self.read_bsmp_variable(41,'float')) + " A")
                print("IGBT 2 Current Mod 3: " + str(self.read_bsmp_variable(42,'float')) + " A")
                print("IGBT 1 Current Mod 4: " + str(self.read_bsmp_variable(43,'float')) + " A")
                print("IGBT 2 Current Mod 4: " + str(self.read_bsmp_variable(44,'float')) + " A")
                
                print("\nDC-Link Voltage Mod 1: " + str(self.read_bsmp_variable(45,'float')) + " V")
                print("DC-Link Voltage Mod 2: " + str(self.read_bsmp_variable(46,'float')) + " V")
                print("DC-Link Voltage Mod 3: " + str(self.read_bsmp_variable(47,'float')) + " V")
                print("DC-Link Voltage Mod 4: " + str(self.read_bsmp_variable(48,'float')) + " V")

                print("\nMean Duty-Cycle: " + str(self.read_bsmp_variable(49,'float')) + " %")
                print("IGBT 1 Duty-Cycle Mod 1: " + str(self.read_bsmp_variable(50,'float')) + " %")
                print("IGBT 2 Duty-Cycle Mod 1: " + str(self.read_bsmp_variable(51,'float')) + " %")
                print("IGBT 1 Duty-Cycle Mod 2: " + str(self.read_bsmp_variable(52,'float')) + " %")
                print("IGBT 2 Duty-Cycle Mod 2: " + str(self.read_bsmp_variable(53,'float')) + " %")
                print("IGBT 1 Duty-Cycle Mod 3: " + str(self.read_bsmp_variable(54,'float')) + " %")
                print("IGBT 2 Duty-Cycle Mod 3: " + str(self.read_bsmp_variable(55,'float')) + " %")
                print("IGBT 1 Duty-Cycle Mod 4: " + str(self.read_bsmp_variable(56,'float')) + " %")
                print("IGBT 2 Duty-Cycle Mod 4: " + str(self.read_bsmp_variable(57,'float')) + " %")
                
                if not iib == 0:
                    print("\nIIB " + str(iib) + " Input Voltage: " + str(self.read_bsmp_variable(58 + iib_offset,'float')) + " V")
                    print("IIB " + str(iib) + " Output Voltage: " + str(self.read_bsmp_variable(59 + iib_offset,'float')) + " V")
                    print("IIB " + str(iib) + " IGBT 1 Current: " + str(self.read_bsmp_variable(60 + iib_offset,'float')) + " A")
                    print("IIB " + str(iib) + " IGBT 2 Current: " + str(self.read_bsmp_variable(61 + iib_offset,'float')) + " A")
                    print("IIB " + str(iib) + " IGBT 1 Temp: " + str(self.read_bsmp_variable(62 + iib_offset,'float')) + " ºC")
                    print("IIB " + str(iib) + " IGBT 2 Temp: " + str(self.read_bsmp_variable(63 + iib_offset,'float')) + " ºC")
                    print("IIB " + str(iib) + " Driver Voltage: " + str(self.read_bsmp_variable(64 + iib_offset,'float')) + " V")
                    print("IIB " + str(iib) + " Driver Current 1: " + str(self.read_bsmp_variable(65 + iib_offset,'float')) + " A")
                    print("IIB " + str(iib) + " Driver Current 2: " + str(self.read_bsmp_variable(66 + iib_offset,'float')) + " A")
                    print("IIB " + str(iib) + " Inductor Temp: " + str(self.read_bsmp_variable(67 + iib_offset,'float')) + " ºC")
                    print("IIB " + str(iib) + " Heat-Sink Temp: " + str(self.read_bsmp_variable(68 + iib_offset,'float')) + " ºC")
                    print("IIB " + str(iib) + " Ground Leakage Current: " + str(self.read_bsmp_variable(69 + iib_offset,'float')) + " A")
                    print("IIB " + str(iib) + " Board Temp: " + str(self.read_bsmp_variable(70 + iib_offset,'float')) + " ºC")
                    print("IIB " + str(iib) + " Board RH: " + str(self.read_bsmp_variable(71 + iib_offset,'float')) + " %")
                    print("IIB " + str(iib) + " Interlocks: " + str(self.read_bsmp_variable(72 + iib_offset,'uint32_t')))
                    print("IIB " + str(iib) + " Alarms: " + str(self.read_bsmp_variable(73 + iib_offset,'uint32_t')))

                time.sleep(dt)
                
            self.SetSlaveAdd(old_add)
            
        except Exception as e: 
            print(e)
            self.SetSlaveAdd(old_add)
            
    def read_vars_fap_2p2s(self, n = 1, com_add = 1, dt = 0.5, iib = 0):
    
        old_add = self.GetSlaveAdd()
        iib_offset = 16*(iib-1)
        
        try:
            for i in range(n):
            
                self.SetSlaveAdd(com_add)
            
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                self.read_vars_common()
    
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fap_2p2s_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fap_2p2s_hard_interlocks)
                    
                for j in range(4):
                    iib_itlks = self.read_bsmp_variable(78 + j*16,'uint32_t')
                    print("\nIIB " + str(j+1) + " Interlocks: " + str(iib_itlks))
                    if(iib_itlks):
                        self.decode_interlocks(iib_itlks, list_fap_4p_iib_interlocks)
                        
                    iib_alarms = self.read_bsmp_variable(79 + j*16,'uint32_t')
                    print("IIB " + str(j+1) + " Alarms: " + str(iib_alarms))
                    if(iib_alarms):
                        self.decode_interlocks(iib_alarms, list_fap_4p_iib_alarms)
        
                print("\nMean Load Current: " + str(self.read_bsmp_variable(33,'float')) + " A")
                print("Load Current 1: " + str(self.read_bsmp_variable(34,'float')) + " A")
                print("Load Current 2: " + str(self.read_bsmp_variable(35,'float')) + " A")
                
                print("\nArm Current 1: " + str(self.read_bsmp_variable(36,'float')) + " A")
                print("Arm Current 2: " + str(self.read_bsmp_variable(37,'float')) + " A")
                
                print("\nIGBT 1 Current Mod 1: " + str(self.read_bsmp_variable(38,'float')) + " A")
                print("IGBT 2 Current Mod 1: " + str(self.read_bsmp_variable(39,'float')) + " A")
                print("IGBT 1 Current Mod 2: " + str(self.read_bsmp_variable(40,'float')) + " A")
                print("IGBT 2 Current Mod 2: " + str(self.read_bsmp_variable(41,'float')) + " A")
                print("IGBT 1 Current Mod 3: " + str(self.read_bsmp_variable(42,'float')) + " A")
                print("IGBT 2 Current Mod 3: " + str(self.read_bsmp_variable(43,'float')) + " A")
                print("IGBT 1 Current Mod 4: " + str(self.read_bsmp_variable(44,'float')) + " A")
                print("IGBT 2 Current Mod 4: " + str(self.read_bsmp_variable(45,'float')) + " A")
                
                print("\nDC-Link Voltage Mod 1: " + str(self.read_bsmp_variable(50,'float')) + " V")
                print("DC-Link Voltage Mod 2: " + str(self.read_bsmp_variable(51,'float')) + " V")
                print("DC-Link Voltage Mod 3: " + str(self.read_bsmp_variable(52,'float')) + " V")
                print("DC-Link Voltage Mod 4: " + str(self.read_bsmp_variable(53,'float')) + " V")

                print("\nMean Duty-Cycle: " + str(self.read_bsmp_variable(54,'float')) + " %")
                print("Differential Duty-Cycle: " + str(self.read_bsmp_variable(55,'float')) + " %")
                print("\nIGBT 1 Duty-Cycle Mod 1: " + str(self.read_bsmp_variable(56,'float')) + " %")
                print("IGBT 2 Duty-Cycle Mod 1: " + str(self.read_bsmp_variable(57,'float')) + " %")
                print("IGBT 1 Duty-Cycle Mod 2: " + str(self.read_bsmp_variable(58,'float')) + " %")
                print("IGBT 2 Duty-Cycle Mod 2: " + str(self.read_bsmp_variable(59,'float')) + " %")
                print("IGBT 1 Duty-Cycle Mod 3: " + str(self.read_bsmp_variable(60,'float')) + " %")
                print("IGBT 2 Duty-Cycle Mod 3: " + str(self.read_bsmp_variable(61,'float')) + " %")
                print("IGBT 1 Duty-Cycle Mod 4: " + str(self.read_bsmp_variable(62,'float')) + " %")
                print("IGBT 2 Duty-Cycle Mod 4: " + str(self.read_bsmp_variable(63,'float')) + " %")
                
                if not iib == 0:
                    print("\nIIB " + str(iib) + " Input Voltage: " + str(self.read_bsmp_variable(64 + iib_offset,'float')) + " V")
                    print("IIB " + str(iib) + " Output Voltage: " + str(self.read_bsmp_variable(65 + iib_offset,'float')) + " V")
                    print("IIB " + str(iib) + " IGBT 1 Current: " + str(self.read_bsmp_variable(66 + iib_offset,'float')) + " A")
                    print("IIB " + str(iib) + " IGBT 2 Current: " + str(self.read_bsmp_variable(67 + iib_offset,'float')) + " A")
                    print("IIB " + str(iib) + " IGBT 1 Temp: " + str(self.read_bsmp_variable(68 + iib_offset,'float')) + " ºC")
                    print("IIB " + str(iib) + " IGBT 2 Temp: " + str(self.read_bsmp_variable(69 + iib_offset,'float')) + " ºC")
                    print("IIB " + str(iib) + " Driver Voltage: " + str(self.read_bsmp_variable(70 + iib_offset,'float')) + " V")
                    print("IIB " + str(iib) + " Driver Current 1: " + str(self.read_bsmp_variable(71 + iib_offset,'float')) + " A")
                    print("IIB " + str(iib) + " Driver Current 2: " + str(self.read_bsmp_variable(72 + iib_offset,'float')) + " A")
                    print("IIB " + str(iib) + " Inductor Temp: " + str(self.read_bsmp_variable(73 + iib_offset,'float')) + " ºC")
                    print("IIB " + str(iib) + " Heat-Sink Temp: " + str(self.read_bsmp_variable(74 + iib_offset,'float')) + " ºC")
                    print("IIB " + str(iib) + " Ground Leakage Current: " + str(self.read_bsmp_variable(75 + iib_offset,'float')) + " A")
                    print("IIB " + str(iib) + " Board Temp: " + str(self.read_bsmp_variable(76 + iib_offset,'float')) + " ºC")
                    print("IIB " + str(iib) + " Board RH: " + str(self.read_bsmp_variable(77 + iib_offset,'float')) + " %")
                    print("IIB " + str(iib) + " Interlocks: " + str(self.read_bsmp_variable(78 + iib_offset,'uint32_t')))
                    print("IIB " + str(iib) + " Alarms: " + str(self.read_bsmp_variable(79 + iib_offset,'uint32_t')))
                    
                time.sleep(dt)
                
            self.SetSlaveAdd(old_add)
            
        except Exception as e: 
            print(e)
            self.SetSlaveAdd(old_add)       
     
    def read_vars_fap_225A(self, n = 1, com_add = 1, dt = 0.5):
    
        old_add = self.GetSlaveAdd()
        
        try:
            for i in range(n):
            
                self.SetSlaveAdd(com_add)
            
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                self.read_vars_common()
    
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fap_225A_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fap_225A_hard_interlocks)
        
                print("\nLoad Current: " + str(self.read_bsmp_variable(33,'float')) + " A")
                print("\nIGBT 1 Current: " + str(self.read_bsmp_variable(34,'float')) + " A")
                print("IGBT 2 Current: " + str(self.read_bsmp_variable(35,'float')) + " A")
                print("\nIGBT 1 Duty-Cycle: " + str(self.read_bsmp_variable(36,'float')) + " %")
                print("IGBT 2 Duty-Cycle: " + str(self.read_bsmp_variable(37,'float')) + " %")
                print("Differential Duty-Cycle: " + str(self.read_bsmp_variable(38,'float')) + " %")
                
                time.sleep(dt)
                
            self.SetSlaveAdd(old_add)
        except:
            self.SetSlaveAdd(old_add)
            
    def read_vars_fbp_2s_ufjf(self, n = 1, com_add = 1, dt = 0.5):
    
        old_add = self.GetSlaveAdd()
        
        try:
            for i in range(n):
            
                self.SetSlaveAdd(com_add)
            
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                self.read_vars_common()
    
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fbp_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fbp_hard_interlocks)
        
                print("\nLoad Current: " + str(self.read_bsmp_variable(33,'float')) + " A")
                print("Load Error: " + str(self.read_bsmp_variable(34,'float')) + " A")
                
                print("\nMod 1 Load Voltage: " + str(self.read_bsmp_variable(36,'float')) + " V")
                print("Mod 3 Load Voltage: " + str(self.read_bsmp_variable(40,'float')) + " V")
                
                #print("\nMod 1 DC-Link Voltage: " + str(self.read_bsmp_variable(29,'float')) + " V")
                #print("Mod 1 Temperature: " + str(self.read_bsmp_variable(31,'float')) + " ºC")
                
                #print("\nMod 3 DC-Link Voltage: " + str(self.read_bsmp_variable(33,'float')) + " V")
                #print("Mod 3 Temperature: " + str(self.read_bsmp_variable(35,'float')) + " ºC")
                
                print("\nMod 1 Duty-Cycle: " + str(self.read_bsmp_variable(32,'float')) + " %")
                print("Mod 3 Duty-Cycle: " + str(self.read_bsmp_variable(36,'float')) + " %")
                              
                time.sleep(dt)
                
            self.SetSlaveAdd(old_add)
        except:
            self.SetSlaveAdd(old_add)
            
    def read_vars_fac_2p_acdc_imas(self, n = 1, add_mod_a = 2, dt = 0.5, iib = 0):
    
        old_add = self.GetSlaveAdd()
        
        try:
            for i in range(n):
            
                self.SetSlaveAdd(add_mod_a)
            
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                self.read_vars_common()
    
                print('\n *** MODULE A ***')
    
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fac_2p_acdc_imas_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fac_2p_acdc_imas_hard_interlocks)
                
                print("\nCapBank Voltage: " + str(self.read_bsmp_variable(33,'float')) + " V")
                print("Rectifier Current: " + str(self.read_bsmp_variable(34,'float')) + " A")
                print("Duty-Cycle: " + str(self.read_bsmp_variable(35,'float')) + " %")
                        
                self.SetSlaveAdd(add_mod_a+1)
                
                print('\n *** MODULE B ***')
                
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fac_2p_acdc_imas_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fac_2p_acdc_imas_hard_interlocks)
        
                print("\nCapBank Voltage: " + str(self.read_bsmp_variable(33,'float')) + " V")
                print("Rectifier Current: " + str(self.read_bsmp_variable(34,'float')) + " A")
                print("Duty-Cycle: " + str(self.read_bsmp_variable(35,'float')) + " %")
                        
                time.sleep(dt)
                
            self.SetSlaveAdd(old_add)
        except:
            self.SetSlaveAdd(old_add)            
            raise
            
    def read_vars_fac_2p_dcdc_imas(self, n = 1, com_add = 1, dt = 0.5, iib = 0):
    
        old_add = self.GetSlaveAdd()
        
        try:
            for i in range(n):
    
                self.SetSlaveAdd(com_add)
            
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                
                self.read_vars_common()
                
                print("\nSync Pulse Counter: " + str(self.read_bsmp_variable(5,'uint32_t')))
                                
                soft_itlks = self.read_bsmp_variable(31,'uint32_t')
                print("\nSoft Interlocks: " + str(soft_itlks))
                if(soft_itlks):
                    self.decode_interlocks(soft_itlks, list_fac_2p_dcdc_imas_soft_interlocks)
                    print('')
                
                hard_itlks = self.read_bsmp_variable(32,'uint32_t')
                print("Hard Interlocks: " + str(hard_itlks))
                if(hard_itlks):
                    self.decode_interlocks(hard_itlks, list_fac_2p_dcdc_imas_hard_interlocks)
                
                print("\nLoad Current: " + str(self.read_bsmp_variable(33,'float')) + ' A')
                print("Load Current Error: " + str(self.read_bsmp_variable(34,'float')) + ' A')
                
                print("\nArm 1 Current: " + str(self.read_bsmp_variable(35,'float')) + ' A')
                print("Arm 2 Current: " + str(self.read_bsmp_variable(36,'float')) + ' A')
                print("Arms Current Diff: " + str(self.read_bsmp_variable(37,'float')) + ' A')
                
                print("\nCapBank Voltage 1: " + str(self.read_bsmp_variable(38,'float')) + ' V')
                print("CapBank Voltage 2: " + str(self.read_bsmp_variable(39,'float')) + ' V')
                
                print("\nDuty-Cycle 1: " + str(self.read_bsmp_variable(40,'float')) + ' %')
                print("Duty-Cycle 2: " + str(self.read_bsmp_variable(41,'float')) + ' %')
                print("Differential Duty-Cycle: " + str(self.read_bsmp_variable(42,'float')) + ' %')

                time.sleep(dt)
                
            self.SetSlaveAdd(old_add)
        except:
            self.SetSlaveAdd(old_add)            
            raise
            
    def check_param_bank(self, param_file):
        fbp_param_list = []
        
        max_sampling_freq = 600000
        c28_sysclk = 150e6
        
        with open(param_file,newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                fbp_param_list.append(row)

        for param in fbp_param_list:
            if str(param[0]) == 'Num_PS_Modules' and param[1] > 4:
                print("Invalid " + str(param[0]) + ": " + str(param[1]) + ". Maximum is 4")
                
            elif str(param[0]) == 'Freq_ISR_Controller' and param[1] > 6000000:
                print("Invalid " + str(param[0]) + ": " + str(param[1]) + ". Maximum is 4" )
                
            else:
                for n in range(64):
                    try:
                        print(str(param[0]) + "["+ str(n) + "]: " + str(param[n+1]))
                        print(self.set_param(str(param[0]),n,float(param[n+1])))
                    except:
                        break
                        
    def set_param_bank(self, param_file):
        fbp_param_list = []
        with open(param_file,newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                fbp_param_list.append(row)

        for param in fbp_param_list:
            if str(param[0]) == 'PS_Name':
                print(str(param[0]) + "[0]: " + str(param[1]))
                print(self.set_ps_name(str(param[1])))
            else:
                for n in range(64):
                    try:
                        print(str(param[0]) + "["+ str(n) + "]: " + str(param[n+1]))
                        print(self.set_param(str(param[0]),n,float(param[n+1])))
                    except:
                        break
        #self.save_param_bank()
        
    def get_default_ramp_waveform(self, interval=500, nrpts=4000, ti=None, fi=None, forms=None):
        from siriuspy.magnet.util import get_default_ramp_waveform
        return get_default_ramp_waveform(interval, nrpts, ti, fi, forms)
    
    def save_ramp_waveform(self, ramp):
        filename = input('Digite o nome do arquivo: ')
        with open( filename + '.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(ramp)
            
    def save_ramp_waveform_col(self, ramp):
        filename = input('Digite o nome do arquivo: ')
        with open( filename + '.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for val in ramp:
                writer.writerow([val])
    
    def read_vars_fac_n(self, n = 1, dt = 0.5):
        old_add = self.GetSlaveAdd()
        try:
            for i in range(n):
                print('\n--- Measurement #' + str(i+1) + ' ------------------------------------------\n')
                self.SetSlaveAdd(1)
                self.read_vars_fac_dcdc()
                print('\n-----------------------\n')
                self.SetSlaveAdd(2)
                self.read_vars_fac_acdc()
                time.sleep(dt)
            self.SetSlaveAdd(old_add)
        except:
            self.SetSlaveAdd(old_add)
            
    def get_step_buffer_fbp_ufjf(self, net1, net2, i_0, i_f, dly):
        self.set_param('Analog_Var_Max',4,net1)
        self.set_param('Analog_Var_Max',5,net2)
        self.set_slowref(i_0)
        time.sleep(0.5)
        self.enable_buf_samples()
        time.sleep(dly)
        self.set_slowref(i_f)
        self.disable_buf_samples()
        buf = self.read_buf_samples_ctom()
        buf1 = buf[0:4096:2]
        buf2 = buf[1:4096:2]
        fig = plt.figure()
        ax1 = fig.add_subplot(2,1,1)
        ax2 = fig.add_subplot(2,1,2)
        ax1.plot(buf1)
        ax1.grid()
        ax2.plot(buf2)
        ax2.grid()
        fig.show()
        return [buf1,buf2]
    
    def set_buf_samples_freq(self, fs):
        self.set_param('Freq_TimeSlicer',1,fs)
        self.save_param_eeprom('Freq_TimeSlicer',1)
        self.reset_udc()
                                
    def calc_pi(self, r_load, l_load, f_bw, v_dclink, send_drs = 0, dsp_id = 0):
        kp = 2*3.1415*f_bw*l_load/v_dclink
        ki = kp*r_load/l_load
        print('\n  Kp = ' + str(kp))
        print('  Ki = ' + str(ki) + '\n')
        if send_drs:
            self.set_dsp_coeffs(3,dsp_id,[kp,ki,0.95,-0.95])
        return [kp,ki]
        
    def config_dsp_modules_drs_fap_tests(self):
        kp_load = 0
        ki_load = 20.95
        kp_share = 0.000032117
        ki_share = 0.0012
        
        drs.set_dsp_coeffs(3,0,[kp_load,ki_load,0.6,0])
        drs.set_dsp_coeffs(3,1,[kp_share,ki_share,0.0015,-0.0015])
        drs.save_dsp_modules_eeprom()

    def set_prbs_sampling_freq(self,freq, type_memory):
        self.set_param('Freq_TimeSlicer',0,freq)
        self.set_param('Freq_TimeSlicer',1,freq)
        self.save_param_bank(type_memory)

    def get_dsp_modules_bank(self, list_dsp_classes = [1,2,3,4,5,6], print_modules = 1):
        dsp_modules_bank = []
        for dsp_class in list_dsp_classes:
            for dsp_id in range(num_dsp_modules[dsp_class]):
                dsp_module = [dsp_classes_names[dsp_class], dsp_class, dsp_id]
                for dsp_coeff in range(num_coeffs_dsp_modules[dsp_class]):
                    try:
                        coeff = self.get_dsp_coeff(dsp_class,dsp_id,dsp_coeff)
                        if dsp_class == 3 and dsp_coeff == 1:
                            coeff *= self.get_param('Freq_ISR_Controller',0)
                        dsp_module.append(coeff)
                    except:
                        dsp_module.append('nan')
                dsp_modules_bank.append(dsp_module)
                if(print_modules):
                    print(dsp_module)
        
        return dsp_modules_bank
        
    def store_dsp_modules_bank_csv(self, bank):
        filename = input('Digite o nome do arquivo: ')
        with open( filename + '.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            for dsp_module in bank:
                writer.writerow(dsp_module)
                
    def set_dsp_modules_bank(self, dsp_modules_file, save_eeprom = 0):
        dsp_modules_row = []
        with open(dsp_modules_file,newline='') as f:
            reader = csv.reader(f)
            
            for dsp_module in reader:
                if not dsp_module == []:
                    if not dsp_module[0][0] == '#':
                        list_coeffs = []
                        
                        for coeff in dsp_module[3:3+num_coeffs_dsp_modules[int(dsp_module[1])]]:
                            list_coeffs.append(float(coeff))
                            
                        print(str(int(dsp_module[1])) + ' ' + str(int(dsp_module[2])) + ' ' + str(list_coeffs))
                        self.set_dsp_coeffs(int(dsp_module[1]),int(dsp_module[2]),list_coeffs)
        
        if(save_eeprom):
            self.save_dsp_modules_eeprom()
        else:
            print('\n *** Aviso: Os coeficientes configurados não foram salvos na memória EEPROM. Caso deseje salvar, utilize o argumento save_eeprom = 1')
       
    def set_param_bank(self, param_file):
        fbp_param_list = []
        with open(param_file,newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                fbp_param_list.append(row)

        for param in fbp_param_list:
            if str(param[0]) == 'PS_Name':
                print(str(param[0]) + "[0]: " + str(param[1]))
                print(self.set_ps_name(str(param[1])))
            else:
                for n in range(64):
                    try:
                        print(str(param[0]) + "["+ str(n) + "]: " + str(param[n+1]))
                        print(self.set_param(str(param[0]),n,float(param[n+1])))
                    except:
                        break
        #self.save_param_bank()

    def select_param_bank(self, cfg_dsp_modules = 0):

        add = int(input('\n Digite o endereco serial atual do controlador a ser configurado: '))
        
        oldadd = self.GetSlaveAdd()
        self.SetSlaveAdd(add)
            
        areas = ['IA','LA','PA']
        ps_models = ['fbp','fbp_dclink','fap','fap_4p','fap_2p4s','fac','fac_2s']
        ps_folders = ['fbp','fbp_dclink','fap','fap',]
        la_fap = ['TB-Fam:PS-B','TS-01:PS-QF1A','TS-01:PS-QF1B','TS-02:PS-QD2',
                  'TS-02:PS-QF2','TS-03:PS-QF3','TS-04:PS-QD4A','TS-04:PS-QD4B',
                  'TS-04:PS-QF4']
        
        print('\n Selecione area: \n')
        print('   0: Sala de racks')
        print('   1: Linhas de transporte')
        print('   2: Sala de fontes\n')
        area = int(input(' Digite o numero correspondente: '))
        
        if area == 0:
            sector = input('\n Digite o setor da sala de racks [1 a 20]: ')
            
            if int(sector) < 10:
                sector = '0' + sector
            
            rack = input('\n Escolha o rack em que a fonte se encontra [1/2/3]: ')
            
            #if (rack != '1') and (rack != '2'):
            if not ((rack == '1') or (rack == '2') or (sector == '09' and rack == '3')):
                print(' \n *** RACK INEXISTENTE ***\n')
                return
                
            print('\n Escolha o tipo de fonte: \n')
            print('   0: FBP')
            print('   1: FBP-DCLink\n')
            ps_model = int(input(' Digite o numero correspondente: '))
            
            if ps_model == 0:
                crate = '_crate_' + input('\n Digite a posicao do bastidor, de cima para baixo. Leve em conta os bastidores que ainda nao foram instalados : ')
                
            elif ps_model == 1:
                crate = ''
            
            else:
                print(' \n *** TIPO DE FONTE INEXISTENTE ***\n')
                return
            
            file_dir = '../ps_parameters/IA-' + sector + '/' + ps_models[ps_model] + '/'
            
            file_name = 'parameters_' + ps_models[ps_model] + '_IA-' + sector + 'RaPS0' + rack + crate + '.csv'
            
            file_path = file_dir + file_name
            
            print('\n Banco de parametros a ser utilizado: ' + file_path)
            
        elif area == 1:
            
            print('\n Escolha o tipo de fonte: \n')
            print('   0: FBP')
            print('   1: FBP-DCLink')
            print('   2: FAP\n')
            
            ps_model = int(input(' Digite o numero correspondente: '))
            
            if ps_model == 0 or ps_model == 1:
            
                crate = input('\n Digite a posicao do bastidor, de cima para baixo. Leve em conta os bastidores que ainda nao foram instalados : ')
                ps_name = '_LA-RaPS06_crate_' + crate
                
                file_dir = '../ps_parameters/LA/' + ps_models[ps_model] + '/'
                file_name = 'parameters_' + ps_models[ps_model] + ps_name + '.csv'
                file_path = file_dir + file_name
            
            elif ps_model == 2:
            
                ps_list = []
                
                file_dir = '../ps_parameters/LA/fap/'
                for entry in os.listdir(file_dir):
                    if os.path.isfile(os.path.join(file_dir, entry)):
                        ps_list.append(entry)

                print('\n ### Lista de fontes FAP da linha de transporte ### \n')
                
                for idx, ps in enumerate(ps_list):
                    print('   ' + str(idx) + ': ' + ps)

                ps_idx = int(input('\n Escolha o índice da fonte correspondente: '))            
            
                file_path = file_dir + ps_list[ps_idx]      
            
            else:
                print(' \n *** TIPO DE FONTE INEXISTENTE ***\n')
                return
                
            print('\n Banco de parametros a ser utilizado: ' + file_path)
        
        elif area == 2:
            print('\n Escolha o tipo de fonte: \n')
            print('   0: FAC')
            print('   1: FAP\n')
            
            ps_model = int(input(' Digite o numero correspondente: '))
            
            if ps_model == 0:
            
                ps_list = []
                
                file_dir = '../ps_parameters/PA/fac/'
                for entry in os.listdir(file_dir):
                    if os.path.isfile(os.path.join(file_dir, entry)):
                        ps_list.append(entry)

                print('\n ### Lista de bastidores de controle FAC da sala de fontes ### \n')
                
                for idx, ps in enumerate(ps_list):
                    print(' ', idx, ': ', ps)

                ps_idx = int(input('\n Escolha o índice da fonte correspondente: '))            
            
                file_path = file_dir + ps_list[ps_idx]     
                
            elif ps_model == 1:
            
                ps_list = []
                
                file_dir = '../ps_parameters/PA/fap/'
                for entry in os.listdir(file_dir):
                    if os.path.isfile(os.path.join(file_dir, entry)):
                        ps_list.append(entry)

                print('\n ### Lista de bastidores de controle FAP da sala de fontes ### \n')
                
                for idx, ps in enumerate(ps_list):
                    print(' ', idx, ': ', ps)

                ps_idx = int(input('\n Escolha o índice da fonte correspondente: '))            
            
                file_path = file_dir + ps_list[ps_idx]  
                
            else:
                print(' \n *** TIPO DE FONTE INEXISTENTE ***\n')
                return
                
            print('\n Banco de parametros a ser utilizado: ' + file_path)
            
        else:
            print(' \n *** SALA INEXISTENTE ***\n')
            return
            
        r = input('\n Tem certeza que deseja prosseguir? [Y/N]: ')
        
        if (r != 'Y') and (r != 'y'):
            print(' \n *** OPERAÇÃO CANCELADA ***\n')
            return
        self.SetSlaveAdd(add)
        
        if ps_model == 0 and cfg_dsp_modules == 1:
            print('\n Enviando parametros de controle para controlador ...')
            
            dsp_file_dir = '../dsp_parameters/IA-' + sector + '/' + ps_models[ps_model] + '/'
            
            dsp_file_name = 'dsp_parameters_' + ps_models[ps_model] + '_IA-' + sector + 'RaPS0' + rack + crate + '.csv'
            
            dsp_file_path = dsp_file_dir + dsp_file_name
            
            self.set_dsp_modules_bank(dsp_file_path)
            
            print('\n Gravando parametros de controle na memoria ...')
            time.sleep(1)
            self.save_dsp_modules_eeprom()
            
        print('\n Enviando parametros de operacao para controlador ...\n')
        time.sleep(1)
        self.set_param_bank(file_path)
        print('\n Gravando parametros de operacao na memoria EEPROM onboard ...')
        self.save_param_bank(2)
        time.sleep(5)
        

        print('\n Resetando UDC ...')
        self.reset_udc()
        time.sleep(2)
        
        print('\n Pronto! Não se esqueça de utilizar o novo endereço serial para se comunicar com esta fonte! :)\n')
        
        self.SetSlaveAdd(oldadd)

    def get_siggen_vars(self):
        print('\n### SigGen Variables ###\n')
        print('Enable: ' + str((self.read_bsmp_variable(6,'uint16_t'))))
        print('Type: ' + ListSigGenTypes_v2_1[int(self.read_bsmp_variable(7,'uint16_t'))])
        print('Num Cycles: ' + str(self.read_bsmp_variable(8,'uint16_t')))
        print('Index: ' + str(self.read_bsmp_variable(9,'float')))
        print('Frequency: ' + str(self.read_bsmp_variable(10,'float')))
        print('Amplitude: ' + str(self.read_bsmp_variable(11,'float')))
        print('Offset: ' + str(self.read_bsmp_variable(12,'float')))
        
        self.read_var(self.index_to_hex(13))
        reply_msg = self.ser.read(21)
        val = struct.unpack('BBHffffB',reply_msg)
        
        print('Aux Param 0: ' + str(val[3]))
        print('Aux Param 1: ' + str(val[4]))
        print('Aux Param 2: ' + str(val[5]))
        print('Aux Param 3: ' + str(val[6]))

    def firmware_initialization(self):
        print("\n ### Inicialização de firmware ### \n")
        
        print("\n Lendo status...")
        print(self.read_ps_status())
        
        print("\n Lendo versão de firmware...")
        self.read_udc_version()
        
        print("\n Desbloqueando UDC...")
        print(self.unlock_udc(0xFFFF))
        
        print("\n Habilitando EEPROM onboard...")
        self.enable_onboard_eeprom()
        
        print("\n Alterando senha...")
        print(self.set_param('Password',0,0xCAFE))
        print(self.save_param_eeprom('Password',0,2))
        
        print("\n Configurando banco de parâmetros...")
        self.select_param_bank()
        
        print("\n ### Fim da inicialização de firmware ### \n")

    def cfg_hensys_ps_model(self):
    
        list_files = ['fbp_dclink/parameters_fbp_dclink_hensys.csv',
                      'fac/parameters_fac_acdc_hensys.csv',
                      'fac/parameters_fac_dcdc_hensys.csv',
                      'fac/parameters_fac_2s_acdc_hensys.csv',
                      'fac/parameters_fac_2s_dcdc_hensys.csv',
                      'fac/parameters_fac_2p4s_acdc_hensys.csv',
                      'fac/parameters_fac_2p4s_dcdc_hensys.csv',
                      'fap/parameters_fap_hensys.csv',
                      'fap/parameters_fap_2p2s_hensys.csv',
                      'fap/parameters_fap_4p_hensys.csv']
        
        print('\n Desbloqueando UDC ...')
        print(self.unlock_udc(0xCAFE))
        
        print('\n *** Escolha o modelo de fonte a ser configurado ***\n')
        print(' 0: FBP-DClink')
        print(' 1: FAC-ACDC')
        print(' 2: FAC-DCDC')
        print(' 3: FAC-2S-ACDC')
        print(' 4: FAC-2S-DCDC')
        print(' 5: FAC-2P4S-ACDC')
        print(' 6: FAC-2P4S-DCDC')
        print(' 7: FAP')
        print(' 8: FAP-2P2S')
        print(' 9: FAP-4P')
        
        model_idx = int(input('\n Digite o índice correspondente: '))  
        file_path = '../ps_parameters/development/' + list_files[model_idx]
        
        print('\n Banco de parametros a ser utilizado: ' + file_path)
        
        r = input('\n Tem certeza que deseja prosseguir? [Y/N]: ')
        
        if (r != 'Y') and (r != 'y'):
            print(' \n *** OPERAÇÃO CANCELADA ***\n')
            return

        print('\n Enviando parametros de operacao para controlador ...\n')
        time.sleep(1)
        self.set_param_bank(file_path)
        
        print('\n Gravando parametros de operacao na memoria EEPROM onboard ...')
        self.save_param_bank(2)
        time.sleep(5)
        
        print('\n Resetando UDC ...')
        self.reset_udc()
        time.sleep(2)
        
        print('\n Pronto! Nao se esqueca de utilizar o novo endereco serial para se comunicar com esta fonte! :)\n')
        
    def test_bid_board(self, password):
    
        r = input("\n Antes de iniciar, certifique-se que o bastidor foi energizado sem a placa BID.\n Para prosseguir, conecte a placa BID a ser testada e pressione qualquer tecla... ")
        
        print("\n Desbloqueando UDC ...")
        print(self.unlock_udc(password))
        
        print("\n Carregando banco de parametros da memoria onboard ...")
        print(self.load_param_bank(type_memory = 2))
        
        print("\n Banco de parametros da memoria onboard:\n")

        max_param = ListParameters.index('Scope_Source')
        param_bank_onboard = []
        
        for param in ListParameters[0:max_param]:
            val = self.get_param(param,0)
            print(param + ':',val)
            param_bank_onboard.append(val)
        
        print("\n Salvando banco de parametros na memoria offboard ...")
        print(self.save_param_bank(type_memory = 1))
        
        time.sleep(5)
        
        print("\n Resetando UDC ...")
        self.reset_udc()
        
        time.sleep(3)
        
        self.read_ps_status()
        
        print("\n Desbloqueando UDC ...")
        print(self.unlock_udc(password))
        
        print("\n Carregando banco de parametros da memoria offboard ...")
        print(self.load_param_bank(type_memory = 1))
        
        self.read_ps_status()
        
        print("\n Verificando banco de parametros offboard apos reset ... \n")
        try:
            param_bank_offboard = []
        
            for param in ListParameters[0:max_param]:
                val = self.get_param(param,0)
                print(param, val)
                param_bank_offboard.append(val)

            if param_bank_onboard == param_bank_offboard:
                print("\n Placa BID aprovada!\n")
            else:
                print("\n Placa BID reprovada!\n")
                
        except:
            print(" Placa BID reprovada!\n")
            
    def upload_parameters_bid(self, password):
        print("\n Desbloqueando UDC ...")
        print(self.unlock_udc(password))
        
        print("\n Carregando banco de parametros da memoria offboard ...")
        print(self.load_param_bank(type_memory = 1))
        time.sleep(1)
        
        print("\n Salvando banco de parametros na memoria onboard ...")
        print(self.save_param_bank(type_memory = 2))
        time.sleep(5)
        
        print("\n Carregando coeficientes de controle da memoria offboard ...")
        print(self.load_dsp_modules_eeprom(type_memory = 1))
        time.sleep(1)
        
        print("\n Salvando coeficientes de controle na memoria onboard ...\n")
        print(self.save_dsp_modules_eeprom(type_memory = 2))
        
    def download_parameters_bid(self,password):
        print("\n Desbloqueando UDC ...")
        print(self.unlock_udc(password))
        
        print("\n Carregando banco de parametros da memoria onboard ...")
        print(self.load_param_bank(type_memory = 2))
        time.sleep(1)
        
        print("\n Salvando banco de parametros na memoria offboard ...")
        print(self.save_param_bank(type_memory = 1))
        time.sleep(5)
        
        print("\n Carregando coeficientes de controle da memoria onboard ...")
        print(self.load_dsp_modules_eeprom(type_memory = 2))
        time.sleep(1)
        
        print("\n Salvando coeficientes de controle na memoria offboard ...")
        print(self.save_dsp_modules_eeprom(type_memory = 1))
