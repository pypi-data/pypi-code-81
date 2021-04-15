"""RawlsStats class which enables statistics other multiples Rawls instance
"""

# main imports
import numpy as np
import math

# stats import
from scipy.stats import skew, kurtosis
from ipfml import utils

# modules imports
from .rawls import Rawls
from .utils import check_file_paths


class RawlsStats():
    """RawlsStats class which enables statistics other multiples Rawls instance

    Attributes:
        data: {ndrray} -- merged buffer data numpy array with higher dimension of all Rawls instance
        nelements: {int} -- number Rawls instance used
        details: {Details} -- details instance information
        mean_samples_per_element: {float} -- statistic which gives mean number of samples used (if Rawls images do not have same number of samples)
        expected_shape: {(int, int, int)} -- describe expected shape of an Rawls image element
    """
    def __init__(self, rawls_images): 
        """Init RawlsStats instance using list of Rawls instances
        
        Arguments:
            rawls_images {[Rawls]} -- list of Rawls instances
        
        Raises:
            Exception: Input format expection, unvalid input shape

        Example:

        >>> from rawls.rawls import Rawls
        >>> from rawls.stats import RawlsStats
        >>> paths = [ 'images/example_1.rawls', 'images/example_2.rawls' ]
        >>> rawls_img = [ Rawls.load(p) for p in paths ]
        >>> rawls_stats = RawlsStats(rawls_img)
        >>> rawls_stats.nelements
        2
        >>> rawls_stats.mean_samples_per_element
        1.0
        """

        shapes = []

        for img in rawls_images:
            shapes.append(img.shape)

        if not shapes[1:] == shapes[:-1]:
            raise Exception('Input rawls images do not have same shapes')

        # create array with higher dimension
        merged_values = np.array([img.data for img in rawls_images])

        # get total number of samples used
        total_samples = sum([img.details.samples for img in rawls_images])

        # details based on first element
        merged_details = rawls_images[0].details
        merged_details.samples = total_samples

        # set instance attributes
        self.data = merged_values
        self.nelements = len(rawls_images)
        self.details = merged_details
        self.mean_samples_per_element = self.details.samples / self.nelements
        self.expected_shape = shapes[0]

    @classmethod
    def load(self, filepaths):
        """load data from rawls files
        
        Arguments:
            filepath: {[str]} -- list of paths of .rawls files

        Returns:
            {RawlsStats} : RawlsStats instance

        >>> from rawls.rawls import Rawls
        >>> from rawls.stats import RawlsStats
        >>> paths = [ 'images/example_1.rawls', 'images/example_2.rawls' ]
        >>> rawls_stats = RawlsStats.load(paths)
        >>> rawls_stats.nelements
        2
        >>> rawls_stats.mean_samples_per_element
        1.0
        """

        # check if given paths are corrects
        check_file_paths(filepaths)

        # read rawls
        rawls_images = []

        for filepath in filepaths:
            rawls_images.append(Rawls.load(filepath))

        # build
        return RawlsStats(rawls_images)

    def append(self, rawls_img):
        """Append list or rawls image element to current Rawls stats instance

        Arguments:
            rawls_img {[Rawls]} -- Rawls or list of Rawls instance

        Raises:
            Exception: Invalid rawls shape, impossible to add this shape with others elements

        >>> from rawls.rawls import Rawls
        >>> from rawls.stats import RawlsStats
        >>> paths = [ 'images/example_1.rawls', 'images/example_2.rawls' ]
        >>> rawls_stats = RawlsStats.load(paths)
        >>> rawls_stats.nelements
        2
        >>> rawls_stats.append(paths)
        >>> rawls_stats.nelements
        4
        """
        # check if list and recursively add elements if needed
        if isinstance(rawls_img, list):
            for img in rawls_img:

                # check current instance
                self.append(img)

        else:
            # load if necessary
            if isinstance(rawls_img, str):
                check_file_paths(rawls_img)
                rawls_img = Rawls.load(rawls_img)

            # check elements
            if rawls_img.shape != self.expected_shape:
                raise Exception(
                    'Invalid rawls shape, impossible to add this shape with others elements'
                )

            rawls_data = np.expand_dims(rawls_img.data, axis=0)

            # append data to current elements
            self.data = np.concatenate([self.data, rawls_data], axis=0)

            # update others data
            self.details.samples += rawls_img.details.samples
            self.nelements += 1
            self.mean_samples_per_element = self.details.samples / self.nelements

    def mean(self):
        """Compute mean on `.rawls` samples
        
        Returns:
            {Rawls} -- new rawls object with mean data of rawls files
        """

        mean_values = np.mean(self.data, axis=0)
        return Rawls(self.expected_shape, mean_values, self.details)

    def var(self):
        """Compute variance on `.rawls` samples
        
        Returns:
            {Rawls} -- new rawls object with variance data of rawls files
        """

        var_values = np.var(self.data, axis=0)
        return Rawls(self.expected_shape, var_values, self.details)

    def std(self):
        """Compute std on `.rawls` samples
        
        Returns:
            {Rawls} -- new rawls object with std data of rawls files
        """

        std_values = np.std(self.data, axis=0)
        return Rawls(self.expected_shape, std_values, self.details)

    def skew(self):
        """Compute skewness on `.rawls` samples
        
        Returns:
            {Rawls} -- new rawls object with skewness data of rawls files
        """

        skew_values = skew(self.data, axis=0, nan_policy='raise')
        return Rawls(self.expected_shape, skew_values, self.details)

    def kurtosis(self):
        """Compute kurtosis on `.rawls` samples
        
        Returns:
            {Rawls} -- new rawls object with kurtosis data of rawls files
        """

        kurtosis_values = kurtosis(self.data, axis=0, nan_policy='raise')
        return Rawls(self.expected_shape, kurtosis_values, self.details)

    def mon(self):
        """Compute Median Of meaNs on `.rawls` samples
        
        Returns:
            {Rawls} -- new rawls object with MON data of rawls files
        """

        median_values = np.median(self.data, axis=0)

        return Rawls(self.expected_shape, median_values, self.details)


    def __variance_evolution(self, means):
        """Extract variance evolution when removing max element from current mean distribution

        Args:
            means [{float}] -- list of extract means

        Returns:
            [{float}] -- variance evolution
        """
        distances = []
        l = list(means).copy()
        
        for _ in range(len(means)):
            
            l.pop(l.index(max(l)))
            
            if len(l) > 2:
                distances.append(np.var(l))
            
        return distances


    def __pak_mon_pixel(self, means, rho=None, alpha=None):

        sorted_means = sorted(means)
        k_elements = len(means)
        middle_index = int(k_elements / 2)
        
        # use of entropy from {means} in order to determine dynamically {alpha} and {rho} parameter
        if alpha == None:
            alpha = utils.get_entropy(self.__variance_evolution(means))
            #print(f'Dynamic alpha computed using entropy ({utils.get_entropy(variance_evolution(means))}): {alpha}')
            
        if rho == None:
            rho = int(middle_index * utils.get_entropy(self.__variance_evolution(means)))
            #print(f'Dynamic rho computed using entropy ({utils.get_entropy(variance_evolution(means))}): {rho}')
            
        if rho > int(k_elements / 2):
            raise(f"Error, rho set to {rho} is too high depending of k={k_elements}")
        
        # get lower and higher center indices (to generalize with case of even number of elements)
        lower_index = None
        higher_index = None
            
        # compute the median
        if k_elements % 2 == 0:
            
            lower_index = middle_index - 1
            higher_index = middle_index
            
            # classical median when even number of elements
            median = sorted_means[lower_index] * 0.5 + sorted_means[middle_index] * 0.5
            
        else:
            lower_index = middle_index - 1
            higher_index = middle_index - 1
            
            # classical when odd number of elements
            median = sorted_means[middle_index - 1]
        
        # add neighborhood information
        sum_to_divide = 1
        weighted_median = median # default only median
        
        for i in range(1, rho + 1):
            
            # confidence {alpha} parameter using distance criterion
            mult_factor = math.pow(alpha, i)
            
            # add left and right neighbor contribution
            weighted_median += sorted_means[lower_index - i] * mult_factor
            weighted_median += sorted_means[higher_index + i] * mult_factor
            
            # weighting contribution to take in account
            sum_to_divide += 2 * mult_factor
        
        # weighted median with neigborhood information
        return weighted_median / sum_to_divide

    def pak_mon(self, alpha=None, rho=None):
        """PAK-MON is an new version of Median Of meaNs (MON) which takes advantage of the best between the mean and the MON estimators.

        - It gives better estimation of the mean using neighbordhood knowledge when outliers seems to not be detected.
        - Automatic settings of `rho` and `alpha` parameters are based on the variance evolution from `means` and shannon entropy.

        Args:
            rho: {float} -- number of neighbors to taken as confident
            alpha: {float} -- confidence parameter according to the distance from the neighbour (a \in [0, 1]).

        Raises:
            Exception: invalid `rho` parameter value

        Returns:
            {float}: final estimated value
        """
        intern_pakmon = lambda x: self.__pak_mon_pixel(x, alpha, rho)
        pak_mon_values = np.apply_along_axis(func1d=intern_pakmon, axis=0, arr=self.data)

        return Rawls(self.expected_shape, pak_mon_values, self.details)


    def __str__(self):
        """Display RawlsStats information
        
        Returns:
            {str} RawlsStats information
        """
        return "--------------------------------------------------------\nnelements: \n\t{0}\nDetails: \n{1}\nMean samples per element: \n\t{2}\nExpected shape: \n\t{3}\n--------------------------------------------------------".format(
            self.nelements, self.details, self.mean_samples_per_element,
            self.expected_shape)
