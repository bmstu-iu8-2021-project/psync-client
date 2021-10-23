import json
import os
import sys

import requests
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QFileDialog, QApplication, QGridLayout, QTabWidget, \
    QTableWidgetItem, QTableWidget, QWidget, QAbstractItemView

from UI import ui_about, call_ui, create_menu, ui_change_password, ui_change_email
from data_processing.constants import IP, PORT, PROTOCOL
from data_processing.data_validation import check_request
from data_processing.get_folder_data import get_mac, get_files, get_json

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
import sys


class FWindow(QMainWindow):
    def __init__(self, token, login, folder, version):
        super(FWindow, self).__init__()
        self.token = token
        self.login = login
        self.folder = folder
        self.version = version

        self.setWindowTitle('SyncGad • Sign In')
        self.setGeometry(700, 400, 500, 385)
        self.setFixedSize(self.size())

        font = QtGui.QFont()
        font.setPointSize(15)

        self.name_label = QtWidgets.QLabel(self)
        self.name_label.setGeometry(10, 20, 440, 31)
        self.name_label.setFont(font)
        self.name_label.setText(f'Current user: {self.login}')

        self.add_button = QtWidgets.QPushButton(self)
        self.add_button.setGeometry(450, 75, 40, 40)
        self.add_button.setIcon(QIcon('icons/workplace/add_folder.svg'))
        self.add_button.setIconSize(QtCore.QSize(30, 30))
        self.add_button.setToolTip('Add new folder or version')
        self.add_button.clicked.connect(self.add_folder)

        self.delete_button = QtWidgets.QPushButton(self)
        self.delete_button.setGeometry(450, 125, 40, 40)
        self.delete_button.setIcon(QIcon('icons/workplace/delete_folder.svg'))
        self.delete_button.setIconSize(QtCore.QSize(30, 30))
        self.delete_button.setToolTip('Delete chosen version')
        self.delete_button.clicked.connect(self.delete_folder)

        self.update_button = QtWidgets.QPushButton(self)
        self.update_button.setGeometry(450, 175, 40, 40)
        self.update_button.setIcon(QIcon('icons/workplace/update_folder.svg'))
        self.update_button.setIconSize(QtCore.QSize(30, 30))
        self.update_button.setToolTip('Update chosen folder')
        self.update_button.clicked.connect(self.update_version)

        self.sync_button = QtWidgets.QPushButton(self)
        self.sync_button.setGeometry(450, 225, 40, 40)
        self.sync_button.setIcon(QIcon('icons/workplace/sync_folder.svg'))
        self.sync_button.setIconSize(QtCore.QSize(30, 30))
        self.sync_button.setToolTip('Synchronize chosen folder')

        # TODO: добавить иконки в кнопки, добавить вывод данных, добавить возможность добавить папку, удалить,
        #  обновить, синхронизировать. Добавить возможность смотреть содержимое папки. Добавить полный функционал

        self.tableWidget = QTableWidget(self)
        self.create_table()

        create_menu.du_menu(self)

    def create_table(self):
        columns = 2
        rows = 10
        # 430 = 300 + 60 + 70
        self.tableWidget.setGeometry(
            QtCore.QRect(10, 52, 430, self.tableWidget.verticalHeader().height() * (rows + 1) + 15))
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(columns)
        self.tableWidget.setHorizontalHeaderLabels(('File', 'Edited at'))
        self.tableWidget.setColumnWidth(0, 358)
        self.tableWidget.setColumnWidth(1, 70)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

        self.tableWidget.itemDoubleClicked.connect(self.get_files)

        self.fill_table()

    def get_files(self):
        row = self.tableWidget.currentRow()
        if not (self.tableWidget.item(row, 0) is None):
            folder = self.tableWidget.item(row, 0).text()
            version = self.tableWidget.item(row, 1).text()

    def add_folder(self):
        path_name = QFileDialog.getExistingDirectory(self, 'Choose the folder to add')
        if path_name:
            mac = get_mac()
            folder_content = get_json(get_files(path_name))
            folder_content['login'] = self.login
            folder_content['mac'] = mac
            folder_content['path_file'] = path_name

            version, flag = QInputDialog.getText(
                self,
                'Enter version name',
                'Enter a version name so that you can recognize this version.',
            )
            if flag:
                folder_content['new_version'] = version

                head = {'Content-Type': 'application/json', 'Authorization': self.token}
                # проверка, сохранены есть ли уже сохранение этой папки с этим названием версии
                request = requests.get(
                    f'{PROTOCOL}://{IP}:{PORT}/find_version/',
                    params={
                        'login': self.login,
                        'mac': mac,
                        'folder_path': path_name,
                        'version': version
                    },
                    headers=head
                )

                if check_request(request):
                    if int(request.content.decode('UTF-8')) == 1:
                        call_ui.show_warning('Conflict of versions!',
                                             'Version with this name for this folder is already exist!')
                    else:
                        # отправляем данные
                        request = requests.get(
                            f'{PROTOCOL}://{IP}:{PORT}/add_version/',
                            data=json.dumps(folder_content),
                            headers=head
                        )
                        if check_request(request):
                            self.fill_table()

    # TODO: спрашивать согласие пользователя
    def delete_folder(self):
        row = self.tableWidget.currentRow()
        if not (self.tableWidget.item(row, 0) is None):
            folder = self.tableWidget.item(row, 0).text()
            version = self.tableWidget.item(row, 1).text()

            head = {'Content-Type': 'application/json', 'Authorization': self.token}
            # удаляем данные
            request = requests.get(
                f'{PROTOCOL}://{IP}:{PORT}/delete_version/',
                params={
                    'login': self.login,
                    'mac': get_mac(),
                    'folder_path': folder,
                    'version': version,
                },
                headers=head
            )
            if check_request(request):
                self.fill_table()
        else:
            pass

    # заполнение таблицы актуальными данными (старые стираются)
    def fill_table(self):
        head = {'Content-Type': 'application/json', 'Authorization': self.token}
        # получаем файлы пользователя для конкретной папки и версии
        request = requests.get(
            f'{PROTOCOL}://{IP}:{PORT}/get_files/',
            params={
                'login': self.login,
                'mac': get_mac(),
                'folder': self.folder,
                'version': self.version
            },
            headers=head
        )
        if check_request(request):
            data = json.loads(request.content.decode('UTF-8'))

            data_count = len(data)

            self.tableWidget.setRowCount(0)
            if data_count <= 10:
                self.tableWidget.setColumnWidth(0, 298)
                self.tableWidget.setRowCount(10)
            else:
                self.tableWidget.setColumnWidth(0, 284)
                self.tableWidget.setRowCount(data_count)
            for i in range(len(data.keys())):
                key = list(data.keys())[i]
                for j in range(len(data[key])):
                    self.tableWidget.setItem(j, i, QTableWidgetItem(str(data[key][j])))

        # добавляем подсказки к ячейкам первого столбца
        for i in range(self.tableWidget.rowCount()):
            if not self.tableWidget.item(i, 0) is None:
                self.tableWidget.item(i, 0).setToolTip(self.tableWidget.item(i, 0).text())

    def choose_path(self):
        pass
        # path_name = QFileDialog.getExistingDirectory(self, 'Choose the folder')
        # self.path_lineedit.setText(path_name)

    def add_version(self):
        pass
        # path = self.path_lineedit.text()
        # if not os.path.exists(path):
        #     call_ui.show_warning('Wrong data!', 'This folder does not exist!')
        # else:
        #     mac = get_mac()
        #     folder_content = get_json(get_files(path))
        #     folder_content['login'] = self.login
        #     folder_content['mac'] = mac
        #     folder_content['path_file'] = path
        #
        #     version, flag = QInputDialog.getText(
        #         self,
        #         'Enter version name',
        #         'Enter a version name so that you can recognize this version.',
        #     )
        #     if flag:
        #         folder_content['new_version'] = version
        #
        #         head = {'Content-Type': 'application/json', 'Authorization': self.token}
        #         request = requests.get(
        #             f'{PROTOCOL}://{IP}:{PORT}/find_version/',
        #             params={
        #                 'login': self.login,
        #                 'mac': mac,
        #                 'folder_path': path,
        #                 'version': version
        #             },
        #             headers=head
        #         )
        #
        #         if check_request(request):
        #             if request.content.decode('UTF-8') == '1':
        #                 call_ui.show_warning('Conflict of versions!', 'Version with this name is already exist!')
        #             else:
        #                 request = requests.get(
        #                     f'{PROTOCOL}://{IP}:{PORT}/add_version/',
        #                     data=json.dumps(folder_content),
        #                     headers=head
        #                 )
        #                 check_request(request)

    def update_version(self):
        row = self.tableWidget.currentRow()
        if not (self.tableWidget.item(row, 0) is None):
            path = self.tableWidget.item(row, 0).text()
            old_version = self.tableWidget.item(row, 1).text()
            mac = get_mac()
            data = get_json(get_files(path))
            data['login'] = self.login
            data['mac'] = mac
            data['path_file'] = path
            data['old_version'] = old_version

            head = {'Content-Type': 'application/json', 'Authorization': self.token}
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
                if check_request(request):
                    self.fill_table()

    def synchronize(self):
        pass
        # path = self.path_lineedit.text()
        # if not os.path.exists(path):
        #     call_ui.show_warning('Wrong data!', 'This folder does not exist!')
        # else:
        #     print('exist. synchronize')

    @QtCore.pyqtSlot()
    def saved_folders(self):
        pass
        # print('saved folders')

    @QtCore.pyqtSlot()
    def change_password(self):
        pass
        # self.cp_window = ui_change_password.CPWindow(self.login, self.token)
        # self.cp_window.show()

    @QtCore.pyqtSlot()
    def change_mail(self):
        pass
        # self.ce_window = ui_change_email.CEWindow(self.login, self.token)
        # self.ce_window.show()

    @QtCore.pyqtSlot()
    def delete_account(self):
        pass
        # verify = QMessageBox()
        # verify.setWindowTitle('Delete account')
        # verify.setText('Are you sure you want to delete your account?')
        # verify.setIcon(QMessageBox.Question)
        # verify.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # verify.setDefaultButton(QMessageBox.No)
        # verify.buttonClicked.connect(self.delete_dialog_action)
        # verify.exec_()

    def delete_dialog_action(self, button):
        pass
        # if button.text() == '&Yes':
        #     count = 0
        #     head = {'Content-Type': 'application/json', 'Authorization': self.token}
        #     request = requests.get(
        #         f'{PROTOCOL}://{IP}:{PORT}/get_password/',
        #         params={'login': self.login},
        #         headers=head)
        #     password = request.content.decode('UTF-8')
        #     while count != 3:
        #         pass_input, flag = QInputDialog.getText(
        #             self,
        #             'Confirm your actions',
        #             'To delete your account, enter your password.',
        #             echo=QtWidgets.QLineEdit.Password
        #         )
        #         if flag and pass_input:
        #             count += 1
        #             if password == pass_input:
        #                 head = {'Content-Type': 'application/json', 'Authorization': self.token}
        #                 request = requests.get(
        #                     f'{PROTOCOL}://{IP}:{PORT}/delete_user/',
        #                     params={'login': self.login},
        #                     headers=head)
        #                 if request.ok:
        #                     self.close()
        #                     break
        #                 else:
        #                     call_ui.show_warning('Error!',
        #                                          f'An error occurred while communicating with the server. Error code: {request.status_code}',
        #                                          'Critical')
        #         else:
        #             break
        #     if count == 3:
        #         call_ui.show_warning('Confirmation error!', 'You have entered the wrong password too many times.')

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
