"""
Тут описывается внутренность вложенного окна, которое вызывается по нажатию кнопки в области движения
"""
import sys

from PySide6 import QtCore
from PySide6.QtGui import QFont, Qt, QPixmap, QIcon
from PySide6.QtWidgets import QLabel, QPushButton, QLineEdit, QWidget, QGridLayout, QCheckBox, QVBoxLayout, QHBoxLayout, \
    QPlainTextEdit, QTextEdit, QMainWindow, QMenuBar, QFrame, QApplication


# Диалоговое окно с общими методами и полями
class EnclosedDialog:

    def __init__(self):

        self.calc_button = QPushButton("Рассчитать")
        self.close_button = QPushButton("Закрыть")
        self.delete_button = QPushButton("Удалить")

        self.close_button.setStyleSheet("background-color: #e24f5f;")

        self.destroy_connect_button = QPushButton("Разорзвать связь")
        self.block_info_button = QPushButton("Таблица")
        self.graph_button = QPushButton("График")
        self.manual_calc = QPushButton("Рассчитать значение")
        self.value_sending_flag = QCheckBox('Разрешить передачу данных')
        self.open_cmp_dialog = QPushButton('Сравнение')
        self.cmp_button = QPushButton('Сравнить')

        self.change_title_label = QLabel("Введите новый заголовок:")
        self.change_title_edit = QLineEdit("Новый заголовок")
        self.change_title_edit.setMaxLength(15)
        self.change_title_button = QPushButton("Сменить заголовок")

        self.base_buttons = [
            self.calc_button,
            self.delete_button,
            self.destroy_connect_button,
            self.block_info_button,
            self.graph_button,
            self.manual_calc,
            self.change_title_button
        ]


