from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow

from UI import ui_about, create_menu, ui_workplace
from UI.call_ui import show_dialog
from data_processing import data_validation
from UI_functional.sign_up import register


class SUWindow(QMainWindow):
    def __init__(self, siw):
        super(SUWindow, self).__init__()
        self.siw = siw

        self.setWindowTitle('SyncGad • Sign Up')
        self.setGeometry(600, 300, 280, 235)
        self.setFixedSize(self.size())

        font = QtGui.QFont()
        font.setPointSize(10)

        self.login_LineEdit = QtWidgets.QLineEdit(self)
        self.login_LineEdit.setGeometry(10, 36, 260, 31)
        self.login_LineEdit.setFont(font)
        self.login_LineEdit.setPlaceholderText('Enter your login')
        self.login_LineEdit.textChanged.connect(self.is_login_valid)

        self.mail_LineEdit = QtWidgets.QLineEdit(self)
        self.mail_LineEdit.setGeometry(10, 76, 260, 31)
        self.mail_LineEdit.setFont(font)
        self.mail_LineEdit.setPlaceholderText('Enter your mail')
        self.mail_LineEdit.textChanged.connect(self.is_mail_valid)

        self.password_LineEdit = QtWidgets.QLineEdit(self)
        self.password_LineEdit.setGeometry(10, 116, 260, 31)
        self.password_LineEdit.setFont(font)
        self.password_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_LineEdit.setPlaceholderText('Enter your password')
        self.password_LineEdit.textChanged.connect(self.is_password_valid)

        self.pasrep_LineEdit = QtWidgets.QLineEdit(self)
        self.pasrep_LineEdit.setGeometry(10, 156, 260, 31)
        self.pasrep_LineEdit.setFont(font)
        self.pasrep_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pasrep_LineEdit.setPlaceholderText('Repeat your password')
        self.pasrep_LineEdit.textChanged.connect(self.are_passwords_same)

        self.signup_Button = QtWidgets.QPushButton(self)
        self.signup_Button.setGeometry(180, 196, 90, 28)
        self.signup_Button.setText("Sign up")
        self.signup_Button.clicked.connect(self.accept)

        font.setBold(True)
        font.setPointSize(8)

        self.login_Label = QtWidgets.QLabel(self)
        self.login_Label.setGeometry(280, 35, 0, 0)
        self.login_Label.setFont(font)
        self.login_Label.setStyleSheet("color: rgb(255, 0, 0);")
        self.login_Label.setWordWrap(True)
        self.login_Label.hide()

        self.mail_Label = QtWidgets.QLabel(self)
        self.mail_Label.setGeometry(280, 75, 0, 0)
        self.mail_Label.setFont(font)
        self.mail_Label.setStyleSheet("color: rgb(255, 0, 0);")
        self.mail_Label.setWordWrap(True)
        self.mail_Label.hide()

        self.password_Label = QtWidgets.QLabel(self)
        self.password_Label.setGeometry(280, 115, 0, 0)
        self.password_Label.setFont(font)
        self.password_Label.setStyleSheet("color: rgb(255, 0, 0);")
        self.password_Label.setWordWrap(True)
        self.password_Label.hide()

        self.pasrep_Label = QtWidgets.QLabel(self)
        self.pasrep_Label.setGeometry(280, 155, 0, 0)
        self.pasrep_Label.setFont(font)
        self.pasrep_Label.setStyleSheet("color: rgb(255, 0, 0);")
        self.pasrep_Label.setWordWrap(True)
        self.pasrep_Label.hide()

        create_menu.un_menu(self)

    def is_login_valid(self):
        flag, text = data_validation.is_login_valid(self.login_LineEdit.text())
        if not flag and self.login_LineEdit.text():
            self.setFixedWidth(440)
            self.login_Label.setText(text)
            self.login_Label.adjustSize()
            self.login_Label.show()
        else:
            self.login_Label.hide()
            self.fix_size()

    def is_mail_valid(self):
        flag, text = data_validation.is_mail_valid(self.mail_LineEdit.text())
        if flag or not self.mail_LineEdit.text():
            self.mail_Label.hide()
            self.fix_size()
        else:
            self.setFixedWidth(440)
            self.mail_Label.setText(text)
            self.mail_Label.adjustSize()
            self.mail_Label.show()

    def is_password_valid(self):
        flag, text = data_validation.is_password_valid(self.password_LineEdit.text())
        if flag or not self.password_LineEdit.text():
            self.password_Label.hide()
            self.fix_size()
        else:
            self.setFixedWidth(440)
            self.password_Label.setText(text)
            self.password_Label.adjustSize()
            self.password_Label.show()
        if self.pasrep_LineEdit.text() != '':
            self.are_passwords_same()

    def are_passwords_same(self):
        if self.password_LineEdit.text() and self.password_LineEdit.text() == self.pasrep_LineEdit.text():
            self.pasrep_Label.hide()
            self.fix_size()
        else:
            self.setFixedWidth(440)
            self.pasrep_Label.setText('Entered passwords do not match')
            self.pasrep_Label.adjustSize()
            self.pasrep_Label.show()

    def fix_size(self):
        if not (self.mail_Label.isVisible() or
                self.password_Label.isVisible() or
                self.pasrep_Label.isVisible() or
                self.login_Label.isVisible()):
            self.setFixedWidth(280)

    def accept(self):
        if self.width() == 280:
            token = register(
                login=self.login_LineEdit.text(),
                mail=self.mail_LineEdit.text(),
                password=self.password_LineEdit.text()
            )
            if token:
                self.p_window = ui_workplace.WPWindow(self.login_LineEdit.text(), token, self.siw)
                self.p_window.show()
                self.hide()
        else:
            show_dialog('Wrong data!', 'Check the correctness of the data you entered.')

    @QtCore.pyqtSlot()
    def about(self):
        self.a_window = ui_about.AWindow()
        self.a_window.show()

    @QtCore.pyqtSlot()
    def exit(self):
        self.close()
        self.siw.close()

    def closeEvent(self, event):
        QtWidgets.QApplication.closeAllWindows()
        self.siw.show()
