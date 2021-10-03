from PyQt5.QtWidgets import QMessageBox


def show_warning(title, text):
    error = QMessageBox()
    error.setWindowTitle(title)
    error.setText(text)
    error.setIcon(QMessageBox.Warning)
    error.setStandardButtons(QMessageBox.Ok)
    error.exec_()
