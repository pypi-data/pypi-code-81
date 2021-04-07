from abc import abstractmethod
import numpy as np
import math

from pyDOE2 import fullfact
from SALib.sample import latin, fast_sampler, finite_diff, saltelli, sobol_sequence


class AbstractSampler(object):

    def __init__(self):
        super(AbstractSampler, self).__init__()

    @abstractmethod
    def sample(self, problem, samples):
        pass


class MonteCarloSampler(AbstractSampler):

    def __init__(self):
        super(MonteCarloSampler, self).__init__()

    def sample(self, problem, samples):
        parameter_amount = problem['num_vars']
        mcs = np.random.rand(samples, parameter_amount)
        self.normalize(problem, mcs)
        return mcs

    def normalize(self, problem, sampled_data):
        for col in range(len(sampled_data[0])):
            bounds = problem['bounds'][col]
            sampled_data[:, col] = list(map(lambda x: (x * (int(bounds[1]) - int(bounds[0])) + int(bounds[0])),
                                            sampled_data[:, col]))
        return sampled_data


class LatinHypercubeSampler(AbstractSampler):

    def __init__(self):
        super(LatinHypercubeSampler, self).__init__()

    def sample(self, problem, samples):
        return latin.sample(problem, samples)


class FullFactorialSampler(AbstractSampler):

    def __init__(self):
        super(FullFactorialSampler, self).__init__()

    def sample(self, problem, samples):
        ff_numbers = [int(bound[1] - bound[0] + 1) for bound in problem['bounds']]
        ff = fullfact(ff_numbers)
        ff = self.normalize(problem, ff)
        return ff

    def normalize(self, problem, sampled_data):
        for col in range(len(sampled_data[0])):
            bounds = problem['bounds'][col]
            sampled_data[:, col] = list(map(lambda x: (x + int(bounds[0])), sampled_data[:, col]))
        return sampled_data


class FASTSampler(AbstractSampler):

    def __init__(self):
        super(FASTSampler, self).__init__()

    def sample(self, problem, samples):
        N = math.ceil(samples / problem['num_vars'])
        M = math.floor(math.sqrt(N / 4))
        return fast_sampler.sample(problem, max(N, 5), M=max(M, 1))


class FiniteDifferenceSampler(AbstractSampler):

    def __init__(self):
        super(FiniteDifferenceSampler, self).__init__()

    def sample(self, problem, samples):
        return finite_diff.sample(problem, math.ceil(samples/4))


class SaltelliSampler(AbstractSampler):

    def __init__(self):
        super(SaltelliSampler, self).__init__()

    def sample(self, problem, samples):
        n = samples / (2 * problem['num_vars'] + 2)
        return saltelli.sample(problem, math.ceil(n), calc_second_order=True)


class SobolSampler(AbstractSampler):

    def __init__(self):
        super(SobolSampler, self).__init__()

    def sample(self, problem, samples):
        ss = sobol_sequence.sample(samples, problem['num_vars'])
        return self.normalize(problem, ss)

    def normalize(self, problem, sampled_data):
        for col in range(len(sampled_data[0])):
            bounds = problem['bounds'][col]
            sampled_data[:, col] = list(map(lambda x: (x * (int(bounds[1]) - int(bounds[0])) + int(bounds[0])),
                                            sampled_data[:, col]))
        return sampled_data
