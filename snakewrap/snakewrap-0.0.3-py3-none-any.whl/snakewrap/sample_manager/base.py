import abc

class SampleManager(abc.ABC):
    def __init__(self):
        super().__init__()
        self.samples_processed = False


    @abc.abstractmethod
    def parse_samples(self, files_folders):
        """gets a list of files and folders and gathers sample information"""

    @abc.abstractmethod
    def process_samples(self):
        """processes sample information either parsed or loaded from file
        
        This is used to resolve naming confilcts and ensure that all
        files that enter also come out the other end.
        """

    @abc.abstractmethod
    def write_to_file(self, _file):
        """write to some file format that load_to_file can understand

        ideally this should also be the file format that is provided
        to snakemake
        """

    @abc.abstractmethod
    def load_from_file(self, input_file):
        """loads files written by write_to_file"""


class DummySampleManager(SampleManager):
    def __init__(self):
        super().__init__()
        self.sample_list = []

    def parse_samples(self, files_folders):
        self.sample_list = []

    def process_samples(self):
        self.samples_processed = True

    def write_to_file(self, _file):
        pass

    def load_from_file(self, input_file):
        pass





