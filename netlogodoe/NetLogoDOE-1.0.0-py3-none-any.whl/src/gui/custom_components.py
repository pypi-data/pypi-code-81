import PySimpleGUI as sg


def header(text):
    return sg.Text(text, font=('', 30))


def title(text):
    return sg.Text(text, font=('', 20), auto_size_text=True)


def number_input(key, text=''):
    return sg.Input(text, key=key, size=(5, 1))


def text_input(key, text=''):
    return sg.Input(text, key=key, size=(25, 1))


def explanation(text):
    return sg.Text(text, font=('', 8), pad=(0, 0))


def configuration_parameter_text(text):
    return sg.Text(text, size=(15, 1), pad=(0, 0))


def configuration_value_text(text, key):
    return sg.Text(text, key=key, auto_size_text=False, pad=(0, 0))


def configuration_horizontal_line():
    return sg.Text('---------------------------------------------------------------------------', pad=(0, 0))


def question_mark_button(key, padding=None):
    return sg.Button(' ? ', font=('', 10, 'bold'), key=key, pad=padding)


def metric3_radio_buttons(prefix):
    return [sg.Radio('Average', f'{prefix}_radiogroup', key=f'{prefix}_metric_1', enable_events=True),
            sg.Radio('Minimum', f'{prefix}_radiogroup', key=f'{prefix}_metric_2', enable_events=True),
            sg.Radio('Maximum', f'{prefix}_radiogroup', key=f'{prefix}_metric_3', enable_events=True)]


def metric4_radio_buttons(prefix):
    return [sg.Radio('Average', f'{prefix}_radiogroup', key=f'{prefix}_metric_1'),
            sg.Radio('Minimum', f'{prefix}_radiogroup', key=f'{prefix}_metric_2'),
            sg.Radio('Maximum', f'{prefix}_radiogroup', key=f'{prefix}_metric_3'),
            sg.Radio('Last', f'{prefix}_radiogroup', key=f'{prefix}_metric_4')]
