import Orange.data
import numpy
from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Input
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget, Output

class OWDataSamplerB(OWWidget):
    name = "Data SamplerBB"
    description = "Randomly selects a subset of instances from the dataset."
    icon = "icons/number.svg"

    class Inputs:
        data = Input("Data", Orange.data.Table)

    class Outputs:
        sample = Output("Sampled Data", Orange.data.Table)

    proportion = Setting(50)
    commitOnChange = Setting(0)
    def __init__(self):
        super().__init__()

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something."
        )
        self.infob = gui.widgetLabel(box, "")

        gui.separator(self.controlArea)
        self.optionsBox = gui.widgetBox(self.controlArea, "Options")
        gui.spin(
            self.optionsBox,
            self,
            "proportion",
            minv=10,
            maxv=90,
            step=10,
            label="Sample Size [%]:",
            callback=[self.selection, self.checkCommit],
        )
        gui.checkBox(
            self.optionsBox, self, "commitOnChange", "Commit data on selection change"
        )
        gui.button(self.optionsBox, self, "Commit", callback=self.commit)
        self.optionsBox.setDisabled(True)

    @Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.dataset = dataset
            self.infoa.setText("%d instances in input dataset" % len(dataset))
            self.optionsBox.setDisabled(False)
            self.selection()
        else:
            self.dataset = None
            self.sample = None
            self.optionsBox.setDisabled(False)
            self.infoa.setText("No data on input yet, waiting to get something.")
            self.infob.setText("")
        self.commit()

    def selection(self):
        if self.dataset is None:
            return

        n_selected = int(numpy.ceil(len(self.dataset) * self.proportion / 100.0))
        indices = numpy.random.permutation(len(self.dataset))
        indices = indices[:n_selected]
        self.sample = self.dataset[indices]
        self.infob.setText("%d sampled instances" % len(self.sample))

    def commit(self):
        self.Outputs.sample.send(self.sample)

    def checkCommit(self):
        if self.commitOnChange:
            self.commit()