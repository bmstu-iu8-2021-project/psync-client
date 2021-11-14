from PyQt5.QtWidgets import QMessageBox


def show_dialog(title, text, flag=0):
    dialog = QMessageBox()
    dialog.setWindowTitle(title)
    dialog.setText(text)
    if flag == 0:
        dialog.setIcon(QMessageBox.Warning)
    elif flag == 1:
        dialog.setIcon(QMessageBox.Critical)
    elif flag == 2:
        dialog.setIcon(QMessageBox.Information)
    dialog.setStandardButtons(QMessageBox.Ok)
    dialog.exec_()
