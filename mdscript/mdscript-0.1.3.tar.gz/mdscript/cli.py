import click
from mdscript.runner import Runner
# todo: deprecated

@click.command()
@click.option('--dirpath', '-d', prompt="Dirpath", type=str)
@click.option('--tests', '-t', prompt="Run tests ?", is_flag=True)
def run(dirpath: str, tests: bool):
    run_api(dirpath=dirpath, run_tests=tests)

def run_api(dirpath: str, run_tests: bool):
    runner = Runner()
    runner.run_watch(dirpath=dirpath, run_tests=run_tests)

