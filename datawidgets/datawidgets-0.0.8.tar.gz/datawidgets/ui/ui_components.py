from datawidgets.imports import *
from datawidgets.interface import *
from .style import *

import ipyvuetify as vue
import traitlets


def vue_autocomplete_box(items: list, title: str = "", css_classes: List[str] = []):
    box = vue.Autocomplete(
        items=items, label=title, v_model="", filled=True, dense=True, hide_details=True
    )
    box.add_class(CSS_NAMES.AUTOCOMPLETE_BOX)
    for css_class in css_classes:
        box.add_class(css_class)
    return box


def label_button(label: str, callbacks=[]):
    button = widgets.Button(description=label, layout=Layout(width="auto"))
    button.add_class(CSS_NAMES.LABEL_BUTTON)
    for cb in callbacks:
        button.on_click(cb)
    return button


def generate_upload_button(description="Upload", callbacks=[]):
    max_uploads = 1
    btn = widgets.FileUpload()
    btn.description = description

    if max_uploads is not None:

        def disable_on_max_upload(*args):
            if len(btn.value) >= max_uploads:
                btn.disabled = True
                btn.add_class("file-upload-button-disabled")

        btn.observe(disable_on_max_upload)
        for cb in callbacks:
            btn.observe(cb)

    btn.add_class(CSS_NAMES.FILE_UPLOAD_BUTTON)
    return btn


class UploadButton(AbstractInterface):
    def __init__(self, description="Upload", callbacks=[]):
        self.description = description
        self.callbacks = callbacks
        super().__init__(source=None)

    def setup(self):
        self.upload_button = generate_upload_button(
            description=self.description, callbacks=self.callbacks
        )
        self.refresh_button = Button(description="⟳")
        self.go_button = Button(description="🚀")

        for btn in [self.refresh_button, self.go_button]:
            btn.add_class(CSS_NAMES.FILE_UPLOAD_REFRESH_BUTTON)
            btn.add_class(CSS_NAMES.FILE_UPLOAD_BUTTON)

    def setup_view(self):
        view = HBox(
            [
                self.upload_button,
                self.refresh_button,
                self.go_button,
            ]
        )
        view.add_class(CSS_NAMES.FILE_UPLOAD_CONTAINER)

        def replace_upload_button(*args):
            view.children = [
                generate_upload_button(description=self.description),
                self.refresh_button,
                self.go_button,
            ]

        self.refresh_button.on_click(replace_upload_button)
        self.view = HBox([view])
        self.view.layout = CSS_LAYOUTS.flex_layout

    def _repr_html_(self):
        display(self.view)
