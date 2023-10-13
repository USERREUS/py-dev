import math
import LPH
import WSP_tsilindr_turbiny_v1_3
import Condensator_red


# Функция возведения в квадрат
import compare_model_lph_v2


def square(args):
    return [math.pow(args[0], 2)]


# Класс функции
class Function:

    def __init__(self, name, method):
        self.name = name
        self.method = method


# Метод выполнения функции по имени
def do_func_by_name(name, param):
    for func in functions:
        if func.name == name:
            # print(param)
            return func.method(param)


functions = [
    Function("LPH", compare_model_lph_v2.lph_ideal),
    Function("square", square),
    Function("wsp", WSP_tsilindr_turbiny_v1_3.WSP),
    Function("Cond_red", Condensator_red.condensator)
]
