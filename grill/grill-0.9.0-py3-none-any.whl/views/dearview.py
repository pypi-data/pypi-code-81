from pxr.Usdviewq.stageView import StageView
from pxr.Usdviewq import appController
from PySide2 import QtWidgets
from pxr import Usd


if __name__ == "__main__":
    import sys
    # from PySide2 import QtWebEngine
    # QtWebEngine.QtWebEngine.initialize()
    app = QtWidgets.QApplication(sys.argv)
    print("app")
    stage = Usd.Stage.Open(
        r"B:\read\cg\downloads\Kitchen_set\Kitchen_set\Kitchen_set.usd")
    print("stage")

    _printTiming = True
    _settings2 = appController.settings2.Settings(appController.SETTINGS_VERSION)
    print(_settings2)
    _dataModel = appController.UsdviewDataModel(
                _printTiming, _settings2)
    _dataModel.stage = stage
    print(_dataModel)
    _stageView = StageView(parent=None,
                    dataModel=_dataModel,
                    printTiming=_printTiming)
    _stageView.updateView(resetCam=False, forceComputeBBox=True)
    print(_stageView)
    _stageView.update()
    _stageView.updateView()
    _stageView.show()
    sys.exit(app.exec_())
