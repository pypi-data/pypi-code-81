import cv2
from collections import OrderedDict
import numpy as np
import itertools
from datetime import datetime
from configparser import ConfigParser, MissingSectionHeaderError, NoOptionError, NoSectionError
import pandas as pd
import os

INIFILE = r"Z:\DeepLabCut\DLC_extract\Troubleshooting\DLC_two_mice\project_folder\project_config.ini"

dateTime = datetime.now().strftime('%Y%m%d%H%M%S')
config = ConfigParser()
configFile = str(INIFILE)
try:
    config.read(configFile)
except MissingSectionHeaderError:
    print('ERROR:  Not a valid project_config file. Please check the project_config.ini path.')
projectPath = config.get('General settings', 'project_path')
shap_logs_path = os.path.join(projectPath, 'logs', 'shap')
if not os.path.exists(shap_logs_path): os.makedirs(shap_logs_path)

simba_cw = os.getcwd()
simba_feat_cat_dir = os.path.join(simba_cw, 'assets', 'shap', 'feature_categories')
feat_cat_csv_path = os.path.join(simba_feat_cat_dir, 'shap_feature_categories.csv')

colCats = pd.read_csv(feat_cat_csv_path, header=[0, 1])
firstIndices, secondIndices = list(colCats.columns.levels[0]), list(colCats.columns.levels[1])
outputDfcols = secondIndices.copy()
outputDfcols.append('Sum')
outputDfcols.append('Category')
outputDf = pd.DataFrame(columns=outputDfcols)

for topIndex in firstIndices:
    meanList = []
    for botomIndex in secondIndices:
        currDf = colCats.loc[:, list(itertools.product([topIndex], [botomIndex]))]
        currCols = list(currDf. iloc[:, 0])
        currCols = [x for x in currCols if str(x) != 'nan']
        currShaps = shapValuesDf[currCols]
        currShaps["Shap_sum"] = currShaps.sum(axis=1)
        meanList.append(currShaps["Shap_sum"].mean())
    meanList.append(sum(meanList))
    meanList.append(topIndex)
    outputDf.loc[len(outputDf)] = meanList
