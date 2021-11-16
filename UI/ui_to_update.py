from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QAbstractItemView, QTableWidget, QTableWidgetItem, QCheckBox
from PyQt5.QtWidgets import QMainWindow

from UI_functional.workplace import update_actual_folder, make_no_actual, get_folders, check_synchronized
from UI import ui_synchronized
from UI.call_ui import show_dialog


class TUWindow(QMainWindow):
    def __init__(self, folders, wpw):
        super(TUWindow, self).__init__()
        self.__folders = folders
        self.__wpw = wpw

        self.__flag = False
        self.__login = self.__wpw.login
        self.__token = self.__wpw.token
        self.__wpw.setEnabled(False)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.setWindowTitle('SyncGad • Update folders')
        self.setGeometry(650, 250, 470, 381)
        self.setFixedSize(self.size())

        self.confirm_Button = QtWidgets.QPushButton(self)
        self.confirm_Button.setGeometry(330, 343, 130, 28)
        self.confirm_Button.setText("Confirm changes")
        self.confirm_Button.clicked.connect(self.confirm)

        self.to_update_tableWidget = QTableWidget(self)
        self.create_table()

        QTimer.singleShot(1, lambda: show_dialog('Notification',
                                                 'Some of your actual folders have been changed locally.\n'
                                                 'Update them, otherwise they will no longer be\n'
                                                 'actual and all their syncs will be broken', 2))

    def create_table(self):
        columns = 2
        rows = 10
        self.to_update_tableWidget.setGeometry(
            QtCore.QRect(10, 10, 450, self.to_update_tableWidget.verticalHeader().height() * (rows + 1) + 15))
        self.to_update_tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.to_update_tableWidget.setRowCount(rows)
        self.to_update_tableWidget.setColumnCount(columns)
        self.to_update_tableWidget.setHorizontalHeaderLabels(('', 'Folder'))
        self.to_update_tableWidget.setColumnWidth(0, 20)
        self.to_update_tableWidget.setColumnWidth(1, 391)

        self.to_update_tableWidget.verticalHeader().setVisible(False)
        self.to_update_tableWidget.horizontalHeader().setHighlightSections(False)
        self.to_update_tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.to_update_tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.to_update_tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.to_update_tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

        self.fill_table()

    def fill_table(self):
        for i in range(len(self.__folders)):
            check_box = QCheckBox()
            check_box.setChecked(True)
            check_box.setStyleSheet('''
                QCheckBox {
                    margin: 20px
                };
            ''')
            self.to_update_tableWidget.setCellWidget(i, 0, check_box)
            self.to_update_tableWidget.setItem(i, 1, QTableWidgetItem(self.__folders[i]))
            self.to_update_tableWidget.item(i, 1).setToolTip(self.to_update_tableWidget.item(i, 1).text())

    def confirm(self):
        for i in range(self.to_update_tableWidget.rowCount()):
            if self.to_update_tableWidget.item(i, 1) is not None:
                check_bow = self.to_update_tableWidget.cellWidget(i, 0)
                if check_bow.isChecked():
                    update_actual_folder(
                        login=self.__login,
                        path=self.to_update_tableWidget.item(i, 1).text(),
                        token=self.__token
                    )
                else:
                    make_no_actual(
                        login=self.__login,
                        path=self.to_update_tableWidget.item(i, 1).text(),
                        token=self.__token
                    )
        self.__wpw.fill_table(get_folders(
            login=self.__login,
            token=self.__token
        ))
        self.__flag = True
        self.close()

    def check_synchronized(self):
        to_sync = check_synchronized(
            login=self.__login,
            token=self.__token
        )
        if to_sync is not None:
            if len(to_sync['items']) != 0:
                self.tswindow = ui_synchronized.SWindow(
                    mode=False,
                    data=to_sync,
                    wpw=self.__wpw,
                )
                self.tswindow.show()

    # def show_dialog(self):
    #     show_dialog('Notification', 'Some of your actual folders have been changed locally.\n'
    #                                 'Update them, otherwise they will no longer be\n'
    #                                 'actual and all their syncs will be broken', 2)

    def closeEvent(self, event):
        if not self.__flag:
            for i in range(self.to_update_tableWidget.rowCount()):
                if self.to_update_tableWidget.item(i, 1) is not None:
                    make_no_actual(
                        login=self.__login,
                        path=self.to_update_tableWidget.item(i, 1).text(),
                        token=self.__token
                    )
            self.__wpw.fill_table(get_folders(
                login=self.__login,
                token=self.__token
            ))
        self.__wpw.setEnabled(True)
        self.check_synchronized()
