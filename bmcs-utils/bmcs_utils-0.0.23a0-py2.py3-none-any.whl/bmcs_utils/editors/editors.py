import traits.api as tr
import ipywidgets as ipw
import numpy as np
from .editor_factory import EditorFactory

class FloatEditor(EditorFactory):
    step = tr.Float(None)
    def render(self):
        return ipw.FloatText(description=self.label,
                             value=self.value, step=self.step,
                             tooltip=self.tooltip,
                             disabled=self.disabled)


class IntEditor(EditorFactory):
    step = tr.Int(1)
    def render(self):
        return ipw.IntText(description=self.label,
                           value=self.value, step=self.step,
                           tooltip=self.tooltip,
                           disabled=self.disabled)


class BoolEditor(EditorFactory):
    def render(self):
        return ipw.Checkbox(description=self.label, value=self.value,
                            tooltip=self.tooltip, disabled=self.disabled)

class TextEditor(EditorFactory):
    def render(self):
        return ipw.Text(description=self.label, value=self.value,
                            tooltip=self.tooltip, disabled=self.disabled)


class FloatRangeEditor(EditorFactory):
    low = tr.Float
    high = tr.Float
    low_name = tr.Str
    high_name = tr.Str
    n_steps = tr.Int(20)
    n_steps_name = tr.Str
    continuous_update = tr.Bool(False)
    readout = tr.Bool(True)
    readout_format = tr.Str

    def render(self):
        if self.low_name:
            self.low = getattr(self.model, str(self.low_name))
        if self.high_name:
            self.high = getattr(self.model, str(self.high_name))
        if self.n_steps_name:
            self.n_steps = getattr(self.model, str(self.n_steps_name))
        step = (self.high - self.low) / self.n_steps

        round_value = self._get_round_value(self.low, self.high, self.n_steps)
        if not self.readout_format:
            self.readout_format = '.' + str(round_value) + 'f'

        # There's a bug in FloatSlider for very small step, see https://github.com/jupyter-widgets/ipywidgets/issues/259
        # it will be fixed in ipywidgets v8.0.0, but until then, the following fix will be used
        # with this implementation, entering the number manually in the readout will not work
        values = np.linspace(self.low, self.high, int(self.n_steps))
        values = np.round(values, round_value)

        # This is for SelectionSlider because 'value' must match exactly one of values array
        self.value = self._find_nearest(values, self.value)
        return ipw.SelectionSlider(
            options=values,
            value=self.value,
            tooltip=self.tooltip,
            continuous_update=self.continuous_update,
            description=self.label,
            disabled=self.disabled,
            readout=self.readout,
        )

        # return ipw.FloatSlider(
        #     value=self.value,
        #     min=self.low,
        #     max=self.high,
        #     step=step,
        #     tooltip=self.tooltip,
        #     continuous_update=self.continuous_update,
        #     description=self.label,
        #     disabled=self.disabled,
        #     readout=self.readout,
        #     readout_format=self.readout_format
        # )

    def _find_nearest(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    def _get_round_value(self, low, high, n_steps):
        magnitude_n_steps = self._get_order_of_magnitude(n_steps)
        magnitude_low = self._get_order_of_magnitude(low)
        magnitude_high = self._get_order_of_magnitude(high)
        min_magnitude = min(magnitude_low, magnitude_high)
        if min_magnitude >= 0:
            req_decimals = 2
        else:
            req_decimals = abs(min_magnitude) + magnitude_n_steps
        return req_decimals

    def _get_order_of_magnitude(self, num):
        sci_num = '{:.1e}'.format(num)
        sci_num_suffix = sci_num.split('e')[1]
        return int(sci_num_suffix)


class ButtonEditor(EditorFactory):
    icon = tr.Str('check')

    def render(self):
        button = ipw.Button(
            description=self.label,
            disabled=False,
            button_style='',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip=self.tooltip,
            icon=self.icon  # (FontAwesome names without the `fa-` prefix)
        )

        def button_clicked(change):
            setattr(self.model, self.name, True)

        button.on_click(button_clicked)
        return button


class ArrayEditor(EditorFactory):
    step = tr.Float(1)

    def render(self):
        array_values_widgets = [ipw.FloatText(value=value, step=self.step) for value in self.value]
        accordion = ipw.Accordion(children=[ipw.VBox(array_values_widgets)], disabled=self.disabled)
        accordion.set_title(0, self.label)
        return accordion


# class EnumEditor(EditorFactory):
#     options_tuple_list = tr.List
#
#     def render(self):
#         # if self.options_tuple_list:
#         #     self.options_tuple_list = getattr(self.model, str(self.options_tuple_list))
#
#         return ipw.Dropdown(
#             description=self.label,
#             options=self.options_tuple_list, #[('One', 1), ('Two', 2), ('Three', 3)],
#             value=self.value,
#             tooltip=self.tooltip,
#         )
