from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow

from UI_functional.change_perosnal_data import change_password
from UI.call_ui import show_dialog


class CPWindow(QMainWindow):
    def __init__(self, login, token):
        super(CPWindow, self).__init__()
        self.login = login
        self.token = token

        self.setWindowTitle('Change password')
        self.setGeometry(600, 300, 280, 169)
        self.setFixedSize(self.size())

        font = QtGui.QFont()
        font.setPointSize(10)

        self.old_password_LineEdit = QtWidgets.QLineEdit(self)
        self.old_password_LineEdit.setGeometry(10, 10, 260, 31)
        self.old_password_LineEdit.setFont(font)
        self.old_password_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.old_password_LineEdit.setPlaceholderText('Enter your old password')

        self.new_password_LineEdit = QtWidgets.QLineEdit(self)
        self.new_password_LineEdit.setGeometry(10, 50, 260, 31)
        self.new_password_LineEdit.setFont(font)
        self.new_password_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.new_password_LineEdit.setPlaceholderText('Enter your new password')

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
        if (self.old_password_LineEdit.text() and
                self.new_password_LineEdit.text() and
                self.repeat_password_LineEdit.text()):
            if self.new_password_LineEdit.text() == self.repeat_password_LineEdit.text():
                if change_password(
                        login=self.login,
                        old_password=self.old_password_LineEdit.text(),
                        new_password=self.new_password_LineEdit.text(),
                        token=self.token
                ):
                    self.close()
            else:
                show_dialog('Wrong data!', 'You entered different passwords')
