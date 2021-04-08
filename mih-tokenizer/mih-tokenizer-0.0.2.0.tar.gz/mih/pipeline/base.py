# encoding: utf-8

import uuid
import json
import numpy as np
import pandas as pd

from collections import OrderedDict
from typing import List, Set, Dict, Union, Tuple, Optional, Any, Callable


# Define type aliases
Name = str
Required = List[Name]
Function = Callable[[Any],Any]
Args = List
Kwargs = Dict
FunctionTuple = Union[
    Tuple[Function],
    Tuple[Function, Args],
    Tuple[Function, Kwargs],
    Tuple[Function, Args, Kwargs],
    Tuple[Function, Args, Required],
    Tuple[Function, Kwargs, Required],
    Tuple[Function, Args, Kwargs, Required],
]

# Init default value
DEPEND_PREV_DEFAULT = True


class Step:

    def __init__(self, *args, **kwargs):
        self._id = str(uuid.uuid4())
        self.name = kwargs.pop('_name', self._id) # TODO: for required specify
        self.required = kwargs.pop('_required', [])
        self.args = args
        self.kwargs = kwargs
        self.outputs = None

    @property
    def info(self):
        return {
            'id': self._id,
            'name': self.name,
            'required': self.required,
            'args': self.args,
            'kwargs': self.kwargs,
            'outputs': self.outputs
        }

    @classmethod
    def from_callable(cls, _callable: Union[Callable, FunctionTuple]):
        obj = cls()
        if isinstance(_callable, Callable):
            obj._execute = _callable
        elif isinstance(_callable, (list, tuple, np.ndarray, pd.Series)):
            if 1 == len(_callable):
                obj._execute = _callable[0]
            elif 2 == len(_callable):
                function, _ = _callable
                if isinstance(function, Callable):
                    obj._execute = function
                    if isinstance(_, (list, tuple)):
                        obj.args = _
                    elif isinstance(_, dict):
                        obj.kwargs = _
                    else:
                        raise ValueError(
                            f"type of args or kwargs unknown: {type(_)}. "
                            f"Should be list, tuple or dict."
                        ) 
                else:
                    raise ValueError(
                        f"type of function unknown: {type(function)}. "
                        f"Should be Callable."
                    ) 
            elif 3 == len(_callable):
                function, t1, t2 = _callable
                if isinstance(function, Callable):
                    obj._execute = function
                    if isinstance(t1, (list, tuple)):
                        if isinstance(t2, dict):
                            obj.args = t1
                            obj.kwargs = t2
                        elif isinstance(t2, (list, tuple)):
                            obj.args = t1
                            obj.required = t2
                        else:
                            raise ValueError(
                                f"type of args, kwargs, required unknown: {type(t1), type(t2)}. "
                                f"Should be (list, dict), (list, list)."
                            ) 
                    elif isinstance(t1, dict):
                        if isinstance(t2, (list, tuple)):
                            obj.kwargs = t1
                            obj.required = t2
                        else:
                            raise ValueError(
                                f"type of kwargs, required unknown: {type(t1), type(t2)}. "
                                f"Should be (dict, dict)."
                            ) 
                    else:
                        raise ValueError(
                            f"type of args or kwargs unknown: {type(t1)}. "
                            f"Should be list, tuple or dict."
                        ) 
                else:
                    raise ValueError(
                        f"type of function unknown: {type(function)}. "
                        f"Should be Callable."
                    ) 
            elif 4 == len(_callable):
                obj._execute, obj.args, obj.kwargs, obj.required = _callable
            else:
                raise ValueError(
                    f"length of callable wrong: {len(_callable)}. "
                    f"Should be 1 to 4 for Tuple[Function, Args, Kwargs, Required]"
                ) 
        else:
            raise ValueError(
                f"type of callable unknown: {type(_callable)}. "
                f"Should be one of a Callable, list, tuple, np.ndarray or pd.Series."
            ) 
        return obj

    def meet(self, ready: Set[Name]):
        return not (set(self.required)-set(ready)) 

    def __call__(self, *args, **kwargs):
        kwargs.update(self.kwargs)
        self.outputs = self._execute(*(list(args)+list(self.args)), **kwargs)
        return self.outputs

    def _execute(self, *args, **kwargs):
        """
        Args:
            args (:obj:`list`):
                The arguments from dependency steps.
            kwargs (:obj:`dict`):
                The arguments given by user directly.
        """
        raise NotImplementedError


class StepPipeline:

    def __init__(self, base, callables: List[Union[Name, Step, FunctionTuple]], **kwargs):

        def build(callables: List[Union[Name, Step, FunctionTuple]], **kwargs) -> List[Step]:
            """
            Convert FunctionTuple to Steps.
            Parsing relations between Steps for not specified.
            """
            depend_prev = kwargs.get('depend_prev', DEPEND_PREV_DEFAULT)

            new_callables = []
            for i, step in enumerate(callables):
                if isinstance(step, str):
                    try:
                        step = Step.from_callable(getattr(self, step))
                    except:
                        step = Step.from_callable(getattr(base, step))
                elif not isinstance(step,Step) and isinstance(step, Callable):
                    step = Step.from_callable(step)
                elif isinstance(step, tuple):
                    if isinstance(step[0], str):
                        step = list(step)
                        try:
                            step[0] = getattr(self, step[0])
                        except:
                            step[0] = getattr(base, step[0])
                        step = Step.from_callable(tuple(step))
                    elif not isinstance(step[0],Step) and isinstance(step[0], Callable):
                        step = Step.from_callable(step)
                    else:
                        raise ValueError(
                            f"type of step[0] unknown: {type(step[0])}. "
                            f"Should be str, Callable."
                        ) 
                elif isinstance(step, Step):
                    step = Step.from_callable(step)
                else:
                    raise ValueError(
                        f"type of step unknown: {type(step)}. "
                        f"Should be str, Callable, tuple or Step."
                    ) 
                if depend_prev and not step.required and 0 != i:
                    step.required = set([new_callables[-1]._id])
                new_callables.append(step)
            return new_callables

        self.wait = build(callables)
        self.start = True
        self.finish = OrderedDict()

    @property
    def info(self):
        return [step.info for step in (self.wait if self.wait else self.finish)]

    def __call__(self, *args, **kwargs):
        
        def required(step):
            return [self.finish[req].outputs for req in step.required]

        while(self.wait):
            step = self.wait.pop(0)
            if step.meet(self.finish_names):
                req = required(step)
                if self.start:
                    req = list(args) + req
                    self.start = False
                    step(*req, **kwargs)
                else:
                    step(*req)
                self.finish[step._id] = step
            else:
                self.wait.append(step)
        return self.finish.popitem()[1].outputs

    @property
    def finish_names(self):
        return set(self.finish.keys())


class Pipeline:

    def __init__(self, callables: List[Union[Name, Step, FunctionTuple]], **kwargs):
        self.callables = callables
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return StepPipeline(self, self.callables, **self.kwargs)(*args, **kwargs)
