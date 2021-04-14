from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, qApp


class UserNameDialog(QDialog):
    """Класс для построения диалогового окна запуска клиентской части. Запрос логина и пароля.
        Определение размеров элементов для графической визуализации окна"""

    def __init__(self):
        super().__init__()

        self.ok_pressed = False

        self.setWindowTitle('Привет! Начните общение!')
        self.setFixedSize(310, 150)

        self.label = QLabel('Введите свое имя:', self)
        self.label.move(10, 10)
        self.label.setFixedSize(290, 15)

        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(290, 20)
        self.client_name.move(10, 35)

        self.btn_ok = QPushButton('Начать', self)
        self.btn_ok.move(10, 105)
        self.btn_ok.clicked.connect(self.click)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(195, 105)
        self.btn_cancel.clicked.connect(qApp.exit)

        self.label_passwd = QLabel('Введите пароль:', self)
        self.label_passwd.move(10, 60)
        self.label_passwd.setFixedSize(290, 15)

        self.client_passwd = QLineEdit(self)
        self.client_passwd.setFixedSize(290, 20)
        self.client_passwd.move(10, 80)
        self.client_passwd.setEchoMode(QLineEdit.Password)

        self.show()

    def click(self):
        """Метод обработки кнопки ОК"""

        if self.client_name.text() and self.client_passwd.text():
            self.ok_pressed = True
            qApp.exit()


if __name__ == '__main__':
    app = QApplication([])
    dial = UserNameDialog()
    app.exec_()
