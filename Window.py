import datetime
import os
import sys
import header
import hashpw

from functools import partial
from PyQt5.Qt import *
from PyQt5 import QtCore, QtWidgets


from decrypt_dialog import DecryptDialog
from encrypt_dialog import EncryptDialog

from center import center
from api import encrypt_file
from api import decrypt_file
from algorithm import Algorithm


class DBFormWindow(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
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
        self.setMinimumSize(QSize(700, 100))
        self.middle = center
        self.wrapper = partial(center, self)
        QtCore.QTimer.singleShot(0, self.wrapper)
        self.setWindowTitle("Крипто Завр 719")

        self.boxVertical_main = QtWidgets.QVBoxLayout()  # Общий
        self.buttons_layout = QtWidgets.QHBoxLayout()  # Кнопки

        self.select_file_label = QLabel(self.file_open_name)
        self.select_file_label.setAlignment(Qt.AlignCenter)
        self.boxVertical_main.addWidget(self.select_file_label)

        self.select_file_to_save_label = QLabel(self.file_save_name)
        self.select_file_to_save_label.setAlignment(Qt.AlignCenter)
        self.boxVertical_main.addWidget(self.select_file_to_save_label)

        select_file_button = QPushButton("Открыть ...", self)
        self.buttons_layout.addWidget(select_file_button)

        select_file_to_save_button = QPushButton("Сохранить в ...", self)
        self.buttons_layout.addWidget(select_file_to_save_button)

        encrypt_button = QPushButton("Зашифровать", self)
        self.buttons_layout.addWidget(encrypt_button)

        decrypt_button = QPushButton("Дешифровать", self)
        self.buttons_layout.addWidget(decrypt_button)

        self.vision_text_button = QPushButton("Показать содержимое файла", self)
        self.buttons_layout.addWidget(self.vision_text_button)

        self.boxVertical_main.addLayout(self.buttons_layout)
        self.setLayout(self.boxVertical_main)

        self.list = QTextBrowser(self)
        #self.list.setGeometry(QtCore.QRect(10, 110, 620, 270))
        self.list.setVisible(False)
        self.boxVertical_main.addWidget(self.list)

        select_file_to_save_button.clicked.connect(self.__select_file_to_save)
        select_file_button.clicked.connect(self.__select_file)
        decrypt_button.clicked.connect(self.__decrypt)
        encrypt_button.clicked.connect(self.__encrypt)
        self.vision_text_button.clicked.connect(self.__change_vision_text)

    def __change_vision_text(self):
        if self.list.isVisible() == 1:
            self.list.setVisible(False)
            self.vision_text_button.setText("Показать содержимое файла")
            QtCore.QTimer.singleShot(0, self.wrapper)
            self.setFixedSize(QSize(700, 100))
            self.setMinimumSize(QSize(700, 100))
        else:
            self.list.setVisible(True)
            self.vision_text_button.setText("Скрыть содержимое файла")
            QtCore.QTimer.singleShot(0, self.wrapper)
            self.setMinimumSize(QSize(700, 480))

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
                            string = string + "\n--Было выведено 10000 символов--"
                        print("Файл " + file_pathname + " открыт на чтение")
                except UnicodeDecodeError:
                    with open(file_pathname, 'rb') as f:
                        string = f.read(10000)
                        if f.tell() > 10000:
                            string = string + "\n--Было выведено 10000 символов--\n".encode("UTF-8")
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
            self.showMessageBox("Ошибка",
                                "Произошла ошибка (" + str(e) + ") при открытии файла", "error")
            print("return from __open_file: " + str(e))
            print("parametrs in __open_file: "
                  "file_pathname = " + file_pathname + " | mode = " + mode)
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

        try:
            hdr = header.Header()
            with open(self.path_to_open, 'rb') as ifstream:
                hdr.read(ifstream)
                try:
                    hashpw.HashFunc(hdr.hash_function)
                except ValueError:
                    raise ValueError('Unknown hash function in header')
                algorithm = Algorithm(hdr.algorithm)
                if algorithm.is_symmetric() == 1:
                    mode = "password"
                else:
                    mode = "key"
        except Exception as error:
            self.showMessageBox("Ошибка", "Неверный формат файла",
                                'error')
            print(error)
            return

        dial = DecryptDialog(mode)
        res = dial.exec_()
        if dial.state == 0:
            return 1
        if mode == "password":
            password = dial.key
            privkey_files = None
        else:
            password = None
            privkey_files = dial.key

        if res == 0:
            print("Password from dialog ", password)

        if self.file_save_name in ('', 'Выберите конечный файл '
                                       'или сгенерируйте его в процессе работы', None):
            res = self.change_result_file("decrypt")
            if res == 1:
                return 1
        else:
            dil_result = self.showDilemaBox("Сохранить в ...",
                                            "Вы уверены, что хотите сохранить "
                                            "результат шифрования в файле "
                                            "" + str(self.file_save_name))
            if dil_result == 0:
                res = self.change_result_file("encrypt")
                print("Res = " + str(res))
                if res == 1:
                    return 1

        try:
            print("parametrs to decrypt_file: "
                  "path_to_open = " + self.path_to_open + " | path_to_save = "
                  + self.path_to_save + " | password = " + str(password) + " | pubkey_files = "
                  + str(privkey_files))
            decrypt_file(self.path_to_open, self.path_to_save, password, privkey_files)
        except Exception as er:
            if er == "Invalid password":
                self.showMessageBox("Ошибка", "Неверный пароль",
                                    'error')
            else:
                self.showMessageBox("Ошибка", "Произошла ошибка "
                                    "(" + str(er) + ") при дешировке файла! Ищите виноватых!",
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

        algorithm = self.__translate_algorithm(dial.algorithm.currentText())
        if algorithm != "rsa":
            passwords = dial.data
            pubkey_files = None
        else:
            passwords = None
            pubkey_files = dial.data

        if res == 0:
            print("Passwords from dialog ", passwords)
            print("Algorithm from dialog ", algorithm)
            print("pubkey_files from dialog ", pubkey_files)

        if self.file_save_name in ('', 'Выберите конечный файл '
                                   'или сгенерируйте его в процессе работы', None):
            res = self.change_result_file("encrypt")
            print("Res = " + str(res))
            if res == 1:
                return 1
        else:
            dil_result = self.showDilemaBox("Сохранить в ...",
                                            "Вы уверены, что хотите сохранить "
                                            "результат шифрования в файле "
                                            "" + str(self.file_save_name))
            if dil_result == 0:
                res = self.change_result_file("encrypt")
                print("Res = " + str(res))
                if res == 1:
                    return 1

        try:
            print("parametrs to decrypt_file: "
                  "path_to_open = " + self.path_to_open + " | path_to_save = "
                  + self.path_to_save + " |  "
                  "algorithm= " + algorithm + " | password(s) = " + str(passwords)
                  + " | pubkey_files = " + str(pubkey_files))
            encrypt_file(self.path_to_open, self.path_to_save, algorithm, passwords, pubkey_files)
        except Exception as er:
            self.showMessageBox("Ошибка", "Произошла ошибка (" + str(er) + ") "
                                "при шифровании файла! Ищите виноватых!",
                                'error')
            print("Ошибка при шифровании: " + str(er))
            return 1
        print("---Конец шифрования---")
        self.__open_file(self.path_to_save, "read")
        self.showMessageBox("Успех", "Файл успешно зашифрован", 'info')

    def change_result_file(self, mode):

        result = self.showDilemaBox("Внимание!", "Записать результат в новый файл?")
        if result == 1:
            time = str(datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
            if mode == "encrypt":
                filename = "encrypted_file_" + time + ".txt"
            elif mode == "decrypt":
                filename = "decrypted_file_" + time + ".txt"
            else:
                self.showMessageBox("Ошибка", "Неизвестный способ "
                                    "формирования названия файла", "error")
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
        elif algorithm == "RSA":
            return "rsa"

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
    w = DBFormWindow()
    w.show()
    # ex = Dialog()
    sys.exit(app.exec_())
