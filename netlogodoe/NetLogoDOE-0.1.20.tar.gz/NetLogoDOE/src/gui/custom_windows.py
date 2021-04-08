import math

import PySimpleGUI as sg


def show_error_window(text):
    layout = [[sg.Text(text)],
              [sg.CloseButton('Ok')]]
    error_window = sg.Window('Error', layout=layout, element_justification='c', finalize=True)

    error_window.read()


def show_help_window(text, location=(600, 100)):
    returns = text.count('\n')
    if returns == 0:
        layout = [[sg.Text(text, size=(50, math.ceil(len(text) / 50)))],
                  [sg.CloseButton('Ok')]]
    else:
        layout = [[sg.Text(text, size=(50, math.floor(len(text) / 50) + returns))],
                  [sg.CloseButton('Ok')]]
    error_window = sg.Window('Help', layout=layout, element_justification='c', finalize=True,
                             location=(location[0] + 100, location[1] + 100))

    error_window.read()
