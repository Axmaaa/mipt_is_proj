from PyQt5.Qt import *
from PyQt5 import QtCore, QtWidgets
import sys
from functools import partial
import datetime
import os

from decrypt_dialog import DecryptDialog
from encrypt_dialog import EncryptDialog

from center import center
from api import encrypt_file
from api import decrypt_file


# Необходимо подумать о пересмотрении способа поддрежки множества паролей в encrypt_dialog.py


class DBFormWindow(QMainWindow):
    def __init__(self, user_id, parent=None):
        QMainWindow.__init__(self, parent)
        self.path_to_open = ''
        self.path_to_save = ''
        self.file_open_name = 'Выберите исходный файл'
        self.file_save_name = 'Выберите конечный файл или сгенерируйте его в процессе работы'

        self.__init_ui()

    def __change_select_file_label(self):
        temp = self.path_to_open.split("/")
        print("temp in __change_select_file_label = " + str(temp))
        self.file_open_name = temp[len(temp)-1]
        self.select_file_label.setText("Исходный файл: " + self.file_open_name)

    def __change_select_file_to_save_label(self):
        temp = self.path_to_save.split("/")
        self.file_save_name = temp[len(temp)-1]
        self.select_file_to_save_label.setText("Конечный файл: " + self.file_save_name)

    def __init_ui(self):
        self.setFixedSize(QSize(640, 480))
        wrapper = partial(center, self)
        QtCore.QTimer.singleShot(0, wrapper)
        self.setWindowTitle("Крипто Завр 719")

        self.LayoutWidget1 = QtWidgets.QWidget(self)
        self.LayoutWidget1.setGeometry(QtCore.QRect(10, 10, 620, 30))
        self.Layout1 = QtWidgets.QHBoxLayout(self.LayoutWidget1)
        self.Layout1.setContentsMargins(0, 0, 0, 0)

        self.LayoutWidget2 = QtWidgets.QWidget(self)
        self.LayoutWidget2.setGeometry(QtCore.QRect(10, 10, 620, 100))
        self.Layout2 = QtWidgets.QHBoxLayout(self.LayoutWidget2)
        self.Layout2.setContentsMargins(0, 0, 0, 0)

        self.LayoutWidget3 = QtWidgets.QWidget(self)
        self.LayoutWidget3.setGeometry(QtCore.QRect(10, 10, 620, 170))
        self.Layout3 = QtWidgets.QHBoxLayout(self.LayoutWidget3)
        self.Layout3.setContentsMargins(0, 0, 0, 0)

        select_file_button = QPushButton("Открыть ...", self)
        self.Layout3.addWidget(select_file_button)

        self.select_file_label = QLabel(self.file_open_name)
        self.select_file_label.setAlignment(Qt.AlignCenter)
        self.Layout1.addWidget(self.select_file_label)

        select_file_to_save_button = QPushButton("Сохранить в ...", self)
        self.Layout3.addWidget(select_file_to_save_button)

        self.select_file_to_save_label = QLabel(self.file_save_name)
        self.select_file_to_save_label.setAlignment(Qt.AlignCenter)
        self.Layout2.addWidget(self.select_file_to_save_label)

        encrypt_button = QPushButton("Зашифровать", self)
        self.Layout3.addWidget(encrypt_button)

        decrypt_button = QPushButton("Дешифровать", self)
        self.Layout3.addWidget(decrypt_button)

        self.list = QTextBrowser(self)
        self.list.setGeometry(QtCore.QRect(10, 110, 620, 270))

        select_file_to_save_button.clicked.connect(self.__select_file_to_save)
        select_file_button.clicked.connect(self.__select_file)
        decrypt_button.clicked.connect(self.__decrypt)
        encrypt_button.clicked.connect(self.__encrypt)

    def __select_file_to_save(self):
        file_pathname, _ = QFileDialog.getOpenFileName()
        print("file_pathname из __select_file_to_save = " + file_pathname)
        if file_pathname == '':
            self.showMessageBox("Внимание", "Конечный файл не был выбран", "info")
            print("return from __select_file_to_save due to empty file_pathname")
            return
        self.path_to_save = file_pathname
        self.__change_select_file_to_save_label()

    def __select_file(self):
        file_pathname, _ = QFileDialog.getOpenFileName()
        print("file_pathname из __select_file = " + file_pathname)
        if file_pathname == '':
            self.showMessageBox("Внимание", "Исходный файл не был выбран", "info")
            print("return from __select_file due to empty file_pathname")
            return
        self.path_to_open = file_pathname
        self.__change_select_file_label()
        self.select_file_label.setText("Исходный файл: " + self.file_open_name)
        self.__open_file(file_pathname, "read")

    def __open_file(self, file_pathname, mode):
        print("---Начало открытия файла---")
        self.list.clear()
        try:
            if mode == "read":
                try:
                    with open(file_pathname, 'r') as f:
                        string = f.read(10000)
                        if f.tell() > 10000:
                            string = string + "\n---Было выведено 10000 символов---"
                        print("Файл " + file_pathname + " открыт на чтение")
                except UnicodeDecodeError:
                    with open(file_pathname, 'rb') as f:
                        string = f.read(10000)
                        if f.tell() > 10000:
                            string = string + "\n---Было выведено 10000 символов---\n".encode("UTF-8")
                        print("Файл " + file_pathname + " открыт на чтение")
            elif mode == "write":
                with open(file_pathname, 'w') as f:
                    f.write("")
                    string = ""
                    print("Файл " + file_pathname + " открыт на запись")
            else:
                self.showMessageBox("Ошибка", "Неизвестный способ открытия файла", "error")
                return 1
        except Exception as e:
            self.showMessageBox("Ошибка", "Произошла ошибка (" + str(e) + ") при открытии файла", "error")
            print("return from __open_file: " + str(e))
            print("parametrs in __open_file: file_pathname = " + file_pathname + " | mode = " + mode)
            return 1
        print('---Конец открытия файла---')
        if string != "":
            self.__edit(string)

    def __edit(self, string):
        self.list.clear()
        self.list.append(str(string))

    def __decrypt(self):

        print("--Начало выполнения дешифрования---")
        if self.file_open_name == 'Выберите исходный файл':
            self.showMessageBox("Внимание!", "Необходимо выбрать исходный файл", "info")
            return
        self.__decrypt_dialog_show()

    def __decrypt_dialog_show(self):

        dial = DecryptDialog()
        res = dial.exec_()
        if dial.state == 0:
            return 1
        password = dial.pswd_line.text()

        if res == 0:
            print("Password from dialog ", password)

        if self.file_save_name in ('', 'Выберите конечный файл или сгенерируйте его в процессе работы', None):
            res = self.change_result_file("decrypt")
            if res == 1:
                return 1
        else:
            dil_result = self.showDilemaBox("Сохранить в ...",
                                            "Вы уверены, что хотите сохранить результат шифрования в файле "
                                            "" + str(self.file_save_name))
            if dil_result == 0:
                res = self.change_result_file("encrypt")
                print("Res = " + str(res))
                if res == 1:
                    return 1

        try:
            print("parametrs to decrypt_file: path_to_open = " + self.path_to_open + " | path_to_save = "
                  + self.path_to_save + " | password = " + password)
            decrypt_file(self.path_to_open, self.path_to_save, password)
        except Exception as er:
            self.showMessageBox("Ошибка", "Произошла ошибка (" + str(er) + ") при дешировке файла! Ищите виноватых!",
                                'error')
            print(er)
            return
        print("--Конец выполнения дешифрования---")
        self.__open_file(self.path_to_save, "read")
        self.showMessageBox("Успех", "Файл успешно дешифрован", 'info')

    def __encrypt(self):

        print("--Начало выполнения шифрования---")
        if self.file_open_name == 'Выберите исходный файл':
            self.showMessageBox("Внимание!", "Необходимо выбрать исходный файл", "info")
            return
        self.__encrypt_dialog_show()

    def __encrypt_dialog_show(self):

        dial = EncryptDialog()
        res = dial.exec_()
        if dial.state == 0:
            return 1

        passwords = dial.data
        algorithm = self.__translate_algorithm(dial.algorithm.currentText())

        if res == 0:
            print("Passwords from dialog ", passwords)
            print("Algorithm from dialog ", algorithm)

        if self.file_save_name in ('', 'Выберите конечный файл или сгенерируйте его в процессе работы', None):
            res = self.change_result_file("encrypt")
            print("Res = " + str(res))
            if res == 1:
                return 1
        else:
            dil_result = self.showDilemaBox("Сохранить в ...",
                                            "Вы уверены, что хотите сохранить результат шифрования в файле "
                                            "" + str(self.file_save_name))
            if dil_result == 0:
                res = self.change_result_file("encrypt")
                print("Res = " + str(res))
                if res == 1:
                    return 1

        try:
            print("parametrs to decrypt_file: path_to_open = " + self.path_to_open + " | path_to_save = "
                  + self.path_to_save + " |  password(s) = " + str(passwords) + " | algorithm = " + algorithm)
            encrypt_file(self.path_to_open, self.path_to_save, algorithm, passwords)
        except Exception as er:
            self.showMessageBox("Ошибка", "Произошла ошибка (" + str(er) + ") при шифровании файла! Ищите виноватых!",
                                'error')
            print("Ошибка при шифровании: " + str(er))
            return 1
        print("---Конец шифрования---")
        self.__open_file(self.path_to_save, "read")
        self.showMessageBox("Успех", "Файл успешно зашифрован", 'info')

    def change_result_file(self, mode):

        result = self.showDilemaBox("Внимание!", "Записать результат в новый файл?")
        if result == 1:
            if mode == "encrypt":
                filename = "encrypted_file_" + str(datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")) + ".txt"
            elif mode == "decrypt":
                filename = "decrypted_file_" + str(datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")) + ".txt"
            else:
                self.showMessageBox("Ошибка", "Неизвестный способ формирования названия файла", "error")
                return 1
            file_pathname = (str(os.path.abspath(os.curdir)) + "/" + filename)
            print(file_pathname)
            if self.__open_file(file_pathname, "write") == 1:
                return 1
            self.path_to_save = file_pathname
            self.__change_select_file_to_save_label()
        elif result == 0:
            file_pathname, _ = QFileDialog.getOpenFileName()
            if file_pathname == '':
                return 1
            print(file_pathname)
            self.path_to_save = file_pathname
            self.__change_select_file_to_save_label()

    @staticmethod
    def __translate_algorithm(algorithm):
        if algorithm == "Цезарь":
            return 'caesar'
        elif algorithm == "Виженер":
            return "vigenere"
        elif algorithm == "AES":
            return "aes"
        elif algorithm == "DES":
            return "des"
        elif algorithm == "Magma":
            return "magma"
        elif algorithm == "Кузнечик":
            return "kuznechik"

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

    @staticmethod
    def showDilemaBox(title, message):
        dil_box = QMessageBox()
        dil_box.setIcon(QMessageBox.Question)
        dil_box.setWindowTitle(title)
        dil_box.setText(message)
        wrapper = partial(center, dil_box)
        QtCore.QTimer.singleShot(0, wrapper)
        dil_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        if dil_box.exec() == QMessageBox.Yes:
            return 1
        else:
            return 0

    def closeEvent(self, e):
        result = self.showDilemaBox("Выход", "Вы уверены, что хотите выйти?")
        if result == 1:
            e.accept()
        else:
            e.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = DBFormWindow('0')
    w.show()
    # ex = Dialog()
    sys.exit(app.exec_())