class CustomizeWindow(QMainWindow, EnclosedDialog):
    def __init__(self, title, heigth, width, parent=None):
        QMainWindow.__init__(self, parent)
        EnclosedDialog.__init__(self)

        self.setFixedSize(width, heigth)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_widget.setStyleSheet("border: 1px solid black;")

        self.hbox_frame = QHBoxLayout(self)
        self.vbox_frame = QVBoxLayout(self)

        self.lefttop = QFrame(self)
        self.righttop = QFrame(self)
        # self.window_icon = QFrame(self)

        self.righttop.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)

        self.lefttop.setFrameShape(QFrame.StyledPanel)
        self.lefttop.setStyleSheet("border: none;")
        self.lefttop.setFrameShadow(QFrame.Raised)
        self.lefttop.setFixedSize(int(self.width() / 2), 30)

        # self.window_icon.setFrameShape(QFrame.StyledPanel)
        # self.window_icon.setStyleSheet("border: none;")
        # self.window_icon.setFrameShadow(QFrame.Raised)
        # self.window_icon.setFixedSize(40, 50)

        self.righttop.setFrameShape(QFrame.StyledPanel)
        self.righttop.setStyleSheet("border: none;")
        self.righttop.setFrameShadow(QFrame.Raised)
        self.righttop.setFixedSize(int(self.width() / 2), 30)

        self.bottom = QFrame(self)
        self.bottom.setFrameShape(QFrame.StyledPanel)
        self.bottom.setStyleSheet("border: none;")
        self.bottom.setFrameShadow(QFrame.Raised)

        # pixmap = QPixmap("images/block.xpm")
        # self.label_icon = QLabel(self.window_icon)
        # self.label_icon.setPixmap(pixmap)
        # self.label_icon.setFixedSize(40, 50)

        self.label_title = QLabel(self.lefttop)
        self.label_title.setText(title)

        # self.label_title.setPixmap(QIcon("images/okpic.xpm"))
        self.label_title.setFixedSize(int(self.width() / 2), 30)
        self.label_title.mousePressEvent = self.mouse_press
        self.label_title.mouseMoveEvent = self.mouse_move

        # self.window_icon.setStyleSheet(
        #     'background-color: #C7EFDECD; '
        #     'padding: 10px; '
        #     'border: 1px solid black; '
        #     'border-right: none; '
        #     'padding-right: 5px; '
        #     'padding-left: 5px; '
        # )

        self.common_actions = QMenuBar(self.righttop)
        self.common_actions.mousePressEvent = self.mouse_press
        self.common_actions.mouseMoveEvent = self.mouse_move

        icon_hide = QIcon("images/hide.xpm")
        self.common_actions.addAction("__", self.showMinimized)
        self.common_actions.actions()[0].setIcon(icon_hide)

        self.common_actions.setFixedSize(int(self.width() / 2), 30)

        # self.hbox_frame.addWidget(self.window_icon)
        self.hbox_frame.addWidget(self.lefttop)
        self.hbox_frame.addWidget(self.righttop)

        self.bottom.setFixedSize(self.width(), self.height() - 30)

        self.vbox_frame.addLayout(self.hbox_frame)
        self.vbox_frame.addWidget(self.bottom)
        self.vbox_frame.setContentsMargins(0, 0, 0, 0)
        self.vbox_frame.setSpacing(0)

        self.main_widget.setLayout(self.vbox_frame)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.input_line_edits = []
        self.output_line_edits = []
        self.labels = []
        self.comment_labels = []

    def apply_style(self):
        self.label_title.setStyleSheet(
            'background-color: #C7EFDECD; '
            'padding: 5px; '
            'font: 14px; '
            'border: 1px solid black; '
            'border-right: none; '
        )

        self.common_actions.setStyleSheet(
            'background-color: #C7EFDECD; '
            'padding: 5px; '
            'border: 1px solid black; '
            'border-left: none;'
        )

        self.change_title_label.setStyleSheet("""
                    font: 14px;
                """)

        if self.base_buttons:
            for button in self.base_buttons:
                button.setStyleSheet("""
                             QPushButton {
                             background-color: #d1d1cf;
                             border-style: outset;
                             border-width: 2px;
                             border-radius: 6px;
                             border-color: #a1a1a1;
                             font: 14px;
                             padding: 6px;
                         }
                         QPushButton:pressed {
                             background-color: white;
                             border-style: inset;
                         }
                        """)

        if self.close_button:
            self.close_button.setStyleSheet("""
                             QPushButton {
                             background-color: #e24f5f;
                             border-style: outset;
                             border-width: 2px;
                             border-radius: 6px;
                             border-color: #a1a1a1;
                             font: 14px;
                             padding: 6px;
                         }
                         QPushButton:pressed {
                             background-color: white;
                             border-style: inset;
                         }
                    """)

        if self.value_sending_flag:
            self.value_sending_flag.setStyleSheet("""
                         QCheckBox {
                         spacing: 5px;
                         font: 14px;
                     }
    
                     QCheckBox::indicator {
                         width: 13px;
                         height: 13px;
                     }
                    """)

        if self.change_title_edit:
            self.change_title_edit.setStyleSheet("""
                        QLineEdit {
                         border: 2px solid gray;
                         border-radius: 6px;
                         padding: 0 8px;
                         selection-background-color: darkgray;
                         font: 14px;
                     }
                    """)

        if self.input_line_edits:
            for line in self.input_line_edits:
                line.setStyleSheet("""
                        QLineEdit {
                         border: 2px solid gray;
                         border-radius: 6px;
                         padding: 0 8px;
                         selection-background-color: darkgray;
                         font: 14px;
                     }
                    """)

        if self.output_line_edits:
            for line in self.output_line_edits:
                line.setStyleSheet("""
                        QLineEdit {
                         background-color: #e3e3e3;
                         border: 2px solid gray;
                         border-radius: 6px;
                         padding: 0 8px;
                         selection-background-color: darkgray;
                         font: 14px;
                     }
                    """)

        if self.labels:
            for label in self.labels:
                label.setStyleSheet("""
                    font: 14px;
                    padding-left: 2px;
                """)

        if self.comment_labels:
            for label in self.comment_labels:
                label.setStyleSheet("""
                        font-size: 16px; 
                        font-weight: 600;
                        padding-top: 15px;
                """)

    def mouse_press(self, event):
        if self.width() / 2 - 100 < event.scenePosition().x() < self.width() / 2 + 100:
            self.click_position = event.globalPosition().toPoint()
        if event.scenePosition().x() > self.width() / 2:
            QMenuBar.mousePressEvent(self.common_actions, event)
        else:
            QLabel.mousePressEvent(self.label_title, event)

    def mouse_move(self, event):
        if not self.isFullScreen():
            if self.width() / 2 - 100 < event.scenePosition().x() < self.width() / 2 + 100:
                if event.buttons() == Qt.LeftButton:
                    new_pos = self.pos() + event.globalPosition().toPoint() - self.click_position
                    self.move(new_pos)
                    self.click_position = event.globalPosition().toPoint()
        if event.scenePosition().x() > self.width() / 2:
            QMenuBar.mouseMoveEvent(self.common_actions, event)
        else:
            QLabel.mouseMoveEvent(self.label_title, event)


