from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QFileDialog, QAbstractItemView, QTableWidget, \
    QTableWidgetItem
from PyQt5.QtGui import QIcon

from UI import ui_about, create_menu, ui_change_password, ui_change_email
from UI_functional.workplace import add_folder, update_folder, delete_version, delete_user, get_folders


class WPWindow(QMainWindow):
    def __init__(self, token, siw, login):
        super(WPWindow, self).__init__()
        self.token = token
        self.siw = siw
        self.login = login

        self.setWindowTitle('SyncGad • Sign In')
        self.setGeometry(600, 300, 580, 385)
        self.setFixedSize(self.size())

        font = QtGui.QFont()
        font.setPointSize(15)

        self.name_Label = QtWidgets.QLabel(self)
        self.name_Label.setGeometry(10, 20, 440, 31)
        self.name_Label.setFont(font)
        self.name_Label.setText(f'Current user: {self.login}')

        self.add_Button = QtWidgets.QPushButton(self)
        self.add_Button.setGeometry(530, 75, 40, 40)
        self.add_Button.setIcon(QIcon('icons/workplace/add_folder.svg'))
        self.add_Button.setIconSize(QtCore.QSize(30, 30))
        self.add_Button.setToolTip('Add new folder or version')
        self.add_Button.clicked.connect(self.add_folder)

        self.delete_Button = QtWidgets.QPushButton(self)
        self.delete_Button.setGeometry(530, 125, 40, 40)
        self.delete_Button.setIcon(QIcon('icons/workplace/delete_folder.svg'))
        self.delete_Button.setIconSize(QtCore.QSize(30, 30))
        self.delete_Button.setToolTip('Delete chosen version')
        self.delete_Button.clicked.connect(self.delete_version)

        self.update_Button = QtWidgets.QPushButton(self)
        self.update_Button.setGeometry(530, 175, 40, 40)
        self.update_Button.setIcon(QIcon('icons/workplace/update_folder.svg'))
        self.update_Button.setIconSize(QtCore.QSize(30, 30))
        self.update_Button.setToolTip('Update chosen folder')
        self.update_Button.clicked.connect(self.update_version)

        self.sync_Button = QtWidgets.QPushButton(self)
        self.sync_Button.setGeometry(530, 225, 40, 40)
        self.sync_Button.setIcon(QIcon('icons/workplace/sync_folder.svg'))
        self.sync_Button.setIconSize(QtCore.QSize(30, 30))
        self.sync_Button.setToolTip('Synchronize chosen folder')

        self.folders_tableWidget = QTableWidget(self)
        self.create_table()

        create_menu.du_menu(self)

    def create_table(self):
        columns = 3
        rows = 10
        # 510 = 280 + 60 + 170
        self.folders_tableWidget.setGeometry(
            QtCore.QRect(10, 52, 510, self.folders_tableWidget.verticalHeader().height() * (rows + 1) + 15))
        self.folders_tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.folders_tableWidget.setRowCount(rows)
        self.folders_tableWidget.setColumnCount(columns)
        self.folders_tableWidget.setHorizontalHeaderLabels(('Folder', 'Version', 'Edited at'))
        self.folders_tableWidget.setColumnWidth(0, 278)
        self.folders_tableWidget.setColumnWidth(1, 60)
        self.folders_tableWidget.setColumnWidth(2, 170)

        self.folders_tableWidget.verticalHeader().setVisible(False)
        self.folders_tableWidget.horizontalHeader().setHighlightSections(False)
        self.folders_tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.folders_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.folders_tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.folders_tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.folders_tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

        self.fill_table()

    # def get_files(self):
    #     row = self.folders_tableWidget.currentRow()
    #     if not (self.folders_tableWidget.item(row, 0) is None):
    #         folder = self.folders_tableWidget.item(row, 0).text()
    #         version = self.folders_tableWidget.item(row, 1).text()
    #         self.f_window = ui_files.FWindow(self.token, self.login, folder, version)
    #         self.f_window.show()

    def add_folder(self):
        path_name = QFileDialog.getExistingDirectory(self, 'Choose the folder to add')
        if path_name:
            version, flag = QInputDialog.getText(
                self,
                'Enter version name',
                'Enter a version name so that you can recognize this version.',
            )
            if flag:
                if add_folder(
                        login=self.login,
                        path=path_name,
                        version=version,
                        token=self.token
                ):
                    self.fill_table()

            # mac = get_mac()
            # folder_content = get_json(get_files(path_name))
            # folder_content['login'] = self.login
            # folder_content['mac'] = mac
            # folder_content['path_file'] = path_name
            #
            # version, flag = QInputDialog.getText(
            #     self,
            #     'Enter version name',
            #     'Enter a version name so that you can recognize this version.',
            # )
            # if flag:
            #     folder_content['new_version'] = version
            #
            #     head = {'Content-Type': 'application/json', 'Authorization': self.token}
            #
            #     # проверка, сохранены есть ли уже сохранение этой папки с этим названием версии
            #     request = requests.get(
            #         f'{PROTOCOL}://{IP}:{PORT}/find_version/',
            #         params={
            #             'login': self.login,
            #             'mac': mac,
            #             'folder_path': path_name,
            #             'version': version
            #         },
            #         headers=head
            #     )
            #
            #     if check_request(request):
            #         if request.content.decode('UTF-8') == 'False':
            #             call_ui.show_warning('Conflict of versions!',
            #                                  'Version with this name for this folder is already exist!')
            #         else:
            #             # создаем архив
            #             zip_name = '_'.join([self.login, path_name[path_name.rfind('/') + 1:], version]) + '.zip'
            #             zip_folder = zipfile.ZipFile(zip_name, 'w')
            #             for root, dirs, files in os.walk(path_name):
            #                 for file in files:
            #                     zip_folder.write(os.path.join(root, file))
            #             zip_folder.close()
            #
            #             # отправляем архив
            #             request = requests.get(
            #                 f'{PROTOCOL}://{IP}:{PORT}/send_folder/',
            #                 files={
            #                     'file': (zip_name, open(zip_name, 'rb'))
            #                 },
            #                 headers={'Authorization': self.token},
            #             )
            #
            #             if check_request(request):
            #                 # удаляем архив
            #                 os.remove(zip_name)
            #
            #                 # отправляем данные в бд
            #                 request = requests.get(
            #                     f'{PROTOCOL}://{IP}:{PORT}/add_version/',
            #                     data=json.dumps(folder_content),
            #                     headers=head,
            #                 )
            #
            #                 if check_request(request):
            #                     self.fill_table()

    def delete_version(self):
        row = self.folders_tableWidget.currentRow()
        if not (self.folders_tableWidget.item(row, 0) is None):
            if delete_version(
                login=self.login,
                path=self.folders_tableWidget.item(row, 0).text(),
                version=self.folders_tableWidget.item(row, 1).text(),
                token=self.token
            ):
                self.fill_table()
        #     folder = self.folders_tableWidget.item(row, 0).text()
        #     version = self.folders_tableWidget.item(row, 1).text()
        #
        #     head = {'Content-Type': 'application/json', 'Authorization': self.token}
        #     # удаляем данные
        #     request = requests.get(
        #         f'{PROTOCOL}://{IP}:{PORT}/delete_version/',
        #         params={
        #             'login': self.login,
        #             'mac': get_mac(),
        #             'folder_path': folder,
        #             'version': version,
        #         },
        #         headers=head
        #     )
        #     if check_request(request):
        #         self.fill_table()
        # else:
        #     pass

    # заполнение таблицы актуальными данными (старые стираются)
    def fill_table(self):
        self.folders_tableWidget.setRowCount(10)
        # head = {'Content-Type': 'application/json', 'Authorization': self.token}
        # # получаем данные о папках этого пользователя, этого устройства
        # request = requests.get(
        #     f'{PROTOCOL}://{IP}:{PORT}/get_folders/',
        #     params={
        #         'login': self.login,
        #         'mac': get_mac(),
        #     },
        #     headers=head
        # )
        # if check_request(request):
        #     data = json.loads(request.content.decode('UTF-8'))
        
        data = get_folders(login=self.login, token=self.token)
        if not (data is None):
            data_count = len(data)
            self.folders_tableWidget.setRowCount(0)
            if data_count <= 10:
                # self.folders_tableWidget.setColumnWidth(0, 298)
                self.folders_tableWidget.setRowCount(10)
            else:
                # self.folders_tableWidget.setColumnWidth(0, 284)
                self.folders_tableWidget.setRowCount(data_count)
            for i in range(len(data.keys())):
                key = list(data.keys())[i]
                for j in range(len(data[key])):
                    self.folders_tableWidget.setItem(j, i, QTableWidgetItem(str(data[key][j])))

        # добавляем подсказки к ячейкам первого столбца
        for i in range(self.folders_tableWidget.rowCount()):
            if not self.folders_tableWidget.item(i, 0) is None:
                self.folders_tableWidget.item(i, 0).setToolTip(self.folders_tableWidget.item(i, 0).text())

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
        row = self.folders_tableWidget.currentRow()
        if not (self.folders_tableWidget.item(row, 0) is None):
            new_version, flag = QInputDialog.getText(
                self,
                'Enter version name',
                'Enter a new version name',
            )
            if flag:
                if update_folder(
                        login=self.login,
                        path=self.folders_tableWidget.item(row, 0).text(),
                        old_version=self.folders_tableWidget.item(row, 1).text(),
                        new_version=new_version,
                        token=self.token
                ):
                    self.fill_table()

            # path = self.folders_tableWidget.item(row, 0).text()
            # old_version = self.folders_tableWidget.item(row, 1).text()
            # mac = get_mac()
            # data = get_json(get_files(path))
            # data['login'] = self.login
            # data['mac'] = mac
            # data['path_file'] = path
            # data['old_version'] = old_version
            #
            # head = {'Content-Type': 'application/json', 'Authorization': self.token}
            # new_version, flag = QInputDialog.getText(
            #     self,
            #     'Enter version name',
            #     'Enter a new version name',
            # )
            # if flag:
            #     data['new_version'] = new_version
            #
            #     request = requests.get(
            #         f'{PROTOCOL}://{IP}:{PORT}/update_version/',
            #         data=json.dumps(data),
            #         headers=head
            #     )
            #     if check_request(request):
            #         self.fill_table()

    def synchronize(self):
        pass

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

            if delete_user(
                login=self.login,
                token=self.token,
                window=self
            ):
                self.siw.login_lineedit.setText('')
                self.close()

            # count = 0
            # head = {'Content-Type': 'application/json', 'Authorization': self.token}
            # request = requests.get(
            #     f'{PROTOCOL}://{IP}:{PORT}/get_password/',
            #     params={
            #         'login': self.login
            #     },
            #     headers=head)
            # if check_request(request):
            #     password = request.content
            #     while count != 3:
            #         pass_input, flag = QInputDialog.getText(
            #             self,
            #             'Confirm your actions',
            #             'To delete your account, enter your password.',
            #             echo=QtWidgets.QLineEdit.Password
            #         )
            #         if flag and pass_input:
            #             count += 1
            #             if bcrypt.checkpw(pass_input.encode('UTF-8'), password):
            #                 head = {'Content-Type': 'application/json', 'Authorization': self.token}
            #                 request = requests.get(
            #                     f'{PROTOCOL}://{IP}:{PORT}/delete_user/',
            #                     params={'login': self.login},
            #                     headers=head)
            #                 if check_request(request):
            #                     self.siw.login_lineedit.setText('')
            #                     self.close()
            #                     break
            #         else:
            #             break
            #     if count == 3:
            #         call_ui.show_warning('Confirmation error!', 'You have entered the wrong password too many times.')

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
