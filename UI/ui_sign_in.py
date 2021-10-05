from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

from UI import call_ui, ui_profile, ui_about, ui_sign_up, create_menu
from data_processing.constants import IP, PORT, PROTOCOL
import requests
import json


class SIWindow(QMainWindow):
    def __init__(self):
        super(SIWindow, self).__init__()
        self.token = ''

        self.setWindowTitle('SyncGad • Sign In')
        self.setGeometry(600, 300, 285, 160)
        self.setFixedSize(self.size())

        font = QtGui.QFont()
        font.setPointSize(10)

        self.login_lineedit = QtWidgets.QLineEdit(self)
        self.login_lineedit.setGeometry(10, 36, 260, 31)
        self.login_lineedit.setFont(font)
        self.login_lineedit.setPlaceholderText('Enter your login or email')

        self.password_lineedit = QtWidgets.QLineEdit(self)
        self.password_lineedit.setGeometry(10, 76, 260, 31)
        self.password_lineedit.setFont(font)
        self.password_lineedit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_lineedit.setPlaceholderText('Enter your password')

        self.enter_button = QtWidgets.QPushButton(self)
        self.enter_button.setGeometry(10, 116, 140, 30)
        self.enter_button.setText('Sign in')
        self.enter_button.clicked.connect(self.enter)

        self.registration_button = QtWidgets.QPushButton(self)
        self.registration_button.setGeometry(160, 116, 110, 30)
        self.registration_button.setText('Sign up')
        self.registration_button.clicked.connect(self.register)

        create_menu.un_menu(self)

    def enter(self):
        login = self.login_lineedit.text()
        password = self.password_lineedit.text()
        request = requests.get(f'{PROTOCOL}://{IP}:{PORT}/auth/',
                               params={
                                   'login': login,
                                   'password': password,
                               })
        token = request.content
        if json.loads(token)['token']:
            self.token = token
            self.password_lineedit.setText('')
            self.p_window = ui_profile.PWindow(self.token, self, login)
            self.p_window.show()
            self.hide()
        else:
            self.password_lineedit.setText('')
            call_ui.show_warning('Wrong data!', 'The entered login or password is incorrect.')
        # key = db_action.access_request(self.conn, login, password)
        # self.password_lineedit.setText('')
        # if key:
        #     self.p_window = ui_profile.PWindow(self.conn, self, login)
        #     self.p_window.show()
        #     self.hide()
        # else:
        #     call_ui.show_warning('Wrong data!', 'The entered login or password is incorrect.')

    def register(self):
        self.su_window = ui_sign_up.SUWindow(self)
        self.su_window.show()
        self.hide()

    @QtCore.pyqtSlot()
    def about(self):
        self.a_window = ui_about.AWindow()
        self.a_window.show()

    @QtCore.pyqtSlot()
    def exit(self):
        self.close()

    def closeEvent(self, event):
        QtWidgets.QApplication.closeAllWindows()


def sign_in_window():
    si_app = QApplication(sys.argv)
    si_window = SIWindow()
    si_window.show()
    sys.exit(si_app.exec_())
