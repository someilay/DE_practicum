import logging
from unittest import TestCase
from application.methods.numerical_method import NumericalMethod
from application.methods.euler_method import EulerMethod
from application.methods.improved_euler_method import ImprovedEulerMethod
from application.methods.runge_kutta_method import RungeKuttaMethod


# Some tests
class TestNumericalMethod(TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        self.__logger = logging.getLogger(__name__)
        self.__x0 = 1
        self.__y0 = 2
        self.__x = 1.5
        self.__n = 5
        self.__max_n = 15
        self.__e_m = EulerMethod(lambda x, y: (y ** 2 + x * y - x ** 2) / x ** 2,
                                 lambda x: x * (1 + x ** 2 / 3) / (1 - x ** 2 / 3))
        self.__i_e_m = ImprovedEulerMethod(lambda x, y: (y ** 2 + x * y - x ** 2) / x ** 2,
                                           lambda x: x * (1 + x ** 2 / 3) / (1 - x ** 2 / 3))
        self.__rk_m = RungeKuttaMethod(lambda x, y: (y ** 2 + x * y - x ** 2) / x ** 2,
                                       lambda x: x * (1 + x ** 2 / 3) / (1 - x ** 2 / 3))

    def test_compute(self):
        x_, y_, lte, gte = self.__e_m.compute(self.__x0, self.__y0, self.__x, self.__n)
        self.__logger.info(f"Euler method: gte = {gte}, max_gte = {self.__e_m.get_max_abs_gte()}")
        x_, y_, lte, gte = self.__i_e_m.compute(self.__x0, self.__y0, self.__x, self.__n)
        self.__logger.info(f"Improved Euler method: gte = {gte}, max_gte = {self.__i_e_m.get_max_abs_gte()}")
        x_, y_, lte, gte = self.__rk_m.compute(self.__x0, self.__y0, self.__x, self.__n)
        self.__logger.info(f"Runge-Kutta method: gte = {gte}, max_gte = {self.__rk_m.get_max_abs_gte()}")

    def test_get_gte_dependency(self):
        def test_one_gte_dependency(method: NumericalMethod, name: str):
            ns_, gte_d_ = method.get_gte_dependency(self.__x0, self.__y0, self.__x, self.__n, self.__max_n)
            self.assertTrue(abs(gte_d_[-1] - method.get_max_abs_gte()) < 10 ** -3)
            self.__logger.info(f"{name}: gte_d = {gte_d_}")

        test_one_gte_dependency(self.__e_m, "Euler method")
        test_one_gte_dependency(self.__i_e_m, "Improvede Euler method")
        test_one_gte_dependency(self.__rk_m, "Runge-Kuttta method")
