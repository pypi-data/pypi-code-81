import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

class Bootstrap_CIHT:
    """ Uses bootstrap sampling to create confidence intervals and perform a
    hypothesis test on a single group or the difference between two groups.

    Attributes:
        data (Pandas dataframe): unprocessed user data. Should contain at least
                                 a column with the data to analyze. For
                                 proportions, data should be coded as 0 or 1.
                                 If a two-group comparison, should also have
                                 a column containing group membership labels
        data_col (string): name of column containing the data to be analyzed
        num_vars (int): number of groups (1 or 2)
        null_mean(float): for one-group test, comparison mean or proportion

        group_col (string): name of column with group labels (if two-group
                            comparison)
        group1 (int, bool, string): label of first (control) group
        group2 (int, bool, string): label of second (experiment) group
        samples (int): number of bootstrap samples
        alpha (float): sets size of confidence interval (100*(1-alpha))
        h_sides (int): one- or two-sided hypothesis test & confidence interval
        h1_dir (string): inequality direction for 1-sided alternative hypothesis:
                         'greater' -> experiment parameter > control parameter
                         'less' -> experiment parameter < control parameter
                         None (default) -> 2-sided comparison
        df (Pandas object): dataframe for the data to be evaluated

    """
    def __init__(self, data, data_col, num_vars=1, null_mean=0.0, group_col=None,\
                 group1=None, group2=None, samples=10000, alpha=0.05, h_sides=2,\
                 h1_dir=None):

        self.data = data
        self.num_vars = num_vars
        self.null_mean = null_mean
        self.data_col = data_col
        self.group_col = group_col
        self.group1 = group1
        self.group2 = group2
        self.samples = samples
        self.alpha = alpha
        self.h_sides = h_sides
        self.h1_dir = h1_dir
        self.df = self.fill_data()

    def fill_data(self):
        """ Process user-supplied data into starndardized dataframe

        Args:
            data: user-supplied dataframe

        Returns:
            df: dataframe containing data to be analyzed ("data" column) and
                group membership ("group" column) for two-group comparison

        """
        df = pd.DataFrame()

        # reduce the user's dataframe to just the columns needed
        # data_col is forced to float for division etc. (if 1/0 may be int)
        df['data'] = self.data[self.data_col].astype(float)
        if self.num_vars == 2:
            df['group'] = self.data[self.group_col]
        self.df = df

        return self.df

    def calculate_CI(self, means):
        """ Compute and print 100*(1-alpha) confidence interval(s) for the
            relevant sampling distributions. For a one-group case, this is for
            the mean of the data. For a two-group case, it is for the difference
            in means.

        Args:
            means (np array): bootstrapped means (of data, for single group, or
                              differences for two-group case)
        Returns:
          CI (tuple): upper & lower confidence limits

        """
        CI = ()
        CI_low = 100*self.alpha/float(self.h_sides)
        CI_high = 100.0-CI_low

        # two-sided confidence interval
        if self.h_sides == 2:
            print('2-sided CI limits:', CI_low, CI_high)
            CI = (np.percentile(means, CI_low), \
                  np.percentile(means, CI_high))
        # one-sided confidence interval with h1: mean > null mean
        elif self.h1_dir == 'greater':
        # for a one-sided hypothesis mu1 > mu0, if mu0 < CI_low, reject H0
            print('1-sided lower limit, H1 greater:', CI_low)
            CI = (np.percentile(means, CI_low), math.inf)
        # one-sided confidence interval with h1: mean < null mean
        else:
            print('1-side upper limit, H1 less:', CI_high)
        # for a one-sided hypothesis mu1 < mu0, if mu0 > CI_high, reject H0
            CI = (-math.inf, np.percentile(means, CI_high))

        # print CI
        if self.num_vars == 2:
            print('{:.0f}% {:.0f}-sided CI for differences in means of {}: {}'\
                  .format(100.0*(1.0-self.alpha), self.h_sides, self.data_col, \
                  CI))
        else:
            print('{:.0f}% {:.0f}-sided CI for variable {}: {}'.format(100.0*(1.0-\
                  self.alpha), self.h_sides, self.data_col, CI))
        print('\n')

        return CI

    def plot_hist_CI(self, means, CI, bins=10):
        """ Plot the sampling distribution with confidence intervals as
            vertical red line(s). For single group, also plots the null mean as
            a green vertical line

            Args:
               means (np array): bootstrapped means (of data, for single group, or
                              differences for two-group case)
               CI (tuple): confidence limits
               bins(int): number of bins in the histogram

            Returns:
               None

        """

        plt.hist(x=means, bins=bins)
        if self.num_vars == 2:
            plt.xlabel('Difference in Means of {}'.format(self.data_col))
            plt.title('Sampling Distribution of Difference in Means \n \
Red Bar(s) at {}% CI'.format(100.0*(1.0-self.alpha)))
        else:
            plt.xlabel('Means of: {}'.format(self.data_col))
            plt.title('Sampling Distribution of Mean \n \
Red Bar(s) at {}% CI\n Green Bar at Null Mean'.format(100.0*(1.0-self.alpha)))
            plt.axvline(x=self.null_mean, color = 'green')
        plt.ylabel('Count')
        # one-sided hypothesis
        if self.h_sides == 1:
            if self.h1_dir == 'greater':
                plt.axvline(x=CI[0], color = 'red')
            else:
                plt.axvline(x=CI[1], color = 'red')
        # two-sided Hypothesis
        else:
            plt.axvline(x=CI[0], color = 'red')
            plt.axvline(x=CI[1], color = 'red')

        plt.show();

        return

    def plot_distribs(self, experiment_mean, control_mean, bins=10):
        """ For a two-group comparison, plot the control and experimental
            sampling distributions on a single graph

            Args:
               experiment_mean (np array): bootstrapped samples for experiment group
                                           (or the single group if num_vars=1)
               control_mean (np array): bootstrapped samples for control group
               bins(int): number of bins in the histogram

            Returns:
               None

        """


        plt.hist(control_mean, bins, alpha = 0.5, label=self.group1)
        plt.hist(experiment_mean, bins, alpha = 0.5, label=self.group2)
        plt.legend(loc='upper left', title=self.group_col)
        plt.xlabel('group: {}'.format(self.data_col))
        plt.ylabel('Count')
        plt.title('Sampling Distributions for Mean of {}'.format(self.data_col))
        plt.show();

        return

    def calculate_hypothesis_test(self, means):
        """ Calculate p-value at level alpha for a 1- or 2-side hypothesis test
            comparing the sample mean to the null mean.

            Args:
               means:  numpy array containing either the bootstrapped mean (for a
               single group) or difference in means (for two groups)
               control_mean (np array): bootstrapped samples for control group

            Returns:
               p_value (float): the probablility of the null hypothesis

        """
        # standard deviation of the bootstrapped sample
        sample_stdev = np.std(means)

        # means from original sample for hypothesis testing
        if self.num_vars == 2:
            mean2 = self.df.query('group == @self.group2')['data'].mean()
            mean1 = self.df.query('group == @self.group1')['data'].mean()
            sample_mean =  mean2 - mean1
            print('experimental group: {}; mean: {:.4f}'.format(self.group2, mean2))
            print('control group: {}; mean: {:.4f}'.format(self.group1, mean1))
            print('difference of means, sampling distribution SD: {:.4f}, {:.4f}'.format(\
                  sample_mean, sample_stdev))
        else:
            sample_mean = self.df['data'].mean()
            print('sample mean for {}, sampling distribution SD: {:.4f}, {:.4f}'.format(\
                  self.data_col, sample_mean, sample_stdev))

        # construct a null distribution with the null mean & bootstrap sample SD
        null_dist = np.random.normal(self.null_mean, sample_stdev, 10000)
        # plot the null distribution with the sample mean
        plt.hist(null_dist, bins=20)
        if self.num_vars == 2:
            plt.xlabel('Mean')
        else:
            plt.xlabel('Difference in Means')
        plt.ylabel('Count')
        plt.title('Sampling Distribution under Null Hypothesis \n Line at Sample Mean')
        plt.axvline(x=sample_mean, color = 'red')
        plt.show();

        # calcululate the p-value
        delta = abs(sample_mean-self.null_mean)
        upper_bound = self.null_mean + delta
        lower_bound = self.null_mean - delta
        p_low = (null_dist < lower_bound).mean()
        p_high = (null_dist > upper_bound).mean()

        # one-sided test
        if self.h_sides == 1:
           if self.h1_dir == "greater":
               p_value = p_high
           else:
               p_value = p_low
        # two-sided test
        else:
            p_value = p_low + p_high

        if self.num_vars == 2:
            hyp_0 = 'H0: Difference in means {} vs {} = 0'.format(self.group2, self.group1)
            if self.h_sides == 2:
                hyp_1 = 'H1: Difference in means {} vs {} <> 0'.format(self.group2, self.group1)
            else:
                if self.h1_dir == 'greater':
                    hyp_1 = 'H1: Difference in means {} vs {} > 0'.format(self.group2, self.group1)
                else:
                    hyp_1 = 'H1: Difference in means {} vs {} < 0'.format(self.group2, self.group1)
        else:
            hyp_0 = 'H0: Mean of {} = {:.3f}'.format(self.data_col, self.null_mean)
            if self.h_sides == 2:
                hyp_1 = 'H1: Mean of {} <> {:.3f}'.format(self.data_col, self.null_mean)
            else:
                if self.h1_dir == 'greater':
                    hyp_1 = 'H1: Mean of {} > {:.3f}'.format(self.data_col, self.null_mean)
                else:
                    hyp_1 = 'H1: Mean of {} < {:.3f}'.format(self.data_col, self.null_mean)

        print(hyp_0+'\n'+hyp_1+'\n')
        print('p-value: {:f} \n'.format(p_value))

        return p_value



    def get_bootstrap_sample(self):
        """ Create a sampling distribution with bootstrapping

        Args:
            None

        Returns:
            for one-group comparison:
                experiment_mean (numpy array): bootstrapped means
            for two-group comparison:
                experiment_mean (numpy array): bootstrapped means for
                                               experiment group
                control_mean (numpy array): bootstrapped means for control group
                diffs (numpy array): difference in means from bootstrapped samples

        """

        # for single group, only need to bootstrap one mean
        experiment_mean = np.empty(self.samples, dtype=float)
        size = self.df.shape[0]

        # for two groups, also do control and difference (for plotting)
        if self.num_vars == 2:
            control_mean = np.empty(self.samples, dtype=float)
            diffs = np.empty(self.samples, dtype=float)

        # get the bootstrap samples
        for x in range(self.samples):
            b_samp = self.df.sample(size, replace=True)
            # two-group case
            if self.num_vars == 2:
                control_df = b_samp.query('group == @self.group1')
                experiment_df = b_samp.query('group == @self.group2')
                control_mean[x] = control_df['data'].mean()
                experiment_mean[x] = experiment_df['data'].mean()
                diffs[x] = experiment_mean[x] - control_mean[x]
            # one-group case
            else:
                experiment_mean[x] = b_samp['data'].mean()

        # two-group case
        if self.num_vars == 2:
            return  experiment_mean, control_mean, diffs
        # one-group case
        else:
            return experiment_mean
