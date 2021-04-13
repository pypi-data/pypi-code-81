from .base import SampleManager
from .. import utils
import pandas
import re
import os



DEFAULT_FILENAME_PATTERNS = [
    ("illumina_some_institute_1",{
        "regex":r"(?P<date>\d+)_(?P<lab_id>\d{2}-\d{4,5}(-[^_]+)?)_(?P<sample_id>.+)"
                r"_(?P<snum>S\d+)_(?P<lane>L\d{3})_(?P<read>R[12])"
                r"_(?P<running>\d{3})",
        "ambig": ["lane","running"]
        }),
    ("illumina1",{
        "regex":r"(?P<sample_id>.+)_(?P<snum>S[\d]+)_(?P<lane>L[\d]{3})_"
                r"(?P<read>R[12])_(?P<running>\d{3})",
        "ambig":["lane","running"] }),
    ("illumina2",{
        "regex":r"(?P<sample_id>.+)_(?P<snum>S[\d]+)_"
                r"(?P<read>R[12])_(?P<running>\d{3})",
        "ambig":["running"] }),
    ("illumina3",{
        "regex":r"(?P<sample_id>.+)_(?P<snum>S[0-9]+)_(?P<lane>L[0-9]{3})_"
                r"(?P<read>R[12])",
        "ambig":["lane"] }),
    ("illumina4",{
        "regex":r"(?P<sample_id>.+)_S(?P<snum>[0-9]+)_"
                r"(?P<read>R[12])",
        "ambig":[] }),
    ("illumina_fallback",{
        "regex":r"(?P<sample_id>.+)_"
                r"(?P<read>R[12])(?P<residual>_.+)?",
        "ambig":[] }),
    ("SRA",{
         "regex":r"(?P<sample_id>SR.+)_(?P<read>[12])",
         "ambig":[] }),

    ("fallback1",{
         "regex":r"(?P<sample_id>.+)_(?P<read>[A-Za-z0-9]+)",
         "ambig":[] }),
    ("fallback2",{
         "regex":r"(?P<sample_id>.+)\.(?P<read>[A-Za-z0-9]+)",
         "ambig":[],
         "sep":"."})
    ]


DEFAULT_PAIRED_READ_REF = {
        "1":1,
        "2":2,
        "R1":1,
        "R2":2,
        "FORWARD":1,
        "REVERSE":2,
        "FWD":1,
        "REV":2,
        "F":1,
        "R":2,
        "P":1,
        "M":2,
        "PLUS":1,
        "MINUS":2,
        "SENSE":1,
        "ANTI":2
        }

