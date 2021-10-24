import sys
from math import e
from application.gui.main_window import MainWindow
from application.middleware import Midleware
from PyQt5 import QtWidgets


class Application:
    @staticmethod
    def run():
        """
        Run application

        :return:
        """
        app = QtWidgets.QApplication([])
        midleware = Midleware(
            lambda x, y: (3 * y + 2 * x * y) / x ** 2,
            lambda x: e ** (3 - 3 / x) * x ** 2
        )

        main_window = MainWindow(app, midleware)
        main_window.show()

        sys.exit(app.exec())
