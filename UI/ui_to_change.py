from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QTableWidget, QTableWidgetItem, QCheckBox
from PyQt5.QtWidgets import QMainWindow

from UI_functional.workplace import update_actual_folder, make_no_actual


class TCWindow(QMainWindow):
    def __init__(self, login, token, folders, wpw):
        super(TCWindow, self).__init__()
        self.login = login
        self.token = token
        self.folders = folders
        self.wpw = wpw

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)

        self.setWindowTitle('SyncGad • Update folders')
        self.setGeometry(650, 250, 470, 381)
        self.setFixedSize(self.size())

        self.confirm_Button = QtWidgets.QPushButton(self)
        self.confirm_Button.setGeometry(330, 343, 130, 28)
        self.confirm_Button.setText("Confirm changes")
        self.confirm_Button.clicked.connect(self.confirm)

        self.to_update_tableWidget = QTableWidget(self)
        self.create_table()

    def create_table(self):
        columns = 2
        rows = 10
        # 470 = 20 + 450
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
        for i in range(len(self.folders['folder_name'])):
            check_box = QCheckBox()
            check_box.setChecked(True)
            check_box.setStyleSheet('''
                QCheckBox {
                    margin: 20px
                };
            ''')
            self.to_update_tableWidget.setCellWidget(i, 0, check_box)
            self.to_update_tableWidget.setItem(i, 1, QTableWidgetItem(str(self.folders['folder_name'][i])))
            self.to_update_tableWidget.item(i, 1).setToolTip(self.to_update_tableWidget.item(i, 1).text())

    def confirm(self):
        for i in range(self.to_update_tableWidget.rowCount()):
            if not (self.to_update_tableWidget.item(i, 1) is None):
                check_bow = self.to_update_tableWidget.cellWidget(i, 0)
                if check_bow.isChecked():
                    update_actual_folder(
                        login=self.login,
                        path=self.to_update_tableWidget.item(i, 1).text(),
                        token=self.token
                    )
                else:
                    make_no_actual(
                        login=self.login,
                        path=self.to_update_tableWidget.item(i, 1).text(),
                        token=self.token
                    )
        self.wpw.fill_table()
        self.close()

    def closeEvent(self, event):
        self.wpw.setEnabled(True)
