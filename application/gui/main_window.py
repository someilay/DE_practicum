from PyQt5 import QtWidgets
from application.middleware import Midleware
from qui_configurator import GuiConfigurator


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app: QtWidgets.QApplication, midleware: Midleware):
        """
        Init MainWindow

        :param app: QApplication
        :param midleware: Midleware for connecting GUI with numerical methods
        """
        super(MainWindow, self).__init__()
        self.__midleware = midleware
        self.__configurator = GuiConfigurator(self, app)
        self.__screen_height = app.primaryScreen().size().height()
        self.__screen_width = app.primaryScreen().size().width()

        # Labels & Textedits
        self.__x0_label, self.__x0_textbox = self.__configurator.create_labled_double_text_edit(
            GuiConfigurator.X0_LABEL,
            GuiConfigurator.X0_DEFAULT,
            self.__screen_width * GuiConfigurator.WINDOW_X_SCALE * GuiConfigurator.WINDOW_TEXT_EDIT_WIDTH_SCALE
        )
        self.__y0_label, self.__y0_textbox = self.__configurator.create_labled_double_text_edit(
            GuiConfigurator.Y0_LABEL,
            GuiConfigurator.Y0_DEFAULT,
            self.__screen_width * GuiConfigurator.WINDOW_X_SCALE * GuiConfigurator.WINDOW_TEXT_EDIT_WIDTH_SCALE
        )
        self.__x_label, self.__x_textbox = self.__configurator.create_labled_double_text_edit(
            GuiConfigurator.X_LABEL,
            GuiConfigurator.X_DEFAULT,
            self.__screen_width * GuiConfigurator.WINDOW_X_SCALE * GuiConfigurator.WINDOW_TEXT_EDIT_WIDTH_SCALE
        )
        self.__n_label, self.__n_textbox = self.__configurator.create_labled_int_text_edit(
            GuiConfigurator.N_LABEL,
            GuiConfigurator.N_DEFAULT,
            self.__screen_width * GuiConfigurator.WINDOW_X_SCALE * GuiConfigurator.WINDOW_TEXT_EDIT_WIDTH_SCALE
        )
        self.__from_label, self.__from_textbox = self.__configurator.create_labled_int_text_edit(
            GuiConfigurator.INPUT_FROM_LABEL,
            GuiConfigurator.INPUT_FROM_TEXTEDIT,
            self.__screen_width * GuiConfigurator.WINDOW_X_SCALE * GuiConfigurator.INPUT_TEXTEDIT_WIDTH_SCALE
        )
        self.__to_label, self.__to_textbox = self.__configurator.create_labled_int_text_edit(
            GuiConfigurator.INPUT_TO_LABEL,
            GuiConfigurator.INPUT_TO_TEXTEDIT,
            self.__screen_width * GuiConfigurator.WINDOW_X_SCALE * GuiConfigurator.INPUT_TEXTEDIT_WIDTH_SCALE
        )

        # Checkboxes
        self.__c_euler = self.__configurator.create_check_box(GuiConfigurator.EULER_METHOD)
        self.__c_improved_euler = self.__configurator.create_check_box(GuiConfigurator.IMPROVED_EULER_METHOD)
        self.__c_runge_kutta = self.__configurator.create_check_box(GuiConfigurator.RUNGE_KUTTA_METHOD)

        # Buttons
        self.__button_lte = self.__configurator.create_button(GuiConfigurator.BUTTON_LTE)
        self.__button_gte = self.__configurator.create_button(GuiConfigurator.BUTTON_GTE)
        self.__button_gte_d = self.__configurator.create_button(GuiConfigurator.BUTTON_GTE_D)
        self.__button_plot = self.__configurator.create_button(GuiConfigurator.BUTTON_PLOT)

        # Graph space
        self.__sc, self.__toolbar = self.__configurator.create_plot_space()

        # init all
        self.__initUI()

    def __initUI(self):
        """
        Init UI components and place them

        :return:
        """
        self.__configurator.configurate_window_size(self.__screen_width, self.__screen_height)

        # Layots init
        x0_layout = self.__configurator.create_horizontal_layout(label=self.__x0_label, textedit=self.__x0_textbox)
        y0_layout = self.__configurator.create_horizontal_layout(label=self.__y0_label, textedit=self.__y0_textbox)
        x_layout = self.__configurator.create_horizontal_layout(label=self.__x_label, textedit=self.__x_textbox)
        n_layout = self.__configurator.create_horizontal_layout(label=self.__n_label, textedit=self.__n_textbox)
        from_layout = self.__configurator.create_horizontal_layout(label=self.__from_label, textedit=self.__from_textbox)
        to_layout = self.__configurator.create_horizontal_layout(label=self.__to_label, textedit=self.__to_textbox)
        from_to_layout = self.__configurator.create_horizontal_layout(from_layot=from_layout, to_layot=to_layout)

        control_layot = self.__configurator.create_vertical_layout(
            x0_layot=x0_layout,
            y0_layot=y0_layout,
            x_layot=x_layout,
            n_layot=n_layout,
            c_euler=self.__c_euler,
            c_improved_euler=self.__c_improved_euler,
            c_runge_kutta=self.__c_runge_kutta,
            from_to_layot=from_to_layout,
            button_lte=self.__button_lte,
            button_gte=self.__button_gte,
            button_gte_d=self.__button_gte_d,
            button_plot=self.__button_plot
        )
        control_layot.setSpacing(GuiConfigurator.WINDOW_LAYOT_SPACING_SCALE * self.__screen_height)
        control_layot = self.__configurator.create_horizontal_layout(sc=self.__sc, control_layot=control_layot)
        common_layot = self.__configurator.create_vertical_layout(toolbar=self.__toolbar, control_layot=control_layot)

        widget = QtWidgets.QWidget()
        widget.setLayout(common_layot)
        self.setCentralWidget(widget)

        # Plot exact solution
        x0, y0, x, n = self.__get_default_input()
        self.__midleware.plot_graphs(
            self.__sc,
            x0,
            y0,
            x,
            n,
            title=GuiConfigurator.APPROXIMATION_TITLE,
            xlabel=GuiConfigurator.APPROXIMATION_XLABEL,
            ylabel=GuiConfigurator.APPROXIMATION_YLABEL,
            exact_label=GuiConfigurator.SOLUTION_TITLE,
            exact_color=GuiConfigurator.SOLUTION_COLOR,
            graph_type=GuiConfigurator.GRAPH
        )

        # Conncet buttons with actions
        self.__button_plot.clicked.connect(self.__button_plot_click)
        self.__button_lte.clicked.connect(self.__button_lte_click)
        self.__button_gte.clicked.connect(self.__button_gte_click)
        self.__button_gte_d.clicked.connect(self.__button_gte_d_click)

    def __set_error_input_color(self, **kwargs: str):
        """
        Set red background of given textedit

        :param kwargs: nickname of textedit [x0, y0, x...]
        :return:
        """
        for value in kwargs.values():
            if value == "x0":
                self.__x0_textbox.setStyleSheet(GuiConfigurator.RED_BACKGROUND)
            elif value == "y0":
                self.__y0_textbox.setStyleSheet(GuiConfigurator.RED_BACKGROUND)
            elif value == "x":
                self.__x_textbox.setStyleSheet(GuiConfigurator.RED_BACKGROUND)
            elif value == "n":
                self.__n_textbox.setStyleSheet(GuiConfigurator.RED_BACKGROUND)
            elif value == "from":
                self.__from_textbox.setStyleSheet(GuiConfigurator.RED_BACKGROUND)
            elif value == "to":
                self.__to_textbox.setStyleSheet(GuiConfigurator.RED_BACKGROUND)

    def __set_default_input_color(self):
        """
        Meke all backgrounds white

        :return:
        """
        self.__x0_textbox.setStyleSheet(GuiConfigurator.WHITE_BACKGROUND)
        self.__y0_textbox.setStyleSheet(GuiConfigurator.WHITE_BACKGROUND)
        self.__x_textbox.setStyleSheet(GuiConfigurator.WHITE_BACKGROUND)
        self.__n_textbox.setStyleSheet(GuiConfigurator.WHITE_BACKGROUND)
        self.__from_textbox.setStyleSheet(GuiConfigurator.WHITE_BACKGROUND)
        self.__to_textbox.setStyleSheet(GuiConfigurator.WHITE_BACKGROUND)

    def __get_initial_values(self):
        """
        Get x0, y0, x from textedits

        :return: x0, y0, x
        """

        x0 = float(self.__x0_textbox.text().replace(",", '.'))
        y0 = float(self.__y0_textbox.text().replace(",", '.'))
        x = float(self.__x_textbox.text().replace(",", '.'))
        return x0, y0, x

    def __get_default_input(self):
        """
        Get x0, y0, x, n from textedits

        :return: x0, y0, x, n
        """
        x0, y0, x = self.__get_initial_values()
        n = int(self.__n_textbox.text())
        return x0, y0, x, n

    def __get_from_to_input(self):
        """
        Get x0, y0, x, from, to from textedits

        :return: x0, y0, x, from, to
        """
        x0, y0, x = self.__get_initial_values()
        from_ = int(self.__from_textbox.text())
        to_ = int(self.__to_textbox.text())
        return x0, y0, x, from_, to_

    def __plot_result(self, graph_type: str):
        """
        Plot graphs by given input

        :param graph_type: type of grap [approximation, lte, gte...]
        :return:
        """
        self.__set_default_input_color()
        try:
            x0, y0, x, n = self.__get_default_input()
            show_euler = bool(self.__c_euler.checkState())
            show_improved_euler = bool(self.__c_improved_euler.checkState())
            show_runge_kutta = bool(self.__c_runge_kutta.checkState())
        except ValueError:
            # If no input provided
            self.__set_error_input_color(a="x0", b="y0", c="x", d="n")
            self.__configurator.create_message_box(GuiConfigurator.INPUT_ERROR, "No input provided")
            return

        try:
            # Give task to midleware
            self.__midleware.plot_graphs(
                self.__sc,
                x0,
                y0,
                x,
                n,
                title=GuiConfigurator.APPROXIMATION_TITLE,
                xlabel=GuiConfigurator.APPROXIMATION_XLABEL,
                ylabel=GuiConfigurator.APPROXIMATION_YLABEL,
                exact_label=GuiConfigurator.SOLUTION_TITLE,
                exact_color=GuiConfigurator.SOLUTION_COLOR,
                euler_label=GuiConfigurator.EULER_METHOD,
                euler_color=GuiConfigurator.EULER_METHOD_COLOR,
                improved_euler_label=GuiConfigurator.IMPROVED_EULER_METHOD,
                improved_euler_color=GuiConfigurator.IMPROVED_EULER_METHOD_COLOR,
                runge_kutta_label=GuiConfigurator.RUNGE_KUTTA_METHOD,
                runge_kutta_color=GuiConfigurator.RUNGE_KUTTA_METHOD_COLOR,
                show_euler=show_euler, show_improved_euler=show_improved_euler, show_runge_kutta=show_runge_kutta,
                graph_type=graph_type
            )
        except ValueError as e:
            # If some error is occuried
            if len(e.args) > 1:
                self.__set_error_input_color(**e.args[1])
            self.__configurator.create_message_box(GuiConfigurator.INPUT_ERROR, e.args[0])

    def __button_plot_click(self):
        """
        When plot button is clicked

        :return:
        """
        self.__plot_result(GuiConfigurator.GRAPH)

    def __button_lte_click(self):
        """
        When lte button is clicked

        :return:
        """
        self.__plot_result(GuiConfigurator.LTE)

    def __button_gte_click(self):
        """
        When gte button is clicked

        :return:
        """
        self.__plot_result(GuiConfigurator.GTE)

    def __button_gte_d_click(self):
        """
        When gte dependency button is clicked

        :return:
        """
        self.__set_default_input_color()
        try:
            x0, y0, x, from_, to_ = self.__get_from_to_input()
            show_euler = bool(self.__c_euler.checkState())
            show_improved_euler = bool(self.__c_improved_euler.checkState())
            show_runge_kutta = bool(self.__c_runge_kutta.checkState())
        except ValueError:
            # If no input provided
            self.__set_error_input_color(a="from", b="to", x0="x0", x="x", y0="y0")
            self.__configurator.create_message_box(GuiConfigurator.INPUT_ERROR, "No input provided")
            return

        try:
            # Give task to midleware
            self.__midleware.plot_gte_dependency(
                self.__sc,
                x0,
                y0,
                x,
                from_,
                to_,
                title=GuiConfigurator.GTE_DEPENDENCY_TITLE,
                xlabel=GuiConfigurator.GTE_DEPENDENCY_XLABEL,
                ylabel=GuiConfigurator.GTE_DEPENDENCY_YLABEL,
                euler_label=GuiConfigurator.EULER_METHOD,
                euler_color=GuiConfigurator.EULER_METHOD_COLOR,
                improved_euler_label=GuiConfigurator.IMPROVED_EULER_METHOD,
                improved_euler_color=GuiConfigurator.IMPROVED_EULER_METHOD_COLOR,
                runge_kutta_label=GuiConfigurator.RUNGE_KUTTA_METHOD,
                runge_kutta_color=GuiConfigurator.RUNGE_KUTTA_METHOD_COLOR,
                show_euler=show_euler, show_improved_euler=show_improved_euler, show_runge_kutta=show_runge_kutta
            )
        except ValueError as e:
            # If some error occuried
            if len(e.args) > 1:
                self.__set_error_input_color(**e.args[1])
            self.__configurator.create_message_box(GuiConfigurator.INPUT_ERROR, e.args[0])
