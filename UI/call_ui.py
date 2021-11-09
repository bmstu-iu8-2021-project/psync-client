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


def notification(title, text):
    note = QMessageBox()
    note.setWindowTitle(title)
    note.setText(text)
    note.setIcon(QMessageBox.Information)
    note.exec_()
