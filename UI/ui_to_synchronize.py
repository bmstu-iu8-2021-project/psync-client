# from PyQt5 import QtWidgets, QtCore
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QAbstractItemView, QTableWidget, QTableWidgetItem, QCheckBox
# from PyQt5.QtWidgets import QMainWindow
#
# from UI_functional.workplace import get_folders
# from UI_functional.synchronized import terminate_all_sync, synchronize_folder
#
#
# class TSWindow(QMainWindow):
#     def __init__(self, login, folders, wpw, token):
#         super(TSWindow, self).__init__()
#         self.login = login
#         self.token = token
#         self.folders = folders
#         self.wpw = wpw
#         self.flag = False
#
#         self.wpw.setEnabled(False)
#         self.setWindowFlags(Qt.WindowStaysOnTopHint)
#
#         self.setWindowTitle('SyncGad • Synchronize folders')
#         self.setGeometry(650, 250, 540, 231)
#         self.setFixedSize(self.size())
#
#         self.confirm_Button = QtWidgets.QPushButton(self)
#         self.confirm_Button.setGeometry(350, 193, 180, 28)
#         self.confirm_Button.setText("Confirm synchronization")
#         self.confirm_Button.clicked.connect(self.confirm)
#
#         self.to_update_tableWidget = QTableWidget(self)
#         self.create_table()
#
#     def create_table(self):
#         columns = 3
#         rows = 5
#         self.to_update_tableWidget.setGeometry(
#             QtCore.QRect(10, 10, 520, self.to_update_tableWidget.verticalHeader().height() * (rows + 1) + 5))
#         self.to_update_tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
#         self.to_update_tableWidget.setRowCount(rows)
#         self.to_update_tableWidget.setColumnCount(columns)
#         self.to_update_tableWidget.setHorizontalHeaderLabels(('', 'Local folder', 'Other user folder'))
#         self.to_update_tableWidget.setColumnWidth(0, 20)
#         self.to_update_tableWidget.setColumnWidth(1, 231)
#         self.to_update_tableWidget.setColumnWidth(2, 230)
#
#         self.to_update_tableWidget.verticalHeader().setVisible(False)
#         self.to_update_tableWidget.horizontalHeader().setHighlightSections(False)
#         self.to_update_tableWidget.horizontalHeader().setSortIndicatorShown(False)
#         self.to_update_tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
#         self.to_update_tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
#         self.to_update_tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
#
#         self.fill_table()
#
#     def fill_table(self):
#         for i in range(len(self.folders['folder'])):
#             check_box = QCheckBox()
#             check_box.setChecked(True)
#             check_box.setStyleSheet('''
#                 QCheckBox {
#                     margin: 20px
#                 };
#             ''')
#             self.to_update_tableWidget.setCellWidget(i, 0, check_box)
#             self.to_update_tableWidget.setItem(i, 1, QTableWidgetItem(self.folders['folder'][i]['current_folder']))
#             self.to_update_tableWidget.setItem(i, 2, QTableWidgetItem(self.folders['folder'][i]['other_folder']))
#             self.to_update_tableWidget.item(i, 1).setToolTip(self.to_update_tableWidget.item(i, 1).text())
#             self.to_update_tableWidget.item(i, 2).setToolTip(self.to_update_tableWidget.item(i, 2).text())
#
#     def confirm(self):
#         for i in range(self.to_update_tableWidget.rowCount()):
#             if self.to_update_tableWidget.item(i, 1) is not None:
#                 check_bow = self.to_update_tableWidget.cellWidget(i, 0)
#                 if check_bow.isChecked():
#                     synchronize_folder(
#                         login=self.login,
#                         path=self.to_update_tableWidget.item(i, 1).text(),
#                         token=self.token
#                     )
#                 else:
#                     terminate_all_sync(
#                         login=self.login,
#                         path=self.to_update_tableWidget.item(i, 1).text(),
#                         token=self.token
#                     )
#         self.wpw.fill_table(get_folders(
#             login=self.login,
#             token=self.token
#         ))
#         self.flag = True
#         self.close()
#
#     def closeEvent(self, event):
#         if not self.flag:
#             for i in range(self.to_update_tableWidget.rowCount()):
#                 if self.to_update_tableWidget.item(i, 1) is not None:
#                     terminate_all_sync(
#                         login=self.login,
#                         path=self.to_update_tableWidget.item(i, 1).text(),
#                         token=self.token
#                     )
#         self.wpw.setEnabled(True)
