import pytest

from snakewrap.wrapper import *


class Test_Config():

    def test_01_create_config(self, tmpdir):
        conf = ConfigManager()
        assert isinstance(conf, ConfigManager)

    def test_02_fill_config(self):
        conf = ConfigManager()
        val = 1337
        conf.set("some_opt",  val)
        assert conf.get("some_opt") is val

        

class Test_Exceptions():

    def test_snakemake_run_error(self):
        with pytest.raises(SNAKEMAKE_RUN_ERROR):
            raise SNAKEMAKE_RUN_ERROR(-1)

    def test_config_option_not_found(self):    
        with pytest.raises(ConfigOptionNameNotFound):
            raise ConfigOptionNameNotFound("someopt")

    def test_type_not_argument_parser(self):
        with pytest.raises(TypeNotArgumentParser):
            raise TypeNotArgumentParser(type(str))

    def test_arguments_not_parsed(self):
        with pytest.raises(ArgumentsNotParsedError):
            raise ArgumentsNotParsedError()

    def test_configuration_error(self):
        with pytest.raises(CONFIGURATION_ERROR):
            raise CONFIGURATION_ERROR(errlist=["Test ERROR"])
    def test_configuration_errors(selfs):
        with pytest.raises(CONFIGURATION_ERROR):
            raise CONFIGURATION_ERROR(errlist=["Test ERROR", "And Another"])

    def test_sample_config_error(self):
        with pytest.raises(SAMPLE_CONFIG_ERROR):
            raise SAMPLE_CONFIG_ERROR(errlist=["one test error"])
    
    def test_sample_config_errors(self):
        with pytest.raises(SAMPLE_CONFIG_ERROR):
            raise SAMPLE_CONFIG_ERROR(errlist=["one test error",
                                               "and the second"])


class Test_Snakeapp():
    
    def test_incomplete_subclassing(self):
        class App(SnakeApp):
            def __init__(self):
                super().__init__()
        with pytest.raises(TypeError):
            app = App()

    def test_dummy_app_no_argparse(self):
        class App(SnakeApp):
            def __init__(self):
                super().__init__()
        
            def args_to_config_dict(self):
                config = vars(self.args)
                return config

            def get_argparser(self):
                return 
        with pytest.raises(TypeNotArgumentParser):
            app = App()


    def test_dummy_app(self, tmp_path):
        dummy_dir = tmp_path / "dummy_test"
        dummy_dir.mkdir()
        log_file = dummy_dir / "dummy.log"
        snake_file = dummy_dir / "Snakefile"

        snake_file.write_text("""
            # Dummy Snakefile
            
            """.strip())

        class App(SnakeApp):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
        
            def args_to_config_dict(self):
                config = vars(self.args)
                return config

            def get_argparser(self):
                parser = argparse.ArgumentParser()
                parser.add_argument("--input")
                parser.add_argument("--config")
                parser.add_argument("-o", "--outdir", type=os.path.realpath, default=".")
                return parser
            
            def init_setup(self):
                if self.args.outdir is not None:
                    self.workdir = self.args.outdir
                

        app = App("dummyapp")
        assert (app.appname == "dummyapp")
        app.set_snakefile(str(snake_file))
        app.add_log_file(log_file)
        app.run(["--input", str(dummy_dir), "-o", str(dummy_dir)])
    
    def test_dummy_app_syntax_error(self, tmp_path):
        dummy_dir = tmp_path / "dummy_test"
        dummy_dir.mkdir()
        log_file = dummy_dir / "dummy.log"
        snake_file = dummy_dir / "Snakefile"

        snake_file.write_text("""
            # Dummy Snakefile
            rule all:
            \toinput: 
            """.strip())

        class App(SnakeApp):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
        
            def args_to_config_dict(self):
                config = vars(self.args)
                return config

            def get_argparser(self):
                parser = argparse.ArgumentParser()
                parser.add_argument("--input")
                parser.add_argument("--config")
                parser.add_argument("-o", "--outdir", type=os.path.realpath, default=".")
                return parser
            
            def init_setup(self):
                if self.args.outdir is not None:
                    self.workdir = self.args.outdir
                

        app = App("dummyapp")
        assert (app.appname == "dummyapp")
        app.set_snakefile(str(snake_file))
        app.add_log_file(log_file)
        with pytest.raises(SNAKEMAKE_RUN_ERROR):
            try:
                app.run(["--input", str(dummy_dir), "-o", str(dummy_dir)])
            except SNAKEMAKE_RUN_ERROR as e:
                raise e