class IlluminaSampleManager(SampleManager):
    def __init__(self, 
                 contingency_no_folder_found=lambda : [], 
                 filename_patterns=DEFAULT_FILENAME_PATTERNS,
                 read_pair_guide=DEFAULT_PAIRED_READ_REF):
        super().__init__()
        self.filename_pattern_guide = None
        self.read_id_pairings = None
        self.ext_regex = r'.(fq|fnq|fastq)(.gz)?'
        self.pandas_parse_store = None  
        self.total_seen_files = 0
        self.files_passing_filter = 0
        self.num_samples = 0 
        self.delta_files = []
        self.sample_config = []
        self.search_depth = 1 
        self.has_warning = False
        self.has_error = False
        self.error_list = []
        self.warning_list = []
        self.contingency_no_folder_found = contingency_no_folder_found 
        #self.contingency_no_folder_found = lambda : [os.path.realpath(".")]
        self.register_filename_pattern_guide(filename_patterns)
        self.register_read_id_pairings(read_pair_guide)
        self.setup_parser()

        
    def load_from_file(self, sample_file):
        file_samples_alt_id =((sample_config[sample][key], sample,
                            utils.default_if_not("alt_id", sample_config[sample],
                                           "PLACE_HOLDER"))
                            for sample in sample_config
                            for key in sample_config[sample]
                            if re.match("read[12]",key))
        # Add files from previously found sample file
        for (_file, sample, alt_id) in file_samples_alt_id:
            self.check_and_add_fastq([_file], res, None, sample_names=[sample],
                                alt_ids=[alt_id])

    def process_samples(self):
        self.resolve_sample_id_conflicts()

    def setup_parser(self):
        self.pandas_parse_store = pandas.DataFrame(
                columns=["path", "unambig_id", "ambig_id","read", "read_id",
                         "sample_id", "sub_sample_id",
                         "alt_sample_id", "alt_sub_sample_id",
                         "file","match","regex", "state"])
        
        self.pandas_parse_store.set_index(
                ["path","unambig_id","ambig_id","read"], 
                inplace=True, drop=False)

    def write_to_file(self, _file):
        pass

    def parse_samples(self, files_folders):

        # Add files added on the command line
        max_level=self.search_depth
        df_2_check = files_folders
        df_2_check = [x for input_list in files_folders for x in input_list]
        if len(df_2_check) == 0:
            df_2_check = self.contingency_no_folder_found()
        for dirfile in df_2_check:
            if os.path.isfile(dirfile):
                self.total_seen_files += 1
                self.check_and_add_fastq([dirfile], None)
            else:
                for pdir, _dir, _files in utils.walklevel(dirfile, max_level):
                    self.total_seen_files += len(_files)
                    self.check_and_add_fastq(_files, pdir)

    def _clean_parent_dir(self, _file, pdir=None):
        if pdir is None:
            path = os.path.dirname(os.path.realpath(_file))
        else:
            path = os.path.realpath(pdir)
        return path

    def check_and_add_fastq(self, _files, pdir,
                            sample_names=None, alt_ids=None):
        single_mode = len(_files) == 1 and sample_names is not None
        patterns=dict(self.filename_pattern_guide)
        patterns_in_order = [key for key, _ in self.filename_pattern_guide]
        end = self.ext_regex
        for _file in (fl for fl in _files 
                      if re.match(".*{end}".format(end=end),
                                  fl)):
            path = self._clean_parent_dir(_file, pdir)
            _file = os.path.basename(_file)
            for pnum, pattern in enumerate(patterns_in_order):
                regex_string = ('{patternregex}{end}'.format(
                                    patternregex=patterns[pattern]["regex"],
                                    end=end))
                match = re.match(regex_string, _file)
                if match is None:
                    if pnum-1 == len(patterns):
                        logger.error("FastQ does not meet any known spec:\n"
                               "file: {_file}".format(
                                   _file=os.path.join(path,_file)))
                    continue
                sep = utils.default_if_not("sep", patterns[pattern],"_")
                ambig_keys=utils.default_if_not("ambig",patterns[pattern], [])
                match_dict = match.groupdict()
                ambig = sep.join(match_dict[a]
                                 for a in sorted(ambig_keys))
                nonambig = sep.join(match_dict[na]
                                    for na in sorted(match_dict.keys())
                                    if na not in ambig_keys + ["read"])
                sub_sample_id = sep.join(
                        [val for (_id, val) in list(match.groupdict().items())
                         if _id not in ["read"]])
                if pattern.startswith("illumina_some_institute"):
                    matchdict = match.groupdict()
                    sub_sample_id = "{sid}_{lid}".format(
                            sid=matchdict["sample_id"],
                            lid=matchdict["lab_id"])
                read = "R1"
                read_id = 1
                try:
                    read = match_dict["read"]
                except KeyError:
                    pass
                try:
                    read_id = self.read_id_pairings[read.upper()]
                except KeyError:
                    utils.eprint("Warning: Read name \"",read,"\" not known")
                    utils.eprint(
                           "         Using Regex-pattern: {patt}\n"
                           "           {regex}\n"
                           "         File:\n"
                           "           {_file}"
                           "".format(patt=pattern, regex=regex_string,
                                     _file=_file))


                key=(path,nonambig,ambig,read)
                if key in self.pandas_parse_store.index:
                    break
                new_entry=pandas.DataFrame(dict(zip(self.pandas_parse_store.columns,
                        ([a]
                         for a
                         in  [path, nonambig, ambig, read, read_id,
                              "PLACE_HOLDER",
                              sample_names[0] if single_mode
                                             and sample_names is not None
                                             else sub_sample_id,
                              "PLACE_HOLDER",
                              alt_ids[0] if single_mode
                                         and alt_ids is not None
                                         else "PLACE_HOLDER",
                              _file, pattern,
                              '{regexpattern}{end}'.format(
                                  regexpattern=patterns[pattern]["regex"],end=end),
                              "new"]))))
                new_entry.set_index(["path","unambig_id","ambig_id","read"],inplace=True, drop=False)
                self.pandas_parse_store = self.pandas_parse_store.append(new_entry)
                break
    
    def resolve_sample_id_conflicts(self):
        sample_data = self.pandas_parse_store
        self.generate_alternative_ids()
        prelim_groups = sample_data.groupby(["sub_sample_id"]).groups
        for sub_id in prelim_groups:
            paths_subgroup = sample_data[
                    sample_data.sub_sample_id == sub_id].groupby(level="path").groups
            num_subids = len(paths_subgroup)
            if num_subids == 1:
                continue

            self.warning_list.append("Warning: Found multiple samples "
                            "({num}) with id {sub}!\n"
                            '"DUPLICATE_[Number]_" will be prepended to'
                            "duplicates".format(num=num_subids,
                                                sub=sub_id))
            for (_id, path) in enumerate(paths_subgroup):
                if _id == 0: # Skip first occurance
                    continue
                sample_data.loc[((sample_data.sub_sample_id == sub_id) &
                                (sample_data.path == path)),
                                "sub_sample_id"] = "Duplicate_{_id}_{samp}".format(
                                        _id=_id, samp=sub_id)
            
    def generate_alternative_ids(self):
        sample_data = self.pandas_parse_store
        if not ((sample_data["alt_sub_sample_id"]=="PLACE_HOLDER").any()):
            return
        old_samples = sample_data.loc[
                sample_data.alt_sub_sample_id != "PLACE_HOLDER"].copy()
        old_sample_groups = old_samples.groupby(
                level=["path", "unambig_id"]).groups
        num_old_samples = len(old_sample_groups)
        new_samples = sample_data.loc[
                sample_data.alt_sub_sample_id == "PLACE_HOLDER"].copy()
        new_sample_groups = new_samples.groupby(
                level=["path", "unambig_id"]).groups
        num_new_samples = len(new_sample_groups)
        for key in (key
                    for key in new_sample_groups if key in old_sample_groups):
            new_sample_data = sample_data.loc[new_sample_groups[key]].copy()
            old_sample_data = sample_data.loc[old_sample_groups[key]].copy()
            old_sample_sub_groups = old_sample_data.groupby(
                    level=["ambig_id"]).groups
            new_sample_sub_groups = new_sample_data.groupby(
                    level=["ambig_id"]).groups
            for sub_key in (s_key
                            for s_key in new_sample_sub_groups
                            if s_key in old_sample_sub_groups):
                old_alt_id = old_sample_data.loc[
                        old_sample_sub_groups[sub_key]].alt_sub_sample_id[0]
                sample_data.loc[
                        new_sample_sub_groups[sub_key],
                        "alt_sub_sample_id"] = old_alt_id

            for sub_key in (skey
                            for skey in new_sample_sub_groups
                            if skey not in old_sample_sub_groups):
                raise RuntimeError(
                        "Use if given sample names and conflict resolution through"
                        " longest common prefix is not implemented yet!!!")

        new_samples = sample_data.loc[
                sample_data.alt_sub_sample_id == "PLACE_HOLDER"].copy()
        new_sample_groups = new_samples.groupby(
                level=["path", "unambig_id"]).groups
        for (_id, (path, unambig)) in enumerate(new_sample_groups):
            main_name = "Sample_{nid}".format(nid=_id+1+num_old_samples)
            sample_data.loc[
                    new_sample_groups[(path, unambig)],
                                      "alt_sample_id"] = main_name
            sub_groups = sample_data[
                    sample_data.alt_sample_id == main_name].groupby(
                            level=["ambig_id"]).groups
            if len(sub_groups) == 1:
                # Easy Case when sample not split between lanes or in
                # multiple files with differing running number
                sample_data.loc[sample_data.alt_sample_id == main_name,
                                "alt_sub_sample_id"] = main_name
            else:
                for (_id, ambig) in enumerate(sub_groups):
                    sample_data.loc[((sample_data.alt_sample_id == main_name) &
                                    (sample_data.ambig_id == ambig)),
                                    "alt_sub_sample_id"] = "{sid}.{nid}".format(
                                            sid=main_name, nid=_id+1)
        if (sample_data["alt_sub_sample_id"] == "PLACE_HOLDER").any():
            raise RuntimeError("Some unique ids could not assigned")
 

    def register_filename_pattern_guide(self, guide):
        self.filename_pattern_guide = guide

    def register_read_id_pairings(self, pairings):
        self.read_id_pairings = pairings




