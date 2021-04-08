from collections import OrderedDict

import numpy
from AnyQt.QtWidgets import QTableWidget, QTableWidgetItem

import Orange.data
import Orange.classification
import Orange.evaluation
from bayes_opt import BayesianOptimization
from bayes_opt import UtilityFunction
import warnings
from Orange.widgets import gui, settings
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input
from Orange.evaluation.testing import Results


class OWLearningCurveA(OWWidget):
    name = "hyperparameter_optimization"
    description = (
        "Takes a dataset and a set of learners and shows a learning curve in "
        "a table."
    )
    icon = "icons/plus.svg"
    priority = 1000

    # [start-snippet-1]
    class Inputs:
        data = Input("Data", Orange.data.Table)
        learner = Input("Learner", Orange.base.Learner, multiple=True)

    # [end-snippet-1]

    #: cross validation folds
    folds = settings.Setting(5)
    #: points in the learning curve
    steps = settings.Setting(10)
    #: index of the selected scoring function
    scoringF = settings.Setting(0)
    #: compute curve on any change of parameters

    def __init__(self):
        super().__init__()

        # [start-snippet-2]
        self.scoring = [
            ("Classification Accuracy", Orange.evaluation.scoring.CA),
            ("AUC", Orange.evaluation.scoring.AUC),
            ("Precision", Orange.evaluation.scoring.Precision),
            ("Recall", Orange.evaluation.scoring.Recall),
        ]
        # [end-snippet-2]
        #: input data on which to construct the learning curve
        self.data = None
        #: A {input_id: Learner} mapping of current learners from input channel
        self.learners = OrderedDict()
        #: A {input_id: List[Results]} mapping of input id to evaluation
        #: results list, one for each curve point
        self.results = OrderedDict()
        #: A {input_id: List[float]} mapping of input id to learning curve
        #: point scores

        # GUI
        # table widget
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(box, "No data on input.")
        self.infob = gui.widgetLabel(box, "No learners.")
        self.table = gui.table(self.mainArea)

    ##########################################################################
    # slots: handle input signals

    @Inputs.data
    def set_dataset(self, data):
        """Set the input train dataset."""
        # Clear all results/scores
        for id in list(self.results):
            self.results[id] = None

        self.data = data

        if data is not None:
            self.infoa.setText("%d instances in input dataset" % len(data))
        else:
            self.infoa.setText("No data on input.")

    @Inputs.learner
    def set_learner(self, learner, id):
        """Set the input learner for channel id."""
        if id in self.learners:
            if learner is None:
                # remove a learner and corresponding results
                del self.learners[id]
                del self.results[id]
            else:
                # update/replace a learner on a previously connected link
                self.learners[id] = learner
                # invalidate the cross-validation results and curve scores
                # (will be computed/updated in `_update`)
                self.results[id] = None
        else:
            if learner is not None:
                self.learners[id] = learner
                # initialize the cross-validation results and curve scores
                # (will be computed/updated in `_update`)
                self.results[id] = None

        if len(self.learners):
            self.infob.setText("%d learners on input." % len(self.learners))
            self._update_table()
        else:
            self.infob.setText("No learners.")


    def _update_table(self):
        self.table.setRowCount(0)
        self.table.setRowCount(300)
        self.table.setColumnCount(len(self.learners))

        self.table.setHorizontalHeaderLabels(
            tuple([x[0] for x in self.scoring])
        )
        #self.table.setVerticalHeaderLabels(
            #["{:.2f}".format(p) for p in n_estimators]
        #)
        print(self.opt())

        for column in self.opt():
            self.table.setItem(
                QTableWidgetItem("{:.5f}".format(column))
            )
    def black_box_function(self, n_estimators):
        n_estimators = int(n_estimators)
        rf = Orange.classification.RandomForestLearner(n_estimators=n_estimators)
        res = Orange.evaluation.CrossValidation(self.data, [rf], k=10)
        return Orange.evaluation.scoring.CA(res)[0]

    def opt(self):
        optimizer = BayesianOptimization(
            f=self.black_box_function,
            pbounds={'n_estimators': (1, 10)},
            verbose=5
        )
        optimizer.maximize(init_points=50, n_iter=10, acq='ei', xi=0.6)

        return optimizer.max

if __name__ == "__main__":
    WidgetPreview(OWLearningCurveA).run()
