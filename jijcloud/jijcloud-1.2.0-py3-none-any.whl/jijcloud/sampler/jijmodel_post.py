import dimod
from abc import ABCMeta
from typing import Dict, Union
from numbers import Number
import numpy as np
import json
from jijcloud.post_api import post_instance_and_query
from jijmodeling.expression.expression import Expression
from jijmodeling import Problem

from jijcloud.response import DimodResponse


class JijModelingInterface(metaclass=ABCMeta):
    algorithm_model = ''

    def sample_model(
            self,
            model: Union[Expression, Problem],
            feed_dict: Dict[str, Union[Number, list, np.ndarray]],
            multipliers: Dict[str, Union[float, Number]],
            search: bool = False,
            sync=True,
            **kwargs):

        if isinstance(model, Problem):
            m_seri = model.model.to_serializable()
        elif isinstance(model, Expression):
            m_seri = model.to_serializable()
        else:
            raise TypeError('model is jijmodeling.Expression' +
                            ' or jijmodeling.Problem.')

        parameters = kwargs
        parameters['multipliers'] = multipliers
        parameters['mul_search'] = search

        _feed_dict = {k: v.tolist() if isinstance(v, np.ndarray) else v
                      for k, v in feed_dict.items()}

        response = post_instance_and_query(
            DimodResponse,
            self.client,
            instance_type='JijModeling',
            instance={
                'mathematical_model': json.dumps(m_seri),
                'instance_data': _feed_dict
            },
            solver=self.algorithm_model,
            parameters=parameters,
            sync=sync
        )


        return response
