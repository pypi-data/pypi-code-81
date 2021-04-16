import abc
import asyncio
import copy
import inspect
import time
from typing import Callable, Dict, Any, List, Union
from toposort import toposort

class Perform(object):

    def __init__(self, id: str, should_verify: bool) -> None:
        self.id = id
        self.execution_time = None
        self.should_verify = should_verify

    @abc.abstractclassmethod
    async def fn(self, input: Dict[str, Any]) -> Any:
        raise NotImplementedError()

    @staticmethod
    def __verify_fn_inputs__(fn: Callable, actual_input: Dict[str, Any]):
        """
            Verify input type of fn such that the actual input has same type.
        """

        for k, param in dict(inspect.signature(fn).parameters).items():
            if not k in actual_input:
                raise Exception(f"Argument '{k}' is missing when computing function {fn}")
            
            actual_input_type = type(actual_input[k])
            expected_input_type = param._annotation
            if not expected_input_type == Any:
                if not actual_input_type == expected_input_type:
                    raise TypeError(f"For function {fn}: Expected input type {expected_input_type} but got {actual_input_type}.")

    @staticmethod
    def __verify_fn_output__(fn: Callable, acutal_output: Any):
        """
            Verify return type of fn such that the output has same type.
        """
        expected_output_type = inspect.signature(fn).return_annotation
        actual_output_type = type(acutal_output)
        try:
            if not expected_output_type == Any:
                if not expected_output_type.__name__ == actual_output_type.__name__:
                    raise TypeError(
                        f"For function {fn}: Expected output type was {expected_output_type} but got {actual_output_type}."
                    )
        except Exception as e:
            raise Exception(f"Could not type check output for function {fn}: {e}")

    async def __timeit__(self, async_method):
        tic = time.time()
        result = await async_method
        self.execution_time = time.time() - tic
        return result

    @staticmethod
    def _fit_input_kwargs_from_fn(fn: Callable, input: Dict[str, Any]):
        fn_keys = dict(inspect.signature(fn).parameters)
        kwargs = input if 'kwargs' in fn_keys else {k:v for k, v in input.items() if k in fn_keys}
        args = list(input.values()) if 'args' in fn_keys else []
        return args, kwargs
            
    async def _perform(self, input: Dict[str, Any] = {}) -> Any:
        if self.should_verify:
            Piece.__verify_fn_inputs__(self.fn, actual_input=input)
        
        args, kwargs = self._fit_input_kwargs_from_fn(self.fn, input)
        output = await self.__timeit__(
            async_method=self.fn(*args, **kwargs)
        )
        if self.should_verify:
            Piece.__verify_fn_output__(self.fn, acutal_output=output)
        return output

    async def perform(self, input: Union[Dict[str, Any], List[Dict[str, Any]]] = {}) -> Any:
        if isinstance(input, list):
            performers = [self._perform(input=inp) for inp in input]
            result = await asyncio.gather(*performers, return_exceptions=True)
        else:
            result = await self._perform(input=input)
        return result

    def copy(self):
        return copy.deepcopy(self)

class Piece(Perform):

    def __init__(self, id: str, fn: Callable, inputs: dict = {}, should_verify: bool = False) -> None:
        super().__init__(id=id, should_verify=should_verify)
        Piece.__validate_fn_input__(fn=fn)
        Piece.__validate_fn_output__(fn=fn)

        self.fn = fn
        self.inputs = inputs

    @staticmethod
    def __validate_fn_input__(fn: Callable):
        """
            Validates such that expected input type of fn is same as been given on init.
        """
        parameters = dict(inspect.signature(fn).parameters)
        if not parameters:
            raise Exception(f"Function {fn} is missing inputs. A Piece-function must have at least one input.")

        for _, param in parameters.items():
            if param._annotation == inspect._empty:
                raise TypeError(f"Input arguments cannot be untyped. In function {fn}, got '{param._annotation}'")

    @staticmethod
    def __validate_fn_output__(fn: Callable):
        """
            Validates such that expected output type of fn is same as been given on init.
        """
        expected_output_type = inspect.signature(fn).return_annotation
        if expected_output_type == inspect._empty:
            raise TypeError(f"Output type cannot be untyped. In function {fn}, got '{expected_output_type}'")

    async def _perform(self, input: Dict[str, Any]) -> Any:
        return await super()._perform(input={**self.inputs, **input})

class PerformExecutor(object):

    def __init__(self, execute: Callable, *args, **kwargs) -> None:
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

class SimultaneousPerform(Perform):

    def __init__(self, id: str, should_verify: bool, executor: PerformExecutor) -> None:
        super().__init__(id, should_verify)
        self.executor = executor

