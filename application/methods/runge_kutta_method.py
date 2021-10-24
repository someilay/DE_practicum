from typing import Callable
from application.methods.numerical_method import NumericalMethod


class RungeKuttaMethod(NumericalMethod):
    def __init__(self, f: Callable[[float, float], float], solution: Callable[[float], float]):
        """
        Init Runge-Kutta method

        :param f: target method
        :param solution: analytical solution
        """
        super().__init__(
            lambda x, y, h: (
                                    f(x, y) +
                                    2 * f(x + h / 2, y + h * f(x, y) / 2) +
                                    2 * f(x + h / 2, y + h * f(x + h / 2, y + h * f(x, y) / 2) / 2) +
                                    f(x + h, y + h * f(x + h / 2, y + h * f(x + h / 2, y + h * f(x, y) / 2) / 2))
                            ) / 6,
            solution
        )
