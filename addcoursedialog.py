

from PyQt5.QtWidgets import QMessageBox, QDialog
from PyQt5.uic import loadUi
from database import database


class Ui_Dialog(QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        loadUi("ui/dialog.ui", self)
        self.db = database()

    # it takes the courseName, teacherName and stores into db
    def accept(self):
        msgBox = QMessageBox()
        courseName = self.courseNameLineEdit.text()
        teacherName = self.teacherNameLineEdit.text()
        result = self.db.insertCourse(courseName, teacherName)
        if result:
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Course is successfully created")
            msgBox.setWindowTitle("Success")
        else:
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Course is already exists")
            msgBox.setWindowTitle("Warning")
        msgBox.exec()

