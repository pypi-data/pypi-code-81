import pytest
import random
from snakewrap.sample_manager.illumina_sample_manager import *
from collections import Counter


class RunIds():
    def __init__(self, run_id_list, to_string_fun):
        self.run_id_list = run_id_list
        self.run_id_to_string = to_string_fun

    def get_id_fun_gen(self):
        return ( 
                lambda *args, **kwargs: self.run_id_to_string(val_list, *args, **kwargs) 
                for val_list in self.run_id_list) 




def get_base_run_ids(num=20, dates=[20201001], start_labcount=1):
    dates = sorted(random.choices(dates, k=num)) 
    years = [str(x)[2:4] for x in dates]
    y_change = sorted(set(years))
    users = sorted(random.choices(
        ["mg1", "zbr2", "foo", "bar", "bas","ban","usr"], k=num))
    user_count = Counter(users)
    customids = []
    for user in sorted(set(users)):
        customids.extend(
            ["{user}-{n:03d}".format(n=n, user=user)
             for n in range(1, 1 + user_count[user])])
    custom_ids = [ "{date}-{uid}".format(date=date, uid=uid) 
                  for date, uid  in zip(dates, customids)]

    count = Counter(years)
    labids = []
    laneids = ["L001"] * num
    scounters = ["S{n}".format(n=n) for n in range(1, 1+num)]
    
    for year in y_change:
        labids.extend(
            ["{year}-{n:04d}".format(n=n, year=year) 
             for n in range(start_labcount, 
                            start_labcount + count[year])])
    def to_string_fun(id_item, 
                   date=None, labId=None, customId=None, sampleId=None,
                   laneId=None, read="R1", running="001", sep="_" ):
        date = id_item[0] if date is None else str(date)
        labId = id_item[1] if labId is None else str(labId)
        customId = id_item[2] if customId is None else str(customId)
        sampleId = id_item[3] if sampleId is None else str(sampleId)
        laneId = id_item[4] if laneId is None else str(laneId)
        return sep.join([date,labId,customId,sampleId,laneId,read,running])

    sample_base = [[str(date), lab_id, cid,  scount, lane_id] 
                   for date, lab_id, cid, scount, lane_id 
                   in zip(dates, labids, customids, scounters, laneids)]
    return RunIds(sample_base, to_string_fun)