class DialogDB(CustomizeWindow):
    def __init__(self, title, height, width, parent=None):
        CustomizeWindow.__init__(self, title, height, width, parent=parent)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        grid_layout.addWidget(self.change_title_label, 1, 0)
        grid_layout.addWidget(self.change_title_edit, 1, 1)
        grid_layout.addWidget(self.value_sending_flag, 2, 0)

        buttons = QGridLayout()

        buttons.addWidget(self.destroy_connect_button, 1, 0)
        buttons.addWidget(self.graph_button, 1, 1)
        buttons.addWidget(self.block_info_button, 1, 2)
        buttons.addWidget(self.change_title_button, 1, 3)

        buttons.addWidget(self.manual_calc, 2, 0)
        buttons.addWidget(self.delete_button, 2, 2)
        buttons.addWidget(self.close_button, 2, 3)

        vbox = QVBoxLayout(self.bottom)
        vbox.addLayout(grid_layout)
        vbox.addSpacing(20)
        vbox.addLayout(buttons)
        vbox.setContentsMargins(20, 10, 20, 10)

        self.apply_style()


# Диалоговое окно функции подогревателя (LPH) для работы с БД
class LPHDialogDB(EnclosedDialog):
    def __init__(self):
        super(LPHDialogDB, self).__init__()

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        self.setWindowTitle("Подогреватель. База данных.")

        grid_layout.addWidget(self.change_title_label, 1, 0)
        grid_layout.addWidget(self.change_title_edit, 1, 1)
        grid_layout.addWidget(self.value_sending_flag, 2, 0)

        buttons = QGridLayout()

        buttons.addWidget(self.destroy_connect_button, 1, 0)
        buttons.addWidget(self.graph_button, 1, 1)
        buttons.addWidget(self.block_info_button, 1, 2)
        buttons.addWidget(self.change_title_button, 1, 3)

        buttons.addWidget(self.manual_calc, 2, 0)
        # buttons.addWidget(self.open_cmp_dialog, 2, 1)
        buttons.addWidget(self.delete_button, 2, 2)
        buttons.addWidget(self.close_button, 2, 3)

        vbox = QVBoxLayout()
        vbox.addLayout(grid_layout)
        vbox.addSpacing(20)
        vbox.addLayout(buttons)

        self.setLayout(vbox)


