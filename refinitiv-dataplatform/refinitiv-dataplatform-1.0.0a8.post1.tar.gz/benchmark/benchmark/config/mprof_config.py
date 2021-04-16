"""
mprof profiler.
https://github.com/pythonprofilers/memory_profiler

Usage: mprof [options]

Options:
  -h, --help            show this help message and exit
  --interval INTERVAL, -T INTERVAL
                        Sampling period (in seconds), defaults to 0.1
  --include-children, -C
                        Monitors forked processes as well (sum up all process memory)
  --multiprocess, -M    Monitors forked processes creating individual plots for each child (disables --python features)
  --exit-code, -E       Propagate the exit code
  --output FILENAME, -o FILENAME
                        File to store results in, defaults to 'mprofile_<YYYYMMDDhhmmss>.dat' in the current directory,
                        (where <YYYYMMDDhhmmss> is the date-time of the program start).
                        This file contains the process memory consumption, in Mb (one value per line).
"""

from benchmark.config.basic_config import BasicConfig
from docopt import docopt


class MProfConfig(BasicConfig):

    def get_run_output_filename_pattern(self):
        return self._get_option('profilers.mprof', 'run.output.filename')

    def get_plot_output_filename_pattern(self):
        return self._get_option('profilers.mprof', 'plot.output.filename')

    def get_interval(self):
        interval = self._get_option('--interval', fromc='console')

        if interval is not None:
            return interval

        return self._get_option('profilers.mprof', 'interval')

    def parse_config_console(self, argv):
        if not argv:
            return {}

        args = docopt(__doc__, argv)
        print('MProfConfig parsed console config.')
        self.config_console.update(args)
