from PyQt5.Qt import *
from PyQt5 import QtCore, QtWidgets
import sys
from functools import partial

from center import center


class EncryptDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.state = 2
        self.previous_algorithm_index = 0
        self.previous_password_amount = 0
        self.current_password_amount = 1
        self.data = list()
        self.__init_ui()

    def __init_ui(self):
        self.setMinimumSize(QSize(420, 330))  # Устанавливаем размеры
        wrapper = partial(center, self)
        QtCore.QTimer.singleShot(0, wrapper)
        self.setWindowTitle("Шифрование")

        self.boxVertical_main = QtWidgets.QVBoxLayout()  # Общее
        self.boxHorizontal_pas_amount = QtWidgets.QHBoxLayout()  # Для количества паролей
        self.boxGrid = QtWidgets.QGridLayout()  # Для паролей
        self.boxHorizontal_input = QtWidgets.QHBoxLayout()

        self.algorithm = QComboBox(self)  # Названия алгоритмов
        self.algorithm.setEditable(True)
        self.algorithm.lineEdit().setAlignment(Qt.AlignCenter)
        self.algorithm.lineEdit().setReadOnly(True)
        self.algorithm.activated[str].connect(self.__asymmetric)
        self.boxVertical_main.addWidget(self.algorithm)
        self.__get_algorithm()

        self.passwords = QLabel("Количество паролей:", self)
        self.minus_box = QPushButton("-", self)
        self.password_amount = QLabel(str(self.current_password_amount), self)
        self.password_amount.setAlignment(Qt.AlignCenter)
        self.plus_box = QPushButton("+", self)

        self.boxHorizontal_pas_amount.addWidget(self.passwords)
        self.boxHorizontal_pas_amount.addWidget(self.minus_box)
        self.boxHorizontal_pas_amount.addWidget(self.password_amount)
        self.boxHorizontal_pas_amount.addWidget(self.plus_box)

        self.minus_box.clicked.connect(self.__minus)
        self.plus_box.clicked.connect(self.__plus)

        self.__change_password_line()

        self.boxVertical_main.addLayout(self.boxHorizontal_pas_amount)
        self.boxVertical_main.addLayout(self.boxGrid)
        self.boxVertical_main.addLayout(self.boxHorizontal_input)
        self.setLayout(self.boxVertical_main)

        self.multy_pass = QCheckBox("Показать пароль(и)", self)
        self.multy_pass.stateChanged.connect(self.__change_mod)
        self.boxVertical_main.addWidget(self.multy_pass)

        self.passwords_by_hands_button = QPushButton("Ввести пароли вручную", self)
        self.boxHorizontal_input.addWidget(self.passwords_by_hands_button)
        self.passwords_by_hands_button.clicked.connect(self.__change_input)

        self.passwords_from_txt_button = QPushButton("Извлечь пароли из файла", self)
        self.boxHorizontal_input.addWidget(self.passwords_from_txt_button)
        self.passwords_from_txt_button.clicked.connect(self.__open_file)

        encrypt_button = QPushButton("Зашифровать", self)
        self.boxVertical_main.addWidget(encrypt_button)
        encrypt_button.clicked.connect(self.__encrypt)

    def __asymmetric(self):
        if self.algorithm.currentIndex() == 7:
            self.passwords.setText("Количество ключей")
            self.passwords_by_hands_button.setEnabled(False)
            self.passwords_from_txt_button.setEnabled(False)
            self.multy_pass.setEnabled(False)
            self.__change_input_type()
        else:
            if self.previous_algorithm_index == 7:
                self.passwords.setText("Количество паролей")
                self.passwords_by_hands_button.setEnabled(True)
                self.passwords_from_txt_button.setEnabled(True)
                self.multy_pass.setEnabled(True)
                self.__change_input_type()

        self.previous_algorithm_index = self.algorithm.currentIndex()

    def __change_input_type(self):
        if self.current_password_amount == 1:
            self.boxGrid.takeAt(1).widget().setParent(None)
            self.boxGrid.takeAt(0).widget().setParent(None)
        else:
            temp_pos = 2 * self.current_password_amount - 1
            for i in range(2 * self.current_password_amount):
                position = temp_pos
                self.boxGrid.takeAt(position).widget().setParent(None)
                if temp_pos > 0:
                    temp_pos = temp_pos - 1

        if self.algorithm.currentIndex() == 7:
            temp_pos = 0
            for i in range(self.current_password_amount):
                position = temp_pos

                if position % 2 == 0:
                    password_label = QLabel("Ключ №" + str(position+1), self)
                    self.boxGrid.addWidget(password_label, position // 2, 0)

                    key_line = QPushButton("Выбрать ключ", self)
                    key_line.clicked.connect(lambda checked, button=key_line: self.__chose_key(button))
                    self.boxGrid.addWidget(key_line, position // 2, 1)
                else:
                    password_label = QLabel("Ключ №" + str(position+1), self)
                    self.boxGrid.addWidget(password_label, position // 2, 2)

                    key_line = QPushButton("Выбрать ключ", self)
                    key_line.clicked.connect(lambda checked, button=key_line: self.__chose_key(button))
                    self.boxGrid.addWidget(key_line, position // 2, 3)
                temp_pos = temp_pos + 1
        else:
            temp_pos = 0
            for i in range(self.current_password_amount):
                position = temp_pos

                if position % 2 == 0:
                    password_label = QLabel("Пароль №" + str(position + 1), self)
                    self.boxGrid.addWidget(password_label, position // 2, 0)

                    password_line = QLineEdit(self)
                    password_line.setEchoMode(self.state)
                    password_line.setCursorPosition(1)
                    self.boxGrid.addWidget(password_line, position // 2, 1)
                else:
                    password_label = QLabel("Пароль №" + str(position + 1), self)
                    self.boxGrid.addWidget(password_label, position // 2, 2)

                    password_line = QLineEdit(self)
                    password_line.setEchoMode(self.state)
                    password_line.setCursorPosition(1)
                    self.boxGrid.addWidget(password_line, position // 2, 3)
                temp_pos = temp_pos + 1

    def __add_key(self):
        position = self.current_password_amount - 1

        if position % 2 == 0:
            password_label = QLabel("Ключ №" + str(self.current_password_amount), self)
            self.boxGrid.addWidget(password_label, position // 2, 0)

            key_line = QPushButton("Выбрать ключ", self)
            key_line.clicked.connect(lambda checked, button=key_line: self.__chose_key(button))
            self.boxGrid.addWidget(key_line, position // 2, 1)
        else:
            password_label = QLabel("Ключ №" + str(self.current_password_amount), self)
            self.boxGrid.addWidget(password_label, position // 2, 2)

            key_line = QPushButton("Выбрать ключ", self)
            key_line.clicked.connect(lambda checked, button=key_line: self.__chose_key(button))
            self.boxGrid.addWidget(key_line, position // 2, 3)

    def __remove_element(self):
        if self.algorithm.currentIndex() == 7:
            if len(self.data) != 0:
                self.data.pop(len(self.data) - 1)
        position = 2 * self.current_password_amount
        self.boxGrid.takeAt(position).widget().setParent(None)
        self.boxGrid.takeAt(position).widget().setParent(None)

    def __change_key_line(self):
        if self.current_password_amount > self.previous_password_amount:
            self.__add_key()
        else:
            self.__remove_element()

    def __chose_key(self, button):
        file_pathname, _ = QFileDialog.getOpenFileName()
        if file_pathname == '':
            self.showMessageBox("Внимание", "Файл с ключом не был выбран", "info")
            return
        path_to_key = file_pathname
        with open(file_pathname, 'r') as f:
            key = f.read()
            print("Файл " + file_pathname + " открыт на чтение")
            print("data: " + key)
        self.data.append(file_pathname)
        temp = path_to_key.split("/")
        key_file_name = temp[len(temp)-1]
        button.setText(key_file_name)

    def __change_input(self):
        self.plus_box.setEnabled(True)
        self.minus_box.setEnabled(True)
        for row in range(self.boxGrid.rowCount()):
            for column in range(self.boxGrid.columnCount()):
                if column % 2 == 1:
                    try:
                        self.boxGrid.itemAtPosition(row, column).widget().setEnabled(True)
                    except AttributeError:
                        pass

    def __open_file(self):
        file_pathname, _ = QFileDialog.getOpenFileName()

        self.plus_box.setEnabled(False)
        self.minus_box.setEnabled(False)
        for row in range(self.boxGrid.rowCount()):
            for column in range(self.boxGrid.columnCount()):
                if column % 2 == 1:
                    try:
                        self.boxGrid.itemAtPosition(row, column).widget().setEnabled(False)
                    except AttributeError:
                        pass

        with open(file_pathname, 'r') as f:
            string = f.read()
        passwords = string.split('\n')
        for el in passwords:
            if el == '':
                passwords.remove(el)
        self.data = passwords
        print(self.data)

    def __change_mod(self, state):
        if state == 2:
            self.state = 0
        else:
            self.state = 2
        if state == Qt.Checked:
            for row in range(self.boxGrid.rowCount()):
                for column in range(self.boxGrid.columnCount()):
                    if column % 2 == 1:
                        try:
                            self.boxGrid.itemAtPosition(row, column).widget().setEchoMode(0)
                        except AttributeError:
                            pass
        else:
            for row in range(self.boxGrid.rowCount()):
                for column in range(self.boxGrid.columnCount()):
                    if column % 2 == 1:
                        try:
                            self.boxGrid.itemAtPosition(row, column).widget().setEchoMode(2)
                        except AttributeError:
                            pass

    def __add_password(self):
        position = self.current_password_amount - 1

        if position % 2 == 0:
            password_label = QLabel("Пароль №" + str(self.current_password_amount), self)
            self.boxGrid.addWidget(password_label, position // 2, 0)

            password_line = QLineEdit(self)
            password_line.setEchoMode(self.state)
            password_line.setCursorPosition(1)
            self.boxGrid.addWidget(password_line, position // 2, 1)
        else:
            password_label = QLabel("Пароль №" + str(self.current_password_amount), self)
            self.boxGrid.addWidget(password_label, position // 2, 2)

            password_line = QLineEdit(self)
            password_line.setEchoMode(self.state)
            password_line.setCursorPosition(1)
            self.boxGrid.addWidget(password_line, position // 2, 3)

    def __change_password_line(self):
        if self.current_password_amount > self.previous_password_amount:
            self.__add_password()
        else:
            self.__remove_element()

    def box_grid_data(self):
        if len(self.data) > 10:
            return
        self.data.clear()
        for row in range(self.boxGrid.rowCount()):
            for column in range(self.boxGrid.columnCount()):
                if column % 2 == 1:
                    try:
                        self.data.append(self.boxGrid.itemAtPosition(row, column).widget().text())
                    except AttributeError:
                        pass

    def __plus(self):
        if self.algorithm.currentIndex() == 7:
            if self.current_password_amount == 10:
                self.showMessageBox("Внимание!", "Для записи более 10 ключей используйте текстовый файл", "info")
            else:
                self.previous_password_amount = self.current_password_amount
                self.current_password_amount = self.current_password_amount + 1
                self.password_amount.setText(str(self.current_password_amount))
                self.__change_key_line()
        else:
            if self.current_password_amount == 10:
                self.showMessageBox("Внимание!", "Для записи более 10 паролей используйте текстовый файл", "info")
            else:
                self.previous_password_amount = self.current_password_amount
                self.current_password_amount = self.current_password_amount + 1
                self.password_amount.setText(str(self.current_password_amount))
                self.__change_password_line()

    def __minus(self):
        if self.algorithm.currentIndex() == 7:
            if self.current_password_amount == 1:
                self.showMessageBox("Ошибка!", "Минимальное количество ключей - 1", "error")
            else:
                self.previous_password_amount = self.current_password_amount
                self.current_password_amount = self.current_password_amount - 1
                self.password_amount.setText(str(self.current_password_amount))
                self.__change_password_line()
        else:
            if self.current_password_amount == 1:
                self.showMessageBox("Ошибка!", "Минимальное количество паролей - 1", "error")
            else:
                self.previous_password_amount = self.current_password_amount
                self.current_password_amount = self.current_password_amount - 1
                self.password_amount.setText(str(self.current_password_amount))
                self.__change_password_line()

    def __get_algorithm(self):
        self.algorithm.insertItem(0, "--Выберите алгоритм--")
        self.algorithm.insertItem(1, "Цезарь")
        self.algorithm.insertItem(2, "Виженер")
        self.algorithm.insertItem(3, "AES")
        self.algorithm.insertItem(4, "DES")
        self.algorithm.insertItem(5, "Magma")
        self.algorithm.insertItem(6, "Кузнечик")
        self.algorithm.insertItem(7, "RSA")
        self.algorithm.setCurrentIndex(0)

    def __encrypt(self):
        for row in range(self.boxGrid.rowCount()):
            for column in range(self.boxGrid.columnCount()):
                if column % 2 == 1:
                    try:
                        if self.boxGrid.itemAtPosition(row, column).widget().text() == "":
                            print(self.boxGrid.itemAtPosition(row, column).widget().text())
                            self.showMessageBox("Ошибка",
                                                self.boxGrid.itemAtPosition(row, column - 1).widget().text() +
                                                " не был ввыден", "error")
                            return
                    except AttributeError:
                        pass
        if self.algorithm.currentIndex() == 0:
            self.showMessageBox("Ошибка", "Алгоритм не был выбран", "error")
            return
        if self.algorithm.currentIndex() == 7:
            for row in range(self.boxGrid.rowCount()):
                for column in range(self.boxGrid.columnCount()):
                    if column % 2 == 1:
                        try:
                            if self.boxGrid.itemAtPosition(row, column).widget().text() == "Выбрать ключ":
                                self.showMessageBox("Ошибка",
                                                    self.boxGrid.itemAtPosition(row, column - 1).widget().text() +
                                                    " не был ввыден", "error")
                                return
                        except AttributeError:
                            pass
        self.state = 1
        if self.algorithm.currentIndex() != 7:
            self.box_grid_data()
        print("list of keys or passwords = " + str(self.data))
        self.close()

    def keyPressEvent(self, e):
        k = e.key()
        super().keyPressEvent(e)
        if k == Qt.Key_Enter:
            self.__encrypt()

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
    w = EncryptDialog()
    w.show()
    sys.exit(app.exec_())
