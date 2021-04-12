from datawidgets.imports import *
from datawidgets.ui import *
from IPython.display import FileLink


class DownloadModifiedMixin:
    def setup_download_modified(self):
        self.export_area = widgets.Output()

    def prep_download(self, *args, fname: str = None):
        df = self.get_results()
        if fname is None:
            fname = f"__results__{len(df)}-items.csv"
        df.to_csv(fname, index=False)
        link = FileLink(fname, result_html_prefix="<h3> Download Modified Items: </h3>")
        with self.export_area:
            self.export_area.clear_output()
            display(link)
            display(df)

    def generate_export_refresh_button(self, global_callbacks=[]):
        button = Button(description="Refresh Modified Items")
        button.on_click(self.prep_download)
        button.layout = CSS_LAYOUTS.wide_button

        return button


class ViewCompletedMixin:
    def get_completed_items(self):
        # if self.mark_completed_toggle.description == "Show Completed":
        #     self.mark_completed_toggle.click()
        completed_items = []
        for item in self.datapoints:
            if item.needs_refresh:
                item.load_img_bytes()
            if item.is_completed:
                completed_items.append(item)
        return completed_items

    def refresh_completed_grid(self, *args):
        self.review_datapoints = self.get_completed_items()
        self.update_review_grid()

    def generate_review_completed_button(self, global_callbacks=[]):
        button = Button(description="Show All Completed")
        button.on_click(self.refresh_completed_grid)
        button.layout.width = "180px"

        for cb in global_callbacks:
            button.on_click(cb)

        return button


class ViewModifiedMixin:
    def get_modified_items(self):
        review_items = []
        for item in self.datapoints:
            if item.needs_refresh:
                item.load_img_bytes()
            if item.is_modified:
                review_items.append(item)
        return review_items

    def refresh_modified_grid(self, *args):
        self.review_datapoints = self.get_modified_items()
        self.update_review_grid()

    def generate_review_modified_button(self, global_callbacks=[]):
        button = Button(description="Show All Modified")
        button.on_click(self.refresh_modified_grid)
        button.layout.width = "180px"

        for cb in global_callbacks:
            button.on_click(cb)

        return button


class ViewReviewMixin:
    def get_review_items(self):
        review_items = []
        for item in self.datapoints:
            if item.needs_refresh:
                item.load_img_bytes()
            if item.is_under_review:
                review_items.append(item)
        return review_items

    def refresh_review_grid(self, *args):
        self.review_datapoints = self.get_review_items()
        self.update_review_grid()

    def generate_review_review_button(self, global_callbacks=[]):
        button = Button(description="Show All Review")
        button.on_click(self.refresh_review_grid)
        button.layout.width = "180px"

        for cb in global_callbacks:
            button.on_click(cb)

        return button


class ViewDeletedMixin:
    def get_deleted_items(self):
        review_items = []
        for item in self.datapoints:
            if item.needs_refresh:
                item.load_img_bytes()
            if item.is_deleted:
                review_items.append(item)
        return review_items

    def refresh_deleted_grid(self, *args):
        self.review_datapoints = self.get_deleted_items()
        self.update_review_grid()

    def generate_review_deleted_button(self, global_callbacks=[]):
        button = Button(description="Show All Deleted")
        button.on_click(self.refresh_deleted_grid)
        button.layout.width = "180px"

        for cb in global_callbacks:
            button.on_click(cb)

        return button


class ViewSelectedMixin:
    def get_selected_items(self):
        selected_items = []
        for item in self.datapoints:
            if item.needs_refresh:
                item.load_img_bytes()
            if item.is_selected:
                selected_items.append(item)
        return selected_items

    def refresh_selected_grid(self, *args):
        self.review_datapoints = self.get_selected_items()
        self.update_review_grid()

    def generate_selected_refresh_button(self, global_callbacks=[]):
        button = Button(description="Show All Selected")
        button.on_click(self.refresh_selected_grid)
        button.layout.width = "180px"

        for cb in global_callbacks:
            button.on_click(cb)

        return button


class ReviewMixin(
    ViewModifiedMixin,
    ViewSelectedMixin,
    ViewCompletedMixin,
    ViewReviewMixin,
    ViewDeletedMixin,
):
    def update_review_grid(self, *args):
        children = []

        for item in self.review_datapoints:
            if hasattr(self, "minimal_view_mode"):
                if self.minimal_view_mode:
                    item.update_view_minimal()
            children.append(item.view)

        self.review_grid.children = children

    def setup_review_grid(self):
        self.review_grid = widgets.Box(
            children=[],
            width="100%",
            layout=CSS_LAYOUTS.flex_layout,
        )
        # self.view_selected_button = self.generate_review_refresh_button()
        # self.view_modified_items_button = self.generate_review_modified_button()
        # self.view_completed_items_button = self.generate_review_completed_button()
        # self.view_review_items_button = self.generate_review_review_button()
