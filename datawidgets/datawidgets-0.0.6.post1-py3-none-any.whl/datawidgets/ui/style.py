from datawidgets.imports import *


# TODO: Refactor
class CSS_LAYOUTS:
    empty = Layout(width="0px", height="0px")
    button_layout = Layout(
        margin="0",
        width="auto",
        height="30px",
        border="0.1px solid black",
        justify_content="flex-start",
    )
    flex_layout = Layout(
        display="flex",
        flex_flow="row wrap",
        width=f"100%",
        justify_content="center",
        align_items="center",
    )
    flex_layout_col = Layout(
        display="flex",
        flex_flow="column wrap",
        width=f"100%",
        justify_content="center",
        align_items="center",
    )
    center_aligned = Layout(align_items="center")
    autowidth = Layout(width="auto")
    wide_button = Layout(width="200px")
    flex_padded = Layout(
        display="flex",
        padding="0.25em",
        flex_flow="row wrap",
        width=f"100%",
        justify_content="center",
        align_items="center",
    )
    class_map_positive_buttons = Layout(
        display="flex",
        flex_flow="row wrap",
        width=f"100%",
        justify_content="flex-start",
    )
    class_map_negative_buttons = Layout(
        display="flex",
        flex_flow="row wrap",
        width=f"100%",
        justify_content="flex-end",
    )
    right_aligned = Layout(align_items="flex-end")


class CSS_SPACERS:
    def vspace(height: int = 10):
        return HBox([], layout=Layout(height=f"{height}px"))

    def hspace(width: int = 10):
        return HBox([], layout=Layout(width=f"{width}px"))


class CSS_NAMES:
    IMG_BOX = "image-box"
    IMG_COMPLETED = "image-box-completed"
    IMG_DELETED = "image-box-deleted"
    IMG_NOTE = "image-note"
    IMG_NOTE_HIDDEN = "image-note-hidden"
    IMG_IN_REVIEW = "image-in-review"

    TOGGLE_BUTTON = "toggle-button-custom"
    TOGGLE_IMG_NOTE_BUTTON = "toggle-image-note"
    TOGGLE_MATCHING_MODE = "toggle-matching-mode"
    TOGGLE_COMPLETED_STATUS_BUTTON = "toggle-image-completed-status"
    SHOW_COMPLETED_TOGGLE = "mark-as-completed-toggle"

    TOGGLE_REVIEW_STATUS_BUTTON = "toggle-image-review-status"
    SHOW_REVIEW_TOGGLE = "mark-as-review-toggle"

    GRID_RANGE_SLIDER = "grid-range-slider"
    RANGE_NEXT_PREV_BUTTONS = "range-prev-next-buttons"
    LABEL_BUTTON = "label-button"
    MODIFIED_LABEL_BUTTON = "label-button-modified"
    LABEL_BUTTON_TOGGLED = "label-button-toggled"
    LABEL_BUTTON_GROUP = "label-button-group"
    LABEL_SEARCH_BOX = "label-searchbox"
    AUTOCOMPLETE_BOX = "autocomplete-box"
    BATCH_ADD_BUTTON = "batch-add-button"
    BATCH_REMOVE_BUTTON = "batch-remove-button"
    FILE_UPLOAD_BUTTON = "file-upload-button"
    MAIN_INFO_PANEL = "main-info-panel"
    CLASS_MAP_POSITIVE_HEADING = "class-map-positive-heading"
    CLASS_MAP_NEGATIVE_HEADING = "class-map-negative-heading"
    CLASS_MAP_POSITIVE_BUTTONS = "class-map-buttons-positive"
    CLASS_MAP_POSITIVE_CONTAINER = "class-map-buttons-positive-container"
    CLASS_MAP_NEGATIVE_BUTTONS = "class-map-buttons-negative"
    CLASS_MAP_NEGATIVE_CONTAINER = "class-map-buttons-negative-container"

    def __init__(self):
        self.IMG_BOX_HOVER = f"{self.IMG_BOX}-on-hover"
        self.IMG_BOX_SELECTED = f"{self.IMG_BOX}-selected"
        self.IMG_BOX_CONTAINER = f"{self.IMG_BOX}-container"
        self.IMG_BOX_CONTAINER_MINIMAL = f"{self.IMG_BOX_CONTAINER}-minimal"
        self.IMG_BOX_CONTAINER_SELECTED = f"{self.IMG_BOX_CONTAINER}-selected"
        self.FILE_UPLOAD_REFRESH_BUTTON = f"{self.FILE_UPLOAD_BUTTON}-refresh"
        self.FILE_UPLOAD_CONTAINER = f"{self.FILE_UPLOAD_BUTTON}-container"
        self.FILE_UPLOAD_GO_BUTTON = f"{self.FILE_UPLOAD_BUTTON}-go"


CSS_NAMES = CSS_NAMES()
