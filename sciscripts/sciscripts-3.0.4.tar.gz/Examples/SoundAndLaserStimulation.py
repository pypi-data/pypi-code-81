#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@year: 20210411
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[SoundAndLaserStimulation] Loading dependencies...')
from sciscripts.Exps import SoundAndLaserStimulation
print('[SoundAndLaserStimulation] Done.')


#%% Sound and Laser stimulation

# The Parameters dictionary will contain all the parameters for running the
# experiment. From all of those, only 4 are required:
# 'AnimalName', 'StimType', 'System', and 'Setup'.

# If using 'Sound' in StimType, then all parameters under ## === Sound === ##
# are required.

# If using 'Laser' in StimType, then all parameters under ## === Laser === ##
# are required.

# If using 'SoundLaser' in StimType, then all parameters shown here are
# required.

# Besides the required parameters, you can use this dictionary to record any
# information you want about the experiment, since any variable you add to it
# will be recorded to the InfoFile. As example, here the parameters RecCh,
# StimCh and TTLCh are included to make it easier later in the analysis to
# know what recorded channels contains neural data (RecCh), the played stimulus
# (StimCh) or the stimulation timestamps (TTLCh).

# The StimType parameter can only contain three values: 'Sound', 'Laser',
# and/or 'SoundLaser'. 'Sound' and 'Laser' will allow for sound or laser
# stimulation, respectively. 'SoundLaser' will enable simultaneous sound and
# laser stimulation.

# If using SoundLaser as StimType, keep in mind that since both stimulus will
# be provided simultaneously, some extra requirements must be met:
# - The sound and laser total duration must match (in other words,
#   'SoundPauseBeforePulseDur + SoundPulseDur + SoundPauseAfterPulseDur'
#   must be equal to 'LaserPauseBeforePulseDur + LaserPulseDur +
#   LaserPauseAfterPulseDur');
# - The number of sound and laser pulses must match (SoundPulseNo == LaserPulseNo).

# All durations (parameters ending with Dur) are in seconds.

Parameters = dict(
    ## === General === ##
    AnimalName    = 'Test_01',                           # Animal name
    CageName      = 'A1',                                # Animal label in its cage
    StimType      = ['Sound', 'Laser', 'SoundLaser'],    # Type of stimulation


    ## === Sound === ##
    SoundType                   = 'Noise',               # Type of sound stimulus ('Noise' or 'Tone')
    Intensities                 = [70, 40],              # Stimulus intensities in dB
    NoiseFrequency              = [[5000, 15000]],       # Stimulus frequency ranges in Hz
    SoundPulseNo                = 20,                    # Number of sound pulses
    SoundPauseBeforePulseDur    = 0.004,                 # Duration of pause before each pulse
    SoundPulseDur               = 0.003,                 # Duration of each pulse
    SoundPauseAfterPulseDur     = 0.093,                 # Duration of pause after each pulse
    PauseBetweenIntensities     = 10,                    # Duration of pause between each intensity


    ## === Laser === ##
    LaserType                         = 'Sq',            # Type of laser stimulus ('Sq' or 'Sin')
    LaserPauseBeforePulseDur          = 0,               # Duration of pause before each pulse
    LaserPulseDur                     = 0.01,            # Duration of each pulse
    LaserPauseAfterPulseDur           = 0.09,            # Duration of pause after each pulse
    LaserPulseNo                      = 200,             # Number of laser pulses
    LaserStimBlockNo                  = 5,               # Number of stimulation blocks
    LaserPauseBetweenStimBlocksDur    = 10,              # Duration of pause between each block


    ## === Hardware === ##
    System    = 'Jack-IntelOut-Marantz-IntelIn',         # System name as given during calibration
    Setup     = 'UnitRec',                               # Setup name as given during calibration


    ## === Extra === ###
    RecCh     = list(range(1,17)),
    StimCh    = 17,
    TTLCh     = 18,
)

# By default, the code will not run if there are no calibration files for the
# System and Setup defined above, because without those files SciScript cannot
# know what voltages correspond to the requested sound intensities. If you are
# just testing, or if you are calibrating the intensities of your stimulation
# outside SciScripts, for example at a hardware level, you can bypass this
# safety check by manually providing the voltages to be delivered to the
# speaker through the SoundAmpF parameter. To do so, uncomment the following
# lines.

# import numpy as np
# Parameters['SoundAmpF'] = {
#     '-'.join([str(_) for _ in F]): np.array(Parameters['Intensities'])/max(Parameters['Intensities'])
#     for F in Parameters['NoiseFrequency']
# }


# This will prepare the stimulation objects and create an InfoFile with all
# the experimental information
Stimulation, InfoFile = SoundAndLaserStimulation.Prepare(**Parameters)


#%% Run

# This is where the fun begins :) This function will show you a numbered list
# with the requested frequencies where you can choose which frequency you want
# to play. It will also show a 'Baseline' option and a 'Cancel' option.

SoundAndLaserStimulation.Play(Stimulation, InfoFile, ['Sound'], DV='Out')

# The 'Baseline' option plays nothing, but registers in the InfoFile that a
# baseline recording was taken. This is useful for finding what stimulation
# corresponds to each recording later in the analysis. The 'Cancel' option will
# stop the function.

# The third argument defines what stimulation types you want to run (at least
# one value must be in the Parameters['StimType'] list).
# ['Sound'] will play only sound,
# ['Laser'] will enable only the laser, and
# ['Sound', 'Laser'] will enable both simultaneously.
# You can also add any other value, in case you want to record other
# stimulation details, for example, ['Sound', 'Nicotine'] or ['Sound', 'Saline'].

# You can run this function as many times as necessary for your recordings, as
# it will always use the same InfoFile. One use case is to switch the
# stimulation type from 'Sound' to 'Laser', for example.


#%% Check out the played stimulus

# If you want to plot the stimulus played:
import numpy as np
from sciscripts.Analysis.Plot import Plot

Rate = Stimulation['Stim'].samplerate
Time = np.arange(Stimulation['Sound'].shape[0])/Rate
Ax = {'xlabel': 'Time [s]', 'ylabel': 'Channel #'}
Colors = ['b', 'k']

# Each stimulus is at Stimulation dictionary. For 'Sound' and 'SoundLaser',
# the dimensions are [Samples, Channels, Intensities, Frequencies].
# For 'Laser they are [Samples, Channels].

# This will plot the TTL and sound channels at the first intensity
Ax['title'] = 'Sound'
Plot.AllCh(Stimulation['Sound'][:,:,0,0], Time, Colors, AxArgs=Ax)

# This will plot the Laser channels (which should be only at one channel)
Ax['title'] = 'Laser'
Plot.AllCh(Stimulation['Laser'], Time, Colors, AxArgs=Ax)

# This will plot the sound+laser TTL and sound channels at the first intensity
Ax['title'] = 'Sound+Laser'
Plot.AllCh(Stimulation['SoundLaser'][:,:,0,0], Time, Colors, AxArgs=Ax)
