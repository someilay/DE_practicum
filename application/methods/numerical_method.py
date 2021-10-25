import numpy as np
from typing import Callable, Optional


class NumericalMethod:
    def __init__(self, a: Callable[[float, float, float], float], solution: Callable[[float], float]):
        """
        Init abstract numerical method

        :param a: increment function from R^3 -> R
        :param solution: analytical solution
        """
        self._a = a
        self._solution = solution
        self._x: Optional[np.ndarray] = None
        self._y: Optional[np.ndarray] = None
        self._lte: Optional[np.ndarray] = None
        self._gte: Optional[np.ndarray] = None
        self._gte_d: Optional[np.ndarray] = None
        self._ns: Optional[np.ndarray] = None

    def _get_constant_solution(self, x0: float, y0: float):
        if abs(self._solution(x0)) > 10**-9 and abs(y0) > 10**-2:
            return lambda x: self._solution(x) * y0 / self._solution(x0)
        else:
            raise ValueError("Input initial values lead to arithmetical error!", {"x0": "x0", "y0": "y0"})

    def solution(self, x0: float, y0: float, x: float, dpx: int = 200):
        """
        Get points of analytical solution

        :param x0: start point (x component)
        :param y0: start point (y component)
        :param x: end point
        :param dpx: number of points per unit
        :return: array of x, array of corresponding y
        """
        x_array = np.linspace(x0, x, int((x - x0) * dpx))
        return x_array, np.apply_along_axis(self._get_constant_solution(x0, y0), 0, x_array)

    def compute(self, x0: float, y0: float, x: float, n: int):
        """
        Compute approximation, lte and gte

        :param x0: start point (x component)
        :param y0: start point (y component)
        :param x: end point (x component)
        :param n: number of intervals
        :return: array of x, array of corresponding y, array of corresponding lte, array of corresponding gte
        """
        self._x = np.empty(n + 1)
        self._y = np.empty(n + 1)
        self._lte = np.empty(n + 1)
        self._gte = np.empty(n + 1)
        constant_solution = self._get_constant_solution(x0, y0)

        h = (x - x0) / n
        self._x[0] = x0
        self._y[0] = y0
        self._lte[0] = 0.0
        self._gte[0] = 0.0

        # Compute values and lte
        for i in range(1, n + 1):
            self._x[i] = self._x[i - 1] + h
            self._y[i] = self._y[i - 1] + h * self._a(self._x[i - 1], self._y[i - 1], h)
            self._lte[i] = constant_solution(self._x[i]) - constant_solution(self._x[i - 1]) - h * self._a(
                self._x[i - 1], constant_solution(self._x[i - 1]), h
            )

        # Compute gte
        self._gte = np.apply_along_axis(constant_solution, 0, self._x) - self._y

        return self._x, self._y, self._lte, self._gte

    def get_max_abs_gte(self):
        """
        Get max gte by absolute value

        :return: max value
        """
        if self._gte is not None:
            return np.amax(np.absolute(self._gte))
        raise ValueError("You must compute values first!")

    def get_gte_dependency(self, x0: float, y0: float, x: float, from_: int, to_: int):
        """
        Get dependency of max absolute gta from N

        :param x0: start point (x component)
        :param y0: start point (y component)
        :param x: end point (x component)
        :param from_: start of interval
        :param to_: end of interval
        :return: interval as array, corresponding array of max gte
        """
        self._gte_d = np.empty(to_ - from_ + 1)
        self._ns = np.empty(to_ - from_ + 1)

        for n in range(from_, to_ + 1):
            self.compute(x0, y0, x, n)
            self._ns[n - from_] = n
            self._gte_d[n - from_] = self.get_max_abs_gte()

        return self._ns, self._gte_d
