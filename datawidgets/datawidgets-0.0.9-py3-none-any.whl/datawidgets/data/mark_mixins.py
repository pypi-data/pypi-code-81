from datawidgets.imports import *
from ..interface import *
from .image_mixins import *


class MarkAsSelectedMixin:
    def setup_mark_selected(self):
        pass

    def select(self):
        "Select and add respective CSS class"
        self.is_selected = True
        # self.view.add_class(CSS_NAMES.IMG_BOX_CONTAINER_SELECTED)
        self.item.add_class(CSS_NAMES.IMG_BOX_SELECTED)

    def unselect(self):
        "Unselect and remove respective CSS class"
        self.is_selected = False
        # self.view.remove_class(CSS_NAMES.IMG_BOX_CONTAINER_SELECTED)
        self.item.remove_class(CSS_NAMES.IMG_BOX_SELECTED)

    def toggle_selected_status(self):
        if not self.is_selected:
            self.select()
        elif self.is_selected:
            self.unselect()


class MarkAsDeletedMixin:
    def setup_mark_deleted(self):
        pass

    def mark_as_deleted(self):
        self.unselect()
        self.unmark_as_under_review()
        self.unmark_as_completed()
        self.is_deleted = True
        self.view.add_class(CSS_NAMES.IMG_DELETED)

    def unmark_as_deleted(self):
        self.unselect()
        self.is_deleted = False
        self.view.remove_class(CSS_NAMES.IMG_DELETED)


class MarkAsCompletedMixin:
    def setup_mark_completed(self):
        pass

    def mark_as_completed(self):
        self.unselect()
        self.is_completed = True
        self.item.add_class(CSS_NAMES.IMG_COMPLETED)

    def unmark_as_completed(self):
        self.unselect()
        self.is_completed = False
        self.item.remove_class(CSS_NAMES.IMG_COMPLETED)


class MarkAsReviewMixin:
    def setup_mark_review(self):
        pass

    def mark_as_under_review(self):
        self.unselect()
        self.is_under_review = True
        self.item.add_class(CSS_NAMES.IMG_IN_REVIEW)

    def unmark_as_under_review(self):
        self.unselect()
        self.is_under_review = False
        self.item.remove_class(CSS_NAMES.IMG_IN_REVIEW)