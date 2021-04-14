import math

import PySimpleGUI as sg


def get_layout(text):
    returns = text.count('\n')
    if returns == 0:
        layout = [[sg.Text(text, size=(50, math.ceil(len(text) / 50)))],
                  [sg.CloseButton('Ok')]]
    else:
        layout = [[sg.Text(text, size=(50, math.floor(len(text) / 50) + returns))],
                  [sg.CloseButton('Ok')]]
    return layout


def show_error_window(text, location=(600, 100)):
    print(location)
    layout = get_layout(text)
    error_window = sg.Window('Error', layout=layout, element_justification='c', finalize=True,
                            location=(location[0], location[1]))

    error_window.read()


def show_help_window(text, location=(600, 100)):
    layout = get_layout(text)
    help_window = sg.Window('Help', layout=layout, element_justification='c', finalize=True,
                             location=(location[0], location[1]))

    help_window.read()