class TestBasicClassFunctionality():
    
    @pytest.fixture(scope="class") 
    def get_basic_test_dir_with_sample_sheet(self,tmp_path_factory):
        read = """
            @SIM:1:FCX:1:15:6329:1045 {read}:N:0:2
            TCGCACTCAACGCCCTGCATATGACAAGACAGAATC
            +
            <>;##=><9=AAAAAAAAAA9#:<#<;<<<????#=
            """.strip()
        


        main_test_dir = tmp_path_factory.mktemp("basic_test")

        # first_run 
        first_run_dir = main_test_dir / "first_run"
        first_run_dir.mkdir()
        first_run_ids = get_base_run_ids()
        rid_list = first_run_ids.get_id_fun_gen()
        for id_fun in rid_list:
            some_fastq_R1 = first_run_dir / "{base}.fastq".format(base=id_fun(read="R1")) 
            some_fastq_R1.write_text(read.format(read=1))
            some_fastq_R2 = first_run_dir / "{base}.fastq".format(base=id_fun(read="R2"))
            some_fastq_R2.write_text(read.format(read=2))

        return main_test_dir
    

    def test_class_instatiation(self):
        sman = IlluminaSampleManager()
        assert isinstance(sman, IlluminaSampleManager)
    
    def test_name_parser_someinstitute1(self):
        sman = IlluminaSampleManager()
        sman.check_and_add_fastq(["20201008_22-1234_DFGAG1231241_S112_L001_R1_001.fastq.gz"],None)
        sman.check_and_add_fastq(["20201008_22-1234_DFGAG1231241_S112_L001_R2_001.fastq.gz"],None)
        print(sman.pandas_parse_store["match"])
        assert all(sman.pandas_parse_store["match"] == "illumina_some_institute_1") is True
    
    def test_name_parser_someinstitute2(self):
        sman = IlluminaSampleManager()
        sman.check_and_add_fastq(["20201008_22-12344_DFGAG1231241_S112_L001_R1_001.fastq.gz"],None)
        sman.check_and_add_fastq(["20201008_22-12344_DFGAG1231241_S112_L001_R2_001.fastq.gz"],None)
        print(sman.pandas_parse_store["match"])
        assert all(sman.pandas_parse_store["match"] == "illumina_some_institute_1") is True
    
    def test_name_parser_someinstitute3(self):
        sman = IlluminaSampleManager()
        sman.check_and_add_fastq(["20201008_22-12344-G_DFGAG1231241_S112_L001_R1_001.fastq.gz"],None)
        sman.check_and_add_fastq(["20201008_22-12344-G_DFGAG1231241_S112_L001_R2_001.fastq.gz"],None)
        print(sman.pandas_parse_store["match"])
        assert all(sman.pandas_parse_store["match"] == "illumina_some_institute_1") is True

    def test_name_parser_illumina1(self):
        sman = IlluminaSampleManager()
        sman.check_and_add_fastq(["DFGAG1231241_S112_L001_R1_001.fastq.gz"],None)
        sman.check_and_add_fastq(["DFGAG1231241_S112_L001_R2_001.fastq.gz"],None)
        print(sman.pandas_parse_store["match"])
        assert all(sman.pandas_parse_store["match"] == "illumina1") is True

    def test_name_parser_illumina2(self):
        sman = IlluminaSampleManager()
        sman.check_and_add_fastq(["DFGAG1231241_S112_R1_001.fastq.gz"],None)
        sman.check_and_add_fastq(["DFGAG1231241_S112_R2_001.fastq.gz"],None)
        print(sman.pandas_parse_store["match"])
        assert all(sman.pandas_parse_store["match"] == "illumina2") is True

    def test_name_parser_illumina3(self):
        sman = IlluminaSampleManager()
        sman.check_and_add_fastq(["DFGAG1231241_S112_L001_R1.fastq.gz"],None)
        sman.check_and_add_fastq(["DFGAG1231241_S112_L001_R2.fastq.gz"],None)
        print(sman.pandas_parse_store["match"])
        assert all(sman.pandas_parse_store["match"] == "illumina3") is True

    def test_name_parser_illumina4(self):
        sman = IlluminaSampleManager()
        sman.check_and_add_fastq(["DFGAG1231241_S112_R1.fastq.gz"],None)
        sman.check_and_add_fastq(["DFGAG1231241_S112_R2.fastq.gz"],None)
        print(sman.pandas_parse_store["match"])
        assert all(sman.pandas_parse_store["match"] == "illumina4") is True

    def test_name_parser_illumina_fallback(self):
        sman = IlluminaSampleManager()
        sman.check_and_add_fastq(["DFGAG1231241S112_R1.fastq.gz"],None)
        sman.check_and_add_fastq(["DFGAG1231241S112_R2.fastq.gz"],None)
        print(sman.pandas_parse_store["match"])
        assert all(sman.pandas_parse_store["match"] == "illumina4") is True
    
    def test_name_parser_illumina_fallback(self):
        sman = IlluminaSampleManager()
        sman.check_and_add_fastq(["DFGAG1231241S112_R1_Somethings_never_change.fastq.gz"],None)
        sman.check_and_add_fastq(["DFGAG1231241S112_R2_Somethings_never_change.fastq.gz"],None)
        print(sman.pandas_parse_store["match"])
        assert all(sman.pandas_parse_store["match"] == "illumina_fallback") is True

    def test_basic_parser_from_folder(
            self,
            get_basic_test_dir_with_sample_sheet):
        folder = get_basic_test_dir_with_sample_sheet / "first_run"
        sman = IlluminaSampleManager()
        sman.parse_samples([[str(folder)]])
        assert sman.total_seen_files is 40
        sman.process_samples()

    

