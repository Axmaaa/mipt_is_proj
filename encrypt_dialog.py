from PyQt5.Qt import *
from PyQt5 import QtCore, QtWidgets
import sys
from functools import partial

from center import center


class EncryptDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.state = 2
        self.previous_pswd_amount = 0
        self.current_pswd_amount = 1
        self.data = list()
        self.__init_ui()

    def __init_ui(self):
        self.setMinimumSize(QSize(400, 300))  # Устанавливаем размеры
        wrapper = partial(center, self)
        QtCore.QTimer.singleShot(0, wrapper)
        self.setWindowTitle("Шифрование")

        self.boxVertical_main = QtWidgets.QVBoxLayout()  # Общее
        self.boxHorizontal_pas_amount = QtWidgets.QHBoxLayout()  # Для количества паролей
        self.boxGrid = QtWidgets.QGridLayout()  # Для паролей

        self.algorithm = QComboBox(self)  # Названия алгоритмов
        self.algorithm.setEditable(True)
        self.algorithm.lineEdit().setAlignment(Qt.AlignCenter)
        self.algorithm.lineEdit().setReadOnly(True)
        self.boxVertical_main.addWidget(self.algorithm)
        self.__get_algorithm()

        self.pswds = QLabel("Количество паролей:", self)
        minus_box = QPushButton("-", self)
        self.pswd_amount = QLabel(str(self.current_pswd_amount), self)
        self.pswd_amount.setAlignment(Qt.AlignCenter)
        plus_box = QPushButton("+", self)

        self.boxHorizontal_pas_amount.addWidget(self.pswds)
        self.boxHorizontal_pas_amount.addWidget(minus_box)
        self.boxHorizontal_pas_amount.addWidget(self.pswd_amount)
        self.boxHorizontal_pas_amount.addWidget(plus_box)

        minus_box.clicked.connect(self.__minus)
        plus_box.clicked.connect(self.__plus)

        self.__change_pswd_line()

        self.boxVertical_main.addLayout(self.boxHorizontal_pas_amount)
        self.boxVertical_main.addLayout(self.boxGrid)
        self.setLayout(self.boxVertical_main)

        self.multy_pass = QCheckBox("Показать пароль(и)", self)
        self.multy_pass.stateChanged.connect(self.__change_mod)
        self.boxVertical_main.addWidget(self.multy_pass)

        passwords_from_txt_button = QPushButton("Извлечь пароли из файла", self)
        self.boxVertical_main.addWidget(passwords_from_txt_button)
        passwords_from_txt_button.clicked.connect(self.open_file)

        encrypt_button = QPushButton("Зашифровать", self)
        self.boxVertical_main.addWidget(encrypt_button)
        encrypt_button.clicked.connect(self.__encrypt)

    def open_file(self):
        file_pathname, _ = QFileDialog.getOpenFileName()
        with open(file_pathname, 'r') as f:
            string = f.read()
        passwords = string.split('\n')
        for el in passwords:
            if el == '':
                passwords.remove(el)
        self.data = passwords
        print(self.data)
        print(len(self.data))
        if len(self.data) > 10:
            for i in range(len(self.data)):
                if i == 9:
                    self.showMessageBox("Внимание", "Все пароли из файла прочитаны, "
                                                    "но на экран будут выведены только 10 из них", "info")
                    break
                self.__plus()
        else:
            for i in range(len(self.data)-1):
                self.__plus()
        num = 0
        for row in range(self.boxGrid.rowCount()):
            for column in range(self.boxGrid.columnCount()):
                if column % 2 == 1:
                    try:
                        self.boxGrid.itemAtPosition(row, column).widget().setText(self.data[num])
                        num = num + 1
                    except AttributeError:
                        pass

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

    def __change_pswd_line(self):
        if self.current_pswd_amount > self.previous_pswd_amount:
            position = self.current_pswd_amount - 1

            if position % 2 == 0:
                pswd_label = QLabel("Пароль №" + str(self.current_pswd_amount), self)
                self.boxGrid.addWidget(pswd_label, position // 2, 0)

                pswd_line = QLineEdit(self)
                pswd_line.setEchoMode(self.state)
                pswd_line.setCursorPosition(1)
                self.boxGrid.addWidget(pswd_line, position // 2, 1)
            else:
                pswd_label = QLabel("Пароль №" + str(self.current_pswd_amount), self)
                self.boxGrid.addWidget(pswd_label, position // 2, 2)

                pswd_line = QLineEdit(self)
                pswd_line.setEchoMode(self.state)
                pswd_line.setCursorPosition(1)
                self.boxGrid.addWidget(pswd_line, position // 2, 3)
        else:
            position = 2 * self.current_pswd_amount
            self.boxGrid.takeAt(position).widget().setParent(None)
            self.boxGrid.takeAt(position).widget().setParent(None)

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
        if self.current_pswd_amount == 10:
            self.showMessageBox("Внимание!", "Для записи более 10 паролей используйте текстовый файл", "info")
        else:
            self.previous_pswd_amount = self.current_pswd_amount
            self.current_pswd_amount = self.current_pswd_amount + 1
            self.pswd_amount.setText(str(self.current_pswd_amount))
            self.__change_pswd_line()

    def __minus(self):
        if self.current_pswd_amount == 1:
            self.showMessageBox("Ошибка!", "Минимальное количество паролей - 1", "error")
        else:
            self.previous_pswd_amount = self.current_pswd_amount
            self.current_pswd_amount = self.current_pswd_amount - 1
            self.pswd_amount.setText(str(self.current_pswd_amount))
            self.__change_pswd_line()

    def __get_algorithm(self):
        self.algorithm.insertItem(0, "--Выберите алгоритм--")
        self.algorithm.insertItem(1, "Цезарь")
        self.algorithm.insertItem(2, "Виженер")
        self.algorithm.insertItem(3, "AES")
        self.algorithm.insertItem(4, "Des")
        self.algorithm.insertItem(5, "Magma")
        self.algorithm.insertItem(6, "Кузнечик")

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
        self.state = 1
        self.box_grid_data()
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
