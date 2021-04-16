import pathlib
import PySimpleGUI as sg

sg.theme("Reddit")


def create_progress_status():
    return sg.Column(
        [
            [
                sg.Frame(
                    layout=[
                        [
                            sg.ProgressBar(
                                100, orientation="h", key="PROGRESS", size=(50, 2)
                            )
                        ],
                        [
                            sg.Text(
                                key="PROGRESS-TEXT",
                                justification="center",
                                size=(60, 1),
                                text_color="light blue",
                            )
                        ],
                        [
                            sg.Text(
                                key="STATS",
                                justification="left",
                                size=(30, 5),
                                text_color="#b4c1c5",
                            )
                        ],
                        [
                            sg.Text(
                                key="FEEDBACK",
                                justification="center",
                                size=(60, 2),
                                text_color="#f39a87",
                            )
                        ],
                    ],
                    title="Status",
                    element_justification="center",
                )
            ]
        ],
        justification="center",
    )


def create_bottom_buttons(with_authentication=True):

    buttons = [
        sg.Button(
            "Start",
            key="START",
            size=(10, 1),
        ),
        sg.Button("Stop", key="STOP", size=(10, 1), disabled=True),
        sg.Button("View log", key="VIEW-LOG", size=(10, 1), disabled=False),
        sg.Button(
            "Authenticate", key="AUTH", size=(10, 1), visible=with_authentication
        ),
    ]

    bottom_buttons = sg.Column([buttons], justification="center")
    return bottom_buttons


def create_checkboxes():
    result = sg.Column(
        [
            [
                sg.Checkbox("Delete after upload", default=False, key="DELETE"),
                sg.Checkbox(
                    "Date & time as prefix", default=False, key="DATETIME-PREFIX"
                ),
            ]
        ],
        justification="center",
    )
    return result


def create_layout(
    with_bucket_id=True,
    with_authentication=True,
    with_service_account=True,
    with_checkboxes=True,
    with_key=True,
    default_file_browser_text=(
        f"e.g. '{pathlib.Path.home() / 'directory-to-upload'}'   or browse →"
    ),
    default_bucket="",
):

    layout = [
        [
            sg.Text("File(s) or Folder", size=(20, 1)),
            sg.Input(
                default_file_browser_text,
                key="PATHS",
            ),
            sg.FilesBrowse("Files", target="PATHS"),
            sg.FolderBrowse("Folder", target="PATHS"),
        ],
    ]
    if with_bucket_id:
        layout.append(
            [
                sg.Text("Bucket ID", size=(20, 1)),
                sg.Input(default_bucket, key="BUCKET"),
            ],
        )
    if with_service_account:
        layout.append(
            [
                sg.Text("Service Account File", size=(20, 1)),
                sg.Input(
                    "",
                    key="SA-FILE",
                ),
                sg.FileBrowse(),
            ]
        )
    if with_key:
        layout.append(
            [
                sg.Text("Password", size=(20, 1)),
                sg.Input(
                    "",
                    key="PW",
                    password_char='*',
                ),
            ]
        )

    if with_checkboxes:
        layout += [[create_checkboxes()]]

    layout += [
        [create_progress_status()],
        [create_bottom_buttons(with_authentication)],
    ]

    return layout
