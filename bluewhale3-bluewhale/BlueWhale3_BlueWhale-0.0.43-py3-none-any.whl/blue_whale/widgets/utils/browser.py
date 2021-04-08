from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineProfile

from AnyQt.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel
from AnyQt.QtCore import Qt, QSize

from orangewidget.utils.webview import WebviewWidget

from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.settings import Setting
from orangecontrib.blue_whale.i18n_config import *

__all__ = ['MainWindow']


def __(key):
    return i18n.t("bluewhale.browser." + key)


class MainWindow(OWWidget):
    name = __("name")
    want_basic_layout = False
    want_main_area = False
    want_control_area = False
    auto_commit = Setting(False)

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self.webview = WebEngineView(self)
        self.__mainLayout = None
        self.__feedbackUrl = None
        self.__feedbackLabel = None

        self.session = args[0] if len(args) > 0 else {}
        self.setupUi()

    def setupUi(self):
        self.setLayout(QVBoxLayout())
        self.setStyleSheet("background-color: #E8EFF1;")

        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.__mainLayout = QVBoxLayout()
        self.__mainLayout.setContentsMargins(0, 0, 0, 0)
        self.__mainLayout.setSpacing(0)
        self.layout().addLayout(self.__mainLayout)

        self.webview.load(QUrl('https://bo.dashenglab.com/client'))
        self.__mainLayout.addWidget(self.webview)
        self.webview.show()

        self.webview.urlChanged.connect(self.renew_bar)

        bottom_bar = QWidget(objectName="bottom-bar")
        bottom_bar_layout = QHBoxLayout()
        bottom_bar_layout.setContentsMargins(20, 10, 20, 10)
        bottom_bar.setLayout(bottom_bar_layout)
        bottom_bar.setSizePolicy(QSizePolicy.MinimumExpanding,
                                 QSizePolicy.Maximum)

        self.blue_whale = QLabel(textInteractionFlags=Qt.TextBrowserInteraction, openExternalLinks=True, visible=False)
        bottom_bar_layout.addWidget(self.blue_whale, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        self.resource_square = QLabel(textInteractionFlags=Qt.TextBrowserInteraction, openExternalLinks=True,
                                      visible=False)
        bottom_bar_layout.addWidget(self.resource_square, alignment=Qt.AlignCenter | Qt.AlignVCenter)

        self.login = QLabel(textInteractionFlags=Qt.TextBrowserInteraction, openExternalLinks=True,
                            visible=False)
        bottom_bar_layout.addWidget(self.login, alignment=Qt.AlignRight | Qt.AlignVCenter)

        self.layout().addWidget(bottom_bar, alignment=Qt.AlignBottom | Qt.AlignBottom)

        self.setFeedbackUrl(url='https://bw.dashenglab.com', text=__("blue_whale"), attribute=self.blue_whale)
        self.setFeedbackUrl(url='https://bo.dashenglab.com', text=__("resource_square"), attribute=self.resource_square)
        self.setFeedbackUrl(url='https://bo.dashenglab.com/login', text=__("login"), attribute=self.login)
        self.setSizeGripEnabled(False)

    def setFeedbackUrl(self, url, text, attribute):
        # type: (str) -> None
        """
        Set an 'feedback' url. When set a link is displayed in the bottom row.
        """
        self.__feedbackUrl = url
        if url:
            attribute.setText(
                '<a href="{url}">{text}</a>'.format(url=url, text=text)
            )
        else:
            attribute.setText("")
        attribute.setVisible(bool(url))

    # 响应输入的地址
    def renew_bar(self):
        if self.webview.page().url().toString() == "https://bo.dashenglab.com/client/success":
            self.session.update({'SESSION': self.webview.get_session()})
            self.webview.close()
            self.close()

    @staticmethod
    def sizeHint():
        return QSize(655, 550)


class WebEngineView(WebviewWidget):
    def __init__(self, main_window, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.main_window = main_window
        QWebEngineProfile.defaultProfile().cookieStore().deleteAllCookies()
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.cookie_change)
        self.cookies = {}

    def cookie_change(self, cookie):
        name = cookie.name().data().decode('utf-8')  # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')  # 先获取cookie值，再把编码处理一下
        if cookie.domain() == "bo.dashenglab.com":
            self.cookies.update({name: value})

    def get_session(self):
        user_session = self.cookies.get('SESSION')
        return user_session


if __name__ == "__main__":
    WidgetPreview(MainWindow).run()
