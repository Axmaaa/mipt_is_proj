from PyQt5.Qt import *
from PyQt5 import QtCore, QtWidgets
import sys
from functools import partial

from center import center


class DecryptDialog(QDialog):
    def __init__(self, mode, parent=None):
        QDialog.__init__(self, parent)
        self.key = ""
        self.mode = mode
        self.state = 0
        if self.mode == "password":
            self.__init_passwords_ui()
        elif self.mode == "key":
            self.__init_keys_ui()
        else:
            print("Неизвестный способ дешифрования")
            self.showMessageBox("Ошибка", "Неизвестный способ дешифрования", "error")

    def __init_passwords_ui(self):
        self.setMinimumSize(QSize(330, 120))  # Устанавливаем размеры
        wrapper = partial(center, self)
        QtCore.QTimer.singleShot(0, wrapper)
        self.setWindowTitle("Дешифрование")  # Устанавл заголовок окна

        self.boxVertical_main = QtWidgets.QVBoxLayout()  # Общее
        self.passwords_layout = QtWidgets.QHBoxLayout()  # Пароль
        self.boxVertical_main.addLayout(self.passwords_layout)
        self.setLayout(self.boxVertical_main)

        password_label = QLabel("Пароль:", self)
        self.passwords_layout.addWidget(password_label)

        self.password_line = QLineEdit(self)
        self.passwords_layout.addWidget(self.password_line)
        self.password_line.setEchoMode(2)

        decrypt_button = QPushButton("Дешифровать", self)
        self.boxVertical_main.addWidget(decrypt_button)
        decrypt_button.clicked.connect(self.__decrypt)

    def __init_keys_ui(self):
        self.setMinimumSize(QSize(330, 120))  # Устанавливаем размеры
        wrapper = partial(center, self)
        QtCore.QTimer.singleShot(0, wrapper)
        self.setWindowTitle("Дешифрование")  # Устанавл заголовок окна

        self.boxVertical_main = QtWidgets.QVBoxLayout()  # Общее
        self.keys_layout = QtWidgets.QHBoxLayout()  # Ключи
        self.boxVertical_main.addLayout(self.keys_layout)
        self.setLayout(self.boxVertical_main)

        key_label = QLabel("Файл с ключом:", self)
        self.keys_layout.addWidget(key_label)

        self.key_label = QLabel("Выберете файл с ключом", self)
        self.keys_layout.addWidget(self.key_label)

        key_from_file_button = QPushButton("Выбрать ключ из файла", self)
        self.boxVertical_main.addWidget(key_from_file_button)
        key_from_file_button.clicked.connect(self.__open_file_with_key)

        decrypt_button = QPushButton("Дешифровать", self)
        self.boxVertical_main.addWidget(decrypt_button)
        decrypt_button.clicked.connect(self.__decrypt)

    def __open_file_with_key(self):
        file_pathname, _ = QFileDialog.getOpenFileName()
        if file_pathname == '':
            self.showMessageBox("Внимание", "Файл с ключом не был выбран", "info")
            return
        path_to_key = file_pathname
        with open(file_pathname, 'r') as f:
            key = f.read()
            print("Ключ: " + key)
            print("Файл " + file_pathname + " открыт на чтение")
        self.key = file_pathname
        temp = path_to_key.split("/")
        key_file_name = temp[len(temp)-1]
        self.key_label.setText(key_file_name)

    def __decrypt(self):
        if self.mode == "password":
            self.key = self.password_line.text()
            if self.password_line.text() == "":
                self.showMessageBox("Ошибка", "Пароль не был ввыден", "error")
                self.password_line.setFocus()
                return
        elif self.key_label.text() in ("", "Выберете файл с ключом", None):
            self.showMessageBox("Ошибка", "Ключ не был введен", "error")
            return
        self.state = 1
        self.close()

    def keyPressEvent(self, e):
        k = e.key()
        super().keyPressEvent(e)
        if k == Qt.Key_Enter:
            self.__decrypt()

    @staticmethod
    def showMessageBox(title, message, case):
        msg_box = QMessageBox()
        wrapper = partial(center, msg_box)
        QtCore.QTimer.singleShot(0, wrapper)
        if case == "error":
            msg_box.setIcon(QMessageBox.Warning)
        elif case == 'info':
            msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = DecryptDialog(mode="key")
    w.show()
    sys.exit(app.exec_())
