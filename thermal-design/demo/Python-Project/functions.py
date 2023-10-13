import math
import Condensator
import LPH
import WSP_tsilindr_turbiny_v1_3

# Функция возведения в квадрат
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
            return func.method(param)


functions = [
    Function("LPH", LPH.lph),
    Function("Cond", Condensator.capacitor),
    Function("square", square),
    Function("wsp", WSP_tsilindr_turbiny_v1_3.WSP)
]
