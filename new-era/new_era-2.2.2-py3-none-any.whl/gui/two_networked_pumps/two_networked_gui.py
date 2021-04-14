import sys
import logging
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication

from new_era.peristaltic_pump_network import PeristalticPumpNetwork, PeristalticPump
from new_era.utils import NewEraPumpCommError


"""
create a .py from the gui design.ui file
venv\Scripts\pyuic5.exe gui/two_networked_pumps/two_networked_pump_gui_design.ui -o gui/two_networked_pumps/two_networked_pump_gui_design.py

"""


from gui.two_networked_pumps import two_networked_pump_gui_design

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TwoNetworkedPumpGui(QtWidgets.QMainWindow,
                          two_networked_pump_gui_design.Ui_MainWindow,
                          ):
    def __init__(self,
                 pump_1: PeristalticPump,
                 pump_2: PeristalticPump,
                 parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.pump_1 = pump_1
        self.pump_2 = pump_2

        self.get_direction()
        self.get_rate()
        self.start_pop_up_message()

    def setupUi(self, MainWindow):
        super().setupUi(self)
        self.pump_1_start_pushButton.clicked.connect(self.start_pump_1)
        self.pump_1_stop_pushButton.clicked.connect(self.stop_pump_1)
        self.pump_1_dispense_pushButton.clicked.connect(self.set_dispense_pump_1)
        self.pump_1_withdraw_pushButton.clicked.connect(self.set_withdraw_pump_1)
        self.pump_1_set_rate_pushButton.clicked.connect(self.set_rate_pump_1)

        self.pump_2_start_pushButton.clicked.connect(self.start_pump_2)
        self.pump_2_stop_pushButton.clicked.connect(self.stop_pump_2)
        self.pump_2_dispense_pushButton.clicked.connect(self.set_dispense_pump_2)
        self.pump_2_withdraw_pushButton.clicked.connect(self.set_withdraw_pump_2)
        self.pump_2_set_rate_pushButton.clicked.connect(self.set_rate_pump_2)

    def start_pop_up_message(self):
        title = 'Start up'
        message = 'This is a basic GUI to control 2 networked pumps. Mote that if the pump is controlled manually ' \
                  'through the panel the GUI will not update to reflect this change'
        create_pop_up_message_box(message=message, window_title=title)

    def get_direction(self):
        self.get_direction_pump_1()
        self.get_direction_pump_2()

    def get_direction_pump_1(self):
        self.pump_1_direction_label.setText(self.pump_1.get_direction())

    def get_direction_pump_2(self):
        self.pump_2_direction_label.setText(self.pump_2.get_direction())

    def set_dispense_pump_1(self):
        self._set_direction(1, 'dispense')

    def set_dispense_pump_2(self):
        self._set_direction(2, 'dispense')

    def set_withdraw_pump_1(self):
        self._set_direction(1, 'withdraw')

    def set_withdraw_pump_2(self):
        self._set_direction(2, 'withdraw')

    def _set_direction(self, pump_n, direction):
        if pump_n == 1:
            self.pump_1.set_direction(direction)
            self.get_direction_pump_1()
        if pump_n == 2:
            self.pump_2.set_direction(direction)
            self.get_direction_pump_2()

    def get_rate(self):
        self.get_rate_pump_1()
        self.get_rate_pump_2()

    def get_rate_pump_1(self):
        self.pump_1_rate_label.setText(str(self.pump_1.get_rate(unit='ml/min')))

    def get_rate_pump_2(self):
        self.pump_2_rate_label.setText(str(self.pump_2.get_rate(unit='ml/min')))

    def set_rate_pump_1(self):
        rate = self.pump_1_rate_doubleSpinBox.value()
        self._set_rate(1, rate)

    def set_rate_pump_2(self):
        rate = self.pump_2_rate_doubleSpinBox.value()
        self._set_rate(2, rate)

    def _set_rate(self, pump_n, rate):
        if pump_n == 1:
            self.pump_1.set_rate(rate, 'ml/min')
            self.get_rate_pump_1()
        elif pump_n == 2:
            self.pump_2.set_rate(rate, 'ml/min')
            self.get_rate_pump_2()

    def start_pump_1(self):
        logger.debug('start pump 1')
        self.pump_1.start()
        create_pop_up_message_box('Pump 1 started', 'Pump 1 started')
        self.pump_1_running_label.setText('True')

    def start_pump_2(self):
        logger.debug('start pump 2')
        self.pump_2.start()
        create_pop_up_message_box('Pump 2 started', 'Pump 2 started')
        self.pump_2_running_label.setText('True')

    def stop_pump_1(self):
        logger.debug('stop pump 1')
        try:
            self.pump_1.stop()
            create_pop_up_message_box('Pump 1 stopped', 'Pump 1 stopped')
            self.pump_1_running_label.setText('False')
        except NewEraPumpCommError:
            # an error will be thrown if the pump isnt actually running, so ignore this error if it appears when
            # trying to stop the pump
            pump_already_stopped_message()

    def stop_pump_2(self):
        logger.debug('stop pump 2')
        try:
            self.pump_2.stop()
            create_pop_up_message_box('Pump 2 stopped', 'Pump 2 stopped')
            self.pump_2_running_label.setText('False')
        except NewEraPumpCommError:
            # an error will be thrown if the pump isnt actually running, so ignore this error if it appears when
            # trying to stop the pump
            pump_already_stopped_message()


def pump_already_stopped_message():
    title = "Pump is already stopped"
    message = "Pump is already stopped"
    create_pop_up_message_box(message, title)


def create_pop_up_message_box(
        message: str,
        window_title: str,
):
    '''convenience method for creating a pop up message box, with a message and a window title'''
    logger.debug(f'{message}')
    message_box = QtWidgets.QMessageBox()
    message_box.setIcon(QtWidgets.QMessageBox.Information)
    message_box.setText(f"{message}")
    message_box.setWindowTitle(f"{window_title}")
    message_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    message_box.exec()


def main():
    pump_port = 'COM3'
    pump_network = PeristalticPumpNetwork(port=pump_port, baudrate=9600)
    ne_pump_1 = pump_network.add_pump(address=0, baudrate=9600)  # first pump directly connected to the computer
    ne_pump_2 = pump_network.add_pump(address=1, baudrate=9600)  # second pump connected to the first pump

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    form = TwoNetworkedPumpGui(ne_pump_1, ne_pump_2)

    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