# Диалоговое окно функции подогревателя (LPH) для ручного расчета
class LPHDialog(CustomizeWindow):

    def __init__(self, title, height, width, parent=None):
        CustomizeWindow.__init__(
            self, title, height, width, parent
        )

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        """
            P_п = float(input('Введите давление греющего пара, МПа: ')) - ВХОДНОЕ ЗНАЧЕНИЕ
            t_вх = float(input('Введите температуру конденсата на входе в подогреватель, °С: ')) - ВХОДНОЕ ЗНАЧЕНИЕ
            G_к = float(input('Введите расход конденсата через подогреватель, т/ч: ')) - ВХОДНОЕ ЗНАЧЕНИЕ
            d_вн = float(input('Введите внутренний диаметр трубок, м: ')) - ВХОДНОЕ ЗНАЧЕНИЕ
            d_нар = float(input('Введите наружний диаметр трубок, м: ')) - ВХОДНОЕ ЗНАЧЕНИЕ
            z = float(input('Введите число ходов воды: ')) - ВХОДНОЕ ЗНАЧЕНИЕ
            l = float(input('Введите длину трубного пучка, м: ')) - ВХОДНОЕ ЗНАЧЕНИЕ
            N = float(input('Введите колличество трубок в подогревателе, м: ')) - ВХОДНОЕ ЗНАЧЕНИЕ
            F = float(input('Введите значение площади нагрева, м^2: ')) - ВХОДНОЕ ЗНАЧЕНИЕ
            lyambda_me = float(input('Введите темплопроводность металла трубок, Вт/м*°С: ')) - ВХОДНОЕ ЗНАЧЕНИЕ
        """

        comment_in_label = QLabel("Входные данные:")
        comment_out_label = QLabel("Выходные данные:")

        self.comment_labels = [comment_in_label, comment_out_label]

        P_п_label = QLabel('Давление греющего пара, МПа: ')
        t_вх_label = QLabel('Температура конденсата на входе в подогреватель, °С: ')
        G_к_label = QLabel('Расход конденсата через подогреватель, т/ч: ')
        d_вн_label = QLabel('Внутренний диаметр трубок, м: ')
        d_нар_label = QLabel('Наружний диаметр трубок, м: ')
        z_label = QLabel('Число ходов воды: ')
        l_label = QLabel('Длина трубного пучка, м: ')
        N_label = QLabel('Колличество трубок в подогревателе, м: ')
        F_label = QLabel('Значение площади нагрева, м^2: ')
        lyambda_me_label = QLabel('Темплопроводность металла трубок, Вт/м*°С: ')

        """
            Истинный коэффициент теплопередачи: {round(k_ideal, 3)} Вт/м^2*K \n'  # ВЫХОДНОЕ ЗНАЧЕНИЕ
            Недогрев основного конденсата до температуры насыщения: {round(delta_t_out_ideal, 3)} °C\n'  # ВЫХОДНОЕ ЗНАЧЕНИЕ
            Выходная температура конденсата: {round(t_out, 3)} °C\n')  # ВЫХОДНОЕ ЗНАЧЕНИЕ
        """

        k_ideal_label = QLabel("Расход пара на подогреватель, кг/с: ")
        delta_t_out_ideal_label = QLabel("Число параллельных труб по ходу воды, шт: ")
        t_out_label = QLabel("Коэффициент теплоотдачи, Вт/(м^2*K): ")

        self.labels = [
            P_п_label,
            t_вх_label,
            G_к_label,
            d_вн_label,
            d_нар_label,
            z_label,
            l_label,
            N_label,
            F_label,
            lyambda_me_label,
            k_ideal_label,
            delta_t_out_ideal_label,
            t_out_label
        ]

        # поля входных данных
        self.P_п_line_edit = QLineEdit()
        self.t_вх_line_edit = QLineEdit()
        self.G_к_line_edit = QLineEdit()
        self.d_вн_line_edit = QLineEdit()
        self.d_нар_line_edit = QLineEdit()
        self.z_line_edit = QLineEdit()
        self.l_line_edit = QLineEdit()
        self.N_line_edit = QLineEdit()
        self.F_line_edit = QLineEdit()
        self.lyambda_me_line_edit = QLineEdit()
        # ----------

        self.input_line_edits = [
            self.P_п_line_edit,
            self.t_вх_line_edit,
            self.G_к_line_edit,
            self.d_вн_line_edit,
            self.d_нар_line_edit,
            self.z_line_edit,
            self.l_line_edit,
            self.N_line_edit,
            self.F_line_edit,
            self.lyambda_me_line_edit
        ]

        # поля выходных данных
        self.k_ideal_line_edit = QLineEdit()
        self.delta_t_out_ideal_line_edit = QLineEdit()
        self.t_out_line_edit = QLineEdit()

        self.output_line_edits = [
            self.k_ideal_line_edit,
            self.delta_t_out_ideal_line_edit,
            self.t_out_line_edit
        ]

        self.k_ideal_line_edit.setReadOnly(True)
        self.delta_t_out_ideal_line_edit.setReadOnly(True)
        self.t_out_line_edit.setReadOnly(True)
        # ----------

        grid_layout.addWidget(comment_in_label, 1, 0)
        grid_layout.addWidget(P_п_label, 2, 0)
        grid_layout.addWidget(t_вх_label, 3, 0)
        grid_layout.addWidget(G_к_label, 4, 0)
        grid_layout.addWidget(d_вн_label, 5, 0)
        grid_layout.addWidget(d_нар_label, 6, 0)
        grid_layout.addWidget(z_label, 7, 0)
        grid_layout.addWidget(l_label, 8, 0)
        grid_layout.addWidget(N_label, 9, 0)
        grid_layout.addWidget(F_label, 10, 0)
        grid_layout.addWidget(lyambda_me_label, 11, 0)

        grid_layout.addWidget(self.P_п_line_edit, 2, 1)
        grid_layout.addWidget(self.t_вх_line_edit, 3, 1)
        grid_layout.addWidget(self.G_к_line_edit, 4, 1)
        grid_layout.addWidget(self.d_вн_line_edit, 5, 1)
        grid_layout.addWidget(self.d_нар_line_edit, 6, 1)
        grid_layout.addWidget(self.z_line_edit, 7, 1)
        grid_layout.addWidget(self.l_line_edit, 8, 1)
        grid_layout.addWidget(self.N_line_edit, 9, 1)
        grid_layout.addWidget(self.F_line_edit, 10, 1)
        grid_layout.addWidget(self.lyambda_me_line_edit, 11, 1)

        grid_layout.addWidget(comment_out_label, 12, 0)

        grid_layout.addWidget(k_ideal_label, 13, 0)
        grid_layout.addWidget(delta_t_out_ideal_label, 14, 0)
        grid_layout.addWidget(t_out_label, 15, 0)

        grid_layout.addWidget(self.k_ideal_line_edit, 13, 1)
        grid_layout.addWidget(self.delta_t_out_ideal_line_edit, 14, 1)
        grid_layout.addWidget(self.t_out_line_edit, 15, 1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.calc_button)
        hbox.addWidget(self.close_button)

        vbox = QVBoxLayout(self.bottom)
        vbox.addLayout(grid_layout)
        vbox.addSpacing(20)
        vbox.addLayout(hbox)
        vbox.setContentsMargins(20, 10, 20, 10)

        self.apply_style()


