#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20180903
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts

Example script for calibrating a sound card. For more information, read
the sciscripts.Exps.SoundMeasurements module documentation.
"""

print('[CalibratingAudioSetup] Loading dependencies...')
from sciscripts.Exps import SoundMeasurements
from sciscripts.Analysis import SoundMeasurements as Analysis
from sciscripts.Analysis.Plot import SoundMeasurements as Plot
print('[CalibratingAudioSetup] Done.')

Parameters = dict(
    ## Calibration parameters
    Freq = 10000,       # Frequency of the wave used to calibrate the sound card
    WaveDur = 10,       # Duration of the test wave
    Repetitions = 4,    # How many repetitions to average the input signal


    ## Measurements parameters
    Setup = 'LTSpeakers',     # Setup name - To be provided on further experiments
    SoundPulseDur = 2,        # Duration of each pulse at each freq and intensity
    NoiseFrequency = [        # Noise frequency bands to be calibrated
        [8000, 10000],
        [9000, 11000],
        [10000, 12000],
        [12000, 14000],
        [14000, 16000],
        [16000, 18000],
        [8000, 18000]
    ],

    # Mic sensitivity, from mic datasheet, in dB re V/Pa or in V/Pa
    MicSens_dB = -47.46,          # If in dB re V/Pa
    # MicSens_VPa = 0.00423643    # If in V/Pa


    ## Audio system
    Rate = 192000,                       # Audio sampling rate
    BlockSize = 384,                     # Audio block size
    System = 'Jack-IntelOut-IntelIn',    # System name - To be provided on further experiments
)


#%% Calibrate the sound card's output and input
SoundMeasurements.RunCalibration(**Parameters)


#%% Calibrate the audio system

# By default, this function will test 300 logaritmically decreasing voltages,
# starting from the maximum voltage known to output 1V at the sound card output
# (see sciscripts.Exps.SoundMeasurements.CalibrateOutput function
# documentation). To override the default, you can manually provide the
# voltages you want to test through the SoundAmpF parameter:

# Parameters['SoundAmpF'] = [1.7, 0.0001, 0.0],

# If overriding, it is important to always test 0V, because it will tell you
# how much acoustic (and electrical) noise you have on your setup, and,
# consequently, what is the lowest intensity you can use for each frequency
# tested.

SoundMeasurements.RunMeasurement(**Parameters)


#%% Evaluate the intensity in dB and the spectrum of each voltage tested at each frequency
Analysis.Run(**Parameters)


#%% Plot the analysis results
Plot.All(Parameters['System'], Parameters['Setup'])

