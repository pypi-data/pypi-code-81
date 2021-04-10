import psutil
import sys
import time

from multiprocessing import Manager
from concurrent.futures import ProcessPoolExecutor

from collections import namedtuple

ResourceTrace = namedtuple('ResourceTrace', ['t_mem', 'mem', 't_cpu', 'cpu'])


class SamplingResourceMonitor:
    def __init__(self, mem_frq=10., cpu_frq=10.):
        self.mem_sleep_sec = 1.0 / mem_frq
        self.cpu_sleep_sec = 1.0 / cpu_frq
        self.baseline_time = time.time()
        self.baseline_mem = psutil.virtual_memory().free
        self.t_mem = []
        self.mem = []
        self.t_cpu = []
        self.cpu = []
        self.mb_factor = 1.0 / (1024.0 ** 2)
        self.memory_snapshot()
        self.cpu_snapshot()

    def memory_snapshot(self):
        self.t_mem.append(time.time() - self.baseline_time)
        self.mem.append(self.mb_factor *
                        (self.baseline_mem - (psutil.virtual_memory().free + sys.getsizeof(self))))

    def cpu_snapshot(self):
        self.t_cpu.append(time.time() - self.baseline_time)
        self.cpu.append(psutil.cpu_percent(interval=None, percpu=True))

    def measure_mem(self, event):
        while not event.is_set():
            self.memory_snapshot()
            time.sleep(self.mem_sleep_sec)
        return self.t_mem, self.mem

    def measure_cpu(self, event):
        while not event.is_set():
            self.cpu_snapshot()
            time.sleep(self.cpu_sleep_sec)
        return self.t_cpu, self.cpu


def profile_function(func, args=None, mem_frq=10., cpu_frq=10.):
    if args is None:
        args = []
    with Manager() as manager:
        e = manager.Event()
        with ProcessPoolExecutor() as executor:
            monitor = SamplingResourceMonitor(mem_frq=mem_frq, cpu_frq=cpu_frq)
            mem_proc = executor.submit(monitor.measure_mem, e)
            cpu_proc = executor.submit(monitor.measure_cpu, e)
            try:
                fn_proc = executor.submit(func, *args)
                print(fn_proc.result())
            finally:
                e.set()
            t_mem, mem = mem_proc.result()
            t_cpu, cpu = cpu_proc.result()
            return ResourceTrace(t_mem=t_mem, mem=mem, t_cpu=t_cpu, cpu=cpu)
