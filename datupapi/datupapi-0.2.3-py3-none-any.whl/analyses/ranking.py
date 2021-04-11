import math
import numpy as np
import os
import pandas as pd
import re

from datupapi.configure.config import Config


class Ranking(Config):

    def __init__(self, config_file, logfile, log_path, *args, **kwargs):
        Config.__init__(self, config_file=config_file, logfile=logfile)
        self.log_path = log_path


    def rank_abc(self, df, sku_col, rank_col, threshold=[.8, .95]):
        """
        Return a dataframe classifying the SKUs in ABC classes based on the sorting dimension

        :param df: Dataframe consisting of skus and transform column
        :param sku_col: Item column that identify each reference
        :param rank_col: Ranking column to perform the transform based upon, such as sales, volumes costs or margins
        :param threshold: List of thresholds for classification A, B and C. Default [.8, .95]
        :return df_abc: Dataframe including the ABC columns with the transform per item

        >>> df_abc = rank_abc(df, sku_col='Item', rank_col='Volume', threshold=[.8, .95])
        >>> df_abc =
                    Item    Volume     ABC
            idx1     123       345      A
        """
        try:
            df_sum = df.sum()
            df_abc = pd.DataFrame(df_sum, index=df_sum.index, columns=[rank_col]).\
                reset_index().\
                rename(columns={'index': sku_col})
            df_abc = df_abc.sort_values([rank_col], ascending=False).reset_index(drop=True)
            df_abc[rank_col + ' pct'] = round(df_abc[rank_col] / df_abc[rank_col].sum(), 3)
            df_abc[rank_col + ' pct cum'] = round(df_abc[rank_col + ' pct'].cumsum(), 3)
            df_abc[rank_col + ' pct cum inv'] = 1 - df_abc[rank_col + ' pct cum']
            df_abc.loc[df_abc[rank_col + ' pct cum'] <= threshold[0], 'ABC'] = 'A'
            df_abc.loc[(df_abc[rank_col + ' pct cum'] > threshold[0]) &\
                       (df_abc[rank_col + ' pct cum'] <= threshold[1]), 'ABC'] = 'B'
            df_abc.loc[(df_abc[rank_col + ' pct cum'] > threshold[1]), 'ABC'] = 'C'
            df_abc = df_abc.drop([rank_col + ' pct',
                                  rank_col + ' pct cum'], axis='columns')
        except KeyError as err:
            self.logger.exception(f'Invalid column name. Please check dataframe metadata: {err}')
            raise
        return df_abc


    def rank_fsn(self, df, sku_col, rank_col, threshold=[.8, .5]):
        """
        Return a dataframe classifying the SKUs in FSN classes based on the sorting dimension

        :param df: Dataframe consisting of skus and transform column
        :param sku_col: Item column that identify each reference
        :param rank_col: Ranking column to perform the transform based upon, such as sales, volumes costs or margins
        :param threshold: List of thresholds for classification F, S and N. Default [.8, .5]
        :return df_fsn: Dataframe including the FSN columns with the transform per item

        >>> df_fsn = rank_fsn(df, sku_col='Item', rank_col='Volume', threshold=[.8, .5])
        >>> df_fsn =
                    Item    Volume     FSN
            idx1     123       345      F
        """
        try:
            df_nz = round(df.astype(bool).sum()/df.count(), 3)
            df_fsn = pd.DataFrame(df_nz, index=df_nz.index, columns=[rank_col + ' Freq']). \
                reset_index(). \
                rename(columns={'index': sku_col})
            df_fsn.loc[df_fsn[rank_col + ' Freq'] >= threshold[0], 'FSN'] = 'F'
            df_fsn.loc[(df_fsn[rank_col + ' Freq'] < threshold[0]) & \
                       (df_fsn[rank_col + ' Freq'] >= threshold[1]), 'FSN'] = 'S'
            df_fsn.loc[(df_fsn[rank_col + ' Freq'] < threshold[1]), 'FSN'] = 'N'
        except KeyError as err:
            self.logger.exception(f'Invalid column name. Please check dataframe metadata: {err}')
            raise
        return df_fsn


    def rank_xyz(self, df, sku_col, rank_col, threshold=[.25, .75]):
        """
        Return a dataframe classifying the SKUs in XYZ classes based on the sorting dimension

        :param df: Dataframe consisting of skus and transform column
        :param sku_col: Item column that identify each reference
        :param rank_col: Ranking column to perform the transform based upon, such as sales, volumes costs or margins
        :param threshold: List of thresholds for classification X, Y and Z. Default [.25, .75]
        :return df_xyz: Dataframe including the XYZ columns with the transform per item

        >>> df_xyz = rank_xyz(df, sku_col='Item', rank_col='Volume', threshold=[.25, .75])
        >>> df_xyz =
                    Item    Volume     XYZ
            idx1     123       345      X
        """
        try:
            variation_idx = np.power(df.std().values / df.mean().values, 2)
            stability = [0 if math.isnan(e) else round(e, 3) for e in variation_idx]
            df_xyz = pd.DataFrame(data=stability, index=df.columns, columns=[rank_col + ' Stability']). \
                reset_index(). \
                rename(columns={'index': sku_col})
            df_xyz.loc[df_xyz[rank_col + ' Stability'] <= threshold[0], 'XYZ'] = 'X'
            df_xyz.loc[(df_xyz[rank_col + ' Stability'] > threshold[0]) & \
                       (df_xyz[rank_col + ' Stability'] <= threshold[1]), 'XYZ'] = 'Y'
            df_xyz.loc[(df_xyz[rank_col + ' Stability'] > threshold[1]), 'XYZ'] = 'Z'
        except KeyError as err:
            self.logger.exception(f'Invalid column name. Please check dataframe metadata: {err}')
            raise
        return df_xyz


    def concat_ranking(self, df_abc, df_fsn, df_xyz, sku_col):
        """
        Return a dataframe joining the ABC, FSN and XYZ rankings and related columns

        :param df_abc: Dataframe including the ABC columns with the transform per item
        :param df_fsn: Dataframe including the FSN columns with the transform per item
        :param df_xyz: Dataframe including the XYZ columns with the transform per item
        :param sku_col: Item column that identify each reference
        :return df_afx: Dataframe including all three rankings
        """
        try:
            if df_fsn is not None:
                df_afx = pd.merge(df_abc, df_fsn, on=sku_col, how='inner')
            if df_xyz is not None:
                df_afx = pd.merge(df_afx, df_xyz, on=sku_col, how='inner')
            df_afx['Ranking'] = df_afx['ABC'] + df_afx['FSN'] + df_afx['XYZ']
        except KeyError as err:
            self.logger.exception(f'Invalid column name. Please check dataframe metadata: {err}')
            raise
        return df_afx

