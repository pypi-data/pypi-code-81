import Orange.data
import numpy
from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Input
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget, Output

class OWDataSamplerB(OWWidget):
    name = "hyperparameter_optimization"
    description = "searching hyperparameter"
    icon = "icons/plus.svg"

    class Inputs:
        data = Input("Data", Orange.data.Table)
        learner = Input("Learner", Orange.classification.RandomForestLearner, multiple=True)

    class Outputs:
        sample = Output("Sampled Data", Orange.data.Table)
        other = Output("Other Data", Orange.data.Table)

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

    @Inputs.learner
    def set_learner(self, learner, id):
        """Set the input learner for channel id."""
        if id in self.learners:
            if learner is None:
                # remove a learner and corresponding results
                del self.learners[id]
                del self.results[id]
                del self.curves[id]
            else:
                # update/replace a learner on a previously connected link
                self.learners[id] = learner
                # invalidate the cross-validation results and curve scores
                # (will be computed/updated in `_update`)
                self.results[id] = None
                self.curves[id] = None
        else:
            if learner is not None:
                self.learners[id] = learner
                # initialize the cross-validation results and curve scores
                # (will be computed/updated in `_update`)
                self.results[id] = None
                self.curves[id] = None

        if len(self.learners):
            self.infob.setText("%d learners on input." % len(self.learners))
        else:
            self.infob.setText("No learners.")

        self.commitBtn.setEnabled(len(self.learners))

    def selection(self):
        if self.dataset is None:
            return

        n_selected = int(numpy.ceil(len(self.dataset) * self.proportion / 100.0))
        indices = numpy.random.permutation(len(self.dataset))
        indices_sample = indices[:n_selected]
        indices_other = indices[n_selected:]
        self.sample = self.dataset[indices_sample]
        self.otherdata = self.dataset[indices_other]
        self.infob.setText("%d sampled instances" % len(self.sample))

    def commit(self):
        self.Outputs.sample.send(self.sample)
        self.Outputs.sample.send(self.otherdata)

    def checkCommit(self):
        if self.commitOnChange:
            self.commit()