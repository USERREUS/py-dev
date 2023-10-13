"""
Тут описывается внутренность вложенного окна, которое вызывается по нажатию кнопки в области движения
"""
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QPushButton, QLineEdit, QWidget, QGridLayout, QCheckBox, QVBoxLayout, QHBoxLayout


# Диалоговое окно с общими методами и полями
class EnclosedDialog(QWidget):

    def __init__(self):
        super(EnclosedDialog, self).__init__()

        self.calc_button = QPushButton("Рассчитать")
        self.close_button = QPushButton("Закрыть")
        self.delete_button = QPushButton("Удалить")

        self.close_button.setStyleSheet("background-color: #bd4f3a;")
        self.calc_button.setStyleSheet("background-color: #76FF7F;")

        self.destroy_connect_button = QPushButton("Разорзвать связь")
        self.block_info_button = QPushButton("Таблица")
        self.graph_button = QPushButton("График")
        self.manual_calc = QPushButton("Рассчитать значение")
        self.value_sending_flag = QCheckBox('Разрешить передачу')

        self.change_title_label = QLabel("Введите новый заголовок:")
        self.change_title_edit = QLineEdit("Пусто")
        self.change_title_button = QPushButton("Сменить заголовок")

        self.setWindowTitle("Вложенное окно")


# Тестовое диалоговое окно для скалярных функций (НЕ РАБОТАЕТ)
class TESTDialog(EnclosedDialog):

    def __init__(self):
        super(TESTDialog, self).__init__()

        self.variable_text_label = QLabel("Переменная:")
        self.function_text_label = QLabel("Функция:")
        self.result_text_label = QLabel("Результат:")

        self.variable_text_edit = QLineEdit("Пусто")

        self.function_text_edit = QLineEdit("Пусто")
        self.function_text_edit.setReadOnly(True)

        self.result_text_edit = QLineEdit("Пусто")
        self.result_text_edit.setReadOnly(True)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)

        self.setWindowTitle("Тестовое окно")

        self.grid_layout.addWidget(self.change_title_label, 1, 0)
        self.grid_layout.addWidget(self.change_title_edit, 1, 1)
        self.grid_layout.addWidget(self.change_title_button, 1, 2)

        self.grid_layout.addWidget(self.variable_text_label, 2, 0)
        self.grid_layout.addWidget(self.variable_text_edit, 2, 1)

        self.grid_layout.addWidget(self.function_text_label, 3, 0)
        self.grid_layout.addWidget(self.function_text_edit, 3, 1)

        self.grid_layout.addWidget(self.result_text_label, 4, 0)
        self.grid_layout.addWidget(self.result_text_edit, 4, 1)

        self.grid_layout.addWidget(self.value_sending_flag, 5, 0)

        # self.grid_layout.addWidget(self.destroy_connect_button, 2, 2)
        # self.grid_layout.addWidget(self.confirm_button, 3, 2)
        # self.grid_layout.addWidget(self.close_button, 4, 2)
        # self.grid_layout.addWidget(self.delete_button, 5, 2)

        # okButton = QPushButton("OK")
        # cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        # hbox.addStretch(1)
        hbox.addWidget(self.destroy_connect_button)
        hbox.addWidget(self.graph_button)
        hbox.addWidget(self.delete_button)
        hbox.addWidget(self.block_info_button)  ###
        hbox.addSpacing(50)
        hbox.addWidget(self.confirm_button)
        hbox.addWidget(self.close_button)

        vbox = QVBoxLayout()
        vbox.addLayout(self.grid_layout)
        vbox.addSpacing(50)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        # self.setLayout(self.grid_layout)


