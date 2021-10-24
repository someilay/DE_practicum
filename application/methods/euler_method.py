from typing import Callable
from numerical_method import NumericalMethod


class EulerMethod(NumericalMethod):
    def __init__(self, f: Callable[[float, float], float], solution: Callable[[float], float]):
        """
        Init Euler method

        :param f: target method
        :param solution: analytical solution
        """
        super().__init__(lambda x, y, h: f(x, y), solution)
