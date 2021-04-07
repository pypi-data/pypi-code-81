from datawidgets.imports import *
from .review_mixins import *
from .filtering_mixins import *
from .dataset_mixins import *
from .mark_mixins import *
from datawidgets.data import *
from datawidgets.interface import *
from datawidgets.utils import *


class ImageDataset(
    AbstractInterface,
    ImageGridMixin,
    WidthSliderMixin,
    SelectionMixin,
    InfoMixin,
):
    def __init__(
        self, df, batch_size: int = 50, width: int = 100, filename_col: str = "filename"
    ):
        self.df = df
        self.batch_size = batch_size
        self.filename_col = filename_col
        self.df.index = self.df[self.filename_col]
        self.width = width
        # self.num_deleted = 0

        self.setup()
        self.setup_view()

    def setup_items(self):
        items = {}
        for idx, fname in tqdm(
            self.df[self.filename_col].iteritems(),
            total=len(self),
            desc="Setup Data Items",
        ):
            item = ImageDataPoint(fname)
            items[idx] = item
        self.datapoints = pd.Series(items)

    @staticmethod
    def _check_filter(filter_: Union[Sequence[str], np.ndarray, pd.Series]):
        if isinstance(filter_, pd.Series):
            # Keep only True values if boolean masking
            if isinstance(filter_.iloc[0], (bool, np.bool8, np.bool)):
                filter_ = filter_[filter_]
            filter_ = filter_.index.values
        return filter_

    def filter_dataset(self, filter_: Union[Sequence[str], np.ndarray, pd.Series]):
        "Returns a view of `self.df` without any modifications"
        filter_ = self._check_filter(filter_)
        return self.df.loc[filter_]

    def filter_and_mutate_dataset(
        self, filter_: Union[Sequence[str], np.ndarray, pd.Series]
    ):
        """
        Reorder and/or delete items from internal dataset by self.df's index, which
            is set to the filename on init
        If passing in a boolean `pd.Series` mask, only True values are kept
        """
        filter_ = self._check_filter(filter_)
        items = {}
        for i in filter_:
            # del self.datapoints[i]
            items[i] = self.datapoints[i]
        self.datapoints = items
        self.df = self.df.loc[filter_]

    def refresh(self):
        self.update_grid()
        self.update_info()

    def setup(self):
        self.setup_items()
        self.setup_logging()
        self.setup_width_slider()
        self.setup_img_grid()
        self.setup_info()

    def __len__(self):
        return len(self.df)

    # TODO: Is it inefficient to have these properties for very large datasets?
    @property
    def selected_names(self):
        return [item.source for item in self.selected_items]

    @property
    def num_modified(self):
        return sum([item.is_modified for item in self.datapoints])

    @property
    def num_deleted(self):
        return sum([item.is_deleted for item in self.datapoints])

    @property
    def num_selected(self):
        num_selected = sum([item.is_selected for item in self.datapoints])
        if hasattr(self, "similarity_button"):
            if num_selected > 1:
                self.similarity_button.disabled = True
            else:
                self.similarity_button.disabled = False
        return num_selected

    @property
    def selected_items(self):
        return [item for item in self.datapoints if item.is_selected]
        # return [item for item in self.active_datapoints if item.is_selected]

    @property
    def num_loaded(self):
        return sum([item.is_loaded for item in self.datapoints])


