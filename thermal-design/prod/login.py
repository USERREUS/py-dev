import sys
import json
import hashlib
import secrets
import DB

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, \
    QApplication, QInputDialog, QGridLayout, QDialog


# Класс для диалога регистрации пользователя
class UserDataDialog(QDialog):
    """
    Диалог для регистрации нового пользователя.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setup_ui()

    def setup_ui(self):
        """
        Настройка пользовательского интерфейса.
        """
        self.login_label = QLabel("Логин:")  # Метка для логина
        self.password_label = QLabel("Пароль:")  # Метка для пароля
        self.name_label = QLabel("Имя пользователя:")  # Метка для имени пользователя
        self.login_edit = QLineEdit()  # Поле ввода для логина
        self.password_edit = QLineEdit()  # Поле ввода для пароля
        self.name_edit = QLineEdit()  # Поле ввода для имени пользователя
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)  # Установка режима отображения пароля
        self.enter_button = QPushButton("Ввод")  # Кнопка "Ввод"

        vbox = QVBoxLayout()  # Вертикальное расположение виджетов
        vbox.addWidget(self.login_label)
        vbox.addWidget(self.login_edit)
        vbox.addWidget(self.password_label)
        vbox.addWidget(self.password_edit)
        vbox.addWidget(self.name_label)
        vbox.addWidget(self.name_edit)
        vbox.addSpacing(20)
        buttons_layout = QHBoxLayout()  # Горизонтальное расположение кнопок
        buttons_layout.addWidget(self.enter_button)
        buttons_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(vbox)
        main_layout.addLayout(buttons_layout)

        self.enter_button.clicked.connect(self.on_enter)

    def on_enter(self):
        """
        Обработчик события нажатия кнопки "Ввод".
        """
        self.accept()


# Класс для диалога получения идентификатора пользователя
class UserGetIdDialog(QDialog):
    """
    Диалог для ввода идентификатора пользователя.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ввод идентификатора")
        self.setup_ui()

    def setup_ui(self):
        """
        Настройка пользовательского интерфейса.
        """
        self.id_label = QLabel("Идентификатор:")  # Метка для идентификатора
        self.id_edit = QLineEdit()  # Поле ввода для идентификатора
        self.enter_button = QPushButton("Ввод")  # Кнопка "Ввод"
        self.cancel_button = QPushButton("Отмена")  # Кнопка "Отмена"
        vbox = QVBoxLayout()  # Вертикальное расположение виджетов
        vbox.addWidget(self.id_label)
        vbox.addWidget(self.id_edit)
        vbox.addSpacing(20)
        buttons_layout = QHBoxLayout()  # Горизонтальное расположение кнопок
        buttons_layout.addWidget(self.enter_button)
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(vbox)
        main_layout.addLayout(buttons_layout)
        self.enter_button.clicked.connect(self.on_enter)
        self.cancel_button.clicked.connect(self.on_cancel)

    def on_enter(self):
        """
        Обработчик события нажатия кнопки "Ввод".
        """
        self.accept()

    def on_cancel(self):
        """
        Обработчик события нажатия кнопки "Отмена".
        """
        self.reject()


