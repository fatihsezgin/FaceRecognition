# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/App.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from addcoursedialog import Ui_Dialog
from PyQt5.QtWidgets import QMessageBox
from database import database
import os
import sqlite3 as sqlite



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1014, 703)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.CoursesTab = QtWidgets.QWidget()
        self.CoursesTab.setObjectName("CoursesTab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.CoursesTab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(self.CoursesTab)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMinimumSize(QtCore.QSize(256, 0))
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.pBOpenCourseAddDialog = QtWidgets.QPushButton(self.CoursesTab)
        self.pBOpenCourseAddDialog.setObjectName("pBOpenCourseAddDialog")
        self.verticalLayout.addWidget(self.pBOpenCourseAddDialog)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tableWidget = QtWidgets.QTableWidget(self.CoursesTab)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(5)
        self.verticalLayout_3.addWidget(self.tableWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.CoursesTab)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.tabWidget.addTab(self.CoursesTab, "")
        self.StudentTab = QtWidgets.QWidget()
        self.StudentTab.setObjectName("StudentTab")
        self.formLayoutWidget = QtWidgets.QWidget(self.StudentTab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 281, 431))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.nameLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.nameLabel.setObjectName("nameLabel")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.nameLabel)
        self.nameLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.nameLineEdit)
        self.surnameLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.surnameLabel.setObjectName("surnameLabel")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.surnameLabel)
        self.surnameLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.surnameLineEdit.setObjectName("surnameLineEdit")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.surnameLineEdit)
        self.schoolNumberLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.schoolNumberLabel.setObjectName("schoolNumberLabel")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.schoolNumberLabel)
        self.schoolNumberLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.schoolNumberLineEdit.setObjectName("schoolNumberLineEdit")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.schoolNumberLineEdit)
        self.facultyLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.facultyLabel.setObjectName("facultyLabel")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.facultyLabel)
        self.facultyLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.facultyLineEdit.setObjectName("facultyLineEdit")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.facultyLineEdit)
        self.departmentLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.departmentLabel.setObjectName("departmentLabel")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.LabelRole, self.departmentLabel)
        self.departmentLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.departmentLineEdit.setObjectName("departmentLineEdit")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.FieldRole, self.departmentLineEdit)
        self.buttonAddImage = QtWidgets.QPushButton(self.formLayoutWidget)
        self.buttonAddImage.setObjectName("buttonAddImage")
        self.formLayout.setWidget(
            5, QtWidgets.QFormLayout.FieldRole, self.buttonAddImage)
        self.buttonDbSave = QtWidgets.QPushButton(self.formLayoutWidget)
        self.buttonDbSave.setObjectName("buttonDbSave")
        self.formLayout.setWidget(
            6, QtWidgets.QFormLayout.FieldRole, self.buttonDbSave)
        self.tabWidget.addTab(self.StudentTab, "")
        self.horizontalLayout_3.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1014, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.db = database()
        self.getDataForList()

        # signal slots
        self.pBOpenCourseAddDialog.clicked.connect(self.addCourseClicked)
        self.buttonDbSave.clicked.connect(self.insertStudent)
        self.tabWidget.currentChanged.connect(self.getDataForList)

    def addCourseClicked(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()


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
    
    def getDataForList(self):
        if(self.tabWidget.currentIndex() == 0):
            self.listWidget.clear()
            fillCourses(self)
            fillStudents(self)
            QtWidgets.QApplication.processEvents()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pBOpenCourseAddDialog.setText(
            _translate("MainWindow", "Add Course"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.CoursesTab), _translate("MainWindow", "Courses"))
        self.nameLabel.setText(_translate("MainWindow", "Name"))
        self.surnameLabel.setText(_translate("MainWindow", "Surname"))
        self.schoolNumberLabel.setText(
            _translate("MainWindow", "SchoolNumber"))
        self.facultyLabel.setText(_translate("MainWindow", "Faculty"))
        self.departmentLabel.setText(_translate("MainWindow", "Department"))
        self.buttonAddImage.setText(_translate("MainWindow", "Add Image"))
        self.buttonDbSave.setText(_translate("MainWindow", "Save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.StudentTab), _translate("MainWindow", "Student"))


def fillCourses(self):
    
    # get all files' and folders' names in the current directory
    filenames = os.listdir("./courses/")
    print(filenames)
    self.listWidget.addItems(filenames)
    #QApplication.processEvents()

    

def fillStudents(self):
    with sqlite.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM students")
        cur=cursor.fetchall()
        
        self.tableWidget.setRowCount(0)
        for i,row in enumerate(cur):
            self.tableWidget.insertRow(i)
            for j,val in enumerate(row):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
