from typing import Dict, Tuple, Callable, Union, List
from broccoli_server.interface.worker import Worker, WorkContext
from broccoli_server.pipeline import StateUpdate
from broccoli_server.pipeline.pipeline_worker_class import PipelineWorkerClass


class WorkerCache(object):
    def __init__(self):
        self._module_cache = {}  # type: Dict[str, Callable]
        self._pipeline_func_cache = {}  # type: Dict[str, Callable]

    def register_module(self, module_name: str, constructor):
        self._module_cache[module_name] = constructor

    def register_pipeline_worker(self, worker_id: str, func):
        self._pipeline_func_cache[worker_id] = func

    def get_modules_names(self) -> List[str]:
        # pipeline funcs are not exposed so that they can't be initialized from web UI
        return list(sorted(self._module_cache.keys()))

    def load(self, name: str, args: Dict) -> Tuple[bool, Union[str, Worker]]:
        if name not in self._module_cache and name not in self._pipeline_func_cache:
            return False, f"Module {name} not found"

        if name in self._module_cache:
            clazz = self._module_cache[name]
            final_args = {}
            for arg_name, arg_value in args.items():
                final_args[arg_name] = arg_value
            try:
                obj = clazz(**final_args)
            except Exception as e:
                return False, str(e)
            return True, obj
        else:
            worker_id = name
            func = self._pipeline_func_cache[worker_id]

            # creating Worker class seems to work here compared to in application.py but why?
            class _Worker(PipelineWorkerClass):
                def get_id(self) -> str:
                    return worker_id

                def pre_work(self, context: WorkContext):
                    pass

                def process(self, context: WorkContext, documents: List[Dict]) -> List[StateUpdate]:
                    return func(context, documents)
            return True, _Worker(**args)
