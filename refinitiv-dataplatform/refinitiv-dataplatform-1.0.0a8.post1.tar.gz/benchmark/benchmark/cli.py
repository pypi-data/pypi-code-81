"""
Benchmark.

Usage:
    benchmark run <benchmark_name> [--prof <profiler> --log --config <str>  --bench-config <str>  --desc <str>]
    benchmark (--measure <measured_value>  |  --prof <profiler>)  [--log  --config <str>  --bench-config <str>]
    benchmark list [<profiler>]
    benchmark plot
    benchmark reporting
    benchmark -h | --help

Options:
  -h, --help                        Show this screen.
  --measure MEASURED_VALUE, -m MEASURED_VALUE
                                    Run benchmarks by time or memory measured value
  --prof PROFILER                   Run benchmarks by profiler used
  --desc str, -d str                Description of the benchmark, used to describe the result data
  --log, -l                         Is printing log to console
  --config str, -c str              Config from console
  --bench-config str, -b str        Config for a benchmark
"""

from docopt import docopt
from benchmark import app
from benchmark.app import config_manager


def main():
    args = docopt(__doc__)

    config_manager.parse_config_console(args.get("--config"))
    config_manager.parse_config_benchmark(args.get("--bench-config"))

    profiler = args.get("--prof")
    measured_value = args.get("--measure")
    is_print_out = args.get("--log")

    if args.get('list'):
        if not profiler:
            app.print_benchmarks_and_profilers()
        else:
            app.print_benchmarks_by_profiler(profiler)

    elif args.get('run'):
        app.process_benchmark(args.get("<benchmark_name>"), profiler, is_print_out, args.get("--desc"))

    elif measured_value:
        app.process_benchmarks_by_measured_value(measured_value, is_print_out)

    elif profiler:
        app.process_benchmarks_by_profiler(profiler, is_print_out)

    elif args.get('plot'):
        app.process_plotting()

    elif args.get('reporting'):
        app.process_reporting()
