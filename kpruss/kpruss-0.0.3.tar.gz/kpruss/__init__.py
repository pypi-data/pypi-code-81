import pathlib


def setup(app):
    app.add_html_theme("kpruss", pathlib.Path(__file__).parent)
