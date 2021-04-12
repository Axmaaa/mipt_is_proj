from PyQt5.Qt import *
from PyQt5 import QtCore, QtWidgets
import sys
from functools import partial

from center import center


class DecryptDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.state = 0

        self.__init_ui()

    def __init_ui(self):
        self.setFixedSize(QSize(270, 120))  # Устанавливаем размеры
        wrapper = partial(center, self)
        QtCore.QTimer.singleShot(0, wrapper)
        self.setWindowTitle("Дешифрование")  # Устанавл заголовок окна

        self.LayoutWidget1 = QtWidgets.QWidget(self)
        self.LayoutWidget1.setGeometry(QtCore.QRect(10, 10, 250, 30))
        self.Layout1 = QtWidgets.QHBoxLayout(self.LayoutWidget1)
        self.Layout1.setContentsMargins(0, 0, 0, 0)

        self.LayoutWidget2 = QtWidgets.QWidget(self)
        self.LayoutWidget2.setGeometry(QtCore.QRect(10, 10, 250, 100))
        self.Layout2 = QtWidgets.QHBoxLayout(self.LayoutWidget2)
        self.Layout2.setContentsMargins(0, 0, 0, 0)

        pswd_label = QLabel("Пароль:", self)
        self.Layout1.addWidget(pswd_label)

        self.pswd_line = QLineEdit(self)
        self.Layout1.addWidget(self.pswd_line)
        self.pswd_line.setEchoMode(2)

        decrypt_button = QPushButton("Дешифровать", self)
        self.Layout2.addWidget(decrypt_button)
        decrypt_button.clicked.connect(self.__decrypt)

    def __decrypt(self):
        if self.pswd_line.text() == "":
            self.showMessageBox("Ошибка", "Пароль не был ввыден", "error")
            self.pswd_line.setFocus()
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
    w = DecryptDialog()
    w.show()
    sys.exit(app.exec_())
