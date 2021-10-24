from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow

from UI_functional.change_perosnal_data import change_password
from UI.call_ui import show_warning


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
                show_warning('Wrong data!', 'You entered different passwords')
            # head = {'Content-Type': 'application/json', 'Authorization': self.token}
            # request = requests.get(
            #     f'{PROTOCOL}://{IP}:{PORT}/get_password/',
            #     params={'login': self.login},
            #     headers=head)
            # if data_validation.check_request(request):
            #     if bcrypt.checkpw(self.old_password_LineEdit.text().encode('UTF-8'), request.content):
            #         if self.new_password_LineEdit.text() == self.repeat_password_LineEdit.text():
            #             check = data_validation.is_password_valid(self.new_password_LineEdit.text())
            #             if check[0]:
            #                 head = {'Content-Type': 'application/json', 'Authorization': self.token}
            #                 request = requests.get(
            #                     f'{PROTOCOL}://{IP}:{PORT}/change_password/',
            #                     params={
            #                         'login': self.login,
            #                         'password': bcrypt.hashpw(self.new_password_LineEdit.text().encode('UTF-8'),
            #                                                   bcrypt.gensalt(rounds=5))
            #                     },
            #                     headers=head)
            #                 if not data_validation.check_request(request):
            #                     pass
            #                 else:
            #                     self.close()
            #             else:
            #                 call_ui.show_warning('Wrong data!', check[1])
            #         else:
            #             call_ui.show_warning('Wrong data!', 'You entered different passwords')
            #     else:
            #         call_ui.show_warning('Wrong data!', 'You entered wrong password!')
