from PyQt5.QtWidgets import QMessageBox


def show_warning(title, text, flag='Warning'):
    error = QMessageBox()
    error.setWindowTitle(title)
    error.setText(text)
    if flag == 'Warning':
        error.setIcon(QMessageBox.Warning)
    elif flag == 'Critical':
        error.setIcon(QMessageBox.Critical)
    error.setStandardButtons(QMessageBox.Ok)
    error.exec_()
