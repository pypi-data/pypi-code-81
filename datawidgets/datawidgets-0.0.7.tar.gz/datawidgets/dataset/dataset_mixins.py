from datawidgets.imports import *
from datawidgets.utils import *
from datawidgets.data import *
from .image_dataset import *


class BatchClassificationLabelsMixin:
    _works_with = "ImageDatasetWithLabels"

    def setup_batch_labelling(self):
        # Create add and remove buttons
        self.batch_add_button = vue_autocomplete_box(
            items=self.classes,
            css_classes=[CSS_NAMES.BATCH_ADD_BUTTON],
        )

        self.batch_remove_button = vue_autocomplete_box(
            items=self.classes,
            css_classes=[CSS_NAMES.BATCH_REMOVE_BUTTON],
        )

        # Attach observers / callbacks to batch labelling buttons
        self.batch_add_button.observe(self.add_batch_label)
        self.batch_remove_button.observe(self.remove_batch_label)

    @property
    def batch_add_value(self):
        return self.batch_add_button.v_model

    @property
    def batch_remove_value(self):
        return self.batch_remove_button.v_model

    def update_batch_labelling_descriptions(self, *args):
        self.batch_add_button.label = f"Batch Add ({len(self.selected_items)})"
        self.batch_remove_button.label = f"Batch Remove ({len(self.selected_items)})"

        # `hasattr` is used here IN CASE this function is called before
        # `setup_batch_labelling` is called. We could probably do away with
        # it but it's here for safety as setup functions don't have an order
        if hasattr(self, "class_map_negative_buttons"):
            self.batch_remove_button.items = flatten(
                [item.labels for item in self.selected_items]
            )

    def add_batch_label(self, change):
        if self.batch_add_value in self.classes:
            for item in self.selected_items:
                if not item.max_labels_selected:
                    item.add_label(self.batch_add_value)
            self.batch_add_button.v_model = ""

    def remove_batch_label(self, change):
        if self.batch_remove_value in self.classes:
            for item in self.selected_items:
                item.remove_label(self.batch_remove_value)
            self.batch_remove_button.v_model = ""


class WidthSliderMixin:
    def setup_width_slider(self):
        self.width_slider = widgets.IntSlider(
            value=self.width,
            min=1,
            max=100,
            description="Image Width:",
            layout=widgets.Layout(align_items="center"),
        )
        self.width_slider.continuous_update = False
        self.width_slider.observe(
            lambda x: setattr(self, "width", self.width_slider.value)
        )


class SelectionMixin:
    ""
    selection_source = "active_datapoints"

    def unselect_all(self, *args, callbacks=[]):
        for item in getattr(self, self.selection_source):
            item.unselect()

    def select_all(self, *args, callbacks=[]):
        for item in getattr(self, self.selection_source):
            item.select()

    def invert_selection(self, *args, callbacks=[]):
        for item in getattr(self, self.selection_source):
            if item.is_selected:
                item.unselect()
            else:
                item.select()

    def generate_unselect_all_button(self, callbacks=[]):
        "Generates a button that unselects all selected items"

        unselect_all_button = Button(description="Unselect All")
        unselect_all_button.on_click(self.unselect_all)
        for cb in callbacks:
            unselect_all_button.on_click(cb)

        return unselect_all_button

    def generate_select_all_button(self, callbacks=[]):
        "Generates a button that selects all selected items"

        select_all_button = Button(description="Select All")
        select_all_button.on_click(self.select_all)
        for cb in callbacks:
            select_all_button.on_click(cb)

        return select_all_button

    def generate_invert_selection_button(self, callbacks=[]):
        "Generates a button to invert selected items"

        button = Button(description="Invert Selection")
        button.on_click(self.invert_selection)
        for cb in callbacks:
            button.on_click(cb)

        return button


class EmbeddingSimilarityMixin:
    from scipy import spatial

    # TODO: Unused
    def setup_similarity(self, callbacks=[]):
        menu = widgets.Dropdown(options=self.embedding_colname)
        self.compare_key_options = menu

    def disable_similarity_button(self, *args):
        "Disable when more than 1 image is selected"
        if len(self.selected_names) > 1:
            self.similarity_button.disabled = True

    def generate_similarity_button(self, callbacks=[]):
        ""

        def calc_similarity(*args):
            df = self.df
            filt = df[self.filename_col].apply(str).isin(self.selected_names)
            self.log(f"Selected {df[filt][self.filename_col]}")

            similarity = df.apply(
                lambda row: self.compute_similarity(df[filt], row),
                axis=1,
            )
            sorting_indices = similarity.sort_values().index.values

            self.log(f"Computed similarity")
            self.log(f"Similarity indices: sorting_indices")

            self.datapoints[sorting_indices[0]].unselect()
            self.filter_and_mutate_dataset(sorting_indices)
            self.refresh()
            # self.reset(df=df.loc[similarity.sort_values().index.values])
            self.log(f"Reset")

            for cb in callbacks:
                cb()

        button = widgets.Button(description="Sort By Similarity")
        button.layout.width = "200px"
        button.on_click(calc_similarity)
        return button

    def compute_similarity(
        self,
        source: Union[pd.Series, pd.DataFrame],
        target: pd.Series,
    ):
        source = convert_single_row_to_series(source)

        compare_key = self.compare_key_options.value
        self.log(f"Computing similarity by {compare_key}")

        return self.embedding_similarity_metric(
            source[compare_key], target[compare_key]
        )


