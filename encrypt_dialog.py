from PyQt5.Qt import *
from PyQt5 import QtCore, QtWidgets
import sys
from functools import partial

from center import center


class EncryptDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.state = 0

        self.__init_ui()

    def __init_ui(self):
        self.setFixedSize(QSize(300, 170))  # Устанавливаем размеры
        wrapper = partial(center, self)
        QtCore.QTimer.singleShot(0, wrapper)
        self.setWindowTitle("Шифрование")  # Устанавл заголовок окна

        self.LayoutWidget1 = QtWidgets.QWidget(self)
        self.LayoutWidget1.setGeometry(QtCore.QRect(10, 40, 280, 120))
        self.Layout1 = QtWidgets.QVBoxLayout(self.LayoutWidget1)
        self.Layout1.setContentsMargins(0, 0, 0, 0)

        self.LayoutWidget2 = QtWidgets.QWidget(self)
        self.LayoutWidget2.setGeometry(QtCore.QRect(10, 10, 280, 30))
        self.Layout2 = QtWidgets.QHBoxLayout(self.LayoutWidget2)
        self.Layout2.setContentsMargins(0, 0, 0, 0)

        pswd_label = QLabel("Пароль:", self)
        self.Layout2.addWidget(pswd_label)

        self.pswd_line = QLineEdit(self)
        self.pswd_line.setCursorPosition(1)
        self.Layout2.addWidget(self.pswd_line)
        self.pswd_line.setEchoMode(2)

        self.multy_pass = QCheckBox("Несколько паролей", self)
        self.multy_pass.stateChanged.connect(self.__change_mod)
        self.Layout1.addWidget(self.multy_pass)

        self.algorithm = QComboBox(self)
        self.Layout1.addWidget(self.algorithm)
        self.__get_algorithm()

        encrypt_button = QPushButton("Зашифровать", self)
        self.Layout1.addWidget(encrypt_button)
        encrypt_button.clicked.connect(self.__encrypt)

    def __change_mod(self, state):
        if state == Qt.Checked:
            self.pswd_line.setEchoMode(0)
        else:
            self.pswd_line.setEchoMode(2)

    def __get_algorithm(self):
        self.algorithm.insertItem(0, "--Выберите алгоритм--")
        self.algorithm.insertItem(1, "Цезарь")
        self.algorithm.insertItem(2, "Виженер")
        self.algorithm.insertItem(2, "AES")


    def __encrypt(self):
        if self.pswd_line.text() == "":
            self.showMessageBox("Ошибка", "Пароль не был ввыден", "error")
            self.pswd_line.setFocus()
            return
        if self.algorithm.currentIndex() == 0:
            self.showMessageBox("Ошибка", "Алгоритм не был выбран", "error")
            self.pswd_line.setFocus()
            return
        self.state = 1
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
