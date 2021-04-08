import pytest
import os 
from snakewrap.utils import *


class TestGeneralErrorClasses():

    def test_DirectAbstractionCall(self):
        with pytest.raises(DirectAbstractMethodCallError):
            raise DirectAbstractMethodCallError("testing")

    def test_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            raise NotImplementedError("testing")

class TestToolInfo():
    def test_tool_info_creation(self):
        tinfo = ToolInfo("python")
    
    def test_tool_info_path_not_found(self):
        with pytest.raises(ToolInfoNotFoundError):
            tinfo = ToolInfo("unknown_tool_somewhere7264")

    def test_tool_path_finding(self):
        tinfo = ToolInfo("python")
        tinfo.get_tool_path()
        assert isinstance(tinfo.path, str)

    def test_tool_version_finding(self):
        tinfo = ToolInfo("python", ["python", "--version"])
        assert tinfo.version_set is True
        assert (tinfo.version == "UNKNOWN") is False
    
    def test_tool_version_finding_negativ(self):
        with pytest.raises(ToolInfoNotFoundError):
            tinfo = ToolInfo("python", ["pythom", "--version"])


class TestGeneralUtilityFuncts():
    def test_eprint(self):
        eprint("hallo")

    def test_mod_string(self):
        test_str = "test_str"
        if (version_info >= (3,0)):
            test_str = b"test_str"
        assert (mod_string(test_str) == "test_str") is True

    def test_realpathify(self):
        fun = lambda x : x
        gold_path = os.path.realpath("stuff")
        mod_fun = realpathify(fun)
        assert (mod_fun("stuff") == gold_path)  
        
    def test_realpathify_notfun(self):
        fun = "stuff"
        gold_path = os.path.realpath("stuff")
        mod_fun = realpathify(fun)
        with pytest.raises(ErrorRealpathifyNeedsCallable):
            mod_fun("stuff") 

    def test_temp_dir(self):
        with tmpdir() as _dir:
            assert os.path.isdir(_dir) is True

    def test_check_if_file(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        some_file = some_dir / "some_file.txt" 
        some_file.write_text("even has content")
        assert check_if_file(some_file) is some_file

    def test_check_if_file_negative(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        with pytest.raises(ValueError):
            check_if_file(os.path.join(some_dir,"not_a_real_file.txt"))
    
    def test_check_if_dir(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        assert check_if_directory(some_dir) is some_dir
    
    def test_check_id_dir_negative(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        with pytest.raises(ValueError):
            check_if_directory(some_dir) 

    def test_check_if_file_or_dir_dirtest(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        assert check_if_file_or_directory(some_dir) is some_dir
    
    def test_check_if_file_or_dir_filetest(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        some_file = some_dir / "some_file.txt" 
        some_file.write_text("even has content")
        assert check_if_file_or_directory(some_file) is some_file

    def test_check_if_fileor_dir_negative(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        with pytest.raises(ValueError):
            check_if_file_or_directory(os.path.join(some_dir,"not_a_real_file.txt"))

    def test_strip_empties(self):
        _input = [
        "The",
        "line",
        "",
        "after",
        "line",
        "should",
        "",
        "be",
        "removed"]
        gold_output = [
        "The",
        "line",
        "after",
        "line",
        "should",
        "be",
        "removed"]
        assert ("\n".join(strip_empty_lines(_input)) 
                == "\n".join(gold_output)) is True


class TestFileExtensionChecks():

    def test_tsv_checks(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        some_tsv_tsv = some_dir / "some_file.tsv" 
        some_tsv_tsv.write_text("even has content")
        some_tsv_tab = some_dir / "some_file.tab" 
        some_tsv_tab.write_text("even has content")

        assert (validate_tsv_ext(str(some_tsv_tsv)) 
                == str(some_tsv_tsv)) is True
        assert (validate_tsv_ext(str(some_tsv_tab)) 
                == str(some_tsv_tab)) is True

    def test_tsv_checks_wrong_name(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        some_tsv_tsv = some_dir / "some_file.tsb" 
        some_tsv_tsv.write_text("even has content")
        with pytest.raises(ValueError):
            validate_tsv_ext(str(some_tsv_tsv)) 
    
    def test_tsv_checks_not_exist(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        some_tsv_tsv = os.path.join(some_dir, "some_file.tsv") 
        with pytest.raises(ValueError):
            validate_tsv_ext(str(some_tsv_tsv)) 

    def test_fasta_checks(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        some_fasta_fasta = some_dir / "some_file.fasta" 
        some_fasta_fasta.write_text("even has content")
        some_fasta_fa = some_dir / "some_file.fa" 
        some_fasta_fa.write_text("even has content")

        assert (validate_fasta_ext(str(some_fasta_fasta)) 
                == str(some_fasta_fasta)) is True
        assert (validate_fasta_ext(str(some_fasta_fa)) 
                == str(some_fasta_fa)) is True

    def test_fasta_checks_wrong_name(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        some_fasta_fasta = some_dir / "some_file.tsb" 
        some_fasta_fasta.write_text("even has content")
        with pytest.raises(ValueError):
            validate_fasta_ext(str(some_fasta_fasta)) 
    
    def test_fasta_checks_not_exist(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        some_fasta_fasta = os.path.join(some_dir, "some_file.fasta") 
        with pytest.raises(ValueError):
            validate_fasta_ext(str(some_fasta_fasta)) 
    
    def test_gff_checks(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        some_gff_gff = some_dir / "some_file.gff" 
        some_gff_gff.write_text("even has content")

        assert (validate_gff_ext(str(some_gff_gff)) 
                == str(some_gff_gff)) is True

    def test_gff_checks_wrong_name(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        some_gff_gff = some_dir / "some_file.tsb" 
        some_gff_gff.write_text("even has content")
        with pytest.raises(ValueError):
            validate_gff_ext(str(some_gff_gff)) 
    
    def test_gff_checks_not_exist(self, tmp_path):
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        some_gff_gff = os.path.join(some_dir, "some_file.gff") 
        with pytest.raises(ValueError):
            validate_gff_ext(str(some_gff_gff)) 

class TestHashingMethods():
    
    def test_hash_strings(self):
        test_string = "This is a test"
        assert (hashstring(test_string) 
                == "c7be1ed902fb8dd4d48997c6452f5d7e509fbcdbe2808b16bcf4edce4c07d14e") is True 

    def test_hash_file(self, tmp_path):
        test_string = "This is a test"
        some_dir = tmp_path / "utils_test"
        some_dir.mkdir()
        some_fasta = some_dir / "some_file.fasta" 
        some_fasta.write_text(test_string)

        assert (hashfile(some_fasta) 
                == "c7be1ed902fb8dd4d48997c6452f5d7e509fbcdbe2808b16bcf4edce4c07d14e") is True 
