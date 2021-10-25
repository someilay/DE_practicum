from typing import Callable

from application.gui.mpl_canvas import MplCanvas
from application.gui.qui_configurator import GuiConfigurator
from application.methods.euler_method import EulerMethod
from application.methods.improved_euler_method import ImprovedEulerMethod
from application.methods.runge_kutta_method import RungeKuttaMethod
from application.methods.numerical_method import NumericalMethod


class Midleware:
    def __init__(self, f: Callable[[float, float], float], solution: Callable[[float], float]):
        """
        Init Midleware, which connects UI and methods

        :param f: target function
        :param solution: analytical solution
        """
        self._e_m = EulerMethod(f, solution)
        self._i_e_m = ImprovedEulerMethod(f, solution)
        self._rk_m = RungeKuttaMethod(f, solution)

    @staticmethod
    def __append_default_kwargs(kwargs: dict, method: NumericalMethod, x0: float, y0: float, x: float, n: int,
                                graph_type: str, show: bool, label: str, color: str):
        """
        Add computed graph to kwargs
        """
        if show:
            x_, y_, lte, gte = method.compute(x0, y0, x, n)
            kwargs[type(method).__name__] = {
                "x": x_,
                "y": y_ if graph_type == GuiConfigurator.GRAPH else lte if graph_type == GuiConfigurator.LTE else gte,
                "label": label,
                "color": color
            }

    @staticmethod
    def __append_gte_d_kwargs(kwargs: dict, method: NumericalMethod, x0: float, y0: float, x: float,
                              from_: int, to_: int, show: bool, label: str, color: str):
        """
        Add computed graph to kwargs. Graph is GTE dependency
        """
        if show:
            ns_, gte_d_ = method.get_gte_dependency(x0, y0, x, from_, to_)
            kwargs[type(method).__name__] = {
                "x": ns_,
                "y": gte_d_,
                "label": label,
                "color": color
            }

    @staticmethod
    def __check_validity_of_interval(x0: float, x: float):
        """
        Check if x0 smaller then x

        :param x0: float
        :param x: float
        :return: bool
        """
        return x0 < x

    @staticmethod
    def __check_interval_for_zero_holding(x0: float, x: float):
        """
        Check if x or x0 to small by absolute value.
        Assumation: (x0, x) - valid interval

        :param x0:
        :param x:
        :return:
        """
        return x0 > GuiConfigurator.EPSILON or x < -GuiConfigurator.EPSILON

    @staticmethod
    def __check_distance(x0: float, x: float):
        """
        Check distanse between x and x0

        :param x0: float
        :param x: float
        :return: bool
        """
        return x - x0 > GuiConfigurator.MINIMAL_DISTANCE_BETWEEN_X_X0

    def __check_x_x0(self, x0: float, x: float):
        """
        Check x and x0 before ploting.
        Raise excaption if they are bad.

        :param x0: float
        :param x: float
        :return:
        """
        if not self.__check_validity_of_interval(x0, x):
            raise ValueError("X0 must be less then x!", {"x0": "x0", "x": "x"})

        if not self.__check_interval_for_zero_holding(x0, x):
            raise ValueError("Interval should not contain too small values", {"x0": "x0", "x": "x"})

        if not self.__check_distance(x0, x):
            raise ValueError("X0 and x are too close!", {"x0": "x0", "x": "x"})

    def plot_graphs(self, sc: MplCanvas, x0: float, y0: float, x: float, n: int,
                    title: str = None, xlabel: str = None, ylabel: str = None,
                    exact_label: str = None, exact_color: str = None,
                    euler_label: str = None, euler_color: str = None,
                    improved_euler_label: str = None, improved_euler_color: str = None,
                    runge_kutta_label: str = None, runge_kutta_color: str = None,
                    graph_type: str = None,
                    show_euler: bool = False, show_improved_euler: bool = False, show_runge_kutta: bool = False):
        """
        Plot approximation, lte, gte
        """
        self.__check_x_x0(x0, x)

        if n == 0:
            raise ValueError("N must be positive!", {"n": "n"})

        if graph_type != GuiConfigurator.GRAPH and not show_euler and not show_improved_euler and not show_runge_kutta:
            raise ValueError("You must choose method!")

        kwargs = dict()
        self.__append_default_kwargs(kwargs, self._e_m, x0, y0, x, n, graph_type,
                                     show_euler, euler_label, euler_color)
        self.__append_default_kwargs(kwargs, self._i_e_m, x0, y0, x, n, graph_type,
                                     show_improved_euler, improved_euler_label, improved_euler_color)
        self.__append_default_kwargs(kwargs, self._rk_m, x0, y0, x, n, graph_type,
                                     show_runge_kutta, runge_kutta_label, runge_kutta_color)

        if graph_type == GuiConfigurator.GRAPH:
            exact_x, exact_y = self._e_m.solution(x0, y0, x)
            kwargs["exact"] = {"x": exact_x, "y": exact_y, "label": exact_label, "color": exact_color}

        sc.plot(title + " | " + graph_type, xlabel, ylabel, **kwargs)

    def plot_gte_dependency(self, sc: MplCanvas, x0: float, y0: float, x: float, from_: int, to_: int,
                            title: str = None, xlabel: str = None, ylabel: str = None,
                            euler_label: str = None, euler_color: str = None,
                            improved_euler_label: str = None, improved_euler_color: str = None,
                            runge_kutta_label: str = None, runge_kutta_color: str = None,
                            show_euler: bool = False, show_improved_euler: bool = False,
                            show_runge_kutta: bool = False):
        """
        Plot gte dependency from N
        """
        self.__check_x_x0(x0, x)

        if from_ >= to_:
            raise ValueError("From must be less then to!", {"from": "from", "to": "to"})

        if not show_euler and not show_improved_euler and not show_runge_kutta:
            raise ValueError("You must choose method!")

        kwargs = dict()
        self.__append_gte_d_kwargs(kwargs, self._e_m, x0, y0, x, from_, to_,
                                   show_euler, euler_label, euler_color)
        self.__append_gte_d_kwargs(kwargs, self._i_e_m, x0, y0, x, from_, to_,
                                   show_improved_euler, improved_euler_label, improved_euler_color)
        self.__append_gte_d_kwargs(kwargs, self._rk_m, x0, y0, x, from_, to_,
                                   show_runge_kutta, runge_kutta_label, runge_kutta_color)

        sc.plot(title, xlabel, ylabel, **kwargs)