class ImageClassificationDataset(
    ImageDataset,
    BatchClassificationLabelsMixin,
    ClassMapFilterMixin,
    ReviewMixin,
    DownloadModifiedMixin,
    MinimalViewMixin,
    MarkSelectedAsCompletedMixin,
    MarkSelectedAsReviewMixin,
    MarkSelectedAsDeletedMixin,
):
    def __init__(
        self,
        df,
        filename_col: str = "filename",
        batch_size: int = 50,
        width: int = 25,
        class_map: Optional[ClassMap] = None,
        label_col: str = "label",
        is_multilabel: bool = False,
    ):
        self.df = df
        self.label_col = label_col
        self.filename_col = filename_col
        self.is_multilabel = is_multilabel

        if class_map is None:
            self.class_map = self.parse_class_map_from_df()
        else:
            self.class_map = class_map
        self.classes = self.class_map._id2class

        # HACK: blah..
        super().__init__(
            df=self.df, filename_col=filename_col, batch_size=batch_size, width=100
        )
        self.width = width
        self.width_slider.value = self.width

    def parse_class_map_from_df(self):
        """
        Derives the ClassMap from all the unique values in `self.label_col`
        """
        self.df[self.label_col] = self.df[self.label_col].apply(convert_labels_to_list)
        if not self.is_multilabel:

            def truly_single_label(row: pd.Series):
                label = row[self.label_col]
                fname = row[self.filename_col]
                if not len(label) == 1:
                    raise ValueError(
                        f"Expected only one label per image in single label mode, but '{fname}' "
                        f"has {len(label)} labels: {label}"
                    )

            self.df.apply(truly_single_label, axis=1)

        all_labels = self.df[self.label_col].values
        return ClassMap(
            classes=uniqueify(flatten(all_labels)),
            background=None,
        )

    def get_results(self):
        # TODO: Use a named tuple or dataclass for rows
        rows = []

        # Iterate through all datapoints and find the completed / modified items
        for fname, item in self.datapoints.items():

            # TODO: Should we load and show all datapoints?
            # or skip the item altogether?
            if not item.is_loaded:
                continue
                # item.load()

            filename = fname
            labels = item.labels
            note = item.note.value

            if not item.is_deleted:
                rows.append(
                    [
                        fname,
                        labels,
                        note,
                        item.is_modified,
                        item.is_completed,
                        item.is_under_review,
                        item.is_deleted,
                    ]
                )

        modified_df = pd.DataFrame(
            rows,
            columns=[
                self.filename_col,
                self.label_col,
                "notes",
                "is_modified",
                "is_completed",
                "is_under_review",
                "is_deleted",
            ],
        )

        # Merge with main dataframe while replacing the `self.label_col`
        modified_df = modified_df.merge(
            self.df.drop(columns=[self.label_col]).reset_index(drop=True),
            on=self.filename_col,
        )
        modified_df.index = modified_df[self.filename_col]
        return modified_df

    def setup(self):
        # super().setup()

        self.setup_logging()
        self.setup_width_slider()
        self.setup_batch_labelling()

        self.setup_review_grid()
        self.setup_download_modified()

        self.setup_info()
        self.setup_items()

        self.setup_class_map_filtering()
        self.setup_img_grid()

        self.update_info()
        self.update_batch_labelling_descriptions()

    @property
    def num_completed(self):
        return sum([item.is_completed for item in self.datapoints])

    def setup_items(self):
        items = {}
        for idx, row in tqdm(
            self.df.iterrows(), total=len(self.df), desc="Setting Up Data Items"
        ):
            item = ImageWithLabels(
                source=getattr(row, self.filename_col),
                class_map=self.class_map,
                labels=row[self.label_col],
                is_multilabel=self.is_multilabel,
                parent_dataset=self,
            )
            items[idx] = item
        self.datapoints = pd.Series(items)

    def setup_view(self, global_callbacks=[]):
        callbacks = [
            self.update_info,
            self.update_batch_labelling_descriptions,
        ]

        self.setup_class_map_filtering_view(global_callbacks=callbacks)

        self.setup_view_mark_completed(callbacks=[self.update_grid] + callbacks)
        self.setup_view_mark_review(callbacks=[self.update_grid] + callbacks)
        self.setup_view_mark_deleted(callbacks=[self.update_grid] + callbacks)

        (
            decrement_range,
            view_range_slider,
            increment_range,
        ) = self.generate_grid_range_slider()
        unselect_button = self.generate_unselect_all_button(callbacks)
        select_button = self.generate_select_all_button(callbacks)
        invert_selection_button = self.generate_invert_selection_button(callbacks)
        self.minimal_view_button = self.generate_minimal_view_button()

        refresh_review_modified_button = self.generate_review_modified_button()
        refresh_view_selected_button = self.generate_selected_refresh_button()
        refresh_review_completed_button = self.generate_review_completed_button()
        refresh_review_review_button = self.generate_review_review_button()
        refresh_review_deleted_button = self.generate_review_deleted_button()
        refresh_export_button = self.generate_export_refresh_button()

        self.class_map_filter_button.on_click(self.update_grid_range_slider)
        self.class_map_filter_button.on_click(self.reset_grid_range_value)

        try:

            def reset_grid_idxs(*args):
                self.grid_range_slider.value = (
                    0,
                    min(self.grid_range_slider.value[1], len(self)),
                )

            self.similarity_button = self.generate_similarity_button(callbacks=[])
            self.similarity_button.on_click(reset_grid_idxs)

        except:
            self.similarity_button = Button()
            self.similarity_button.layout = CSS_LAYOUTS.empty

        self.set_grid_range_slider(view_range_slider)

        status_controls = HBox(
            # [
            #     self.mark_deleted_button,
            #     self.mark_completed_button,
            #     self.mark_review_button,
            #     self.mark_deleted_toggle,
            #     self.mark_completed_toggle,
            #     self.mark_review_toggle,
            # ]
            [
                self.mark_deleted_controls,
                self.mark_completed_contols,
                self.mark_review_controls,
            ]
        )
        selection_controls = HBox(
            [select_button, invert_selection_button, unselect_button]
        )
        image_view_controls = HBox(
            [
                self.width_slider,
                decrement_range,
                self.grid_range_slider,
                increment_range,
            ]
        )
        grid_view_controls = HBox([self.minimal_view_button])
        sorting_controls = HBox([self.similarity_button])
        batch_labelling_controls = HBox(
            [
                self.batch_add_button,
                self.batch_remove_button,
            ]
        )
        review_controls = HBox(
            [
                refresh_review_modified_button,
                refresh_view_selected_button,
                refresh_review_completed_button,
                refresh_review_review_button,
                refresh_review_deleted_button,
            ]
        )

        status_controls.layout = CSS_LAYOUTS.flex_layout
        selection_controls.layout = CSS_LAYOUTS.flex_layout
        image_view_controls.layout = CSS_LAYOUTS.flex_layout
        grid_view_controls.layout = CSS_LAYOUTS.flex_layout
        sorting_controls.layout = CSS_LAYOUTS.flex_layout
        batch_labelling_controls.layout = CSS_LAYOUTS.flex_padded
        review_controls.layout = CSS_LAYOUTS.flex_layout

        REVIEW_TAB = widgets.VBox(
            [
                review_controls,
                self.info,
                HBox([self.width_slider], layout=CSS_LAYOUTS.flex_layout),
                HBox([self.mark_completed_button], layout=CSS_LAYOUTS.flex_layout),
                batch_labelling_controls,
                self.review_grid,
            ]
        )

        # refresh_export_button.click()
        refresh_export_button_centered = HBox([refresh_export_button])
        refresh_export_button_centered.layout = CSS_LAYOUTS.flex_layout
        EXPORT_TAB = VBox(
            [
                refresh_export_button_centered,
                self.export_area,
            ]
        )

        MAIN_CONTROLS = widgets.VBox(
            [
                self.class_map_filtering_controls,
                image_view_controls,
                status_controls,
                selection_controls,
                sorting_controls,
                grid_view_controls,
                batch_labelling_controls,
            ]
        )

        MAIN_OUTPUT = widgets.Tab(
            [
                widgets.VBox([MAIN_CONTROLS, self.info, self.grid]),
                REVIEW_TAB,
                EXPORT_TAB,
            ]
        )

        MAIN_OUTPUT.set_title(0, "Main Labelling Main Labelling")
        MAIN_OUTPUT.set_title(1, "Review")
        MAIN_OUTPUT.set_title(2, "Export")
        self.view = MAIN_OUTPUT


class CinemaNetDataset(ImageClassificationDataset, CinemaNetSimilarityMixin):
    def __init__(
        self,
        df,
        batch_size: int = 50,
        width: int = 25,
        class_map: Optional[ClassMap] = None,
        label_col: str = "label",
        is_multilabel: bool = False,
    ):
        super().__init__(
            df=df,
            batch_size=batch_size,
            width=width,
            label_col=label_col,
            class_map=class_map,
            is_multilabel=is_multilabel,
        )

    def setup(self):
        super().setup()
        self.setup_similarity()
