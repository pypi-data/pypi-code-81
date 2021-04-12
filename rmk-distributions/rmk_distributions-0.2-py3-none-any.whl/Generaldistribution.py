class Distribution:

    def __init__(self, mu = 0, sigma = 1):
        """
        Initialize the class with mu (average) and sigma (standard deviation)
        """
        self.mean = mu
        self.stdev = sigma
        self.data = [] # Will hold data imported from file. Start blank.


    def read_data_file(self, file_name):
        """
        Read in a data file in .txt format. Each line is a value.
        Each value is added to a list and stored in self.data
        """
        data_list = []

        with open(file_name) as f:
            line = f.readline() # read the first line of the file
            while line:
                data_list.append(int(line))
                line = f.readline() # call readline() again, because it remembers first call

        f.close() # Maybe not required, because used with open(). But safe.

        self.data = data_list # store imported data in class's data attribute.
