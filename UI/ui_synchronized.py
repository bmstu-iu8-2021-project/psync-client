from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QTableWidget, QTableWidgetItem, QCheckBox

from UI_functional.synchronized import terminate_sync, synchronize_folder
from UI_functional.workplace import download_folder
from UI.call_ui import show_dialog


class SWindow(QMainWindow):
    def __init__(self, login, mode, data, wpw, token):
        super(SWindow, self).__init__()
        self.__login = login
        self.__token = token
        self.__wpw = wpw
        self.__mode = mode
        self.__data = data
        self.__flag = False
        self.__wpw.setEnabled(False)

        if self.__mode:
            self.setWindowTitle('SyncGad • Synchronized')
            self.setGeometry(600, 300, 770, 233)
            self.setFixedSize(self.size())

            self.terminate_Button = QtWidgets.QPushButton(self)
            self.terminate_Button.setGeometry(670, 193, 90, 30)
            self.terminate_Button.setText('Terminate')
            self.terminate_Button.setToolTip('Break this synchronization')
            self.terminate_Button.clicked.connect(self.terminate_sync)

            self.sync_tableWidget = QTableWidget(self)
            self.create_static_table()
            self.fill_static_table()

        else:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.setWindowTitle('SyncGad • To synchronize')
            self.setGeometry(600, 300, 620, 233)
            self.setFixedSize(self.size())

            self.confirm_Button = QtWidgets.QPushButton(self)
            self.confirm_Button.setGeometry(520, 193, 90, 30)
            self.confirm_Button.setText('Confirm')
            self.confirm_Button.setToolTip('Confirm your choice')
            self.confirm_Button.clicked.connect(self.confirm)

            self.sync_tableWidget = QTableWidget(self)
            self.create_update_table()
            self.fill_update_table()

    def create_static_table(self):
        columns = 4
        rows = 5
        self.sync_tableWidget.setGeometry(
            QtCore.QRect(10, 10, 750, self.sync_tableWidget.verticalHeader().height() * (rows + 1) + 5))
        self.sync_tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sync_tableWidget.setRowCount(rows)
        self.sync_tableWidget.setColumnCount(columns)
        self.sync_tableWidget.setHorizontalHeaderLabels(
            ('Username', 'Local folder', 'Other user`s folder', 'Last local change'))
        self.sync_tableWidget.setColumnWidth(0, 80)
        self.sync_tableWidget.setColumnWidth(1, 250)
        self.sync_tableWidget.setColumnWidth(2, 250)
        self.sync_tableWidget.setColumnWidth(3, 168)

        self.sync_tableWidget.horizontalHeader().setHighlightSections(False)
        self.sync_tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.sync_tableWidget.verticalHeader().setVisible(False)
        self.sync_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.sync_tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.sync_tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.sync_tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

    def create_update_table(self):
        columns = 4
        rows = 5
        self.sync_tableWidget.setGeometry(
            QtCore.QRect(10, 10, 600, self.sync_tableWidget.verticalHeader().height() * (rows + 1) + 5))
        self.sync_tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sync_tableWidget.setRowCount(rows)
        self.sync_tableWidget.setColumnCount(columns)
        self.sync_tableWidget.setHorizontalHeaderLabels(
            ('', 'Username', 'Local folder', 'Other user`s folder'))
        self.sync_tableWidget.setColumnWidth(0, 20)
        self.sync_tableWidget.setColumnWidth(1, 80)
        self.sync_tableWidget.setColumnWidth(2, 231)
        self.sync_tableWidget.setColumnWidth(3, 230)

        self.sync_tableWidget.verticalHeader().setVisible(False)
        self.sync_tableWidget.horizontalHeader().setHighlightSections(False)
        self.sync_tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.sync_tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.sync_tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.sync_tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

    def fill_update_table(self):
        for i in range(len(self.__data['items'])):
            check_box = QCheckBox()
            check_box.setChecked(True)
            check_box.setStyleSheet('''
                QCheckBox {
                    margin: 20px
                };
            ''')
            self.sync_tableWidget.setCellWidget(i, 0, check_box)
            self.sync_tableWidget.setItem(i, 1, QTableWidgetItem(self.__data['items'][i]['other_user']))
            self.sync_tableWidget.setItem(i, 2, QTableWidgetItem(self.__data['items'][i]['current_folder']))
            self.sync_tableWidget.setItem(i, 3, QTableWidgetItem(self.__data['items'][i]['other_folder']))
            self.sync_tableWidget.item(i, 1).setToolTip(self.sync_tableWidget.item(i, 1).text())
            self.sync_tableWidget.item(i, 2).setToolTip(self.sync_tableWidget.item(i, 2).text())
            self.sync_tableWidget.item(i, 3).setToolTip(self.sync_tableWidget.item(i, 3).text())

    def confirm(self):
        for i in range(self.sync_tableWidget.rowCount()):
            if self.sync_tableWidget.item(i, 1) is not None:
                check_box = self.sync_tableWidget.cellWidget(i, 0)
                if check_box.isChecked():
                    if synchronize_folder(
                            current_login=self.__login,
                            other_login=self.sync_tableWidget.item(i, 1).text(),
                            current_folder=self.sync_tableWidget.item(i, 2).text(),
                            other_folder=self.sync_tableWidget.item(i, 3).text(),
                            token=self.__wpw.token
                    ):
                        if not download_folder(
                                login=self.__login,
                                path=self.sync_tableWidget.item(i, 2).text(),
                                token=self.__token,
                                flag=True
                        ):
                            show_dialog('Error', 'Error occurred while synchronizing.\nProcess was stopped.')
                            break
                else:
                    terminate_sync(
                        current_login=self.__login,
                        other_login=self.sync_tableWidget.item(i, 1).text(),
                        current_folder=self.sync_tableWidget.item(i, 2).text(),
                        other_folder=self.sync_tableWidget.item(i, 3).text(),
                        token=self.__wpw.token
                    )
        self.__flag = True
        self.close()

    def fill_static_table(self):
        if self.__data is not None:
            count = len(self.__data)
            if count > 5:
                self.sync_tableWidget.setRowCount(count)
                self.sync_tableWidget.setColumnWidth(3, 156)
            else:
                self.sync_tableWidget.setRowCount(0)
                self.sync_tableWidget.setRowCount(5)
                self.sync_tableWidget.setColumnWidth(3, 168)
            for i in range(count):
                for j in self.__data[i].keys():
                    z = list(self.__data[i].keys()).index(j)
                    self.sync_tableWidget.setItem(i, z, QTableWidgetItem(self.__data[i][j]))
                    if z != self.sync_tableWidget.columnCount() - 1:
                        self.sync_tableWidget.item(i, z).setToolTip(self.sync_tableWidget.item(i, z).text())
        else:
            self.sync_tableWidget.setRowCount(0)
            self.sync_tableWidget.setRowCount(5)

    def terminate_sync(self):
        # TODO: ask user to confirm action
        row = self.sync_tableWidget.currentRow()
        if self.sync_tableWidget.item(row, 0) is not None:
            if terminate_sync(
                    current_login=self.__wpw.login,
                    other_login=self.sync_tableWidget.item(row, 0).text(),
                    current_folder=self.sync_tableWidget.item(row, 1).text(),
                    other_folder=self.sync_tableWidget.item(row, 2).text(),
                    token=self.__wpw.token
            ):
                self.fill_static_table()

    def closeEvent(self, event):
        if not self.__mode:
            if not self.__flag:
                for i in range(self.sync_tableWidget.rowCount()):
                    if self.sync_tableWidget.item(i, 0) is not None:
                        terminate_sync(
                            current_login=self.__login,
                            other_login=self.sync_tableWidget.item(i, 1).text(),
                            current_folder=self.sync_tableWidget.item(i, 2).text(),
                            other_folder=self.sync_tableWidget.item(i, 3).text(),
                            token=self.__wpw.token
                        )
        self.__wpw.setEnabled(True)
