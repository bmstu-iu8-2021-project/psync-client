from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QFileDialog
from databases import db_action
from UI import ui_about, call_ui, create_menu, ui_change_password
from connection import mailing
import os


class PWindow(QMainWindow):
    def __init__(self, conn, siw, login):
        super(PWindow, self).__init__()
        self.conn = conn
        self.siw = siw
        self.login = login

        self.setWindowTitle('SyncGad • Sign In')
        self.setGeometry(600, 300, 550, 220)
        self.setFixedSize(self.size())

        font = QtGui.QFont()
        font.setPointSize(10)

        self.path_lineedit = QtWidgets.QLineEdit(self)
        self.path_lineedit.setGeometry(10, 36, 425, 31)
        self.path_lineedit.setFont(font)
        self.path_lineedit.setPlaceholderText('Enter path of directory you want to synchronize')

        self.choose_button = QtWidgets.QPushButton(self)
        self.choose_button.setGeometry(QtCore.QRect(445, 36, 95, 31))
        self.choose_button.setText('Choose')
        self.choose_button.clicked.connect(self.choose_path)

        self.login_lineedit = QtWidgets.QLineEdit(self)
        self.login_lineedit.setGeometry(10, 76, 271, 31)
        self.login_lineedit.setFont(font)
        self.login_lineedit.setPlaceholderText('Enter login of the second account')

        self.version_checkbox = QtWidgets.QCheckBox(self)
        self.version_checkbox.setGeometry(10, 116, 351, 20)
        self.version_checkbox.setText('Choose an older file between files with the same name')

        self.backup_checkbox = QtWidgets.QCheckBox(self)
        self.backup_checkbox.setGeometry(10, 146, 231, 20)
        self.backup_checkbox.setText('Save a backup copy of existing files')
        self.backup_checkbox.setChecked(True)

        self.sync_button = QtWidgets.QPushButton(self)
        self.sync_button.setGeometry(10, 176, 93, 31)
        self.sync_button.setText('Synchronize')
        self.sync_button.clicked.connect(self.synchronize)

        create_menu.du_menu(self)

    @QtCore.pyqtSlot()
    def exit_profile(self):
        self.close()

    @QtCore.pyqtSlot()
    def delete_account(self):
        verify = QMessageBox()
        verify.setWindowTitle('Delete account')
        verify.setText('Are you sure you want to delete your account?')
        verify.setIcon(QMessageBox.Question)
        verify.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        verify.setDefaultButton(QMessageBox.No)
        verify.buttonClicked.connect(self.dialog_action)
        verify.exec_()

    def dialog_action(self, button):
        if button.text() == '&Yes':
            count = 0
            password = db_action.get_password(self.conn, self.login)
            while count != 3:
                pass_input, flag = QInputDialog.getText(
                    self,
                    'Confirm your actions',
                    'To delete your account, enter your password.',
                    echo=QtWidgets.QLineEdit.Password
                )
                if flag and pass_input:
                    count += 1
                    if password == pass_input:
                        db_action.delete_user(self.conn, self.login)
                        self.close()
                        break
                else:
                    break
            if count == 3:
                call_ui.show_warning('Confirmation error!', 'You have entered the wrong password too many times.')

    @QtCore.pyqtSlot()
    def change_mail(self):
        new_mail, flag_mail = QInputDialog.getText(
            self,
            'Change mail',
            'Enter new mail address',
        )
        if flag_mail and new_mail:
            if not db_action.find_record(self.conn, new_mail, mode=1):
                code = mailing.send_mail(
                    new_mail,
                    'Verify code',
                    'Hello, %s!\nThis is a verification code to confirm the mail: %s' % tuple([self.login, '%s']),
                    True
                )
                count = 0
                while count != 3:
                    code_input, flag = QInputDialog.getText(
                        self,
                        'Verification code',
                        'A verification code was sent to confirm \n'
                        'the new email address. Enter it below.'
                    )
                    if flag and code_input:
                        count += 1
                        if code_input == code:
                            db_action.change_mail(self.conn, self.login, new_mail)
                            break
                if count == 3:
                    call_ui.show_warning('Verification error!', 'You have entered the wrong code too many times.')
                    self.close()
            else:
                call_ui.show_warning('Denied', 'This mail address is already taken.')

    @QtCore.pyqtSlot()
    def change_password(self):
        self.cp_window = ui_change_password.CPWindow(self.conn, self.login)
        self.cp_window.show()

    @QtCore.pyqtSlot()
    def about(self):
        self.a_window = ui_about.AWindow()
        self.a_window.show()

    @QtCore.pyqtSlot()
    def exit(self):
        self.close()
        self.siw.close()

    def choose_path(self):
        path_name = QFileDialog.getExistingDirectory(self, 'Choose the folder')
        self.path_lineedit.setText(path_name)

    def synchronize(self):
        path = self.path_lineedit.text()
        if not os.path.exists(path):
            call_ui.show_warning('Wrong data!', 'This folder does not exist!')
        else:
            print('good')

    def closeEvent(self, event):
        self.siw.show()
