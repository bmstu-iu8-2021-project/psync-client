from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow

from UI_functional.change_password import change_password
from UI.call_ui import show_dialog


class CPWindow(QMainWindow):
    def __init__(self, wpw):
        super(CPWindow, self).__init__()
        self.__wpw = wpw

        self.__login = self.__wpw.login
        self.__token = self.__wpw.token
        self.__wpw.setEnabled(False)

        self.setWindowTitle('Change password')
        self.setGeometry(600, 300, 280, 169)
        self.setFixedSize(self.size())

        font = QtGui.QFont()
        font.setPointSize(10)

        self.old_password_lineEdit = QtWidgets.QLineEdit(self)
        self.old_password_lineEdit.setGeometry(10, 10, 260, 31)
        self.old_password_lineEdit.setFont(font)
        self.old_password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.old_password_lineEdit.setPlaceholderText('Enter your old password')

        self.new_password_lineEdit = QtWidgets.QLineEdit(self)
        self.new_password_lineEdit.setGeometry(10, 50, 260, 31)
        self.new_password_lineEdit.setFont(font)
        self.new_password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.new_password_lineEdit.setPlaceholderText('Enter your new password')

        self.repeat_password_LineEdit = QtWidgets.QLineEdit(self)
        self.repeat_password_LineEdit.setGeometry(10, 90, 260, 31)
        self.repeat_password_LineEdit.setFont(font)
        self.repeat_password_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.repeat_password_LineEdit.setPlaceholderText('Repeat your new password')

        self.accept_Button = QtWidgets.QPushButton(self)
        self.accept_Button.setGeometry(180, 130, 90, 28)
        self.accept_Button.setText("Accept")
        self.accept_Button.clicked.connect(self.accept)

    def accept(self):
        if (self.old_password_lineEdit.text() and
                self.new_password_lineEdit.text() and
                self.repeat_password_LineEdit.text()):
            if self.new_password_lineEdit.text() == self.repeat_password_LineEdit.text():
                if change_password(
                        login=self.__login,
                        old_password=self.old_password_lineEdit.text(),
                        new_password=self.new_password_lineEdit.text(),
                        token=self.__token
                ):
                    self.close()
                    show_dialog('Success', 'Your password was successfully changed.', 2)
            else:
                show_dialog('Wrong data!', 'You entered different passwords')

    def closeEvent(self, event):
        self.__wpw.setEnabled(True)
