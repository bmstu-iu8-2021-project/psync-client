from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

from UI import call_ui, ui_about, ui_sign_up, create_menu, ui_workplace
from UI_functional.sign_in import auth


class SIWindow(QMainWindow):
    def __init__(self):
        super(SIWindow, self).__init__()

        self.setWindowTitle('SyncGad • Sign In')
        self.setGeometry(600, 300, 285, 160)
        self.setFixedSize(self.size())

        font = QtGui.QFont()
        font.setPointSize(10)

        self.login_lineEdit = QtWidgets.QLineEdit(self)
        self.login_lineEdit.setGeometry(10, 36, 260, 31)
        self.login_lineEdit.setFont(font)
        self.login_lineEdit.setPlaceholderText('Enter your login')

        self.password_lineEdit = QtWidgets.QLineEdit(self)
        self.password_lineEdit.setGeometry(10, 76, 260, 31)
        self.password_lineEdit.setFont(font)
        self.password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_lineEdit.setPlaceholderText('Enter your password')

        self.enter_Button = QtWidgets.QPushButton(self)
        self.enter_Button.setGeometry(10, 116, 140, 30)
        self.enter_Button.setText('Sign in')
        self.enter_Button.clicked.connect(self.enter)

        self.registration_Button = QtWidgets.QPushButton(self)
        self.registration_Button.setGeometry(160, 116, 110, 30)
        self.registration_Button.setText('Sign up')
        self.registration_Button.clicked.connect(self.register)

        create_menu.un_menu(self)

    def enter(self):
        login = self.login_lineEdit.text()
        password = self.password_lineEdit.text()
        if login and password:
            token = auth(login, password)
            if token is not None:
                self.password_lineEdit.setText('')
                self.p_window = ui_workplace.WPWindow(login, token, self)
                self.p_window.show()
                self.hide()
        else:
            call_ui.show_dialog('Wrong data!', 'The entered login or password is incorrect.')
        self.password_lineEdit.setText('')

    def register(self):
        self.login_lineEdit.setText('')
        self.password_lineEdit.setText('')
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
