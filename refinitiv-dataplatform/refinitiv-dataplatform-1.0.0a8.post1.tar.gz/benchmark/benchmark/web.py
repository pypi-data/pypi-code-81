from fastapi import FastAPI
from starlette.requests import Request

import benchmark.manager as manager
import benchmark.storage as storage
import benchmark.config as config

app = FastAPI()


@app.get("/mprof-benchmark/run")
def run_mprof_benchmarks(request: Request):
    results = mprof_prof.run_mprof_benchmarks()
    return results


@app.get("/mprof-benchmark/plot")
def plot_mprof_benchmarks(request: Request):
    results = mprof_prof.plot_mprof_benchmarks()
    return results


@app.get("/pytest-benchmark/run")
def run_pytest_benchmarks(request: Request):
    results = pytest_prof.run_pytest_benchmarks()
    return results


@app.get("/pytest-benchmark/plot")
def plot_pytest_benchmarks():
    results = pytest_prof.plot_pytest_benchmarks()
    return results


@app.get("/benchmark/run")
def run_timeit_benchmarks():
    results = timeit_prof.run_benchmarks()
    storage.set_list_of_benches_results(results)
    return {"results": results}


@app.get("/benchmark/reporting")
def plot_timeit_benchmarks():
    manager.process_reporting()
    return {"results": data}


if __name__ == "__main__":
    import uvicorn

    port_str = config.get_web_port()
    port = int(port_str)
    uvicorn.run(config.get_web_app_name(),
                host=config.get_web_host(),
                port=port,
                log_level=config.get_web_log_level(),
                reload=True)
