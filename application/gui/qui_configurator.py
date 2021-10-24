from typing import Union
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon, QFont, QDoubleValidator
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from mpl_canvas import MplCanvas


def _getDoubleValidator(_min: float, _max: float, decimals: int):
    """
    Inits double validator

    :param _min:
    :param _max:
    :param decimals:
    :return:
    """
    validator = QtGui.QDoubleValidator(_min, _max, decimals)
    validator.setNotation(QDoubleValidator.StandardNotation)
    return validator


class GuiConfigurator:
    # Constants of GUI
    WINDOW_ICON_PATH = "application/gui/icon.png"
    WINDOW_STYLE = "Fusion"
    WINDOW_TITLE = "Numerical methods"
    WINDOW_TEXT_FONT = QFont('Arial', 16)
    WINDOW_X_SCALE = 0.6
    WINDOW_Y_SCALE = 0.6
    WINDOW_TEXT_EDIT_WIDTH_SCALE = 0.20
    WINDOW_TOOLBAR_HEIGTH_SCALE = 0.1
    WINDOW_LAYOT_SPACING_SCALE = 0.01
    SCREEN_STANDART_SIZE = 16 / 9

    INPUT_FROM_LABEL = "From:"
    INPUT_TO_LABEL = "To:"
    INPUT_FROM_TEXTEDIT = 1
    INPUT_TO_TEXTEDIT = 10
    INPUT_TEXTEDIT_WIDTH_SCALE = 0.08

    MATPLOT_WIDTH = 10
    MATPLOT_HEIGHT = 10
    MATPLOT_DPI = 100

    APPROXIMATION_TITLE = "y' = (3y + 2xy)/x^2"
    APPROXIMATION_XLABEL = "x"
    APPROXIMATION_YLABEL = "y"

    GTE_DEPENDENCY_TITLE = "MAX GTE(n)"
    GTE_DEPENDENCY_XLABEL = "n"
    GTE_DEPENDENCY_YLABEL = "max GTE"

    X0_LABEL = "X0 = "
    Y0_LABEL = "Y0 = "
    X_LABEL = "X = "
    N_LABEL = "N = "

    X0_DEFAULT = 1.0
    Y0_DEFAULT = 1.0
    X_DEFAULT = 6
    N_DEFAULT = 5
    MINIMAL_DISTANCE_BETWEEN_X_X0 = 0.1

    STANDART_DOUBLE_VALIDATOR = _getDoubleValidator(-9999, 9999, 4)
    STANDART_INT_VALIDATOR = QtGui.QIntValidator(1, 9999)

    EULER_METHOD = "Euler method"
    IMPROVED_EULER_METHOD = "Improved Euler method"
    RUNGE_KUTTA_METHOD = "Runge-Kutta method"

    BUTTON_LTE = "View LTE"
    BUTTON_GTE = "View GTE"
    BUTTON_GTE_D = "View MAX GTE(N)"
    BUTTON_PLOT = "Plot"

    SOLUTION_TITLE = "Exact solution"
    SOLUTION_COLOR = "b"
    EULER_METHOD_COLOR = "r"
    IMPROVED_EULER_METHOD_COLOR = "g"
    RUNGE_KUTTA_METHOD_COLOR = "y"

    EPSILON = 10 ** -3

    RED_BACKGROUND = "QLineEdit { background-color: #ed808b;}"
    WHITE_BACKGROUND = "QLineEdit { background-color: white;}"

    LTE = "LTE"
    GTE = "GTE"
    GRAPH = "GRAPH"

    INPUT_ERROR = "Input error"

    def __init__(self, window: QtWidgets.QMainWindow, app: QtWidgets.QApplication):
        """
        Init configurator

        :param window: target window
        :param app: target application
        """
        self.__window = window
        self.__app = app
        self.__screen_height = app.primaryScreen().size().height()
        self.__screen_width = app.primaryScreen().size().width()

        # Checks for capability
        if abs(self.__screen_width / self.__screen_height - self.SCREEN_STANDART_SIZE) > self.EPSILON:
            raise EnvironmentError("Screen dimensions must be 16 / 9!")

        if self.__screen_width < 900:
            raise EnvironmentError("To small screen!")

    def configurate_window_size(self, screen_width: int, screen_height: int):
        """
        Configurate window size

        :param screen_width: screen width
        :param screen_height: screen height
        :return:
        """

        self.__app.setStyle(self.WINDOW_STYLE)
        self.__window.setWindowIcon(QIcon(self.WINDOW_ICON_PATH))
        self.__window.setWindowTitle(self.WINDOW_TITLE)
        self.__window.setFixedSize(int(screen_width * self.WINDOW_X_SCALE), int(screen_height * self.WINDOW_Y_SCALE))

    def create_labled_int_text_edit(self, title: str, value: int, width: int):
        """
        Creates textedit with corresponding label
        Textedit accepts only integers

        :param title: title of label
        :param value: initial value
        :param width: width of text edit
        :return: QLabel, QLineEdit
        """
        label, textedit = self.__create_lable_text_edit(title, value, width)
        textedit.setValidator(self.STANDART_INT_VALIDATOR)

        return label, textedit

    def create_labled_double_text_edit(self, title: str, value: float, width: int):
        """
        Creates textedit with corresponding label.
        Textedit accepts double values

        :param title: title of label
        :param value: initial value
        :param width: width of text edit
        :return: QLabel, QLineEdit
        """
        label, textedit = self.__create_lable_text_edit(title, value, width)
        textedit.setValidator(self.STANDART_DOUBLE_VALIDATOR)

        return label, textedit

    def __create_lable_text_edit(self, title: str, value: Union[int, float], width: int):
        """
        Creates textedit with corresponding label.

        :param title: title of label
        :param value: initial value
        :param width: width of text edit
        :return: QLabel, QLineEdit
        """
        textedit = QtWidgets.QLineEdit(self.__window)
        textedit.setFont(self.WINDOW_TEXT_FONT)
        textedit.setFixedWidth(width)
        textedit.setText(str(value).replace(".", ","))

        label = QtWidgets.QLabel(self.__window)
        label.setFont(self.WINDOW_TEXT_FONT)
        label.setText(title)

        return label, textedit

    def create_check_box(self, title: str):
        """
        Create checkbox

        :param title: checkbox title
        :return: QCheckBox
        """
        checkbox = QtWidgets.QCheckBox(title, self.__window)
        checkbox.setFont(self.WINDOW_TEXT_FONT)
        return checkbox

    def create_button(self, title: str):
        """
        Create button

        :param title: button title
        :return: QPushButton
        """
        button = QtWidgets.QPushButton(title, self.__window)
        button.setFont(self.WINDOW_TEXT_FONT)
        return button

    def create_plot_space(self):
        """
        Create mplCanvas with navigator

        :return: MplCanvas, NavigationToolbar
        """
        sc = MplCanvas(
            self.__window,
            width=self.MATPLOT_WIDTH,
            height=self.MATPLOT_HEIGHT,
            dpi=self.MATPLOT_DPI
        )
        toolbar = NavigationToolbar(sc, self.__window)
        return sc, toolbar

    def create_message_box(self, title: str, text: str):
        """
        Create and show message box

        :param title: box title
        :param text: box text
        :return:
        """
        message_box = QtWidgets.QMessageBox(self.__window)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setWindowIcon(QtGui.QIcon(GuiConfigurator.WINDOW_ICON_PATH))
        message_box.show()

    @staticmethod
    def create_horizontal_layout(**kwargs: Union[QtWidgets.QLayout, QtWidgets.QWidget]):
        """
        Create horizontal layout for components placement

        :param kwargs: components and layouts
        :return: QHBoxLayout
        """
        layot = QtWidgets.QHBoxLayout()
        for item in kwargs.values():
            if isinstance(item, QtWidgets.QLayout):
                layot.addLayout(item)
            elif isinstance(item, QtWidgets.QWidget):
                layot.addWidget(item)

        return layot

    @staticmethod
    def create_vertical_layout(**kwargs: Union[QtWidgets.QLayout, QtWidgets.QWidget]):
        """
        Create vertical layout for components placement

        :param kwargs: components and layouts
        :return: QVBoxLayout
        """
        layot = QtWidgets.QVBoxLayout()
        for item in kwargs.values():
            if isinstance(item, QtWidgets.QLayout):
                layot.addLayout(item)
            elif isinstance(item, QtWidgets.QWidget):
                layot.addWidget(item)

        return layot
