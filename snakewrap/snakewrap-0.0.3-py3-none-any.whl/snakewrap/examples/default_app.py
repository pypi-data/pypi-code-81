from ..wrapper import SnakeApp 
from ..sample_manager.illumina_sample_manager import IlluminaSampleManager
from .. import utils
import argparse

class DefaultApp(SnakeApp):
    """Default App reading in paired-end illumina fastqs and optional reference
    """
    def __init__(self, *args, **kwargs):
        self.description = "snakemake application"
        super(DefaultApp, self).__init__(*args,**kwargs)
        self.register_sample_manager(IlluminaSampleManager)

    def get_argparser(self):
        parser = argparse.ArgumentParser(prog=self.appname, 
                                         description=self.description)
        parser.add_argument("--input", nargs="*",
                            help="Folders containing fastqs or"
                                 " the files them selfs."
                                 " Can be used multiple times") 
        parser.add_argument("--search_depth", default=2,type=int,
                            help="Maximum search depth for finding fastq files"
                                 " in folders. Default is 2. "
                                 "Set to 0 for unlimited searching")
        parser.add_argument("-o", "--outputfolder", help="Output Folder to use",
                            type=utils.mkdir_if_not_exists,
                            dest="output")
        parser.add_argument("--reference", help="Reference file to use (fasta)",
                            type=utils.realpathify(utils.validate_fasta_ext))
        return parser

