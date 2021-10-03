from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QInputDialog
from data_processing import data_validation
from databases import db_action
from connection import mailing
from UI import call_ui, ui_about, ui_profile, create_menu


class SUWindow(QMainWindow):
    def __init__(self, conn, siw):
        super(SUWindow, self).__init__()
        self.conn = conn
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
        self.login_LineEdit.textChanged.connect(self.login_valid)

        self.mail_LineEdit = QtWidgets.QLineEdit(self)
        self.mail_LineEdit.setGeometry(10, 76, 260, 31)
        self.mail_LineEdit.setFont(font)
        self.mail_LineEdit.setPlaceholderText('Enter your mail')
        self.mail_LineEdit.textChanged.connect(self.mail_valid)

        self.password_LineEdit = QtWidgets.QLineEdit(self)
        self.password_LineEdit.setGeometry(10, 116, 260, 31)
        self.password_LineEdit.setFont(font)
        self.password_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_LineEdit.setPlaceholderText('Enter your password')
        self.password_LineEdit.textChanged.connect(self.password_valid)

        self.pasrep_LineEdit = QtWidgets.QLineEdit(self)
        self.pasrep_LineEdit.setGeometry(10, 156, 260, 31)
        self.pasrep_LineEdit.setFont(font)
        self.pasrep_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pasrep_LineEdit.setPlaceholderText('Repeat your password')
        self.pasrep_LineEdit.textChanged.connect(self.password_same)

        self.signup_button = QtWidgets.QPushButton(self)
        self.signup_button.setGeometry(180, 196, 90, 28)
        self.signup_button.setText("Sign up")
        self.signup_button.clicked.connect(self.accept)

        font.setBold(True)
        font.setPointSize(8)

        self.login_lable = QtWidgets.QLabel(self)
        self.login_lable.setGeometry(280, 35, 0, 0)
        self.login_lable.setFont(font)
        self.login_lable.setStyleSheet("color: rgb(255, 0, 0);")
        self.login_lable.setWordWrap(True)
        self.login_lable.hide()

        self.mail_lable = QtWidgets.QLabel(self)
        self.mail_lable.setGeometry(280, 75, 0, 0)  # -7 on y
        self.mail_lable.setFont(font)
        self.mail_lable.setStyleSheet("color: rgb(255, 0, 0);")
        self.mail_lable.setWordWrap(True)
        self.mail_lable.hide()

        self.password_lable = QtWidgets.QLabel(self)
        self.password_lable.setGeometry(280, 115, 0, 0)
        self.password_lable.setFont(font)
        self.password_lable.setStyleSheet("color: rgb(255, 0, 0);")
        self.password_lable.setWordWrap(True)
        self.password_lable.hide()

        self.pasrep_lable = QtWidgets.QLabel(self)
        self.pasrep_lable.setGeometry(280, 155, 0, 0)
        self.pasrep_lable.setFont(font)
        self.pasrep_lable.setStyleSheet("color: rgb(255, 0, 0);")
        self.pasrep_lable.setWordWrap(True)
        self.pasrep_lable.hide()

        create_menu.un_menu(self)

    @QtCore.pyqtSlot()
    def about(self):
        self.a_window = ui_about.AWindow()
        self.a_window.show()

    @QtCore.pyqtSlot()
    def exit(self):
        self.close()
        self.siw.close()

    def login_valid(self):
        flag, text = data_validation.is_login_valid(self.login_LineEdit.text())
        if not flag and self.login_LineEdit.text():
            self.setFixedWidth(440)
            self.login_lable.setText(text)
            self.login_lable.adjustSize()
            self.login_lable.show()
        else:
            self.login_lable.hide()
            if not (self.mail_lable.isVisible() or self.password_lable.isVisible() or self.pasrep_lable.isVisible()):
                self.setFixedWidth(280)

    def mail_valid(self):
        flag, text = data_validation.is_mail_valid(self.mail_LineEdit.text())
        if flag or not self.mail_LineEdit.text():
            self.mail_lable.hide()
            if not (self.login_lable.isVisible() or self.password_lable.isVisible() or self.pasrep_lable.isVisible()):
                self.setFixedWidth(280)
        else:
            self.setFixedWidth(440)
            self.mail_lable.setText(text)
            self.mail_lable.adjustSize()
            self.mail_lable.show()

    def password_valid(self):
        flag, text = data_validation.is_password_valid(self.password_LineEdit.text())
        if flag or not self.password_LineEdit.text():
            self.password_lable.hide()
            if not (self.login_lable.isVisible() or self.mail_lable.isVisible() or self.password_lable.isVisible()):
                self.setFixedWidth(280)
        else:
            self.setFixedWidth(440)
            self.password_lable.setText(text)
            self.password_lable.adjustSize()
            self.password_lable.show()
        if self.pasrep_LineEdit.text() != '':
            self.password_same()

    def password_same(self):
        if self.password_LineEdit.text() and self.password_LineEdit.text() == self.pasrep_LineEdit.text():
            self.pasrep_lable.hide()
            if not (self.login_lable.isVisible() or self.mail_lable.isVisible() or self.password_lable.isVisible()):
                self.setFixedWidth(280)
        else:
            self.setFixedWidth(440)
            self.pasrep_lable.setText('Entered passwords do not match')
            self.pasrep_lable.adjustSize()
            self.pasrep_lable.show()

    def accept(self):
        if self.width() == 280:
            reg_data = (
                self.login_LineEdit.text(),
                self.mail_LineEdit.text(),
                self.password_LineEdit.text()
            )
            request = db_action.check(self.conn, reg_data)

            if request[0]:
                code = mailing.send_mail(
                    reg_data[1],
                    'Verify code',
                    'Hello, %s!\nThis is a verification code to confirm the mail: %s' % tuple([reg_data[0], '%s']),
                    True
                )
                count = 0
                while count != 3:
                    code_input, flag = QInputDialog.getText(
                        self,
                        'Verification code',
                        'The verification code has been sent to the \n'
                        'specified mail. To complete the registration, \n'
                        'enter it in the field below.'
                    )
                    if flag and code_input:
                        count += 1
                        if code_input == code:
                            db_action.add_user(self.conn, reg_data)
                            self.p_window = ui_profile.PWindow(self.conn, self.siw, reg_data[0])
                            self.p_window.show()
                            self.hide()
                            break
                if count == 4:
                    call_ui.show_warning('Verification error!', 'You have entered the wrong code too many times.')
                    self.close()
            else:
                call_ui.show_warning('Wrong data!', request[1])
        else:
            call_ui.show_warning('Wrong data!', 'Check the correctness of the data you entered.')

    def closeEvent(self, event):
        self.siw.show()
