from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow

from UI_functional.change_perosnal_data import change_mail
from UI.call_ui import show_dialog


class CEWindow(QMainWindow):
    def __init__(self, wpw):
        super(CEWindow, self).__init__()
        self.__wpw = wpw

        self.__login = self.__wpw.login
        self.__token = self.__wpw.token
        self.__wpw.setEnabled(False)

        self.setWindowTitle('Change email')
        self.setGeometry(600, 300, 280, 129)
        self.setFixedSize(self.size())

        font = QtGui.QFont()
        font.setPointSize(10)

        self.new_email_lineEdit = QtWidgets.QLineEdit(self)
        self.new_email_lineEdit.setGeometry(10, 10, 260, 31)
        self.new_email_lineEdit.setFont(font)
        self.new_email_lineEdit.setPlaceholderText('Enter your new email')

        self.password_lineEdit = QtWidgets.QLineEdit(self)
        self.password_lineEdit.setGeometry(10, 50, 260, 31)
        self.password_lineEdit.setFont(font)
        self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_lineEdit.setPlaceholderText('Enter your password')

        self.accept_Button = QtWidgets.QPushButton(self)
        self.accept_Button.setGeometry(180, 90, 90, 28)
        self.accept_Button.setText("Accept")
        self.accept_Button.clicked.connect(self.accept)

    def accept(self):
        if self.password_lineEdit.text() and self.new_email_lineEdit.text():
            if change_mail(
                    login=self.__login,
                    new_mail=self.new_email_lineEdit.text(),
                    password=self.password_lineEdit.text(),
                    token=self.__token
            ):
                self.close()
                show_dialog('Success', 'Your email was successfully changed.', 2)

    def closeEvent(self, event):
        self.__wpw.setEnabled(True)