# Диалоговое окно функции подогревателя (LPH) для работы с БД
class CondDialogDB(EnclosedDialog):
    def __init__(self):
        super(CondDialogDB, self).__init__()

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # self.setWindowTitle("Конденсатор. База данных.")

        grid_layout.addWidget(self.change_title_label, 1, 0)
        grid_layout.addWidget(self.change_title_edit, 1, 1)
        grid_layout.addWidget(self.value_sending_flag, 2, 0)

        buttons = QGridLayout()

        buttons.addWidget(self.destroy_connect_button, 1, 0)
        buttons.addWidget(self.graph_button, 1, 1)
        buttons.addWidget(self.block_info_button, 1, 2)
        buttons.addWidget(self.change_title_button, 1, 3)

        buttons.addWidget(self.manual_calc, 2, 0)
        # buttons.addWidget(self.open_cmp_dialog, 2, 1)
        buttons.addWidget(self.delete_button, 2, 2)
        buttons.addWidget(self.close_button, 2, 3)

        vbox = QVBoxLayout()
        vbox.addLayout(grid_layout)
        vbox.addSpacing(20)
        vbox.addLayout(buttons)

        self.setLayout(vbox)


# Диалоговое окно функции конденсатора (Cond) для ручного расчета
class CondDialog(CustomizeWindow):

    def __init__(self, title, height, width, parent=None):
        CustomizeWindow.__init__(
            self, title, height, width, parent
        )

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
        comment_out_label = QLabel("Выходные данные:")

        self.comment_labels = [comment_in_label, comment_out_label]

        Gп_label = QLabel(" Расход пара в конденсатор, кг/с: ")
        Gв_label = QLabel(" Расход охлаждающей воды, кг/с: ")
        t1в_label = QLabel(" Температура воды на входе в конденсатор, К: ")
        dн_label = QLabel(" Наружный диаметр трубок, мм: ")
        dвн_label = QLabel(" Внутренний диаметр трубок, мм: ")
        W_label = QLabel(" Скорость воды в трубках, м/c: ")
        F_label = QLabel(" Площадь поверхности теплообмена, м2: ")
        tk_label = QLabel(" Температура насыщения в конденсаторе, °С: ")
        z_label = QLabel(" Число ходов воды, шт.: ")
        L_label = QLabel(" Длина трубок, м: ")

        """
            print(f'\nВыходные данные программы: \n\nТемпература воды на выходе из кондесатора: {t2в - 273.15:1.3f}°C\n'
          f'Значение температуры насыщения в конденсаторе: {(tk - 273.15):1.3f}°C\n'
          f'Давление насыщения в конденсаторе: {wsp.PST(tk) * 10 ** 3:1.3f}КПа')
        """

        out1_label = QLabel("Температура воды на выходе из кондесатора, °C: ")
        out2_label = QLabel("Коэффициент теплопередачи трубок, Вт/(м^2*K): ")
        out3_label = QLabel("Температура насыщения в конденсаторе, °C: ")
        out4_label = QLabel("Гидравлическое сопротивление труб, Па:")

        self.labels = [
            Gп_label,
            Gв_label,
            t1в_label,
            dн_label,
            dвн_label,
            W_label,
            F_label,
            tk_label,
            z_label,
            L_label,
            out1_label,
            out2_label,
            out3_label,
            out4_label
        ]

        self.Gп_line_edit = QLineEdit("319.6")
        self.Gв_line_edit = QLineEdit("15700")
        self.t1в_line_edit = QLineEdit("15")
        self.dн_line_edit = QLineEdit("28")
        self.dвн_line_edit = QLineEdit("26")
        self.W_line_edit = QLineEdit("2.1")
        self.F_line_edit = QLineEdit("36138")
        self.tk_line_edit = QLineEdit("50")
        self.z_line_edit = QLineEdit("2")
        self.L_line_edit = QLineEdit("5.714")

        self.input_line_edits = [
            self.Gп_line_edit,
            self.Gв_line_edit,
            self.t1в_line_edit,
            self.dн_line_edit,
            self.dвн_line_edit,
            self.W_line_edit,
            self.F_line_edit,
            self.tk_line_edit,
            self.z_line_edit,
            self.L_line_edit
        ]

        self.out1_line_edit = QLineEdit()
        self.out2_line_edit = QLineEdit()
        self.out3_line_edit = QLineEdit()
        self.out4_line_edit = QLineEdit()

        self.output_line_edits = [
            self.out1_line_edit,
            self.out2_line_edit,
            self.out3_line_edit,
            self.out4_line_edit
        ]

        self.out1_line_edit.setReadOnly(True)
        self.out2_line_edit.setReadOnly(True)
        self.out3_line_edit.setReadOnly(True)
        self.out4_line_edit.setReadOnly(True)

        grid_layout.addWidget(comment_in_label, 1, 0)

        grid_layout.addWidget(Gп_label, 2, 0)
        grid_layout.addWidget(Gв_label, 3, 0)
        grid_layout.addWidget(t1в_label, 4, 0)
        grid_layout.addWidget(dн_label, 5, 0)
        grid_layout.addWidget(dвн_label, 6, 0)
        grid_layout.addWidget(W_label, 7, 0)
        grid_layout.addWidget(F_label, 8, 0)
        grid_layout.addWidget(tk_label, 9, 0)
        grid_layout.addWidget(z_label, 10, 0)
        grid_layout.addWidget(L_label, 11, 0)

        grid_layout.addWidget(self.Gп_line_edit, 2, 1)
        grid_layout.addWidget(self.Gв_line_edit, 3, 1)
        grid_layout.addWidget(self.t1в_line_edit, 4, 1)
        grid_layout.addWidget(self.dн_line_edit, 5, 1)
        grid_layout.addWidget(self.dвн_line_edit, 6, 1)
        grid_layout.addWidget(self.W_line_edit, 7, 1)
        grid_layout.addWidget(self.F_line_edit, 8, 1)
        grid_layout.addWidget(self.tk_line_edit, 9, 1)
        grid_layout.addWidget(self.z_line_edit, 10, 1)
        grid_layout.addWidget(self.L_line_edit, 11, 1)

        grid_layout.addWidget(comment_out_label, 13, 0)

        grid_layout.addWidget(out1_label, 14, 0)
        grid_layout.addWidget(out2_label, 15, 0)
        grid_layout.addWidget(out3_label, 16, 0)
        grid_layout.addWidget(out4_label, 17, 0)

        grid_layout.addWidget(self.out1_line_edit, 14, 1)
        grid_layout.addWidget(self.out2_line_edit, 15, 1)
        grid_layout.addWidget(self.out3_line_edit, 16, 1)
        grid_layout.addWidget(self.out4_line_edit, 17, 1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.calc_button)
        hbox.addWidget(self.close_button)

        vbox = QVBoxLayout(self.bottom)
        vbox.addLayout(grid_layout)
        vbox.addSpacing(20)
        vbox.addLayout(hbox)
        vbox.setContentsMargins(20, 10, 20, 10)

        self.apply_style()


