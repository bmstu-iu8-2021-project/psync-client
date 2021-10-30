from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog, QFileDialog, QAbstractItemView, QTableWidget, \
    QTableWidgetItem
from PyQt5.QtGui import QIcon

from UI import ui_about, create_menu, ui_change_password, ui_change_email, ui_to_change
from UI_functional.workplace import add_folder, update_folder, delete_version, delete_user, get_folders, make_actual
from UI_functional.workplace import check_actuality, download_folder


class WPWindow(QMainWindow):
    def __init__(self, token, siw, login):
        super(WPWindow, self).__init__()
        self.token = token
        self.siw = siw
        self.login = login

        self.setWindowTitle('SyncGad • Workplace')
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

        self.download_Button = QtWidgets.QPushButton(self)
        self.download_Button.setGeometry(530, 225, 40, 40)
        self.download_Button.setIcon(QIcon('icons/workplace/download_folder.svg'))
        self.download_Button.setIconSize(QtCore.QSize(30, 30))
        self.download_Button.setToolTip('Download chosen folder')
        self.download_Button.clicked.connect(self.download_version)

        self.sync_Button = QtWidgets.QPushButton(self)
        self.sync_Button.setGeometry(530, 285, 40, 40)
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
        # self.folders_tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.folders_tableWidget.setRowCount(rows)
        self.folders_tableWidget.setColumnCount(columns)
        self.folders_tableWidget.setHorizontalHeaderLabels(('Folder', 'Version', 'Actual for'))
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

        self.folders_tableWidget.doubleClicked.connect(self.make_actual)

        self.fill_table()
        self.check_actuality()

    def make_actual(self):
        row = self.folders_tableWidget.currentRow()
        if not (self.folders_tableWidget.item(row, 0) is None):
            font = QtGui.QFont()
            font.setBold(True)
            if not (self.folders_tableWidget.item(row, 0).font() == font):
                if make_actual(
                        login=self.login,
                        path=self.folders_tableWidget.item(row, 0).text(),
                        version=self.folders_tableWidget.item(row, 1).text(),
                        token=self.token
                ):
                    self.fill_table()

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

    # заполнение таблицы актуальными данными (старые стираются)
    def fill_table(self):
        self.folders_tableWidget.setRowCount(10)
        data = get_folders(
            login=self.login,
            token=self.token
        )
        self.folders_tableWidget.setRowCount(0)
        self.folders_tableWidget.setRowCount(10)
        if data.keys():
            data_count = len(list(data.values())[0])
            if data_count <= 10:
                self.folders_tableWidget.setColumnWidth(0, 278)
            else:
                self.folders_tableWidget.setRowCount(data_count)
                self.folders_tableWidget.setColumnWidth(0, 264)
            font = QtGui.QFont()
            font.setBold(True)
            for i in range(len(data.keys()) - 1):
                key = list(data.keys())[i]
                for j in range(len(data[key])):
                    self.folders_tableWidget.setItem(j, i, QTableWidgetItem(str(data[key][j])))
                    if data['is_actual'][j] == 'True':
                        self.folders_tableWidget.item(j, i).setFont(font)

        # добавляем подсказки к ячейкам первого столбца
        for i in range(self.folders_tableWidget.rowCount()):
            if not self.folders_tableWidget.item(i, 0) is None:
                self.folders_tableWidget.item(i, 0).setToolTip(self.folders_tableWidget.item(i, 0).text())

    def check_actuality(self):
        data = get_folders(
            login=self.login,
            token=self.token
        )
        # проверяем, свежие ли данные в акутальных версиях
        to_change = check_actuality(self.login, data, self.token)
        if not (to_change is None):
            # self.setWindowModality(QtCore.Qt.ApplicationModal)
            self.tc_window = ui_to_change.TCWindow(self.login, self.token, to_change, self)
            self.tc_window.show()
            self.setEnabled(False)

    def update_version(self):
        row = self.folders_tableWidget.currentRow()
        if not (self.folders_tableWidget.item(row, 0) is None):
            if update_folder(
                    login=self.login,
                    path=self.folders_tableWidget.item(row, 0).text(),
                    version=self.folders_tableWidget.item(row, 1).text(),
                    token=self.token
            ):
                self.fill_table()

    def download_version(self):
        row = self.folders_tableWidget.currentRow()
        if not (self.folders_tableWidget.item(row, 0) is None):
            if download_folder(
                    login=self.login,
                    path=self.folders_tableWidget.item(row, 0).text(),
                    version=self.folders_tableWidget.item(row, 1).text(),
                    token=self.token
            ):
                if make_actual(
                    login=self.login,
                    path=self.folders_tableWidget.item(row, 0).text(),
                    version=self.folders_tableWidget.item(row, 1).text(),
                    token=self.token
                ):
                    self.fill_table()

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
                self.siw.login_LineEdit.setText('')
                self.close()

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
