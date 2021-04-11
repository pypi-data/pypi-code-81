# SOURCE: https://gist.github.com/aplavin/19f3607240c4c0a63cb1d223609ddc3b#file-mywidgets-py-L69

from datawidgets.imports import *
from .style import *
import ipywidgets as iw


class ClassMapButtons(iw.Box):
    description = traitlets.Unicode()
    value = traitlets.Tuple()
    options = traitlets.Union([traitlets.List(), traitlets.Dict()])

    def __init__(self, width="100%", **kwargs):
        super().__init__(**kwargs)
        self._selection_obj = iw.widget_selection._MultipleSelection()
        traitlets.link((self, "options"), (self._selection_obj, "options"))
        traitlets.link((self, "value"), (self._selection_obj, "value"))

        def observe(
            widgets: Union[iw.Widget, Sequence[iw.Widget]],
            trait_name,  # Some attr of self
        ):
            def wrapper(func):
                # When observing `self`
                if isinstance(widgets, iw.Widget):
                    widgets.observe(func, trait_name)
                # When observing `self.buttons`, a list of widgets,
                #   attach it to each widget in the list
                else:
                    for w in widgets:
                        w.observe(func, trait_name)
                func()

            return wrapper

        @observe(self, "options")
        def _(*_):
            self.buttons = []
            for label in self._selection_obj._options_labels:
                button = iw.ToggleButton(
                    description=label, layout=CSS_LAYOUTS.autowidth
                )
                button.add_class(CSS_NAMES.LABEL_BUTTON)
                button.disabled = False
                self.buttons.append(button)
            self.children = self.buttons

            @observe(self.buttons, "value")
            def _(*_):
                for btn in self.buttons:
                    if btn.value:
                        btn.add_class(CSS_NAMES.LABEL_BUTTON_TOGGLED)
                    else:
                        btn.remove_class(CSS_NAMES.LABEL_BUTTON_TOGGLED)
                self.value = tuple(
                    value
                    for btn, value in zip(
                        self.buttons, self._selection_obj._options_values
                    )
                    if btn.value
                )

        self.add_class(CSS_NAMES.LABEL_BUTTON_GROUP)
        # for i in self.children:
        #     i.value = True

    def reset(self):
        opts = self.options
        self.options = []
        self.options = opts


def _with_classes(self, *classes, remove=False):
    if remove:
        for c in classes:
            self.remove_class(c)
    else:
        for c in classes:
            self.add_class(c)
    return self


iw.DOMWidget.with_classes = _with_classes