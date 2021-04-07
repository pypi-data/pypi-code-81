from Orange.widgets.widget import OWWidget, Output
from Orange.widgets.widget import OWWidget, Input
from Orange.widgets import gui
from Orange.widgets.settings import Setting

class IntNumber(OWWidget):
    # Widget's name as displayed in the canvas
    name = "Integer Number"
    # Short widget description
    description = "Lets the user input a number"

    # An icon resource file path for this widget
    # (a path relative to the module where this widget is defined)
    icon = "../icons/number.svg"

    # Widget's outputs; here, a single output named "Number", of type int
    class Outputs:
        number = Output("Number", int)
        # Basic (convenience) GUI definition:
        #   a simple 'single column' GUI layout
    want_main_area = True
    #   with a fixed non resizable geometry.
    resizing_enabled = True
    number = Setting(42)

    def __init__(self):
        super().__init__()

        from AnyQt.QtGui import QIntValidator
        gui.lineEdit(self.controlArea, self, "number", "Enter a number",
                     box="Number",
                     callback=self.number_changed,
                     valueType=int, validator=QIntValidator())
        self.number_changed()

    def number_changed(self):
        # Send the entered number on "Number" output
        self.Outputs.number.send(self.number)



