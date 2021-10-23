import json
import os

import requests
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QFileDialog

from UI import ui_about, call_ui, create_menu, ui_change_password, ui_change_email
from data_processing.constants import IP, PORT, PROTOCOL
from data_processing.data_validation import check_request
from data_processing.get_folder_data import get_mac, get_files, get_json


class PWindow(QMainWindow):
    def __init__(self, token, siw, login):
        super(PWindow, self).__init__()
        self.token = token
        self.siw = siw
        self.login = login

        self.setWindowTitle('SyncGad • Sign In')
        self.setGeometry(600, 300, 550, 115)
        self.setFixedSize(self.size())

        font = QtGui.QFont()
        font.setPointSize(10)

        self.path_lineedit = QtWidgets.QLineEdit(self)
        self.path_lineedit.setGeometry(10, 36, 430, 31)
        self.path_lineedit.setFont(font)
        self.path_lineedit.setPlaceholderText('Enter path of directory you want to synchronize')

        self.choose_button = QtWidgets.QPushButton(self)
        self.choose_button.setGeometry(450, 36, 95, 31)
        self.choose_button.setText('Choose')
        self.choose_button.clicked.connect(self.choose_path)

        self.add_button = QtWidgets.QPushButton(self)
        self.add_button.setGeometry(10, 76, 130, 31)
        self.add_button.setText('Add new version')
        self.add_button.clicked.connect(self.add_version)

        self.update_button = QtWidgets.QPushButton(self)
        self.update_button.setGeometry(150, 76, 190, 31)
        self.update_button.setText('Update excitable version')
        self.update_button.clicked.connect(self.update_version)

        self.sync_button = QtWidgets.QPushButton(self)
        self.sync_button.setGeometry(350, 76, 90, 31)
        self.sync_button.setText('Synchronize')
        self.sync_button.clicked.connect(self.synchronize)

        create_menu.du_menu(self)

    def choose_path(self):
        path_name = QFileDialog.getExistingDirectory(self, 'Choose the folder')
        self.path_lineedit.setText(path_name)

    # def add_version(self):
    #     path = self.path_lineedit.text()
    #     if not os.path.exists(path):
    #         call_ui.show_warning('Wrong data!', 'This folder does not exist!')
    #     else:
    #         mac = get_mac()
    #         folder_content = get_json(get_files(path))
    #         folder_content['login'] = self.login
    #         folder_content['mac'] = mac
    #         folder_content['path_file'] = path
    #
    #         version, flag = QInputDialog.getText(
    #             self,
    #             'Enter version name',
    #             'Enter a version name so that you can recognize this version.',
    #         )
    #         if flag:
    #             folder_content['new_version'] = version
    #
    #             head = {'Content-Type': 'application/json', 'Authorization': self.token}
    #             request = requests.get(
    #                 f'{PROTOCOL}://{IP}:{PORT}/find_version/',
    #                 params={
    #                     'login': self.login,
    #                     'mac': mac,
    #                     'folder_path': path,
    #                     'version': version
    #                 },
    #                 headers=head
    #             )
    #
    #             if check_request(request):
    #                 if request.content.decode('UTF-8') == '1':
    #                     call_ui.show_warning('Conflict of versions!', 'Version with this name is already exist!')
    #                 else:
    #                     request = requests.get(
    #                         f'{PROTOCOL}://{IP}:{PORT}/add_version/',
    #                         data=json.dumps(folder_content),
    #                         headers=head
    #                     )
    #                     check_request(request)

    def update_version(self):
        path = self.path_lineedit.text()
        if not os.path.exists(path):
            call_ui.show_warning('Wrong data!', 'This folder does not exist!')
        else:
            mac = get_mac()
            data = get_json(get_files(path))
            data['login'] = self.login
            data['mac'] = mac
            data['path_file'] = path
            old_version, flag = QInputDialog.getText(
                self,
                'Enter version name',
                'Enter the name of the version you want to update.',
            )
            if flag:
                data['old_version'] = old_version

                head = {'Content-Type': 'application/json', 'Authorization': self.token}
                request = requests.get(
                    f'{PROTOCOL}://{IP}:{PORT}/find_version/',
                    params={
                        'login': self.login,
                        'mac': mac,
                        'folder_path': path,
                        'version': old_version
                    },
                    headers=head
                )
                if check_request(request):
                    if request.content.decode('UTF-8') == '0':
                        call_ui.show_warning('Wrong data!', 'No version with this name!')
                    else:
                        data['new_version'] = old_version
                        new_version, flag = QInputDialog.getText(
                            self,
                            'Enter version name',
                            'Enter a new version name',
                        )
                        if flag:
                            data['new_version'] = new_version

                            request = requests.get(
                                f'{PROTOCOL}://{IP}:{PORT}/update_version/',
                                data=json.dumps(data),
                                headers=head
                            )
                            check_request(request)

    def synchronize(self):
        path = self.path_lineedit.text()
        if not os.path.exists(path):
            call_ui.show_warning('Wrong data!', 'This folder does not exist!')
        else:
            print('exist. synchronize')

    @QtCore.pyqtSlot()
    def saved_folders(self):
        print('saved folders')

    @QtCore.pyqtSlot()
    def change_password(self):
        self.cp_window = ui_change_password.CPWindow(self.login, self.token)
        self.cp_window.show()

    @QtCore.pyqtSlot()
    def change_mail(self):
        self.ce_window = ui_change_email.CEWindow(self.login, self.token)
        self.ce_window.show()

    @QtCore.pyqtSlot()
    def delete_account(self):
        verify = QMessageBox()
        verify.setWindowTitle('Delete account')
        verify.setText('Are you sure you want to delete your account?')
        verify.setIcon(QMessageBox.Question)
        verify.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        verify.setDefaultButton(QMessageBox.No)
        verify.buttonClicked.connect(self.delete_dialog_action)
        verify.exec_()

    def delete_dialog_action(self, button):
        if button.text() == '&Yes':
            count = 0
            head = {'Content-Type': 'application/json', 'Authorization': self.token}
            request = requests.get(
                f'{PROTOCOL}://{IP}:{PORT}/get_password/',
                params={'login': self.login},
                headers=head)
            password = request.content.decode('UTF-8')
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
                        head = {'Content-Type': 'application/json', 'Authorization': self.token}
                        request = requests.get(
                            f'{PROTOCOL}://{IP}:{PORT}/delete_user/',
                            params={'login': self.login},
                            headers=head)
                        if request.ok:
                            self.close()
                            break
                        else:
                            call_ui.show_warning('Error!',
                                                 f'An error occurred while communicating with the server. Error code: {request.status_code}',
                                                 'Critical')
                else:
                    break
            if count == 3:
                call_ui.show_warning('Confirmation error!', 'You have entered the wrong password too many times.')

    # def update_dialog_action(self, button):
    #     if button.text == '&No':
    #         pass
    #     if button.text == '&Yes':
    #         self.update_version()

    @QtCore.pyqtSlot()
    def exit_profile(self):
        self.close()

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
