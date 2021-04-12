# TODO: import necessary libraries
import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

# TODO: make a Binomial class that inherits from the Distribution class. Use the specifications below.
class Binomial(Distribution):
    """ Binomial distribution class for calculating and
    visualizing a Binomial distribution.

    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring

    """
    #       A binomial distribution is defined by two variables:
    #           the probability of getting a positive outcome
    #           the number of trials

    #       If you know these two values, you can calculate the mean and the standard deviation
    #
    #       For example, if you flip a fair coin 25 times, p = 0.5 and n = 25
    #       You can then calculate the mean and standard deviation with the following formula:
    #           mean = p * n
    #           standard deviation = sqrt(n * p * (1 - p))

    #

    # TODO: define the init function
    # Initially didn't realize we were supposed to declare size on instantiation.
    def __init__(self, prob=0.5, size = 20):

        # Just need to add attributes that Binomial has and Distribution does not
        self.n = size
        self.p = prob

        # Distribution __init__ brings in mu, sigma and data_list with it (its attributes)
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())

        # TODO: store the probability of the distribution in an instance variable p
        # TODO: store the size of the distribution in an instance variable n

        # TODO: Now that you know p and n, you can calculate the mean and standard deviation
        #       You can use the calculate_mean() and calculate_stdev() methods defined below along with the __init__ function from the Distribution class

    # TODO: write a method calculate_mean() according to the specifications below
    def calculate_mean(self):
        """Function to calculate the mean from p and n

        Args:
            None

        Returns:
            float: mean of the data set

        """
        # Mean represents expected count of desired outcome.
        # If prob of desired is 20%, and we have 50 trials, mean (expectation) is 10
        # This is because we're effectively averaging a bunch of 1s and 0s
        self.mean = self.p * self.n
        return self.mean

    #TODO: write a calculate_stdev() method accordin to the specifications below.
    def calculate_stdev(self):
        """Function to calculate the standard deviation from p and n.

        Args:
            None

        Returns:
            float: standard deviation of the data set

        """
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))
        return self.stdev
    # TODO: write a replace_stats_with_data() method according to the specifications below. The read_data_file() from the Generaldistribution class can read in a data
    # file. Because the Binomaildistribution class inherits from the Generaldistribution class,
    # you don't need to re-write this method. However,  the method
    # doesn't update the mean or standard deviation of
    # a distribution. Hence you are going to write a method that calculates n, p, mean and
    # standard deviation from a data set and then updates the n, p, mean and stdev attributes.
    # Assume that the data is a list of zeros and ones like [0 1 0 1 1 0 1].
    #
    #       Write code that:
    #           updates the n attribute of the binomial distribution
    #           updates the p value of the binomial distribution by calculating the
    #               number of positive trials divided by the total trials
    #           updates the mean attribute
    #           updates the standard deviation attribute
    #
    #       Hint: You can use the calculate_mean() and calculate_stdev() methods
    #           defined previously.
    def replace_stats_with_data(self):
        """Function to calculate p and n from the data set. The function updates the p and n variables of the object.

        Args:
            None

        Returns:
            float: the p value
            float: the n value

        """
        self.n = float(len(self.data))
        self.p = float(sum(self.data) / self.n)
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()

        return self.p, self.n
    # TODO: write a method plot_bar() that outputs a bar chart of the data set according to the following specifications.
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using
        matplotlib pyplot library.

        Args:
            None

        Returns:
            None
        """
        x = self.data

        fig, ax = plt.subplots(1,1,figsize = (18,12))

        ax.hist(x = x)
        ax.set_ylabel('Frequency of Outcome in self.data', fontsize = 16)
        ax.set_xlabel('Possible Outcomes in self.data', fontsize = 16)

        plt.title('Frequency Distribution, Binomial Test Data', fontsize = 24)
        plt.show()

    #TODO: Calculate the probability density function of the binomial distribution
    def pdf(self, k):
        """Probability density (mass?) function calculator for the binomial distribution.

        Args:
            k (float): Count of times tracked outcome is desired.


        Returns:
            float: probability density function output
        """
        p = self.p
        n = self.n

        count = math.factorial(n) / (math.factorial(n-k) * math.factorial(k)) # desired count of tracked outcome
        prob = (p ** k) * ((1-p) ** (n-k)) # prob of a single tracked outcome

        pdf = count * prob

        return float(pdf)

    # write a method to plot the probability density function of the binomial distribution
    def plot_bar_pdf(self):
        """Function to plot the pdf of the binomial distribution

        Args:
            None

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot

        """

        # TODO: Use a bar chart to plot the probability density function from
        # k = 0 to k = n

        #   Hint: You'll need to use the pdf() method defined above to calculate the
        #   density function for every value of k.

        #   Be sure to label the bar chart with a title, x label and y label

        #   This method should also return the x and y values used to make the chart
        #   The x and y values should be stored in separate lists
        n = int(self.n)

        x = list(range(0, n + 1))
        y = []

        for i in x:
            y.append(self.pdf(i))

        fig, ax = plt.subplots(1,1,figsize = (18,12))

        ax.bar(x = x, y = y)
        ax.set_ylabel('Probability Density at k', fontsize = 16)
        ax.set_xlabel('Count of Tracked Outcome in Binomial Tests (k)', fontsize = 16)

        plt.title('Probability Masses - Binomial Distribution given self.data', fontsize = 24)
        plt.show()

        return x, y

    # write a method to output the sum of two binomial distributions. Assume both distributions have the same p value.
    def __add__(self, other):
        """Function to add together two Binomial distributions with equal p

        Args:
            other (Binomial): Binomial instance

        Returns:
            Binomial: Binomial distribution (instance of the class with its
            attributes populated correctly)

        """

        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise

        # TODO: Define addition for two binomial distributions. Assume that the
        # p values of the two distributions are the same. The formula for
        # summing two binomial distributions with different p values is more complicated,
        # so you are only expected to implement the case for two distributions with equal p.

        # the try, except statement above will raise an exception if the p values are not equal

        # Hint: When adding two binomial distributions, the p value remains the same
        #   The new n value is the sum of the n values of the two distributions.

        result = Binomial() # Instantiate an empty binomial that we can populate with sum attributes
        result.p = self.p # Because we're conveniently adding two dists with equal p
        result.n = self.n + other.n
        result.calculate_mean()
        result.calculate_stdev()

        return result

    # use the __repr__ magic method to output the characteristics of the binomial distribution object.
    def __repr__(self):
        """Function to output the characteristics of the Binomial instance

        Args:
            None

        Returns:
            string: characteristics of the Binomial object

        """

        # TODO: Define the representation method so that the output looks like
        #       mean 5, standard deviation 4.5, p .8, n 20
        #
        #       with the values replaced by whatever the actual distributions values are
        #       The method should return a string in the expected format

        return 'mean {}, standard deviation {}, p {}, n {}'.format(self.mean, self.stdev, self.p, self.n)