# Диалоговое окно функции подогревателя (LPH) для работы с БД
class LPHDialogDB(EnclosedDialog):
    def __init__(self):
        super(LPHDialogDB, self).__init__()

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        self.setWindowTitle("Подогреватель. База данных.")

        grid_layout.addWidget(self.change_title_label, 1, 0)
        grid_layout.addWidget(self.change_title_edit, 1, 1)

        buttons = QGridLayout()

        buttons.addWidget(self.destroy_connect_button, 1, 0)
        buttons.addWidget(self.graph_button, 1, 1)
        buttons.addWidget(self.block_info_button, 1, 2)
        buttons.addWidget(self.change_title_button, 1, 3)

        buttons.addWidget(self.manual_calc, 2, 0)
        buttons.addWidget(self.delete_button, 2, 2)
        buttons.addWidget(self.close_button, 2, 3)

        vbox = QVBoxLayout()
        vbox.addLayout(grid_layout)
        vbox.addSpacing(20)
        vbox.addLayout(buttons)

        self.setLayout(vbox)


# Диалоговое окно функции подогревателя (LPH) для ручного расчета
class LPHDialog(EnclosedDialog):

    def __init__(self):
        super(LPHDialog, self).__init__()

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        """
            P_п = float(input('Введите давление греющего пара, МПа: '))
            t_п = float(input('Введите температуру греющего пара, °С: '))
            t_н = float(input('Введите температуру насыщения в подогревателе, °С: '))
            p_к = float(input('Введите давление нагреваемого конденсата, МПа: '))
            t_вх = float(input('Введите температуру конденсата на входе в подогреватель, °С: '))
            G_к = float(input('Введите расход конденсата через подогреватель, кг/с: '))
            etta_п = float(input('Введите коэффициент полезного действия подогреватель (КПД), в долях: '))
        """

        comment_in_label = QLabel("Входные данные:")
        comment_in_label.setFont(QFont("Times", 12, QFont.Bold))
        comment_out_label = QLabel("Выходные данные:")
        comment_out_label.setFont(QFont("Times", 12, QFont.Bold))

        P_p_label = QLabel("   Давление греющего пара, МПа: ")
        t_p_label = QLabel("   Температура греющего пара, °С: ")
        t_n_label = QLabel("   Температура насыщения в подогревателе, °С: ")
        p_k_label = QLabel("   Давление нагреваемого конденсата, МПа: ")
        t_vx_label = QLabel("  Температура конденсата на входе в подогреватель, °С: ")
        G_k_label = QLabel("   Расход конденсата через подогреватель, кг/с: ")
        etta_p_label = QLabel("    Коэффициент полезного действия подогреватель (КПД), в долях: ")

        """
            print(f'\nВыходные данные программы:\n\nРасход пара на подогреватель: {D_п} кг/с\n'
              f'Число параллеьных труб по ходу воды: {z_1}\n'
              f'Коэффициент теплоотдачи: {k} Вт/(м^2*K)')
        """

        D_p_label = QLabel("   Расход пара на подогреватель, кг/с:")
        z_1_label = QLabel("   Число параллельных труб по ходу воды, шт:")
        k_label = QLabel("   Коэффициент теплоотдачи, Вт/(м^2*K):")

        # поля входных данных
        self.P_p_line_edit = QLineEdit("10")
        self.t_p_line_edit = QLineEdit("300")
        self.t_n_line_edit = QLineEdit("120")
        self.p_k_line_edit = QLineEdit("5")
        self.t_vx_line_edit = QLineEdit("20")
        self.G_k_line_edit = QLineEdit("280")
        self.etta_p_line_edit = QLineEdit("0.95")
        # ----------

        # поля вЫходных данных
        self.D_p_line_edit = QLineEdit()
        self.z_1_line_edit = QLineEdit()
        self.k_line_edit = QLineEdit()

        self.D_p_line_edit.setReadOnly(True)
        self.z_1_line_edit.setReadOnly(True)
        self.k_line_edit.setReadOnly(True)
        # ----------

        self.setWindowTitle("Подогреватель. Ручной расчет.")

        grid_layout.addWidget(comment_in_label, 1, 0)

        grid_layout.addWidget(P_p_label, 2, 0)
        grid_layout.addWidget(t_p_label, 3, 0)
        grid_layout.addWidget(t_n_label, 4, 0)
        grid_layout.addWidget(p_k_label, 5, 0)
        grid_layout.addWidget(t_vx_label, 6, 0)
        grid_layout.addWidget(G_k_label, 7, 0)
        grid_layout.addWidget(etta_p_label, 8, 0)

        grid_layout.addWidget(self.P_p_line_edit, 2, 1)
        grid_layout.addWidget(self.t_p_line_edit, 3, 1)
        grid_layout.addWidget(self.t_n_line_edit, 4, 1)
        grid_layout.addWidget(self.p_k_line_edit, 5, 1)
        grid_layout.addWidget(self.t_vx_line_edit, 6, 1)
        grid_layout.addWidget(self.G_k_line_edit, 7, 1)
        grid_layout.addWidget(self.etta_p_line_edit, 8, 1)

        grid_layout.addWidget(comment_out_label, 9, 0)

        grid_layout.addWidget(D_p_label, 10, 0)
        grid_layout.addWidget(z_1_label, 11, 0)
        grid_layout.addWidget(k_label, 12, 0)

        grid_layout.addWidget(self.D_p_line_edit, 10, 1)
        grid_layout.addWidget(self.z_1_line_edit, 11, 1)
        grid_layout.addWidget(self.k_line_edit, 12, 1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.calc_button)
        hbox.addWidget(self.close_button)

        vbox = QVBoxLayout()
        vbox.addLayout(grid_layout)
        vbox.addSpacing(20)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


