from benchmark.config.config_manager import ConfigManager
from benchmark.profilers.prof_manager import ProfilersManager
from benchmark.profilers.profiler_type import ProfilerType, convert_to_profiler_type

config_manager = ConfigManager("./benchmark/config.ini")
config = config_manager.basic_config

profilers_manager = ProfilersManager(config_manager)


def create_getter(what):
    cache = {}

    def get_or_create():
        manager_name = what
        if cache.get(manager_name, None) is None:
            if manager_name == 'report_manager':
                from benchmark.reporting.report_manager import ReportManager
                cache[manager_name] = ReportManager(config_manager)

            elif manager_name == 'storage':
                from benchmark.storage import Storage
                cache[manager_name] = Storage(config_manager.basic_config)

        return cache.get(manager_name)

    return get_or_create


get_storage = create_getter('storage')
get_report_manager = create_getter('report_manager')


def print_benchmarks_and_profilers():
    for prof_type in config.get_available_profilers():
        print_benchmarks_by_profiler(prof_type)


def print_benchmarks_by_profiler(input_prof_type):
    prof = profilers_manager.get_profiler_by_type(input_prof_type)
    if prof.name in config.get_available_profilers():
        print("-" * 80)
        print(f'[Profiler]: {prof.name}')
        print(f'[Benchmarks]:')
        print("\n".join([f"\t{filename.name}" for filename in prof.get_available_benchmarks()]))
        print("-" * 80)
    else:
        print(f"No have profiler: {input_prof_type}")


def process_benchmark(bench_name, concrete_prof=None, is_print_out=False, description=""):
    if concrete_prof:
        found = False
        for prof_type in config.get_available_profilers():
            if prof_type == concrete_prof:
                prof = profilers_manager.get_profiler_by_type(prof_type)
                out = prof.run_if_can(bench_name, description)
                found = True
                is_print_out and print(out)
                break

        if not found:
            raise Exception(f"Profiler {concrete_prof} doesn't found.")

    else:
        for prof_type in config.get_available_profilers():
            prof = profilers_manager.get_profiler_by_type(prof_type)
            out = prof.run_if_can(bench_name, description)
            is_print_out and print(out)


def process_benchmarks_by_measured_value(measured_value, is_print_out=False):
    available_measures = config.get_available_measures()
    if measured_value in available_measures:
        available_profilers = config.get_available_profilers()
        profs = profilers_manager.get_profilers_by_measured_value(measured_value)
        for prof in profs:
            profiler_name = prof.name
            if profiler_name in available_profilers:
                process_benchmarks(profiler_name, is_print_out)
    else:
        print(f'[WARN] Measure "{measured_value}" not available.')


def process_benchmarks_by_profiler(profiler_name, is_print_out=False):
    available_profilers = config.get_available_profilers()
    if profiler_name in available_profilers:
        process_benchmarks(profiler_name, is_print_out)
    else:
        print(f'[WARN] Profiler "{profiler_name}" not available.')


def process_benchmarks(prof_type, is_print_out=False):
    stdout = None
    prof_type = convert_to_profiler_type(prof_type)
    if prof_type == ProfilerType.timeit:
        stdout = profilers_manager.timeit_prof.run_benchmarks()
        get_storage().set_list_of_benches_results(stdout)
    elif prof_type == ProfilerType.pytest:
        stdout = profilers_manager.pytest_prof.run_benchmarks()
    elif prof_type == ProfilerType.mprof:
        stdout = profilers_manager.mprof_prof.run_benchmarks()

    if is_print_out and stdout:
        print_stdout(stdout)


def print_stdout(stdout):
    if isinstance(stdout, list):
        [print_stdout(out) for out in stdout]
    elif isinstance(stdout, tuple):
        args, out = stdout
        print("---------------------------- Benchmark run info ------------------------------")
        print(", ".join(args))
        print("------------------------------ Captured stdout -------------------------------")
        print_stdout(out)
    else:
        print(stdout)


def process_plotting():
    profilers_manager.mprof_prof.plot_benchmarks()


def process_reporting():
    results = get_storage().get_list_all() + profilers_manager.mprof_prof.get_benchmarks_results()
    get_report_manager().dump_report(results)