class Competition(SimultaneousPerform):

    """
        A Competition is a race between two or more performers of whom is completed
        first. Whenever one is done, results are returned and the others are
        cancelled.
    """

    def __init__(
        self, 
        id: str, 
        pieces: List[Perform], 
        should_verify: bool = False, 
        executor: PerformExecutor = PerformExecutor(asyncio.wait, return_when=asyncio.FIRST_COMPLETED),
        ) -> None:
        super().__init__(id=id, should_verify=should_verify, executor=executor)
        self.pieces = pieces
        self.outs = {}

    async def fn(self, **kwargs) -> Any:        
        tasks = []
        for piece in self.pieces:
            task = asyncio.create_task(piece.perform(kwargs))
            task.id = piece.id
            tasks.append(task)

        self.outs = {}
        result = None
        try:
            while tasks:
                done, pending = await self.executor.execute(
                    tasks,
                    *self.executor.args,
                    **self.executor.kwargs,
                )

                for finished in done:
                    
                    try:
                        result = finished.result()
                        if isinstance(result, Exception):
                            tasks = pending
                            self.outs[finished.id] = result
                            continue
                            
                        for task in pending:
                            self.outs[task.id] = None
                            task.cancel()

                        return result

                    except Exception as e:
                        self.outs[finished.id] = e
                        tasks = pending
                        continue
                    
        except Exception as e:
            raise e

class Dependency(object):

    """
        A Dependency is connecting two pieces on one agreed argument.
        E.g., piece_id="1" is dependent on dependen_on_id="0" and connected on
        argument connected_on="arg", meaning that the result from "0" will be propagated
        to "1" by "arg".
    """

    def __init__(self, piece_id: str, dependent_on_id: str, connected_on: str) -> None:
        self.piece_id = piece_id
        self.dependent_on_id = dependent_on_id
        self.connected_on = connected_on

class Composition(SimultaneousPerform):

    """
        A Composition is a composition of pieces, sub classing Perform and running according to the piece's dependencies.
    """

    def __init__(
        self, 
        id: str, 
        pieces: List[Piece], 
        dependencies: List[Dependency] = [], 
        should_verify: bool = False,
        executor: PerformExecutor = PerformExecutor(asyncio.gather, return_exceptions=True),
        ) -> None:
        super().__init__(id=id, should_verify=should_verify, executor=executor)
        self.pieces = pieces
        self.dependencies = dependencies
        self._pieces_dict = {piece.id: piece for piece in pieces}
        self._dependencies_dict = Composition._key_dependencies(
            pieces=pieces, 
            dependencies=dependencies,
        )
        self.piece_running_order = list(
            toposort(
                Composition._toposort_dependencies(
                    pieces=pieces,
                    dependencies=dependencies,
                ),
            ),
        )
        self.__verify_composition__()
        self.last_performer = self.__select_last_performer__()
        self.outs = {}

    def __verify_composition__(self):
        """
            A Composition must have a single output.
        """
        end_performers = [list(x) for x in self.piece_running_order][-1]
        n_end_performers = len(end_performers)
        if not n_end_performers == 1:
            raise Exception(f"A Composition must end with one single performer. Composition {self.id} has {n_end_performers}: {end_performers}")

    def __select_last_performer__(self):
        return list(self.piece_running_order[-1])[0]

    @staticmethod
    def _toposort_dependencies(pieces: List[Piece], dependencies: List[Dependency]):

        depend = {piece.id: set() for piece in pieces}
        for dependency in dependencies:
            depend[dependency.piece_id].add(dependency.dependent_on_id)

        return depend

    @staticmethod
    def _key_dependencies(pieces: List[Piece], dependencies: List[Dependency]):

        depend = {piece.id: [] for piece in pieces}
        for dependency in dependencies:
            depend[dependency.piece_id].append((dependency.dependent_on_id, dependency.connected_on))
        return depend

    async def fn(self, **kwargs) -> Any:
        
        self.outs = {}
        for piece_paras in self.piece_running_order:
            
            tasks = []
            for piece_key in piece_paras:

                try:
                    input_args = {**{}, **kwargs}
                    if piece_key in self._dependencies_dict:
                        for target_piece_key, piece_arg in self._dependencies_dict[piece_key]:
                            input_args.update({piece_arg: self.outs[target_piece_key]})

                    tasks.append(asyncio.create_task(self._pieces_dict[piece_key].perform(input_args)))
                except Exception as e:
                    raise Exception(f"Could not construct task from piece function '{piece_key}' because of error: {e}")

            tasks += self.executor.args
            piece_results = await self.executor.execute(*tasks, **self.executor.kwargs)
            for piece_result, piece_key in zip(piece_results, piece_paras):
                self.outs[piece_key] = piece_result

        return self.outs[self.last_performer]

    def performer_results(self):
        return self.outs