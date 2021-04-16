from datetime import datetime
from pathlib import Path
from subprocess import Popen, PIPE

from benchmark.profilers import tools
from benchmark.profilers.base import BaseProfiler
from benchmark.profilers.measured_value_type import MeasuredValueType
from benchmark.profilers.profiler_type import ProfilerType


class MProfProfiler(BaseProfiler):
    @property
    def measured_value(self):
        return MeasuredValueType.memory.value

    @property
    def name(self):
        return ProfilerType.mprof.value

    def __init__(self, c) -> None:
        super().__init__(c)

    def prepare_paths(self):
        p = self.config.get_run_output_filename_pattern()
        data_dir = Path(p).parent
        data_dir.mkdir(parents=True, exist_ok=True)

        p = self.config.get_plot_output_filename_pattern()
        plot_dir = Path(p).parent
        plot_dir.mkdir(parents=True, exist_ok=True)

    def run(self, *args):
        benchmark_filepath, description = args
        self.prepare_paths()

        pattern = self.config.get_run_output_filename_pattern()
        output_filename = pattern.format(date=tools.get_current_time(), name=benchmark_filepath.stem)

        args = [
            "mprof",
            "run",
            "--interval",
            self.config.get_interval(),
            "--output",
            output_filename,
            str(benchmark_filepath),
        ]

        if self.config.config_benchmark:
            args.append(self.config.config_benchmark)

        start = datetime.now()

        proc = Popen(args, stderr=PIPE, stdout=PIPE)
        pid = proc.pid

        print(f"{start.isoformat()} PID: {pid} Start run_mprof: {' '.join(args)}")

        out, err = proc.communicate()

        end = datetime.now()
        delta = end - start
        print(f"{end.isoformat()} PID: {pid} End. Duration {delta}")

        output = Path(output_filename)
        if description and output.exists():
            with output.open('r') as f:
                lines = f.readlines()

            with output.open('w') as f:
                lines.insert(0, f'{description}\n')
                f.writelines(lines)

        if err:
            print("---------------------------- Benchmark run info ------------------------------")
            print(", ".join(args))
            print("============================= Captured stderr call =============================")
            print(err.decode("utf-8"))
            print("=" * 80)

        if out:
            out = out.decode("utf-8")

        return args, out

    def plot_benchmarks(self):
        self.prepare_paths()

        pattern = self.config.get_plot_output_filename_pattern()
        plots_dir = Path(pattern).parent

        fn = self.config.get_run_output_filename_pattern()
        data_dir = Path(fn).parent

        data_files_to_plot = [fn for fn in data_dir.iterdir()]

        for plot_filename in plots_dir.iterdir():
            data_filename = plot_filename.stem[15:]
            data_files_to_plot = [data_file for data_file in data_files_to_plot if data_file.stem != data_filename]

        args = [
            {
                'data_filepath': str(fn),
                'title': fn.stem,
                'output_filename': pattern.format(date=tools.get_current_time(), name=fn.stem)
            }
            for fn in data_files_to_plot]
        return tools.multithreading(self.plot, args, 5)

    def plot(self, kwargs):
        data_filepath = kwargs.get('data_filepath')
        title = kwargs.get("title", "")
        output_filename = kwargs.get("output_filename", "")

        args = [
            "mprof",
            "plot"
        ]

        if output_filename:
            args.append("--output")
            args.append(output_filename)

        if title:
            args.append("--title")
            args.append(title)

        args.append(data_filepath)

        print(f"plot_mprof: {' '.join(args)}")

        with Popen(args, stderr=PIPE, stdout=PIPE) as proc:
            out, err = proc.communicate()

        if err:
            print(err.decode("utf-8"))

        out = out.decode("utf-8")

        return out

    def get_benchmarks_results(self):
        pattern = self.config.get_run_output_filename_pattern()
        dir_with_result = Path(pattern).parent

        if not dir_with_result.exists():
            return []

        results = []

        for file_with_result in dir_with_result.iterdir():
            data = []
            result = {
                'name': file_with_result.stem,
                'description': None,
                'data': data
            }
            results.append(result)

            with open(file_with_result, 'r') as f:

                first_line = f.readline()
                if not first_line.startswith('CMDLINE'):
                    result['description'] = first_line.strip()
                    f.readline()  # cmdline skip

                line = f.readline()

                while line:
                    _, mem_mib, timestamp_sec = line.split(" ")
                    mem_mib = float(mem_mib)
                    timestamp_sec = float(timestamp_sec)
                    timestamp_ms = timestamp_sec * 1000.0
                    datum = {
                        'mem_mib': mem_mib,
                        'timestamp_sec': timestamp_sec,
                        'timestamp_ms': timestamp_ms,
                        'v_axis': mem_mib,
                        'h_axis': timestamp_ms,
                    }
                    data.append(datum)
                    line = f.readline()

        return results
