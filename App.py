import sys
from addcoursedialog import Ui_Dialog
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from database import database
import os
import sqlite3 as sqlite
import cv2


def get_gray_scale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        loadUi("ui/App.ui", self)
        self.capture = False
        self.value = 1
        self.buttonOpenCamera.clicked.connect(self.onclicked)
        self.buttonCapture.clicked.connect(self.captureClicked)
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

    def onclicked(self):
        cap = cv2.VideoCapture(0)
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                gray = get_gray_scale(frame)
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                bound = (0, 0, 0, 0)
                for (x, y, w, h) in faces:
                    self.displayImage(cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2))
                    bound = (x, y, w, h)

                self.displayImage(frame)

                # facedeneme.detectRecognition()

                if self.capture:
                    print("capture is clicked")
                    self.value += 1
                    grayScale = get_gray_scale(frame)
                    print(type(grayScale))
                    cv2.imwrite("./images/%s.png" % self.value, grayScale[y:bound[1] + bound[3], x:bound[0] + bound[2]])
                    self.capture = False
                    print("image saved")
            else:
                print("not found")
        cap.release()
        cv2.destroyAllWindows()

    def captureClicked(self):
        self.capture = True

    def displayImage(self, img):

        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.imgLabel.setPixmap(QPixmap.fromImage(img))
        self.imgLabel.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        QApplication.processEvents()

    def insertStudent(self):
        print(self.db)
        print(self.nameLineEdit.text(),
              self.surnameLineEdit.text(), self.schoolNumberLineEdit.text(), self.facultyLineEdit.text(),
              self.departmentLineEdit.text())

        flag = self.db.insertStudent(self.nameLineEdit.text(),
                                     self.surnameLineEdit.text(), self.schoolNumberLineEdit.text(),
                                     self.facultyLineEdit.text(), self.departmentLineEdit.text(),
                                     self.imagePathLineEdit.text())
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        print(flag)
        if flag:
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
        self.imagePathLineEdit.clear()

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
            cursor.execute("PRAGMA table_info(students)")
            cur = cursor.fetchall()
            headers = []
            for i in range(len(cur)):
                headers.append(cur[i][1])
            self.tableWidget.setHorizontalHeaderLabels(headers)
            cursor.execute("SELECT * FROM students")
            cur = cursor.fetchall()

            self.tableWidget.setRowCount(0)
            for i, row in enumerate(cur):
                self.tableWidget.insertRow(i)
                for j, val in enumerate(row):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))

    '''def onclicked(self):
        cap = cv2.VideoCapture(-1)
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                gray = get_gray_scale(frame)
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                bound = (0, 0, 0, 0)
                for (x, y, w, h) in faces:
                    self.displayImage(cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2))
                    bound = (x, y, w, h)

                self.displayImage(frame)

                # facedeneme.detectRecognition()

                if self.capture:
                    print("capture is clicked")
                    self.value += 1
                    grayScale = get_gray_scale(frame)
                    imagePath = f"./images/{self.nameLineEdit.text()}.png"
                    cv2.imwrite(imagePath,
                                grayScale[bound[1]:bound[1] + bound[3], bound[0]:bound[0] + bound[2]])
                    self.imagePathLineEdit.setText(imagePath)
                    self.capture = False
                    print("image saved")
            else:
                print("not found")
        cap.release()
        cv2.destroyAllWindows()

    '''
    def captureClicked(self):
        self.capture = True

    def displayImage(self, img):

        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if (img.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.imgLabel.setPixmap(QPixmap.fromImage(img))
        self.imgLabel.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        QApplication.processEvents()


app = QtWidgets.QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())
