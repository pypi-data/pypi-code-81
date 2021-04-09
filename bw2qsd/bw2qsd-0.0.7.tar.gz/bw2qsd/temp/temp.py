#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 14:10:52 2021

@author: Yalin Li
"""




# %%

# from bw2qsd import DataDownloader


# downloader = DataDownloader()
# downloader.download_ecoinvent()
# downloader.download_forwast()


# %%

from bw2qsd import CFgetter

ei = CFgetter('ei')
ei.load_database('ecoinvent_apos371')

ei.load_indicators(add=True, method='TRACI')

ei.load_activities('building', True)


# ei.remove('indicators', (('TRACI', 'environmental impact', 'acidification'),))

path = ''
# path = '/Users/yalinli_cabbi/OneDrive/Coding/BW2QSD/bw2qsd/sample_output.tsv'
df = ei.get_CF(path=path)



# %%

# Only run this at the very end
from bw2qsd import remove_setups_pickle
remove_setups_pickle()
