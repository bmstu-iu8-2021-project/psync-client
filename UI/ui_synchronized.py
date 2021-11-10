from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QTableWidget, QTableWidgetItem

from UI_functional.synchronized import get_synchronized


class SWindow(QMainWindow):
    def __init__(self, wpw):
        super(SWindow, self).__init__()
        self.__wpw = wpw
        self.__wpw.setEnabled(False)

        self.setWindowTitle('SyncGad • Synchronized')
        self.setGeometry(600, 300, 770, 233)
        self.setFixedSize(self.size())

        self.terminate_Button = QtWidgets.QPushButton(self)
        self.terminate_Button.setGeometry(670, 193, 90, 30)
        self.terminate_Button.setText('Terminate')
        self.terminate_Button.setToolTip('Synchronize chosen folder')
        self.terminate_Button.clicked.connect(self.terminate_sync)

        self.sync_tableWidget = QTableWidget(self)
        self.create_table()
        self.fill_table()

    def create_table(self):
        columns = 4
        rows = 5
        self.sync_tableWidget.setGeometry(
            QtCore.QRect(10, 10, 750, self.sync_tableWidget.verticalHeader().height() * (rows + 1) + 5))
        self.sync_tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sync_tableWidget.setRowCount(rows)
        self.sync_tableWidget.setColumnCount(columns)
        self.sync_tableWidget.setHorizontalHeaderLabels(('Username', 'Local folder', 'Other user`s folder', 'Last change'))
        self.sync_tableWidget.setColumnWidth(0, 80)
        self.sync_tableWidget.setColumnWidth(1, 250)
        self.sync_tableWidget.setColumnWidth(2, 250)
        self.sync_tableWidget.setColumnWidth(3, 168)

        self.sync_tableWidget.verticalHeader().setVisible(False)
        self.sync_tableWidget.horizontalHeader().setHighlightSections(False)
        self.sync_tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.sync_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.sync_tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.sync_tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.sync_tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

    def fill_table(self):
        json_data = get_synchronized(
            login=self.__wpw.login,
            token=self.__wpw.token
        )
        if json_data is not None:
            count = len(json_data)
            if count > 5:
                self.sync_tableWidget.setRowCount(count)
                self.sync_tableWidget.setColumnWidth(0, 156)
            for i in range(count):
                for j in json_data[i].keys():
                    self.sync_tableWidget.setItem(i, list(json_data[i].keys()).index(j), QTableWidgetItem(json_data[i][j]))

    def terminate_sync(self):
        pass

    def closeEvent(self, event):
        self.__wpw.setEnabled(True)
