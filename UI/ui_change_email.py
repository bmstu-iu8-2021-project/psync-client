import requests
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow

from UI import call_ui
from data_processing import data_validation
from data_processing.constants import IP, PORT, PROTOCOL


class CEWindow(QMainWindow):
    def __init__(self, login, token):
        super(CEWindow, self).__init__()
        self.login = login
        self.token = token

        self.setWindowTitle('Change email')
        self.setGeometry(600, 300, 280, 129)
        self.setFixedSize(self.size())

        font = QtGui.QFont()
        font.setPointSize(10)

        self.password_LineEdit = QtWidgets.QLineEdit(self)
        self.password_LineEdit.setGeometry(10, 10, 260, 31)
        self.password_LineEdit.setFont(font)
        self.password_LineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_LineEdit.setPlaceholderText('Enter your password')

        self.new_email_LineEdit = QtWidgets.QLineEdit(self)
        self.new_email_LineEdit.setGeometry(10, 50, 260, 31)
        self.new_email_LineEdit.setFont(font)
        self.new_email_LineEdit.setPlaceholderText('Enter your new email')

        self.accept_button = QtWidgets.QPushButton(self)
        self.accept_button.setGeometry(180, 90, 90, 28)
        self.accept_button.setText("Accept")
        self.accept_button.clicked.connect(self.accept)

    def accept(self):
        if self.password_LineEdit.text() and self.new_email_LineEdit.text():
            head = {'Content-Type': 'application/json', 'Authorization': self.token}
            request = requests.get(
                f'{PROTOCOL}://{IP}:{PORT}/get_password/',
                params={'login': self.login},
                headers=head)
            if request.ok:
                if self.password_LineEdit.text() == request.content.decode('UTF-8'):
                    check = data_validation.is_mail_valid(self.new_email_LineEdit.text())
                    if check[0]:
                        head = {'Content-Type': 'application/json', 'Authorization': self.token}
                        request = requests.get(
                            f'{PROTOCOL}://{IP}:{PORT}/change_mail/',
                            params={'login': self.login, 'email': self.new_email_LineEdit.text()},
                            headers=head)
                        if not request.ok:
                            call_ui.show_warning('Error!',
                                                 f'An error occurred while communicating with the server. Error code: {request.status_code}',
                                                 'Critical')
                        else:
                            self.close()
                    else:
                        call_ui.show_warning('Wrong data!', check[1])
                else:
                    call_ui.show_warning('Wrong data!', 'You entered wrong password!')
            else:
                call_ui.show_warning('Error!',
                                     f'An error occurred while communicating with the server. Error code: {request.status_code}',
                                     'Critical')
