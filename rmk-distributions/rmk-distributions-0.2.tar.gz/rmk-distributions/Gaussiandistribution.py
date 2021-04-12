import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Gaussian(Distribution):
    """
    Class that inherits some attributes from Distribution
    (Generaldistribution.py). Used to import data files
    and run some basic Gaussian analyses on their data.
    """
    def __init__(self, mu = 0, sigma = 0):
        # Populate attributes according to attributes given to Distribution
        Distribution.__init__(self, mu, sigma)
        self.data = []

    def calculate_mean(self):
        """
        Calculate the average of the values in the data attribute.
        Store the mean in the object's mean attribute.

        No args.

        Returns: (float) the mean of the dataset.
        """

        avg = float(sum(self.data) / len(self.data))
        self.mean = avg

        return self.mean

    def calculate_stdev(self, sample = True):
        """
        Calculate standard deviation of dataset in self.data.
        Store value in self.stdev.
        Return self.stdev.

        When argument sample = True, calculate stdev as if self.data contains
        a sample's data rather than a population's.
        """

        if sample:
            n = len(self.data) - 1
        else:
            n = len(self.data)

        mean = self.calculate_mean()

        # There is another way that might be faster:
        # sigma = 0
        # Then iterate through list and add squared error to sigma
        # Maintains a single value rather than a new list of values
        squared_errors = [(x - mean)**2 for x in self.data]
        stdev = math.sqrt(sum(squared_errors) / n)

        self.stdev = stdev

        return self.stdev

    def pdf(self, x):
        """
        For a value, x, estimate the probability density at that point.
        """

        pi = math.pi
        e = math.e

        constant = 1/math.sqrt(2 * pi * (self.stdev**2))
        exponent = -0.5 * (((x - self.mean) / self.stdev) ** 2)

        prob = constant * (e ** exponent)

        return prob

    def plot_histogram(self):
        """
        Plot a histogram in matplotlib describing the data in self.data.
        """

        fig, ax = plt.subplots(figsize = (18,12))

        ax.hist(x = self.data)
        ax.set_ylabel('Count of Values in self.data', fontsize = 16)
        ax.set_ylabel('Values in self.data', fontsize = 16)

        plt.title('Frequency Distribution for Values in self.data')

        plt.show()


    def plot_histogram_pdf(self, n_spaces = 50):

        """Function to plot the normalized histogram of the data and a plot of the
        probability density function along the same range

        This function is beyond me, at the moment. Instructor included it
        as a demo.

        Args:
        	n_spaces (int): number of data points

        Returns:
        	list: x values for the pdf plot
        	list: y values for the pdf plot

        """

        mu = self.mean
        sigma = self.stdev

        min_range = min(self.data)
        max_range = max(self.data)

         # calculates the interval between x values
        interval = float((max_range - min_range) / n_spaces)

        x = []
        y = []

        # calculate the x values to visualize
        # This plots prob density at each x value
        # Derives x values from the data set and the interval calculated above
        # Calculates density using the pdf() method of this class
        for i in range(n_spaces):
        	tmp = min_range + interval*i
        	x.append(tmp)
        	y.append(self.pdf(tmp))

        # make the plots
        fig, axes = plt.subplots(2,sharex=True)
        fig.subplots_adjust(hspace=.5)
        axes[0].hist(self.data, density=True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')

        axes[1].plot(x, y)
        axes[1].set_title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[0].set_ylabel('Density')
        plt.show()

        return x, y

    def __add__(self, other):
        """
        Magic function that tells Python how to add two instances of this class.
        """

        result = Gaussian() # Instantiate an empty Gaussian class that will be our new combined instance
        result.mean = self.mean + other.mean
        result.stdev = math.sqrt(self.stdev ** 2 + other.stdev ** 2)

        return result

    def __repr__(self):
        """
        Magic function that tells Python what to print when I reference this
        class.
        """

        return 'mean {}, standard deviation {}'.format(self.mean, self.stdev)