# диалоговое окно для конкретной функции Cond (НЕ РАБОТАЕТ)
class CondDialog(EnclosedDialog):

    def __init__(self):
        super(CondDialog, self).__init__()

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        """
            Gп = 319.6 #ВХОДНЫЕ ДАННЫЕ
            Gв = 15700 #ВХОДНЫЕ ДАННЫЕ
            t1в = 15 + 273.15 #ВХОДНЫЕ ДАННЫЕ
            dн = 28 #ВХОДНЫЕ ДАННЫЕ
            dвн = 26 #ВХОДНЫЕ ДАННЫЕ
            z = 2 #ВХОДНЫЕ ДАННЫЕ
            W = 2.1 #ВХОДНЫЕ ДАННЫЕ
            F = 36138 #ВХОДНЫЕ ДАННЫЕ
            N = 24296 #ВХОДНЫЕ ДАННЫЕ
        """

        comment_in_label = QLabel("Входные данные:")
        comment_in_label.setFont(QFont("Times", 12, QFont.Bold))
        comment_out_label = QLabel("Выходные данные:")
        comment_out_label.setFont(QFont("Times", 12, QFont.Bold))

        Gп_label = QLabel(" Расход пара в конденсатор, кг/с: ")
        Gв_label = QLabel(" Расход охлаждающей воды, кг/с: ")
        t1в_label = QLabel(" Температуру воды на входе в конденсатор, К: ")
        dн_label = QLabel(" Наружный диаметр трубок, мм: ")
        dвн_vx_label = QLabel(" Внутренний диаметр трубок, мм: ")
        z_label = QLabel(" Число ходов воды: ")
        W_label = QLabel(" Скорость воды в трубках, м/c: ")
        F_label = QLabel(" Площадь поверхности теплообмена, м2: ")
        N_label = QLabel(" Количество трубок, шт.: ")

        """
            print(f'\nВыходные данные программы: \n\nТемпература воды на выходе из кондесатора: {t2в - 273.15:1.3f}°C\n'
          f'Значение температуры насыщения в конденсаторе: {(tk - 273.15):1.3f}°C\n'
          f'Давление насыщения в конденсаторе: {wsp.PST(tk) * 10 ** 3:1.3f}КПа')
        """

        out1_label = QLabel("Температура воды на выходе из кондесатора, °C: ")
        out2_label = QLabel("Значение температуры насыщения в конденсаторе, °C: ")
        out3_label = QLabel("Давление насыщения в конденсаторе, КПа: ")

        self.Gп_line_edit = QLineEdit("319.6")
        self.Gв_line_edit = QLineEdit("15700")
        t1в = 15 + 273.15
        self.t1в_line_edit = QLineEdit(f"{t1в}")
        self.dн_line_edit = QLineEdit("28")
        self.dвн_line_edit = QLineEdit("26")
        self.z_line_edit = QLineEdit("2")
        self.W_line_edit = QLineEdit("2.1")
        self.F_line_edit = QLineEdit("36138")
        self.N_line_edit = QLineEdit("24296")

        self.out1_line_edit = QLineEdit()
        self.out2_line_edit = QLineEdit()
        self.out3_line_edit = QLineEdit()

        self.out1_line_edit.setReadOnly(True)
        self.out2_line_edit.setReadOnly(True)
        self.out3_line_edit.setReadOnly(True)

        self.setWindowTitle("Cond window")

        grid_layout.addWidget(self.change_title_label, 1, 0)
        grid_layout.addWidget(self.change_title_edit, 1, 1)
        grid_layout.addWidget(self.change_title_button, 1, 2)

        grid_layout.addWidget(comment_in_label, 2, 0)

        grid_layout.addWidget(Gп_label, 3, 0)
        grid_layout.addWidget(Gв_label, 4, 0)
        grid_layout.addWidget(t1в_label, 5, 0)
        grid_layout.addWidget(dн_label, 6, 0)
        grid_layout.addWidget(dвн_vx_label, 7, 0)
        grid_layout.addWidget(z_label, 8, 0)
        grid_layout.addWidget(W_label, 9, 0)
        grid_layout.addWidget(F_label, 10, 0)
        grid_layout.addWidget(N_label, 11, 0)

        grid_layout.addWidget(self.Gп_line_edit, 3, 1)
        grid_layout.addWidget(self.Gв_line_edit, 4, 1)
        grid_layout.addWidget(self.t1в_line_edit, 5, 1)
        grid_layout.addWidget(self.dн_line_edit, 6, 1)
        grid_layout.addWidget(self.dвн_line_edit, 7, 1)
        grid_layout.addWidget(self.z_line_edit, 8, 1)
        grid_layout.addWidget(self.W_line_edit, 9, 1)
        grid_layout.addWidget(self.F_line_edit, 10, 1)
        grid_layout.addWidget(self.N_line_edit, 11, 1)

        grid_layout.addWidget(comment_out_label, 12, 0)

        grid_layout.addWidget(out1_label, 13, 0)
        grid_layout.addWidget(out2_label, 14, 0)
        grid_layout.addWidget(out3_label, 15, 0)

        grid_layout.addWidget(self.out1_line_edit, 13, 1)
        grid_layout.addWidget(self.out2_line_edit, 14, 1)
        grid_layout.addWidget(self.out3_line_edit, 15, 1)

        # grid_layout.addWidget(self.value_sending_flag, 16, 0)

        hbox = QHBoxLayout()
        # hbox.addStretch(1)
        hbox.addWidget(self.destroy_connect_button)
        hbox.addWidget(self.delete_button)
        hbox.addSpacing(50)
        hbox.addWidget(self.confirm_button)
        hbox.addWidget(self.close_button)

        vbox = QVBoxLayout()
        vbox.addLayout(grid_layout)
        vbox.addSpacing(50)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


