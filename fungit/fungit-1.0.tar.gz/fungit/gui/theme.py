from .style import Color


class Theme:
    DEFAULT = Color.fg("#ee")
    BOX_SELECTED_COLOR = Color.fg("#48D1CC")  # lightpink

    FILE_NEW = Color.fg("#4682B4")  # SteelBlue
    FILE_UNTRACK = Color.fg("#F08080")  # LightCoral

    FILE_CACHED = Color.fg("#87CEFA")  # LightSkyBlue
    FILE_RENAME = Color.fg("#87CEFA")
    FILE_DELED = Color.fg("#98FB98")

    FILE_DEL = Color.fg("#F08080")
    FILE_CHANGE = Color.fg("#F08080")

    BRANCH = Color.fg("#87CEFA")
    BRANCH_STATUS = Color.fg("#F0E68C")  # Linen

    PUSHED = Color.fg("#F0E68C")
    UNPUSHED = Color.fg("#F08080")

    ADDITION = Color.fg("#87CEFA")
    DELETION = Color.fg("#F08080")