# Диалоговое окно функции подогревателя (LPH) для работы с БД
class WSPDialogDB(EnclosedDialog):
    def __init__(self):
        super(WSPDialogDB, self).__init__()

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        self.setWindowTitle("Турбина. База данных.")

        grid_layout.addWidget(self.change_title_label, 1, 0)
        grid_layout.addWidget(self.change_title_edit, 1, 1)
        grid_layout.addWidget(self.value_sending_flag, 2, 0)

        buttons = QGridLayout()

        buttons.addWidget(self.destroy_connect_button, 1, 0)
        buttons.addWidget(self.graph_button, 1, 1)
        buttons.addWidget(self.block_info_button, 1, 2)
        buttons.addWidget(self.change_title_button, 1, 3)

        buttons.addWidget(self.manual_calc, 2, 0)
        # buttons.addWidget(self.open_cmp_dialog, 2, 1)
        buttons.addWidget(self.delete_button, 2, 2)
        buttons.addWidget(self.close_button, 2, 3)

        vbox = QVBoxLayout()
        vbox.addLayout(grid_layout)
        vbox.addSpacing(20)
        vbox.addLayout(buttons)

        self.setLayout(vbox)


# диалоговое окно для конкретной функции WSP
class WSPDialog(CustomizeWindow):

    def __init__(self, title, height, width, parent=None):
        CustomizeWindow.__init__(
            self, title, height, width, parent
        )

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

        self.input_line_edits = [
            self.P_вход_цилиндра_line_edit,
            self.t_вход_цилинда_line_edit,
            self.этта_цилиндра_line_edit,
            self.P_выход_цилиндра_line_edit,
            self.G_вход_line_edit,
            self.N_отбор_line_edit,
            self.G_отбор_line_edit,
            self.P_отбор_line_edit
        ]

        # БЛОК ВЫХОДНЫХ ДАННЫХ

        comment_out_label = QLabel("Выходные данные:")
        self.comment_labels = [comment_in_label, comment_out_label]

        h_вход_цилинда_label = QLabel(f'Энтальпия пара перед цилиндром, кДж/кг: ')
        s_вход_цилинда_label = QLabel(f'Энтропия пара перед цилиндром, кДж/кг*К: ')
        h_выход_цилинда_реал_label = QLabel(f'Энтальпия пара после цилиндра, кДж/кг: ')
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

        self.labels = [
            P_вход_цилиндра_label,
            t_вход_цилинда_label,
            этта_цилиндра_label,
            P_выход_цилиндра_label,
            G_вход_label,
            N_отбор_label,
            labelG,
            labelP,
            h_вход_цилинда_label,
            s_вход_цилинда_label,
            h_выход_цилинда_реал_label,
            s_выход_цилинда_реал_label,
            t_выход_цилинда_реал_label,
            label_1,
            label_2,
            label_3
        ]

        self.label_2_line_edit = QLineEdit()
        self.label_3_line_edit = QLineEdit()

        self.output_line_edits = [
            self.h_вход_цилинда_line_edit,
            self.s_вход_цилинда_line_edit,
            self.h_выход_цилинда_реал_line_edit,
            self.s_выход_цилинда_реал_line_edit,
            self.t_выход_цилинда_реал_line_edit,
            self.label_2_line_edit,
            self.label_3_line_edit
        ]

        self.h_вход_цилинда_line_edit.setReadOnly(True)
        self.s_вход_цилинда_line_edit.setReadOnly(True)
        self.h_выход_цилинда_реал_line_edit.setReadOnly(True)
        self.s_выход_цилинда_реал_line_edit.setReadOnly(True)
        self.t_выход_цилинда_реал_line_edit.setReadOnly(True)
        self.label_2_line_edit.setReadOnly(True)
        self.label_3_line_edit.setReadOnly(True)

        # РАСПОЛОЖЕНИЕ ДАННЫХ НА ФОРМЕ
        grid_layout.addWidget(comment_in_label, 1, 0)

        grid_layout.addWidget(P_вход_цилиндра_label, 2, 0)
        grid_layout.addWidget(t_вход_цилинда_label, 3, 0)
        grid_layout.addWidget(этта_цилиндра_label, 4, 0)
        grid_layout.addWidget(P_выход_цилиндра_label, 5, 0)
        grid_layout.addWidget(G_вход_label, 6, 0)
        grid_layout.addWidget(N_отбор_label, 7, 0)
        grid_layout.addWidget(labelG, 8, 0)
        grid_layout.addWidget(labelP, 9, 0)

        grid_layout.addWidget(comment_out_label, 10, 0)

        grid_layout.addWidget(h_вход_цилинда_label, 11, 0)
        grid_layout.addWidget(s_вход_цилинда_label, 12, 0)
        grid_layout.addWidget(h_выход_цилинда_реал_label, 13, 0)
        grid_layout.addWidget(s_выход_цилинда_реал_label, 14, 0)
        grid_layout.addWidget(t_выход_цилинда_реал_label, 15, 0)
        grid_layout.addWidget(label_1, 16, 0)
        grid_layout.addWidget(label_2, 17, 0)
        grid_layout.addWidget(label_3, 18, 0)

        grid_layout.addWidget(self.P_вход_цилиндра_line_edit, 2, 1)
        grid_layout.addWidget(self.t_вход_цилинда_line_edit, 3, 1)
        grid_layout.addWidget(self.этта_цилиндра_line_edit, 4, 1)
        grid_layout.addWidget(self.P_выход_цилиндра_line_edit, 5, 1)
        grid_layout.addWidget(self.G_вход_line_edit, 6, 1)
        grid_layout.addWidget(self.N_отбор_line_edit, 7, 1)
        grid_layout.addWidget(self.G_отбор_line_edit, 8, 1)
        grid_layout.addWidget(self.P_отбор_line_edit, 9, 1)

        grid_layout.addWidget(self.h_вход_цилинда_line_edit, 11, 1)
        grid_layout.addWidget(self.s_вход_цилинда_line_edit, 12, 1)
        grid_layout.addWidget(self.h_выход_цилинда_реал_line_edit, 13, 1)
        grid_layout.addWidget(self.s_выход_цилинда_реал_line_edit, 14, 1)
        grid_layout.addWidget(self.t_выход_цилинда_реал_line_edit, 15, 1)
        grid_layout.addWidget(self.label_2_line_edit, 17, 1)
        grid_layout.addWidget(self.label_3_line_edit, 18, 1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.calc_button)
        hbox.addWidget(self.close_button)

        vbox = QVBoxLayout(self.bottom)
        vbox.addLayout(grid_layout)
        vbox.addSpacing(20)
        vbox.addLayout(hbox)
        vbox.setContentsMargins(20, 10, 20, 10)

        self.apply_style()


# Диалоговое окно функции подогревателя (LPH) для работы с БД
class CMPDialog(EnclosedDialog):
    def __init__(self):
        super(CMPDialog, self).__init__()

        self.setWindowTitle("Блок сравнения. База данных.")

        self.textarea = QTextEdit()
        self.textarea.setReadOnly(True)
        self.textarea.insertHtml("<font size='5'>Здесь будет отображаться результат сравнения:</font><br>")
        self.textarea.insertHtml("<font color='red' size='5'><red>красным, если расхождение с эталоном критическое;</font><br>")
        self.textarea.insertHtml("<font color='green' size='5'><red>зеленым, если расхождение в педелах нормы.</font><pre>")

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        buttons.addWidget(self.cmp_button)
        buttons.addWidget(self.close_button)

        vbox = QVBoxLayout()
        vbox.addWidget(self.textarea)
        vbox.addSpacing(10)
        vbox.addLayout(buttons)

        self.setLayout(vbox)
        self.setFixedSize(1200, 380)


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
