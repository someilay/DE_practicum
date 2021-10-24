from typing import Callable
from application.methods.numerical_method import NumericalMethod


class ImprovedEulerMethod(NumericalMethod):
    def __init__(self, f: Callable[[float, float], float], solution: Callable[[float], float]):
        """
        Init Improved Euler method

        :param f: target method
        :param solution: analytical solution
        """
        super().__init__(lambda x, y, h: (f(x, y) + f(x + h, y + h * f(x, y))) / 2, solution)