# диалоговое окно для конкретной функции WSP (НЕ РАБОТАЕТ)
class WSPDialog(EnclosedDialog):

    def __init__(self):
        super(WSPDialog, self).__init__()

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # БЛОК ВХОДНЫХ ДАННЫХ
        """
            #P_вход_цилиндра = float(input('Введите значение давления перед частью турбины, МПа: '))
            #t_вход_цилинда = float(input('Введите значение температуры перед частью турбины, °С: '))
            #этта_цилиндра = float(input('Введите значение КПД части турбины в долях: '))
            #P_выход_цилиндра = float(input('Введите значение давления на выходе из части турбины, МПа: '))
            #G_вход = float(input('Введите значение расхода пара в голову части турбины, кг/с: '))
            #N_отбор = int(input('Введите количество отборов в цилиндре турбины, шт.: '))
            #G_отбор = []
            #P_отбор = []
            
            #for i in range(0, N_отбор):
            #    g_i = input(f'Введите значение расхода пара в {i + 1} отборе, кг/с: ')
            #    p_i = input(f'Введите значение давления пара в {i + 1} отборе, МПа: ')
            #    G_отбор.append(g_i)
            #    P_отбор.append(p_i)
        """

        comment_in_label = QLabel("Входные данные:")
        comment_in_label.setFont(QFont("Times", 12, QFont.Bold))

        P_вход_цилиндра_label = QLabel("Значение давления перед частью турбины, МПа: ")
        t_вход_цилинда_label = QLabel("Значение температуры перед частью турбины, °С: ")
        этта_цилиндра_label = QLabel("Значение КПД части турбины в долях: ")
        P_выход_цилиндра_label = QLabel("Значение давления на выходе из части турбины, МПа: ")
        G_вход_label = QLabel("Значение расхода пара в голову части турбины, кг/с: ")
        N_отбор_label = QLabel("Количество отборов в цилиндре турбины, шт.: ")

        labelG = QLabel(f'Введите значение расхода пара в 1 отборе, кг/с: ')
        labelP = QLabel(f'Введите значение давления пара в 1 отборе, МПа: ')

        self.P_вход_цилиндра_line_edit = QLineEdit("2.53")
        self.t_вход_цилинда_line_edit = QLineEdit("539")
        self.этта_цилиндра_line_edit = QLineEdit("0.935")
        self.P_выход_цилиндра_line_edit = QLineEdit("0.24")
        self.G_вход_line_edit = QLineEdit("116.57")

        self.N_отбор_line_edit = QLineEdit("1")
        self.N_отбор_line_edit.setReadOnly(True)

        self.G_отбор_line_edit = QLineEdit("1.376")
        self.P_отбор_line_edit = QLineEdit("6.303")

        # БЛОК ВЫХОДНЫХ ДАННЫХ

        comment_out_label = QLabel("Выходные данные:")
        comment_out_label.setFont(QFont("Times", 12, QFont.Bold))

        h_вход_цилинда_label = QLabel(f'Энтальпия пара перед цилиндром, кДж/кг: ')
        s_вход_цилинда_label = QLabel(f'Энтропия пара перед цилиндром, кДж/кг*К: ')
        h_выход_цилинда_реал_label = QLabel(f'Энтальпия перед после цилиндра, кДж/кг: ')
        s_выход_цилинда_реал_label = QLabel(f'Энтропия пара после цилиндра, кДж/кг*К: ')
        t_выход_цилинда_реал_label = QLabel(f'Температура пара после цилиндра, К:')

        self.h_вход_цилинда_line_edit = QLineEdit()
        self.s_вход_цилинда_line_edit = QLineEdit()
        self.h_выход_цилинда_реал_line_edit = QLineEdit()
        self.s_выход_цилинда_реал_line_edit = QLineEdit()
        self.t_выход_цилинда_реал_line_edit = QLineEdit()

        label_1 = QLabel(f'Значения в 1 отборе: ')
        label_2 = QLabel('Энтальпия пара, кДж/кг: ')
        label_3 = QLabel('Температура пара в отборе, К: ')

        self.label_2_line_edit = QLineEdit()
        self.label_3_line_edit = QLineEdit()

        self.h_вход_цилинда_line_edit.setReadOnly(True)
        self.s_вход_цилинда_line_edit.setReadOnly(True)
        self.h_выход_цилинда_реал_line_edit.setReadOnly(True)
        self.s_выход_цилинда_реал_line_edit.setReadOnly(True)
        self.t_выход_цилинда_реал_line_edit.setReadOnly(True)
        self.label_2_line_edit.setReadOnly(True)
        self.label_3_line_edit.setReadOnly(True)

        # РАСПОЛОЖЕНИЕ ДАННЫХ НА ФОРМЕ

        self.setWindowTitle("WSPInput window")

        grid_layout.addWidget(self.change_title_label, 1, 0)
        grid_layout.addWidget(self.change_title_edit, 1, 1)
        grid_layout.addWidget(self.change_title_button, 1, 2)

        grid_layout.addWidget(comment_in_label, 2, 0)

        grid_layout.addWidget(P_вход_цилиндра_label, 3, 0)
        grid_layout.addWidget(t_вход_цилинда_label, 4, 0)
        grid_layout.addWidget(этта_цилиндра_label, 5, 0)
        grid_layout.addWidget(P_выход_цилиндра_label, 6, 0)
        grid_layout.addWidget(G_вход_label, 7, 0)
        grid_layout.addWidget(N_отбор_label, 8, 0)
        grid_layout.addWidget(labelG, 9, 0)
        grid_layout.addWidget(labelP, 10, 0)

        grid_layout.addWidget(comment_out_label, 11, 0)

        grid_layout.addWidget(h_вход_цилинда_label, 12, 0)
        grid_layout.addWidget(s_вход_цилинда_label, 13, 0)
        grid_layout.addWidget(h_выход_цилинда_реал_label, 14, 0)
        grid_layout.addWidget(s_выход_цилинда_реал_label, 15, 0)
        grid_layout.addWidget(t_выход_цилинда_реал_label, 16, 0)
        grid_layout.addWidget(label_1, 17, 0)
        grid_layout.addWidget(label_2, 18, 0)
        grid_layout.addWidget(label_3, 19, 0)

        grid_layout.addWidget(self.P_вход_цилиндра_line_edit, 3, 1)
        grid_layout.addWidget(self.t_вход_цилинда_line_edit, 4, 1)
        grid_layout.addWidget(self.этта_цилиндра_line_edit, 5, 1)
        grid_layout.addWidget(self.P_выход_цилиндра_line_edit, 6, 1)
        grid_layout.addWidget(self.G_вход_line_edit, 7, 1)
        grid_layout.addWidget(self.N_отбор_line_edit, 8, 1)
        grid_layout.addWidget(self.G_отбор_line_edit, 9, 1)
        grid_layout.addWidget(self.P_отбор_line_edit, 10, 1)

        grid_layout.addWidget(self.h_вход_цилинда_line_edit, 12, 1)
        grid_layout.addWidget(self.s_вход_цилинда_line_edit, 13, 1)
        grid_layout.addWidget(self.h_выход_цилинда_реал_line_edit, 14, 1)
        grid_layout.addWidget(self.s_выход_цилинда_реал_line_edit, 15, 1)
        grid_layout.addWidget(self.t_выход_цилинда_реал_line_edit, 16, 1)
        grid_layout.addWidget(self.label_2_line_edit, 18, 1)
        grid_layout.addWidget(self.label_3_line_edit, 19, 1)

        hbox = QHBoxLayout()
        # hbox.addStretch(1)
        hbox.addWidget(self.destroy_connect_button)
        hbox.addWidget(self.delete_button)
        hbox.addSpacing(50)
        hbox.addWidget(self.confirm_button)
        hbox.addWidget(self.close_button)

        vbox = QVBoxLayout()
        vbox.addLayout(grid_layout)
        vbox.addSpacing(50)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


