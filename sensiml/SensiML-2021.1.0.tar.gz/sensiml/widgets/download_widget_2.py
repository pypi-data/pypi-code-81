import os
import json
import IPython
from collections import namedtuple
from operator import attrgetter
from pandas import DataFrame
from ipywidgets import widgets
from ipywidgets import (
    Layout,
    Button,
    VBox,
    HBox,
    Box,
    FloatText,
    Textarea,
    Dropdown,
    Label,
    Tab,
    IntSlider,
    Checkbox,
    Text,
    Button,
    SelectMultiple,
    Select,
    HTML,
)
from IPython.display import display
from ipywidgets import IntText
from json import dumps as jdump
from sensiml.widgets.base_widget import BaseWidget
from sensiml.widgets.renderers import WidgetAttributeRenderer


category_item_layout = Layout(
    # display='flex',
    size=16,
    # border='solid 2px',
    justify_content="flex-start",
    # background_color= 'red',
    overflow="visible",
)


def clean_name(name):
    return "".join(e if e.isalnum() else "_" for e in name)


class DownloadWidgetVersion2(BaseWidget):
    def __init__(self, dsk=None, level="Project", folder="knowledgepacks"):
        self._dsk = dsk
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.setup(level=level)

    def setup(self, level):
        self.kb_description = {"parent": {}, "sub": {"Report": "Report"}}

        self.kb_dict = {"parent": [], "sub": []}
        self.level = level

    def select_platform(self, b):
        self._selected_platform = self._dsk.platforms_v2.get_platform_by_id(
            self._widget_platform.value
        )
        supported_source_drivers = self._selected_platform.supported_source_drivers
        supported_source_keys = {x: x for x in list(supported_source_drivers.keys())}

        capture_configurations = {
            k: v.uuid
            for k, v in self._dsk.project.capture_configurations.build_capture_list().items()
        }

        supported_source_keys.update(capture_configurations)
        supported_source_keys["Custom"] = "Custom"

        default_source_driver = supported_source_drivers.get("Default", None)
        applications = self._selected_platform.applications
        self._applications_widget.options = list()
        self._applications_widget.options = list(applications.keys())
        self._applications_widget.observe(self.select_application)

        platform_versions = self._selected_platform.platform_versions
        if default_source_driver is not None:
            # Remove the Default option from the list.
            supported_source_keys.pop("Default")
        if len(platform_versions) == 0:
            self._platform_version_widget.value = None
            self._platform_version_widget.layout.display = "none"
        elif len(platform_versions) == 1:
            self._platform_version_widget.options = platform_versions
            self._platform_version_widget.value = platform_versions[0]
        else:
            self._platform_version_widget.options = list()
            self._platform_version_widget.value = None
            self._platform_version_widget.layout.display = "flex"
            self._platform_version_widget.options = platform_versions
            self._platform_version_widget.value = self._platform_version_widget.options[
                -1
            ]

        self._widget_source.options = supported_source_keys
        if len(self._widget_source.options) > 0:
            if capture_configurations:
                self._widget_source.value = next(iter(capture_configurations.items()))[
                    1
                ]
            else:
                self._widget_source.value = "Custom"
        else:
            self._widget_source.options = {"Custom": "Custom"}
            self._widget_source.value = self._widget_source.options[0]

        self._change_rate("value")
        if len(self._widget_source_rate.options) > 0:
            self._widget_source_rate.value = self._widget_source_rate.options[0]
        else:
            self._widget_source_rate.options = [""]
            self._widget_source_rate.value = ""

        if self._selected_platform.can_build_binary:
            self._widget_download_type.options = ["Binary", "Library"]
        else:
            self._widget_download_type.options = ["Library"]
        self._widget_download_type.value = self._widget_download_type.options[0]

        self._processors_widget.options = self.get_processor_names(
            self._selected_platform
        )
        keys = list(self._processors_widget.options.keys())
        default_proc = self._selected_platform.default_selections.get("processor", None)

        self._processors_widget.value = (
            self._processors_widget.options[keys[0]]
            if default_proc is None
            else default_proc
        )

        self._compilers_widget.options = self.get_compiler_names(
            self._selected_platform
        )

        keys = list(self._compilers_widget.options.keys())
        default_comp = self._selected_platform.default_selections.get("compiler", None)
        self._compilers_widget.value = (
            self._compilers_widget.options[keys[0]]
            if default_comp is None
            else default_comp
        )
        self._applications_widget.value = self._applications_widget.options[0]
        self.select_application(None)

    def select_application(self, b):
        try:
            supported_outputs = self._selected_platform.applications[
                self._applications_widget.value
            ]["supported_outputs"]
            out_opts = list()
            self._widget_app_outputs.options = []
            for so in supported_outputs:
                title = ", ".join(so)
                out_opts.append((title, so))

            self._info_applications.tooltip = """{}""".format(
                self._selected_platform.applications[self._applications_widget.value][
                    "description"
                ]
            )

            self._widget_app_outputs.options = out_opts
            self._widget_app_outputs.value = self._widget_app_outputs.options[0][1]
        except KeyError:
            return

    def select_processor(self, b):
        platform = self._dsk.platforms_v2.get_platform_by_id(
            self._widget_platform.value
        )
        self._float_option_widget.options = self.get_float_list(
            platform, self._processors_widget.value
        )
        if len(self._float_option_widget.options) == 0:
            self._float_option_widget.layout.visibility = "hidden"
            return
        self._float_option_widget.layout.visibility = "visible"

        default_float = platform.default_selections.get("float", "Hard FP")
        self._float_option_widget.value = self._float_option_widget.options[
            default_float
        ]

    def show_hide_filename(self, b):
        if self._rename_after_checkbox.value == True:
            self._file_rename.layout.visibility = "visible"
        else:
            self._file_rename.layout.visibility = "hidden"

    def generate_description(self, b):
        if hasattr(self._dsk, "_auto_sense_ran"):
            if self._dsk._auto_sense_ran:
                self.renderer.render(
                    "KnowledgePack List Needs updating. Updating Now... Reselect and redownload."
                )
                self._refresh_models_list(None)
                self._dsk._auto_sense_ran = False
                return

        platform = self._dsk.platforms_v2.get_platform_by_id(
            self._widget_platform.value
        )
        supported_outputs = platform.supported_outputs
        parent_name = None
        parent_uuid = None
        description = {}
        self.set_parent_model(None)
        if not self.kb_description["parent"]:
            self.renderer.render("No Parent Model Selected.")
            return
        for key in self.kb_description["parent"]:
            description = {
                clean_name(key): {
                    "uuid": self.kb_description["parent"][key],
                    "results": {},
                    "source": self._widget_source.value,
                }
            }
            parent_name = clean_name(key)
            parent_uuid = self.kb_description["parent"][key]
        for parent in self.kb_dict["parent"][0][1:]:
            description[parent_name]["results"].update(
                {format(parent.description.split("-")[0]): clean_name(parent.value)}
            )
        for key in self.kb_description["sub"]:
            if key != "Report":
                sub_description = {
                    "uuid": self.kb_description["sub"][key],
                    "parent": parent_name,
                    "segmenter_from": "parent",
                }
                description.update({clean_name(key): sub_description})

        kp_uuid = parent_uuid
        kp_platform = self._widget_platform.value
        kp_debug = self._widget_debug.value
        kp_test_data = self._widget_test_data.value
        kp_download_type = self._widget_download_type.value

        kp_processor = self._processors_widget.value
        kp_compiler = self._compilers_widget.value
        kp_float_options = (
            self._float_option_widget.value if self._float_option_widget.value else ""
        )

        debug_level = self._widget_debug_level.value
        profile = self._widget_profile.value
        profile_iterations = self._widget_profile_iterations.value
        extra_build_flags = self._extra_flags_widget.value

        if self._platform_version_widget.value is None:
            selected_platform_version = ""
        else:
            selected_platform_version = self._platform_version_widget.value

        sample_rate = (
            self._widget_source_rate.value
            if self._widget_source_rate.value in self._widget_source_rate.options
            else 100
        )
        output_options = [x.lower() for x in self._widget_app_outputs.value]

        kp_application = self._applications_widget.value

        if kp_uuid is not None:
            kp = self._dsk.get_knowledgepack(kp_uuid)
        else:
            return None

        if kp.knowledgepack_description is not None:
            description = kp.knowledgepack_description
            description["Parent"]["source"] = self._widget_source.value

        config = {
            "target_platform": kp_platform,
            "test_data": kp_test_data,
            "target_processor": kp_processor,
            "target_compiler": kp_compiler,
            "float_options": kp_float_options,
            "debug": kp_debug,
            "application": kp_application,
            "sample_rate": sample_rate,
            "output_options": output_options,
            "kb_description": description,
            "debug_level": debug_level,
            "profile": profile,
            "profile_iterations": profile_iterations,
            "extra_build_flags": extra_build_flags,
            "selected_platform_version": selected_platform_version,
        }

        self.renderer.render("Generating Knowledge Pack")

        if self._rename_after_checkbox.value and len(self._file_rename.value) > 1:
            rename_path = self._file_rename.value
            if rename_path[-4:] != ".zip":
                rename_path += ".zip"
        else:
            rename_path = None

        if kp_download_type == "Library":
            save_path, saved = kp.download_library_v2(
                config=config,
                folder="knowledgepacks",
                renderer=self.renderer,
                save_as=rename_path,
            )
        if kp_download_type == "Binary":
            save_path, saved = kp.download_binary_v2(
                config=config,
                folder="knowledgepacks",
                renderer=self.renderer,
                save_as=rename_path,
            )

    def set_parent_model(self, b):

        if self._widget_parent_select.value is None:
            return

        kp = self._dsk.get_knowledgepack(self._widget_parent_select.value)
        kp_item = []
        kp_item.append(Label(value=kp.name))

        for key, value in kp.class_map.items():
            kp_item.append(
                Dropdown(
                    options=self.kb_description["sub"],
                    description="{} - {}".format(key, value),
                )
            )

        self.kb_description["parent"] = {kp.name: kp.uuid}
        self.kb_dict["parent"] = [kp_item]
        self.update_models()

    def get_kp_dict(self):
        if self.level.lower() == "project":
            kps = self._dsk.project.list_knowledgepacks()
        elif self.level.lower() == "pipeline":
            kps = self._dsk.pipeline.list_knowledgepacks()
        else:
            kps = self._dsk.list_knowledgepacks()

        if isinstance(kps, DataFrame) and len(kps):
            kps = sorted(
                [
                    (name, value)
                    for name, value in kps[["Name", "kp_uuid"]].values
                    if name
                ],
                key=lambda s: s[0].lower(),
            )

            return kps

        return [("", None)]

    @staticmethod
    def flatten(l):
        return [item for sublist in l for item in sublist]

    def get_model_list(self):
        return (
            [Label(value="Parent Model")]
            + self.flatten(self.kb_dict["parent"])
            + [Label(value="Sub Model")]
            + self.flatten(self.kb_dict["sub"])
        )

    def get_feature_file_list(self):
        ff = self._dsk.list_featurefiles(silent=True)
        if ff is not None:
            return list(ff["Name"].values)
        else:
            return []

    def get_platform_names(self):
        named_platform = namedtuple("Platform", ["name", "uuid"])
        platform_list = []
        for platform in self._dsk.platforms_v2.platform_list:
            platform_list.append(named_platform(platform.name, platform.uuid))
        platform_list = sorted(platform_list, key=attrgetter("name"))
        ret_dict = {}
        for platform in platform_list:
            ret_dict["{}".format(platform.name)] = platform.uuid

        return ret_dict

    def get_processor_names(self, platform):
        named_processor = namedtuple(
            "Processor",
            ["display_name", "architecture", "manufacturer", "float_options", "uuid"],
        )
        processor_list = list()
        for processor in platform.processors:
            processor_list.append(
                named_processor(
                    processor.display_name,
                    processor.architecture,
                    processor.manufacturer,
                    processor.float_options,
                    processor.uuid,
                )
            )
        processor_list = sorted(
            processor_list, key=attrgetter("display_name", "architecture")
        )
        ret_dict = {}
        for proc in processor_list:
            ret_dict["{} {}".format(proc.manufacturer, proc.display_name)] = proc.uuid

        return ret_dict

    def get_compiler_names(self, platform):
        named_compiler = namedtuple("Compiler", ["name", "compiler_version", "uuid"])
        compiler_list = list()
        for compiler in platform.supported_compilers:
            compiler_list.append(
                named_compiler(compiler.name, compiler.compiler_version, compiler.uuid)
            )
        compiler_list = sorted(
            compiler_list, key=attrgetter("name", "compiler_version")
        )
        ret_dict = {}
        for proc in compiler_list:
            ret_dict["{} {}".format(proc.name, proc.compiler_version)] = proc.uuid

        return ret_dict

    def get_float_list(self, platform, processor):
        if processor is None:
            return dict()
        try:
            proc = list(filter(lambda p: p.uuid == processor, platform.processors))[0]
        except IndexError:
            return dict()

        return proc.float_options

    def _refresh(self):
        if self._dsk is None:
            return
        self._widget_platform.options = self.get_platform_names()
        # self._widget_platform.value = 10
        self._widget_platform.observe(self.select_platform)
        self._processors_widget.observe(self.select_processor)
        self.select_platform(None)
        self.select_processor(None)
        self._widget_test_data.options = [None] + self.get_feature_file_list()
        self._widget_parent_select.options = self.get_kp_dict()
        self._widget_parent_select.value = self._widget_parent_select.options[0][1]
        self._widget_class_map.options = self._get_class_map()

    def _clear(self):
        self._widget_parent_select.options = [""]
        self._widget_parent_select.value = ""
        self._widget_class_map.options = []

    def _update_class_map(self, *args):
        self._widget_class_map.options = self._get_class_map()

    def _get_class_map(self):

        if self._widget_parent_select.value:
            class_map = self._dsk.get_knowledgepack(
                self._widget_parent_select.value
            ).class_map
            return sorted(
                ["{} - {}".format(key, value) for key, value in class_map.items()]
            )
        else:
            return ""

    def _refresh_models_list(self, b):
        if self._dsk:
            if self._dsk.pipeline:
                self._widget_parent_select.options = self.get_kp_dict()
                self._widget_parent_select.value = self._widget_parent_select.options[
                    0
                ][1]
                self._widget_class_map.options = self._get_class_map()

    def update_models(self):
        if self._dsk is None:
            return

        if self.kb_dict["parent"]:
            for output in self.kb_dict["parent"][0][1:]:
                output.options = [k for k, v in self.kb_description["sub"].items()]

    def _change_rate(self, change):
        platform = self._dsk.platforms_v2.get_platform_by_id(
            self._widget_platform.value
        )
        supported_source_drivers = platform.supported_source_drivers

        if self._widget_source.value == "Custom":
            self._widget_source_rate.options = [""]
            self._widget_source_rate.value = None
        else:
            self._widget_source_rate.options = supported_source_drivers.get(
                self._widget_source.value, [""]
            )

        if self._widget_source_rate.options[0] == "":
            self._widget_source_rate.layout.visibility = "hidden"
        else:
            self._widget_source_rate.layout.visibility = "visible"

    def create_widget(self):

        info_layout = Layout(width="35px", visibility="visible")

        description_style = {"description_width": "112px"}

        dropdown_style = {
            "description_width": "120px",
            "align_items": "flex-end",
            "justify_content": "space-around",
        }

        self._info_test_data = widgets.Button(
            icon="question",
            disabled=True,
            tooltip="""
                    Select a test file to upload. The knowledge pack will replace incoming sensor
                    data with this test data. Allows for validating model performance on the device
                    with known results. Once the end of the test data is reached, the knowledge pack
                    will start from the start of the test data again.
                    """,
            layout=info_layout,
        )

        self._info_debug = widgets.Button(
            icon="question",
            disabled=True,
            tooltip="""
                    Enable Debug output over serial.
                    """,
            layout=info_layout,
        )

        self._info_debug_level = widgets.Button(
            icon="question",
            disabled=True,
            tooltip="""
                    Debug Level 1: Classification
                    Debug Level 2: Feature Vector
                    Debug Level 3: Raw Data Fed into Feature Extractors
                    """,
            layout=info_layout,
        )
        self._info_profile = widgets.Button(
            icon="question",
            disabled=True,
            tooltip="""
                    Adds profiling to code which will output the MIPS and Average seconds for
                    each feature extractor and classifier.
                    """,
            layout=info_layout,
        )

        self._info_profile_iterations = widgets.Button(
            icon="question",
            disabled=True,
            tooltip="""
                    The number of iterations to perform when profiling each feature extrator and classifier.
                    """,
            layout=info_layout,
        )

        self._button_generate = Button(
            icon="download", tooltip="Generate and Download", layout=Layout(width="15%")
        )
        self._button_refresh = Button(
            icon="refresh", layout=Layout(width="15%"), tooltip="Refresh Model List"
        )
        self._widget_platform = Dropdown(
            description="HW Platform",
            options=[],
            style=dropdown_style,
            layout=Layout(width="90%"),
        )

        self._widget_download_type = Dropdown(
            description="Format",
            options=[],
            style=dropdown_style,
            layout=Layout(width="90%"),
        )
        self._widget_source = Dropdown(
            description="Data Source",
            options=[],
            style=dropdown_style,
            layout=Layout(width="90%"),
        )
        self._widget_source_rate = Dropdown(
            description="Sample Rate",
            options=[],
            style=dropdown_style,
            layout=Layout(width="90%"),
        )
        self._widget_debug = Dropdown(
            description="Debug", options=[False, True], style=description_style,
        )
        self._widget_debug_level = Dropdown(
            description="Debug Level", options=[1, 2, 3], style=description_style
        )
        self._widget_profile = Dropdown(
            description="Profile", options=[False, True], style=description_style
        )
        self._widget_profile_iterations = IntText(
            description="Profile Iterations", default=1000, style=description_style
        )
        self._widget_test_data = Dropdown(
            description="Test Data", options=[None], style=description_style
        )
        self._widget_parent_select = Dropdown(
            description="Model Name", options=[], layout=Layout(width="85%")
        )
        self._widget_class_map = SelectMultiple(description="Class Map", options=[""])

        self._widget_render_space = HTML()

        self.renderer = WidgetAttributeRenderer(self._widget_render_space, "value")

        self._processors_widget = Dropdown(
            description="Choose Processor",
            options=[],
            style=dropdown_style,
            layout=Layout(width="90%"),
        )
        self._platform_version_widget = Dropdown(
            description="Platform Version",
            options=[],
            style=dropdown_style,
            layout=Layout(width="90%"),
        )
        self._compilers_widget = Dropdown(
            description="Choose Compiler",
            options=[],
            style=dropdown_style,
            layout=Layout(width="90%"),
        )
        self._float_option_widget = Dropdown(
            description="Float Options",
            options=[],
            style=dropdown_style,
            layout=Layout(width="90%"),
        )
        self._extra_flags_widget = Text(
            description="Extra build flags", style=description_style
        )
        self._info_extra_flags = widgets.Button(
            icon="question",
            disabled=True,
            tooltip="""
                    Extra build flags to pass to compiler/linker. These MUST be typed in properly
                    """,
            layout=info_layout,
        )

        self._rename_after_checkbox = widgets.Checkbox(
            value=False,
            description="Rename File After Download",
            disabled=False,
            indent=True,
        )
        self._file_rename = widgets.Text(
            value="",
            placeholder=".zip added automatically",
            description="File Name",
            disabled=False,
            layout=Layout(visibility="hidden"),
        )

        self._applications_widget = widgets.Dropdown(
            description="Application",
            options=[],
            style=dropdown_style,
            layout=Layout(width="99%"),
        )

        self._info_applications = widgets.Button(
            icon="question",
            disabled=True,
            tooltip="""

                    """,
            layout=info_layout,
        )

        self._widget_app_outputs = Select(
            description="Output",
            options=[],
            style=dropdown_style,
            layout=Layout(width="50%", min_height="200"),
        )

        self._rename_after_checkbox.observe(self.show_hide_filename)

        self.kb_items = VBox(
            [
                Tab(
                    [
                        VBox(
                            [
                                HBox(
                                    [
                                        self._widget_parent_select,
                                        self._button_refresh,
                                        self._button_generate,
                                    ]
                                ),
                                self._widget_class_map,
                                Label(
                                    value="Target Device Options",
                                    layout=category_item_layout,
                                ),
                                HBox(
                                    [
                                        VBox(
                                            [
                                                self._widget_platform,
                                                self._platform_version_widget,
                                                self._processors_widget,
                                                self._float_option_widget,
                                                self._compilers_widget,
                                                self._widget_download_type,
                                                self._widget_source,
                                                self._widget_source_rate,
                                            ],
                                            layout=Layout(width="50%"),
                                        ),
                                        VBox(
                                            [
                                                HBox(
                                                    [
                                                        self._applications_widget,
                                                        self._info_applications,
                                                    ],
                                                    layout=Layout(width="50%"),
                                                ),
                                                self._widget_app_outputs,
                                                self._rename_after_checkbox,
                                                self._file_rename,
                                            ],
                                            layout=Layout(width="100%"),
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        HBox(
                            [
                                VBox(
                                    [
                                        HBox(
                                            [
                                                self._widget_test_data,
                                                self._info_test_data,
                                            ],
                                            layout=Layout(align_self="flex-start"),
                                        ),
                                        HBox(
                                            [self._widget_debug, self._info_debug],
                                            layout=Layout(align_self="flex-start"),
                                        ),
                                        HBox(
                                            [
                                                self._widget_debug_level,
                                                self._info_debug_level,
                                            ],
                                            layout=Layout(align_self="flex-start"),
                                        ),
                                        HBox(
                                            [self._widget_profile, self._info_profile],
                                            layout=Layout(align_self="flex-start"),
                                        ),
                                        HBox(
                                            [
                                                self._widget_profile_iterations,
                                                self._info_profile_iterations,
                                            ],
                                            layout=Layout(align_self="flex-start"),
                                        ),
                                        HBox(
                                            [
                                                self._extra_flags_widget,
                                                self._info_extra_flags,
                                            ],
                                            layout=Layout(align_self="flex-start"),
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
                self._widget_render_space,
            ],
        )

        self.kb_items.children[0].set_title(0, "Main Settings")
        self.kb_items.children[0].set_title(1, "Advanced Settings")

        self._button_generate.on_click(self.generate_description)
        self._button_refresh.on_click(self._refresh_models_list)
        self._widget_source.observe(self._change_rate, names="value")
        self._widget_parent_select.observe(self._update_class_map)

        self._refresh()
        return self.kb_items