# Диалоговое окно регистрации и авторизации пользователей
class LoginDialog(QDialog):
    """
    Диалоговое окно для регистрации и авторизации пользователей.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setup_ui()

    def setup_ui(self):
        """
        Инициализация и настройка параметров пользовательского интерфейса.
        """
        self.login_label = QLabel("Логин:")  # Метка для логина
        self.login_edit = QLineEdit()  # Поле ввода для логина
        self.login_edit.setText("admin")
        self.password_label = QLabel("Пароль:")  # Метка для пароля
        self.password_edit = QLineEdit()  # Поле ввода для пароля
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setText("admin")
        self.login_button = QPushButton("Войти")  # Кнопка "Войти"
        self.register_button = QPushButton("Зарегистрироваться")  # Кнопка "Зарегистрироваться"

        vbox = QVBoxLayout()  # Вертикальное расположение виджетов
        vbox.addWidget(self.login_label)
        vbox.addWidget(self.login_edit)
        vbox.addWidget(self.password_label)
        vbox.addWidget(self.password_edit)
        vbox.addSpacing(20)
        buttons_layout = QHBoxLayout()  # Горизонтальное расположение кнопок
        buttons_layout.addWidget(self.login_button)
        buttons_layout.addWidget(self.register_button)
        buttons_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(vbox)
        main_layout.addLayout(buttons_layout)

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self):
        """
        Метод для авторизации пользователей.
        """
        msg, data_users = DB.get_json_data('users')  # Чтение файла записей о пользователях
        if msg:
            QMessageBox.critical(self, "Ошибка открытия файла", msg)
            return

        password = self.password_edit.text()  # Чтение введенного пароля

        for user in data_users["users"]:
            salt = user["salt"]
            hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
            if user["login"] == self.login_edit.text() and user["password"] == hashed_password:
                QMessageBox.information(self, "Успешный вход", f"Добро пожаловать, {user['name']}!")
                if user["role"]:
                    self.done(1)  # администратор
                else:
                    self.done(2)  # обычный пользователь
                return

        QMessageBox.warning(self, "Ошибка входа", "Неправильный логин или пароль. Попробуйте еще раз.")

    def register(self):
        """
        Метод для регистрации пользователей.
        """
        msg, data_codes = DB.get_json_data('codes')  # Чтение файла идентификаторов
        if msg:
            QMessageBox.critical(self, "Ошибка открытия файла", msg)
            return

        dialog = UserGetIdDialog()  # Открытие диалогового окна ввода идентификатора
        result = dialog.exec()
        if result == QtWidgets.QDialog.DialogCode.Accepted:
            code = dialog.id_edit.text()  # Получение данных из диалогового окна
            role = -1

            for item in data_codes['codes']:
                salt = item["salt"]
                hashed_code = hashlib.sha256((code + salt).encode()).hexdigest()
                if item['code'] == hashed_code:
                    data_codes['codes'].remove(item)
                    role = item['role']
                    break

            if role < 0:
                QMessageBox.critical(self, "Ошибка регистрации", "Введенный Вами идентификатор недействителен")
                return

            QMessageBox.information(self, "Идентификация прошла успешно",
                                    "Далее Вам будет предложено ввести личные данные для входа. "
                                    "Учтите, что идентификатор для регистрации действителен только один раз! "
                                    "Для разрешения вопросов обращайтесь в технический отдел Вашей компании.")

            msg, data_users = DB.get_json_data('users')
            if msg:
                QMessageBox.warning(self, "Ошибка открытия файла", msg)
                return

            user_data = UserDataDialog()
            while True:
                result = user_data.exec()
                if not result:
                    return

                login = user_data.login_edit.text()
                find = False

                for user in data_users["users"]:
                    if user["login"] == login:
                        find = True
                        QMessageBox.warning(self, "Ошибка регистрации",
                                            "Пользователь с таким логином уже существует.")

                if not find:
                    break

            salt = secrets.token_hex(16)
            password = user_data.password_edit.text()
            hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
            new_user = {
                "name": user_data.name_edit.text(),
                "login": user_data.login_edit.text(),
                "password": hashed_password,
                "salt": salt,
                "role": role
            }

            data_users["users"].append(new_user)

            with open("codes.json", "w") as f:
                json.dump(data_codes, f, indent=4)

            with open("users.json", "w") as f:
                json.dump(data_users, f, indent=4)

            QMessageBox.information(self, "Успешная регистрация",
                                    "Регистрация прошла успешно. Теперь Вы можете войти в систему.")


if __name__ == '__main__':
    code = "A"
    salt = secrets.token_hex(16)
    role = 0
    hashed_code = hashlib.sha256((code + salt).encode()).hexdigest()
    new_code = {
        "code": hashed_code,
        "salt": salt,
        "role": role
    }

    # чтение файла идентификаторов
    try:
        with open("codes.json", "r") as f:
            data_codes = json.load(f)
    except:
        with open("codes.json", "w") as f:
            data_codes = {'codes': []}
        print("Файл 'codes.json' не найден. Создан новый пустой файл.")
    data_codes['codes'].append(new_code)
    # Записываем данные в файл "codes.json"
    with open("codes.json", "w") as f:
        json.dump(data_codes, f, indent=4)

    app = QApplication(sys.argv)
    temp = LoginDialog()
    temp.show()
    sys.exit(app.exec())