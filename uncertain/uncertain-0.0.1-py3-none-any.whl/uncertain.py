""" Module to deal with uncertain number calculations

.. module:: uncertain
.. moduleauthor:: Miguel Nu\~no <miguel.nuno@sla.rwth-aachen.de>

"""

import numpy as np
from numpy import inf
from scipy.stats import skew
import matplotlib.pyplot as plt
import itertools as it


class UncertainValue:
    """ This class is used to define uncertain real numbers. Each
        uncertain number is described with a nominal value, upper and lower
        bounds as well as a probability distribution between these bounds.

    Args:
        nominal_value (real): Value you'd assign to your variable if no
            uncertainty would to be considered

    Kwargs:
        lower_bound (num): smallest possible value. Default value is
            nominal_value. If the uncertain number has no lower bound, set this
            variable to -inf.
        upper_bound (num): largest possible value. Default value is nominal
            value. If the uncertain number has no upper bound, set this
            variable to inf.
        prob_distribution (string): probability distribution type f the
            uncertainty. Possible input values are 'normal', 'discrete' and
            'uniform' (default value). Other ossible values are 'constant' (if
            the number is a fixed number with lower_bound = nominal_value =
            upper_bound) and 'custom' (results from doing calculations with
            other types of distribution).
        distribution_param (array): parameters needed to describe the given
            probability distribution type. For the 'normal' distribution type,
            the parameters are '[mean, standard deviation]'. For 'uniform', no
            parameters are needed. For a 'discrete' distribution, the
            parameters are either a list of possible values [val1, val2, ...]
            or a list of lists with possible values and the probability of each
            value [[val1, prob1], [val2, prob2], ...].
        n_samples (int): number of samples to be used for the calculation of
            the probability distribution. Default value is 100 000.
    """

    def __init__(self, nominal_value, lower_bound=None, upper_bound=None,
                 prob_distribution='uniform', distribution_param=None,
                 n_samples=100000):
        # # Assign values to self
        self.nominal_value = nominal_value
        self.n_samples = n_samples
        self.distribution_param = distribution_param

        # Bounds definition according to input
        if lower_bound is None and upper_bound is None:
            self.lower_bound = nominal_value
            self.upper_bound = nominal_value
        elif lower_bound is not None and upper_bound is None:
            self.lower_bound = nominal_value-lower_bound
            self.upper_bound = nominal_value+lower_bound
        elif lower_bound is not None and upper_bound is not None:
            self.lower_bound = lower_bound
            self.upper_bound = upper_bound

        # Probability distribution
        # TODO: define definition- should a truncated normal function be
        #     defined as "normal", "custom" or "normal truncated"?.
        if self.lower_bound == self.upper_bound or \
                prob_distribution == 'constant':
            self.prob_distribution = 'constant'
            self.n_samples = 1
        elif prob_distribution == 'normal' and lower_bound == -float('Inf') \
                and upper_bound == float('Inf'):
            self.prob_distribution = 'normal'
        elif prob_distribution == 'discrete':
            self.prob_distribution = 'discrete'
        elif prob_distribution == 'normal':
            self.prob_distribution = 'normal'
        elif prob_distribution == 'uniform':
            self.prob_distribution = 'uniform'
        elif prob_distribution == 'custom':
            self.prob_distribution = 'custom'
        else:
            raise ValueError("Probability distribution type not recognized")

        # Samples
        self.samples = self.__generate_samples(
            self.lower_bound, self.upper_bound,
            self.prob_distribution, distribution_param,
            n_samples)

        # Compute statistical properties
        self.statistical_parameter()

        # # Check input data consistency
        if (self.lower_bound > self.upper_bound):
            raise ValueError("Lower bound (" + str(self.lower_bound)
                             + ") is larger than upper bound ("
                             + str(self.upper_bound) + ".")

        if not(self.lower_bound <= self.nominal_value <= self.upper_bound):
            raise ValueError("Nominal value (" + str(self.nominal_value)
                             + ") is not between bounds ("
                             + str(self.lower_bound) + ", "
                             + str(self.upper_bound) + ").")

    # # Redefine mathematical operations
    def __neg__(self):
        negative = UncertainValue(
            -self.nominal_value,
            -self.upper_bound,
            -self.lower_bound)
        negative.samples = -self.samples
        negative.statistical_parameter()
        return negative

    def __add__(self, other):
        if type(other) is float or type(other) is int:
            other = UncertainValue(other)

        nominal_value = self.nominal_value + other.nominal_value
        lower_bound = self.lower_bound + other.lower_bound
        upper_bound = self.upper_bound + other.upper_bound
        result = UncertainValue(nominal_value, lower_bound, upper_bound,
                                'custom')
        result.samples = self.samples+other.samples
        result.statistical_parameter()
        return result

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if type(other) is float or type(other) is int:
            other = UncertainValue(other)

        nominal_value = self.nominal_value - other.nominal_value
        lower_bound = self.lower_bound - other.upper_bound
        upper_bound = self.upper_bound - other.lower_bound
        result = UncertainValue(nominal_value, lower_bound, upper_bound,
                                'custom')
        result.samples = self.samples-other.samples
        result.statistical_parameter()
        return result

    def __rsub__(self, other):
        return -self+other

    def __mul__(self, other):
        if type(other) is float or type(other) is int:
            other = UncertainValue(other)

        nominal_value = self.nominal_value*other.nominal_value
        bounds = [
            self.lower_bound*other.lower_bound,
            self.lower_bound*other.upper_bound,
            self.upper_bound*other.lower_bound,
            self.upper_bound*other.upper_bound
        ]
        lower_bound = min(bounds)
        upper_bound = max(bounds)
        result = UncertainValue(nominal_value, lower_bound, upper_bound,
                                'custom')
        result.samples = self.samples*other.samples
        result.statistical_parameter()
        return result

    def __rmul__(self, other):
        return self*other

    def __truediv__(self, other):
        if type(other) is float or type(other) is int:
            other = UncertainValue(other)

        nominal_value = self.nominal_value/other.nominal_value
        bounds = [
            self.lower_bound/other.lower_bound,
            self.lower_bound/other.upper_bound,
            self.upper_bound/other.lower_bound,
            self.upper_bound/other.upper_bound
        ]

        lower_bound = min(bounds)
        upper_bound = max(bounds)
        if other.lower_bound < 0 and other.upper_bound > 0:
            lower_bound = -inf
            upper_bound = inf

        prob_distribution = 'custom'
        result = UncertainValue(nominal_value, lower_bound, upper_bound,
                                prob_distribution)
        result.samples = self.samples/other.samples
        result.statistical_parameter()
        return result

    def __rtruediv__(self, other):
        if type(other) is float or type(other) is int:
            other = UncertainValue(other)
        return other/self

    def __pow__(self, other):
        if type(other) is float or type(other) is int:
            other = UncertainValue(other)

        nominal_value = self.nominal_value**other.nominal_value
        # Type check
        if self.lower_bound > 0 \
           or (other.lower_bound == 0 and other.upper_bound == 0):
            # Result equals 1
            bounds = [i[0]**i[1] for i in list(it.product(
                [self.lower_bound, self.upper_bound],
                [other.lower_bound, other.upper_bound]))]
            result = UncertainValue(nominal_value, None, None, 'custom')
            result.lower_bound = min(bounds)
            result.upper_bound = max(bounds)
            result.prob_distribution = 'custom'
        else:
            raise ValueError('Uncertain calculation of exponentiation with '
                             + 'negative basis not implemented')
        result.samples = self.samples**other.samples
        result.n_samples = len(result.samples)
        result.statistical_parameter()
        return result

    def __rpow__(self, other):
        if type(other) is float or type(other) is int:
            other = UncertainValue(other)
        return other**self

    # Redefine comparision

    # Other functions
    def describe(self):
        """ This function is used to display the information describing an
            uncertain value: nominal value, lower bound, upper bound,
            probability distribution type and number of samples.
        """
        desc_string = \
            "\nThis variable is an uncertain value. "\
            + "It has the following properties:" \
            + "\n" \
            + "\n\t- Nominal value: " + str(self.nominal_value) \
            + "\n" \
            + "\n\t- Mean: " + str(self.mean)\
            + "\n\t- Median: " + str(self.median)\
            + "\n\t- Variance: " + str(self.var)\
            + "\n\t- Standard deviation: " + str(self.std)\
            + "\n\t- Skewness: " + str(self.skewness)\
            + "\n" \
            + "\n\t- Lower bound: " + str(self.lower_bound)\
            + "\n\t- Percentile 5: " + str(self.p05)\
            + "\n\t- Q1: " + str(self.q1)\
            + "\n\t- Q3: " + str(self.q3)\
            + "\n\t- Percentile 95: " + str(self.p95)\
            + "\n\t- Upper bound: " + str(self.upper_bound)\
            + "\n" \
            + "\n\t- Probability distribution type: " \
            + str(self.prob_distribution) \
            + "\n\t- Number of samples: " + str(self.n_samples)\
            + "\n"
        return desc_string

    def plot_distribution(self, label=None, new_figure=False, title=None,
                          plot_type='pdf', alpha=1, density=True):
        """ This function is used to plot the probability distribution or
            cumulative probability distribution of an uncertain number.

        Kwargs:
            label (string): String used to label the histogram. Default value
                is None (probability distribution is not labeled).
            new_figure (bool): If True, the value is plotted in a new window.
                Defaut value is False.
            title (string): Plot title. Default value is None.
            plot_type (string): Type of plot. Can be either 'pdf' (probability
                distribution, default value) or 'cdf' (cumulative distribution)

        """
        if new_figure or not plt.get_fignums():
            plt.figure()
            plt.xlabel('Value [-]')
            if plot_type == 'pdf':
                ylabel = 'Probability density [-]'
            elif plot_type == 'cdf':
                ylabel = 'Probability [-]'
            plt.ylabel(ylabel)
            plt.title(title)

        if plot_type == 'pdf':
            histtype = 'bar'
            cum = False
        elif plot_type == 'cdf':
            histtype = 'step'
            cum = True
        else:
            raise ValueError('Unknown plot type.')

        if label is None:
            plt.hist(self.samples, bins=100, density=density,
                     histtype=histtype, cumulative=cum, alpha=alpha)
        elif label is not None:
            plt.hist(self.samples, bins=100, density=density, label=label,
                     histtype=histtype, cumulative=cum, alpha=alpha)
            plt.legend()

        plt.show(block=False)

    # Private methods
    def __generate_samples(self, lower_bound, upper_bound, prob_distribution,
                           distribution_param, n_samples):
        """ Generates the samples of the uncertain number
        """
        if prob_distribution == 'uniform':
            return np.random.uniform(lower_bound, upper_bound, n_samples)
        elif prob_distribution == 'constant':
            return np.array(lower_bound)
        elif prob_distribution == 'normal':
            mean = distribution_param[0]
            deviation = distribution_param[1]
            samples = []
            while len(samples) <= n_samples:
                new_samples = [x for x in
                               np.random.normal(mean, deviation, n_samples)
                               if lower_bound <= x and x <= upper_bound]
                samples = np.append(samples, new_samples)
            output_samples = samples[:n_samples]
            return output_samples
        elif prob_distribution == 'discrete':
            distribution_param = np.array(distribution_param)
            if distribution_param.shape[1] == 1:
                return np.random.choice(distribution_param, n_samples)
            elif distribution_param.shape[1] == 2:
                return np.random.choice(
                    distribution_param[:, 0],
                    n_samples,
                    p=distribution_param[:, 1])
        elif prob_distribution == 'custom':
            if distribution_param is None:
                distribution_param = [0]
            return np.random.choice(distribution_param, n_samples)

    def statistical_parameter(self):
        """ Computes statistical parameters (mean, variance,...) of the
            uncertain number using the given samples.
        """
        self.mean = np.mean(self.samples)
        self.var = np.var(self.samples)
        self.std = np.std(self.samples)
        self.skewness = skew(self.samples)

        self.median = np.median(self.samples)
        self.q1 = np.percentile(self.samples, 25)
        self.q3 = np.percentile(self.samples, 75)
        self.p05 = np.percentile(self.samples, 5)
        self.p95 = np.percentile(self.samples, 95)


# Functions to work with uncertain values
def probability_in_interval(uncertain_value, interval):
    """ This function is used to calculate the probability of an uncertain
        value being in a given interval.

    Args:
        uncertain_value (UncertainValue): uncertain value for which the
            probability is calculated.
        interval (array): interval U defined by a lower and upper bound
            [u_min, u_max].

    """
    samples = uncertain_value.samples
    lower_bound = interval[0]
    upper_bound = interval[1]
    return sum((lower_bound < samples) & (samples < upper_bound)) \
        / len(samples)
