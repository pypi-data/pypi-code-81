from datawidgets.imports import *
from datawidgets.utils import *
from datawidgets.data import *
from .image_dataset import *


class MarkSelectedAsDeletedMixin:
    ""

    def toggle_selected_images_deleted_status(self, *args):
        for item in self.datapoints:
            if item.is_selected:
                if item.is_deleted:
                    item.unmark_as_deleted()
                elif not item.is_deleted:
                    item.mark_as_deleted()

    def toggle_view_mark_deleted(self, *args):
        self.hide_deleted = not self.hide_deleted

    def generate_view_deleted_toggle_button(self, callbacks=[]):
        toggle = widgets.Button(description="Hide Deleted")
        toggle.add_class(CSS_NAMES.SHOW_COMPLETED_TOGGLE)

        def change_btn_description(*args):
            self.toggle_view_mark_deleted()
            if self.hide_deleted:
                toggle.description = "Show Deleted"
            else:
                toggle.description = "Hide Deleted"

        toggle.on_click(change_btn_description)
        for cb in callbacks:
            toggle.on_click(cb)

        return toggle

    def generate_mark_deleted_button(self, callbacks=[]):

        button = Button(description="Delete Images")
        button.add_class(CSS_NAMES.TOGGLE_REVIEW_STATUS_BUTTON)
        button.on_click(self.toggle_selected_images_deleted_status)

        for cb in callbacks:
            button.on_click(cb)

        return button

    def setup_view_mark_deleted(self, callbacks=[]):
        self.hide_deleted = False
        self.mark_deleted_button = self.generate_mark_deleted_button(
            callbacks=callbacks
        )
        self.mark_deleted_toggle = self.generate_view_deleted_toggle_button(
            callbacks=callbacks
        )
        self.mark_deleted_toggle.click()
        self.mark_deleted_controls = VBox(
            [self.mark_deleted_button, self.mark_deleted_toggle],
            layout=CSS_LAYOUTS.center_aligned,
        )


class MarkSelectedAsReviewMixin:
    """
    Enables ability to mark selected images in the _grid_ only as completed
    """

    def toggle_selected_images_review_status(self, *args):
        for item in self.datapoints:
            if item.is_selected:
                if item.is_under_review:
                    item.unmark_as_under_review()
                elif not item.is_under_review:
                    item.mark_as_under_review()

    def toggle_view_mark_review(self, *args):
        self.hide_review = not self.hide_review

    def generate_view_review_toggle_button(self, callbacks=[]):
        toggle = widgets.Button(description="Hide Review")
        toggle.add_class(CSS_NAMES.SHOW_COMPLETED_TOGGLE)

        def change_btn_description(*args):
            self.toggle_view_mark_review()
            if self.hide_review:
                toggle.description = "Show Review"
            else:
                toggle.description = "Hide Review"

        toggle.on_click(change_btn_description)
        for cb in callbacks:
            toggle.on_click(cb)

        return toggle

    def generate_mark_review_button(self, callbacks=[]):

        button = Button(description="Mark For Review")
        button.add_class(CSS_NAMES.TOGGLE_REVIEW_STATUS_BUTTON)
        button.on_click(self.toggle_selected_images_review_status)

        for cb in callbacks:
            button.on_click(cb)

        return button

    def setup_view_mark_review(self, callbacks=[]):
        self.hide_review = False
        self.mark_review_button = self.generate_mark_review_button(callbacks=callbacks)
        self.mark_review_toggle = self.generate_view_review_toggle_button(
            callbacks=callbacks
        )
        self.mark_review_controls = VBox(
            [self.mark_review_button, self.mark_review_toggle],
            layout=CSS_LAYOUTS.center_aligned,
        )


class MarkSelectedAsCompletedMixin:
    """
    Enables ability to mark selected images in the _grid_ only as completed
    """

    def toggle_selected_images_completed_status(self, *args):
        for item in self.datapoints:
            if item.is_selected:
                if item.is_completed:
                    item.unmark_as_completed()
                elif not item.is_completed:
                    item.mark_as_completed()

    def toggle_view_mark_completed(self, *args):
        self.hide_completed = not self.hide_completed

    def generate_view_completed_toggle_button(self, callbacks=[]):
        toggle = widgets.Button(description="Hide Completed")
        toggle.add_class(CSS_NAMES.SHOW_COMPLETED_TOGGLE)

        def change_btn_description(*args):
            self.toggle_view_mark_completed()
            if self.hide_completed:
                toggle.description = "Show Completed"
            else:
                toggle.description = "Hide Completed"

        toggle.on_click(change_btn_description)
        for cb in callbacks:
            toggle.on_click(cb)

        return toggle

    def generate_mark_completed_button(self, callbacks=[]):

        button = Button(description="Mark As Complete / Incomplete")
        button.add_class(CSS_NAMES.TOGGLE_COMPLETED_STATUS_BUTTON)
        button.on_click(self.toggle_selected_images_completed_status)

        for cb in callbacks:
            button.on_click(cb)

        return button

    def setup_view_mark_completed(self, callbacks=[]):
        self.hide_completed = False
        self.mark_completed_button = self.generate_mark_completed_button(
            callbacks=callbacks
        )
        self.mark_completed_toggle = self.generate_view_completed_toggle_button(
            callbacks=callbacks
        )
        self.mark_completed_toggle.click()
        self.mark_completed_contols = VBox(
            [self.mark_completed_button, self.mark_completed_toggle],
            layout=CSS_LAYOUTS.center_aligned,
        )