# # диалоговое окно для конкретной функции LPHD
# class WSPInputSDialog(EnclosedDialog):
#
#     def __init__(self):
#         super(WSPInputSDialog, self).__init__()
#         self.setWindowTitle("WSPInputS window")
#
#         grid_layout = QGridLayout()
#         grid_layout.setSpacing(10)
#
#         """
#             #for i in range(0, N_отбор):
#             #    g_i = input(f'Введите значение расхода пара в {i + 1} отборе, кг/с: ')
#             #    p_i = input(f'Введите значение давления пара в {i + 1} отборе, МПа: ')
#             #    G_отбор.append(g_i)
#             #    P_отбор.append(p_i)
#         """
#
#         comment_in_label = QLabel("Входные данные:")
#         comment_in_label.setFont(QFont("Times", 12, QFont.Bold))
#
#         self.G_отбор = []
#         self.P_отбор = []
#
#         for i in range(3):
#             labelG = QLabel(f'Введите значение расхода пара в {i + 1} отборе, кг/с: ')
#             labelP = QLabel(f'Введите значение давления пара в {i + 1} отборе, МПа: ')
#
#             lineG = QLineEdit()
#             lineP = QLineEdit()
#
#             self.G_отбор.append((labelG, lineG))
#             self.P_отбор.append((labelP, lineP))
#
#         grid_layout.addWidget(self.change_title_label, 1, 0)
#         grid_layout.addWidget(self.change_title_edit, 1, 1)
#         grid_layout.addWidget(self.change_title_button, 1, 2)
#
#         grid_layout.addWidget(comment_in_label, 2, 0)
#
#         i = 3
#         for j in range(len(self.G_отбор)):
#             grid_layout.addWidget(self.G_отбор[j][0], i + j, 0)
#
#         for j in range(len(self.G_отбор)):
#             grid_layout.addWidget(self.G_отбор[j][1], i + j, 1)
#
#         grid_layout.addWidget(self.destroy_connect_button, 2, 2)
#         grid_layout.addWidget(self.confirm_button, 11, 2)
#         grid_layout.addWidget(self.close_button, 12, 2)
#         grid_layout.addWidget(self.delete_button, 13, 2)
#
#         self.setLayout(grid_layout)
#
#
# # диалоговое окно для конкретной функции LPHD
# class WSPOutputDialog(EnclosedDialog):
#
#     def __init__(self):
#         super(WSPOutputDialog, self).__init__()
#         self.setWindowTitle("WSPOutput window")
#
#         grid_layout = QGridLayout()
#         grid_layout.setSpacing(10)
#
#         comment_out_label = QLabel("Выходные данные:")
#         comment_out_label.setFont(QFont("Times", 12, QFont.Bold))
#
#         h_вход_цилинда_label = QLabel(f'Энтальпия пара перед цилиндром, кДж/кг: ')
#         s_вход_цилинда_label = QLabel(f'Энтропия пара перед цилиндром, кДж/кг*К: ')
#         h_выход_цилинда_реал_label = QLabel(f'Энтальпия перед после цилиндра, кДж/кг: ')
#         s_выход_цилинда_реал_label = QLabel(f'Энтропия пара после цилиндра, кДж/кг*К: ')
#         t_выход_цилинда_реал_label = QLabel(f'Температура пара после цилиндра, К:')
#
#         self.list_P_отбор = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
#         self.labels = []
#         self.lines = []
#
#         for i in range(len(self.list_P_отбор)):
#             label_1 = QLabel(f'Значения в {i + 1} отборе: ')
#             label_2 = QLabel('Энтальпия пара, кДж/кг: ')
#             label_3 = QLabel('Температура пара в отборе, К: ')
#
#             line2 = QLineEdit()
#             line3 = QLineEdit()
#
#             self.labels.append([label_1, label_2, label_3])
#             self.lines.append([line2, line3])
#
#         grid_layout.addWidget(self.change_title_label, 1, 0)
#         grid_layout.addWidget(self.change_title_edit, 1, 1)
#         grid_layout.addWidget(self.change_title_button, 1, 2)
#
#         grid_layout.addWidget(comment_out_label, 2, 0)
#
#         i = 3
#         for j in range(len(self.G_отбор)):
#             grid_layout.addWidget(self.G_отбор[j][0], i + j, 0)
#
#         for j in range(len(self.G_отбор)):
#             grid_layout.addWidget(self.G_отбор[j][1], i + j, 1)
#
#         grid_layout.addWidget(self.destroy_connect_button, 2, 2)
#         grid_layout.addWidget(self.confirm_button, 11, 2)
#         grid_layout.addWidget(self.close_button, 12, 2)
#         grid_layout.addWidget(self.delete_button, 13, 2)
#
#         self.setLayout(grid_layout)
