from bmcs_utils.trait_types import \
    Float, Int, Bool, Instance, Range
from bmcs_utils.editors import \
    FloatRangeEditor, ProgressEditor, FloatEditor, HistoryEditor
from bmcs_utils.model import Model
from bmcs_utils.item import Item
from bmcs_utils.view import View
import numpy as np
import time
import traits.api as tr
from bmcs_utils.demo.shape_model import Rectangle, CSShape, Circle

class ModelWithHistory(Model):
    """Example model with a cross sectional shape"""
    name = 'Example'

    b = Int(5, desc='input parameter')
    t = Float(0)
    t_max = Float(10)

    ipw_view = View(
        Item('b', latex=r'\beta', readonly=True),
        Item('t', latex=r't', readonly=True),
        Item('t_max', latex=r'\theta'),
        time_editor=HistoryEditor(var='t',
                                 max_var='t_max',
        )
    )


    def update_plot(self, axes):
        pass
