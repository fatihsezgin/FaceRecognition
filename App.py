import sys
from addcoursedialog import Ui_Dialog
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from database import database
import os
import sqlite3 as sqlite


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        loadUi("ui/App.ui", self)

        self.db = database()
        self.pBOpenCourseAddDialog.clicked.connect(self.addCourseClicked)
        self.buttonDbSave.clicked.connect(self.insertStudent)
        self.tabWidget.currentChanged.connect(self.getDataForList)
        self.getDataForList()


    def addCourseClicked(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()
        self.fillCourses()
        QApplication.processEvents()

    def insertStudent(self):
        print(self.db)
        print(self.nameLineEdit.text(),
              self.surnameLineEdit.text(), self.schoolNumberLineEdit.text(), self.facultyLineEdit.text(), self.departmentLineEdit.text())

        flag = self.db.insertStudent(self.nameLineEdit.text(),
                              self.surnameLineEdit.text(), self.schoolNumberLineEdit.text(), self.facultyLineEdit.text(), self.departmentLineEdit.text())
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        print(flag)
        if(flag):
            msgBox.setText("Student is successfully inserted into db")
            msgBox.setWindowTitle("Success")
        else:
            msgBox.setText("Failed when inserted into db")
            msgBox.setWindowTitle("Error")
        msgBox.exec()
        self.clearStudentLineEdits()

    def clearStudentLineEdits(self):
        self.nameLineEdit.clear()
        self.surnameLineEdit.clear()
        self.schoolNumberLineEdit.clear()
        self.facultyLineEdit.clear()
        self.departmentLineEdit.clear()

    def getDataForList(self):
        if self.tabWidget.currentIndex() == 0:
            self.listWidget.clear()
            self.fillCourses()
            self.fillStudents()
            QtWidgets.QApplication.processEvents()

    def fillCourses(self):
        # get all files' and folders' names in the current directory
        self.listWidget.clear()
        filenames = os.listdir("./courses/")
        print(filenames)
        self.listWidget.addItems(filenames)
        # QApplication.processEvents()

    def fillStudents(self):
        with sqlite.connect('database.db') as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM students")
            cur = cursor.fetchall()

            self.tableWidget.setRowCount(0)
            for i, row in enumerate(cur):
                self.tableWidget.insertRow(i)
                for j, val in enumerate(row):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))


app = QtWidgets.QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())
