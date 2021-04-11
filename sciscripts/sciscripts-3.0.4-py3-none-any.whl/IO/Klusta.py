#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 201?????
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

print('[IO.Klusta] Importing dependencies...')
import os
from numpy import log

from sciscripts.Analysis.Analysis import Pairwise
from sciscripts.IO.IO import RunProcess
from sciscripts.IO.Txt import Print
print('[IO.Klusta] Done.')


def PrbWrite(File, Channels=list(range(15,-1,-1)), Spacing=25):
    Prb = {'0': {}}
    Prb['0']['channels'] = Channels
    Prb['0']['graph'] = list(Pairwise(Prb['0']['channels']))
    Pos = list(range(0, len(Prb['0']['channels'])*Spacing, Spacing))
    Prb['0']['geometry'] = {str(Ch):(0,Pos[C]) for C,Ch in enumerate(Prb['0']['channels'])}
    with open(File, 'w') as F: F.write('channel_groups = '+Print(Prb))

    return(None)


def PrmWrite(File, experiment_name, prb_file, raw_data_files, sample_rate,
             n_channels, dtype, spikedetekt={}, klustakwik2={}, DataInfo={}):

    traces = {
        'raw_data_files': raw_data_files,
        'sample_rate': sample_rate,
        'n_channels': n_channels,
        'dtype': dtype,
    }

    sd = dict(
        filter_low = 500.,
        filter_high_factor = 0.95 * .5,  # will be multiplied by the sample rate
        filter_butter_order = 3,

        # Data chunks.
        chunk_size_seconds = 1.,
        chunk_overlap_seconds = .015,

        # Threshold.
        n_excerpts = 50,
        excerpt_size_seconds = 1.,
        use_single_threshold = True,
        threshold_strong_std_factor = 4.5,
        threshold_weak_std_factor = 2.,
        detect_spikes = 'negative',

        # Connected components.
        connected_component_join_size = 1,

        # Spike extractions.
        extract_s_before = int(sample_rate/1000),
        extract_s_after = int(sample_rate/1000),
        weight_power = 2,

        # Features.
        n_features_per_channel = 3,
        pca_n_waveforms_max = 10000,

    )

    kk = dict(
        prior_point = 1,
        mua_point = 2,
        noise_point = 1,
        points_for_cluster_mask = 100,
        penalty_k = 0.0,
        penalty_k_log_n = 1.0,
        max_iterations = 1000,
        num_starting_clusters = 500,
        use_noise_cluster = True,
        use_mua_cluster = True,
        num_changed_threshold = 0.05,
        full_step_every = 1,
        split_first = 20,
        split_every = 40,
        max_possible_clusters = n_channels * 5,
        dist_thresh = log(10000.0),
        max_quick_step_candidates = 100000000, # this uses around 760 MB RAM
        max_quick_step_candidates_fraction = 0.4,
        always_split_bimodal = False,
        subset_break_fraction = 0.01,
        break_fraction = 0.0,
        fast_split = False,
        max_split_iterations = None,
        consider_cluster_deletion = True,
        num_cpus = 8,
    )

    spikedetekt = {**sd, **spikedetekt}
    klustakwik2 = {**kk, **klustakwik2}
    if not klustakwik2['num_cpus']:
        with open('/proc/cpuinfo', 'r') as f: CPUs = f.readlines()
        klustakwik2['num_cpus'] = len([_ for _ in CPUs if 'processor' in _])

    with open(File, 'w') as F:
        F.write('experiment_name = "'+experiment_name+'"')
        F.write('\n\n')
        F.write('prb_file = "'+prb_file+'"')
        F.write('\n\n')
        F.write('traces = '+Print(traces, breaklineat=50))
        F.write('\n\n')
        F.write('spikedetekt = '+Print(spikedetekt))
        F.write('\n\n')
        F.write('klustakwik2 = '+Print(klustakwik2))
        F.write('\n\n')
        F.write('DataInfo = '+Print(DataInfo))
        F.write('\n\n')

    return(None)


def Run(PrmFile, Path, Overwrite=False, Klusta=os.environ['HOME']+'/.local/bin/klusta'):
    Here = os.getcwd(); os.chdir(Path)
    Cmd = [Klusta, PrmFile]
    if Overwrite: Cmd.append('--overwrite')

    print('Entering in directory', Path, '...')
    print('Clustering spikes...')
    ReturnCode = RunProcess(Cmd, PrmFile+'.log'); os.chdir(Here)
    print('Going back to', Here, '...')

    if ReturnCode: print('Error: ReturnCode', ReturnCode)
    else:
        # os.rmdir('.spikedetekt/')
        print('Done clustering.')
    return(None)


def Phy_Run(KwikFile, Path, Phy=s.environ['HOME']+'/.local/bin/phy'):
    Here = os.getcwd(); os.chdir(Path)
    Cmd = [Phy, 'kwik-gui', KwikFile, '--debug']

    print('Entering in directory', Path, '...')
    print('Loading phy...')
    ReturnCode = RunProcess(Cmd, KwikFile+'.log'); os.chdir(Here)
    print('Going back to', Here, '...')

    if ReturnCode: print('Error: ReturnCode', ReturnCode)
    else: print('Done.')
    return(None)

