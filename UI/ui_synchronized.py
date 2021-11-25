import threading

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QTableWidget, QTableWidgetItem, QCheckBox

from UI_functional.synchronized import terminate_sync, synchronize_folder
from UI_functional.workplace import download_version, get_synchronized
from UI.call_ui import show_dialog, show_verification_dialog


class SWindow(QMainWindow):
    def __init__(self, mode, data, wpw):
        super(SWindow, self).__init__()
        self.__mode = mode
        self.__data = data
        self.__wpw = wpw

        self.__login = self.__wpw.login
        self.__token = self.__wpw.token
        self.__flag = False
        self.__wpw.setEnabled(False)

        if self.__mode:
            self.setWindowTitle('SyncGad • Synchronized')
            self.setGeometry(600, 300, 768, 233)
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
            self.setGeometry(600, 300, 700, 233)
            self.setFixedSize(self.size())

            self.confirm_Button = QtWidgets.QPushButton(self)
            self.confirm_Button.setGeometry(600, 193, 90, 30)
            self.confirm_Button.setText('Confirm')
            self.confirm_Button.setToolTip('Confirm your choice')
            self.confirm_Button.clicked.connect(self.confirm)

            self.sync_tableWidget = QTableWidget(self)
            self.create_update_table()
            self.fill_update_table()

            QTimer.singleShot(1, lambda: show_dialog('Notification',
                                                     'Some of your synced folders have changed. Merge\n'
                                                     'them with matching ones, otherwise their syncs\n'
                                                     'will be broken', 2))

    def create_static_table(self):
        columns = 5
        rows = 5
        self.sync_tableWidget.setGeometry(
            QtCore.QRect(10, 10, 748, self.sync_tableWidget.verticalHeader().height() * (rows + 1) + 5))
        self.sync_tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sync_tableWidget.setRowCount(rows)
        self.sync_tableWidget.setColumnCount(columns)
        self.sync_tableWidget.setHorizontalHeaderLabels(
            ('User`s id', 'Username', 'Local folder', 'Other user`s folder', 'Last local change'))
        self.sync_tableWidget.setColumnWidth(0, 80)
        self.sync_tableWidget.setColumnWidth(1, 80)
        self.sync_tableWidget.setColumnWidth(2, 250)
        self.sync_tableWidget.setColumnWidth(3, 250)
        self.sync_tableWidget.setColumnWidth(4, 168)

        self.sync_tableWidget.horizontalHeader().setHighlightSections(False)
        self.sync_tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.sync_tableWidget.verticalHeader().setVisible(False)
        self.sync_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.sync_tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.sync_tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.sync_tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

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
                    if z != self.sync_tableWidget.columnCount() - 1 and z != 0:
                        self.sync_tableWidget.item(i, z).setToolTip(self.sync_tableWidget.item(i, z).text())
        else:
            self.sync_tableWidget.setRowCount(0)
            self.sync_tableWidget.setRowCount(5)

    def create_update_table(self):
        columns = 5
        rows = 5
        self.sync_tableWidget.setGeometry(
            QtCore.QRect(10, 10, 680, self.sync_tableWidget.verticalHeader().height() * (rows + 1) + 5))
        self.sync_tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sync_tableWidget.setRowCount(rows)
        self.sync_tableWidget.setColumnCount(columns)
        self.sync_tableWidget.setHorizontalHeaderLabels(
            ('', 'User`s id', 'Username', 'Local folder', 'Other user`s folder'))
        self.sync_tableWidget.setColumnWidth(0, 20)
        self.sync_tableWidget.setColumnWidth(1, 80)
        self.sync_tableWidget.setColumnWidth(2, 80)
        self.sync_tableWidget.setColumnWidth(3, 231)
        self.sync_tableWidget.setColumnWidth(4, 230)

        self.sync_tableWidget.verticalHeader().setVisible(False)
        self.sync_tableWidget.horizontalHeader().setHighlightSections(False)
        self.sync_tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.sync_tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.sync_tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.sync_tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

    def fill_update_table(self):
        for i in range(len(self.__data)):
            check_box = QCheckBox()
            check_box.setChecked(True)
            check_box.setStyleSheet('''
                QCheckBox {
                    margin: 20px
                };
            ''')
            self.sync_tableWidget.setCellWidget(i, 0, check_box)
            self.sync_tableWidget.setItem(i, 1, QTableWidgetItem(self.__data[i]['other_id']))
            self.sync_tableWidget.setItem(i, 2, QTableWidgetItem(self.__data[i]['other_user']))
            self.sync_tableWidget.setItem(i, 3, QTableWidgetItem(self.__data[i]['current_folder']))
            self.sync_tableWidget.setItem(i, 4, QTableWidgetItem(self.__data[i]['other_folder']))
            self.sync_tableWidget.item(i, 2).setToolTip(self.sync_tableWidget.item(i, 2).text())
            self.sync_tableWidget.item(i, 3).setToolTip(self.sync_tableWidget.item(i, 3).text())
            self.sync_tableWidget.item(i, 4).setToolTip(self.sync_tableWidget.item(i, 4).text())

    def confirm(self):
        for i in range(self.sync_tableWidget.rowCount()):
            if self.sync_tableWidget.item(i, 1) is not None:
                check_box = self.sync_tableWidget.cellWidget(i, 0)
                if check_box.isChecked():
                    # HERE
                    if synchronize_folder(
                            current_login=self.__login,
                            other_id=self.sync_tableWidget.item(i, 1).text(),
                            current_folder=self.sync_tableWidget.item(i, 2).text(),
                            other_folder=self.sync_tableWidget.item(i, 3).text(),
                            token=self.__wpw.token
                    ):
                        # if not download_version(
                        #         login=self.__login,
                        #         path=self.sync_tableWidget.item(i, 2).text(),
                        #         token=self.__token,
                        #         flag=True
                        # ):
                        #     show_dialog('Error', 'Error occurred while synchronizing.\nProcess was stopped.')
                        #     break
                        threading.Thread(name='download_version', target=download_version, args={
                            'login': self.__login,
                            'path': self.sync_tableWidget.item(i, 2).text(),
                            'token': self.__token,
                            'flag': True
                        }).start()
                else:
                    terminate_sync(
                        current_login=self.__login,
                        other_id=self.sync_tableWidget.item(i, 1).text(),
                        current_folder=self.sync_tableWidget.item(i, 3).text(),
                        other_folder=self.sync_tableWidget.item(i, 4).text(),
                        token=self.__wpw.token
                    )
        self.__flag = True
        self.close()

    def terminate_sync(self):
        row = self.sync_tableWidget.currentRow()
        if self.sync_tableWidget.item(row, 0) is not None:
            if show_verification_dialog('Terminate synchronization', 'Are you sure you want to '
                                                                     'terminate this synchronization?'):
                if terminate_sync(
                        current_login=self.__wpw.login,
                        other_id=self.sync_tableWidget.item(row, 0).text(),
                        current_folder=self.sync_tableWidget.item(row, 2).text(),
                        other_folder=self.sync_tableWidget.item(row, 3).text(),
                        token=self.__wpw.token
                ):
                    self.__data = get_synchronized(
                        login=self.__login,
                        token=self.__token
                    )
                    self.fill_static_table()

    def closeEvent(self, event):
        if not self.__mode:
            if not self.__flag:
                for i in range(self.sync_tableWidget.rowCount()):
                    if self.sync_tableWidget.item(i, 1) is not None:
                        terminate_sync(
                            current_login=self.__login,
                            other_id=self.sync_tableWidget.item(i, 1).text(),
                            current_folder=self.sync_tableWidget.item(i, 3).text(),
                            other_folder=self.sync_tableWidget.item(i, 4).text(),
                            token=self.__wpw.token
                        )
        self.__wpw.setEnabled(True)