class MinimalViewMixin:
    minimal_view_mode = False

    def generate_minimal_view_button(self, callbacks=[]):
        button = Button(description="Toggle Minimal View")
        button.layout.width = "200px"
        button.on_click(self.toggle_minimal_view_mode)

        for cb in callbacks:
            button.on_click(cb)

        return button

    def toggle_minimal_view_mode(self, *args):
        self.minimal_view_mode = not self.minimal_view_mode
        self.update_grid()


class ImageGridMixin:
    """
    Sets up `self.grid` to contains `self.images`.
    Use `generate_grid_range_slider` followed by `set_grid_range_slider` in a global
      context like so:

    dset = ImageDataset(...)
    def REFRESH_GLOBAL_DISPLAY(...)
    indxs_slider = dset.generate_grid_range_slider(callbacks=[REFRESH_GLOBAL_DISPLAY])
    dset.set_grid_range_slider(indxs_slider)
    """

    _maybe_uses = ["ClassMapFilterMixin"]

    def setup_img_grid(self):
        self.grid = widgets.Box(
            children=[],
            width="100%",
            layout=CSS_LAYOUTS.flex_layout,
        )
        self.update_grid()

    def update_grid(self, *args, df: pd.DataFrame = None):
        """Sets up self.grid to all `self.images` if no grid range slider is initialised
        else to the interval values of the slider
        """
        items = []
        if hasattr(self, "grid_range_slider"):
            start, end = self.grid_range_slider.value
        else:
            start, end = (0, self.batch_size)

        # `_upper` exists to increase the upper index when looping, in case
        # we are hiding completed items
        _upper = end

        df = None
        if hasattr(self, "positive_class_map_filter"):
            df = self.filter_dataset(self.class_map_subset_filter)

        # Unload just the img bytes of items we aren't currently viewing
        # if hasattr(self, "active_datapoints"):
        #     # If this item is already in the grid and must remain there,
        #     # then we don't unload it
        #     if not self.class_map_positive_buttons.value == ():
        #         dont_unload = np.intersect1d(
        #             ([item.source for item in self.active_datapoints]),
        #             df[self.filename_col].values,
        #         )
        #     else:
        #         dont_unload = []

        #     for item in self.active_datapoints:
        #         if item.source in dont_unload:
        #             pass
        #         else:
        #             item.unload()

        if hasattr(self, "positive_class_map_filter"):
            # This is what will almost always get executed
            df = self.filter_dataset(self.class_map_subset_filter)
            for i, fname in enumerate(df[self.filename_col]):
                if i >= start and i < _upper:
                    item = self.datapoints[fname]
                    if hasattr(self, "hide_completed") or hasattr(self, "hide_review"):
                        if (
                            (item.is_completed and self.hide_completed)
                            or (item.is_under_review and self.hide_review)
                            or (item.is_deleted and self.hide_deleted)
                        ):
                            _upper += 1
                            continue
                        else:
                            items.append(item)
                    else:
                        items.append(item)

                    if not item.is_loaded:
                        item.load()
                        item.update_view()
                    elif item.is_loaded and item.needs_refresh:
                        item.load_img_bytes()

                    if hasattr(self, "minimal_view_mode"):
                        if self.minimal_view_mode:
                            item.update_view_minimal()
                        else:
                            item.update_view()

        else:
            for i, (key, item) in enumerate(self.datapoints.items()):
                if i >= start and i < end:
                    items.append(item)

        children = [i.view for i in items]
        self.active_datapoints = items
        self.grid.children = children

    def reset_grid_range_value(self, *args):
        self.grid_range_slider.value = (0, self.batch_size)

    def set_grid_range_slider(self, grid_range_slider: widgets.IntRangeSlider):
        self.grid_range_slider = grid_range_slider
        self.update_grid()

    def update_grid_range_slider(self, *args):
        min_value, max_value = self.grid_range_slider.value
        max_limit = len(self)

        if max_value > len(self):
            max_value = len(self)

        num_filtered_items = len(self)
        if hasattr(self, "positive_class_map_filter"):
            num_filtered_items = (
                self.positive_class_map_filter & self.negative_class_map_filter
            ).sum()
            if max_value > num_filtered_items:
                max_value = num_filtered_items
            if min_value > num_filtered_items:
                # HACK ? reset min value...
                min_value = 0
        max_limit = min(len(self), num_filtered_items)

        self.grid_range_slider.value = (min_value, max_value)
        self.grid_range_slider.max = max_limit

    def generate_grid_range_slider(self, callbacks=[]):
        grid_range_slider = widgets.IntRangeSlider(
            value=(0, self.batch_size),
            min=0,
            max=len(self),
            description="Show Images #",
        )
        grid_range_slider.add_class(CSS_NAMES.GRID_RANGE_SLIDER)
        grid_range_slider.continuous_update = False

        def increment_range(*args):
            range_values = grid_range_slider.value
            grid_range_slider.value = (
                range_values[1],
                range_values[1] + self.batch_size,
            )
            self.update_grid_range_slider()

        def decrement_range(*args):
            range_values = grid_range_slider.value
            grid_range_slider.value = (
                range_values[0] - self.batch_size,
                range_values[0],
            )
            self.update_grid_range_slider()

        grid_range_slider.observe(self.update_grid, "value")
        if hasattr(self, "update_info"):
            grid_range_slider.observe(self.update_info, "value")
        grid_range_slider.observe(self.update_grid_range_slider, "value")

        for cb in callbacks:
            grid_range_slider.observe(cb, "value")

        increment_button = Button(description="»")
        decrement_button = Button(description="«")

        increment_button.add_class(CSS_NAMES.RANGE_NEXT_PREV_BUTTONS)
        decrement_button.add_class(CSS_NAMES.RANGE_NEXT_PREV_BUTTONS)
        increment_button.on_click(increment_range)
        decrement_button.on_click(decrement_range)

        return decrement_button, grid_range_slider, increment_button


class InfoMixin:
    def update_info(self, *args, additional_info: List[str] = []):
        if isinstance(additional_info, str):
            additional_info = [additional_info]

        num_images_in_grid = len(getattr(self, self.selection_source))
        if hasattr(self, "class_map_positive_buttons"):
            num_filtered_images = (
                self.positive_class_map_filter & self.negative_class_map_filter
            ).sum()

        info = [
            f"Selected: {self.num_selected}",
            f"Displayed: {num_images_in_grid}",
            f"Filtered: {num_filtered_images}",
            f"Total: {len(self)}",
            f"Deleted: {self.num_deleted}",
            f"Modified: {self.num_modified}",
            f"Looked At: {self.num_loaded}/{len(self)}",
            f"Completed: {self.num_completed}/{len(self)}",
        ]

        info = "&emsp;&emsp;".join(info)
        self.info.value = f"<h5>{info}<h5>"

        self.info.add_class(CSS_NAMES.MAIN_INFO_PANEL)
        self.info.layout = CSS_LAYOUTS.flex_layout

    def setup_info(self):
        self.info = widgets.HTML()


class RestoreProgressMixin:
    def setup_restore_progress_button(self):
        self.restore_button_group = UploadButton(
            description="Upload Progress File (.csv, .feather)"
        )
        self.restore_button_group.upload_button.layout.width = "350px"
        self.restore_button_group.go_button.on_click(self._restore_progress)
        self.restore_button_group.go_button.on_click(self.update_info)
        self.restore_button_group.go_button.on_click(self.update_grid)

    def _restore_progress(self, *args):
        # Read uploaded CSV
        for _, v in self.restore_button_group.upload_button.value.items():
            pass

        try:
            restore_df = pd.read_csv(io.StringIO(str(v["content"], "utf-8")))
        except:
            restore_df = pd.read_feather(io.BytesIO(v["content"]))

        restore_df.index = restore_df[self.filename_col]
        # for item in tqdm(self.datapoints, desc="Restoring Data Items"):
        for index, row in tqdm(
            restore_df.iterrows(), desc="Restoring Data Items", total=len(restore_df)
        ):
            try:
                item = self.datapoints[index]
            except KeyError:
                continue

            item.load()
            item.update_view()

            # Marks require some more complex stuff. Maybe this should be
            # a traitlets implementation, though that might be overkill complexity

            item.mark_as_completed() if row.is_completed else item.unmark_as_completed()
            item.mark_as_deleted() if row.is_deleted else item.unmark_as_deleted()
            item.mark_as_under_review() if row.is_under_review else item.unmark_as_under_review()

            if isinstance(row.label, str):
                labels = ast.literal_eval(row.label)
            else:
                labels = list(row.label)

            item.set_labels(labels)
            item.is_modified = row.is_modified
