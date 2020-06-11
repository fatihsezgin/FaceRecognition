import sys
from addcoursedialog import Ui_Dialog
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialogButtonBox, QFileDialog, QLineEdit
from PyQt5.uic import loadUi
from database import database
import os
import cv2
import facerecognition as fr


def get_gray_scale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        loadUi("ui/App.ui", self)
        self.capture = False
        self.captureCount = 0
        self.buttonOpenCamera.clicked.connect(self.onclicked)
        self.buttonCapture.clicked.connect(self.captureClicked)
        self.db = database()
        self.pBOpenCourseAddDialog.clicked.connect(self.addCourseClicked)
        self.buttonDbSave.clicked.connect(self.insertStudent)
        self.tabWidget.currentChanged.connect(self.getDataForList)
        self.listWidget.itemClicked.connect(self.getCourseStudents)
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.assignStudentToCourse)
        self.getDataForList()
        self.frameList = []
        print(self.db.getStudentsForCourse(1)[1][3])
        self.buttonAddImage.clicked.connect(self.openFileNameDialog)
        self.imagePathLineEdit.setEnabled(False)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;", options=options)
        if fileName:
            self.imagePathLineEdit.setText(fileName)


    def addCourseClicked(self):
        ui = Ui_Dialog()
        ui.show()
        ui.exec_()
        self.fillCourses()
        QApplication.processEvents()

    def getCourseStudents(self):
        self.courseStudentTable.setHorizontalHeaderLabels(self.db.getStudentsTableHeaders())
        courseId = self.db.getCourseId(self.listWidget.currentItem().text())
        cur = self.db.getStudentsForCourse(courseId)
        self.courseStudentTable.setRowCount(0)
        for i, row in enumerate(cur):
            self.courseStudentTable.insertRow(i)
            for j, val in enumerate(row):
                self.courseStudentTable.setItem(i, j-3, QtWidgets.QTableWidgetItem(str(val)))

    def fillStudents(self):
        self.allStudentTable.setHorizontalHeaderLabels(self.db.getStudentsTableHeaders())
        cur = self.db.getAllStudents()
        self.allStudentTable.setRowCount(0)
        for i, row in enumerate(cur):
            self.allStudentTable.insertRow(i)
            for j, val in enumerate(row):
                self.allStudentTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))

    def assignStudentToCourse(self):
        studentId = self.allStudentTable.item(self.allStudentTable.currentRow(), 0).text()
        courseId = self.db.getCourseId(self.listWidget.currentItem().text())
        #for i in self.db.getStudentsForCourse(courseId):
            #i[3] is the studentid



        result = self.db.insertCourseStudent(courseId, studentId)
        if result:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Student is successfully inserted into Course")
            msgBox.setWindowTitle("Success")
            msgBox.exec()
        self.getCourseStudents()

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
        self.listWidget.addItems(self.db.getCourses())

        '''filenames = os.listdir("./courses/")
        print(filenames)
        self.listWidget.addItems(filenames)
        '''
        # QApplication.processEvents()

    def onclicked(self):
        cap = cv2.VideoCapture(-1)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                bound, croppedFrame = fr.detect_faces(frame)
                self.displayImage(cv2.rectangle(frame, (bound[0], bound[1]), (bound[0] + bound[2], bound[1] + bound[3]),
                                                (0, 255, 0), 2))
                if self.capture:
                    print("capture is clicked")
                    self.imageCountLabel.setText("Please take " + str(3 - self.captureCount) + " images for finding the optimum image")
                    if self.captureCount < 4:
                        self.captureCount += 1
                        bound, capturedFace = fr.detect_faces(frame)
                        self.frameList.append(capturedFace)
                        self.capture = False

                        if self.captureCount == 4:
                            print(self.frameList)
                            self.captureCount = 0
                            optimizedPhoto = fr.optimize(self.frameList)
                            lbp = fr.get_lbp(optimizedPhoto)
                            histogram = fr.cal_histogram(lbp)
                            try:
                                os.mkdir(f"./images/{self.schoolNumberLineEdit.text()}")
                                with open(f"./histograms/{self.schoolNumberLineEdit.text()}.txt", 'w') as file_handler:
                                    file_handler.write("\n".join(str(item) for item in histogram))
                            except FileExistsError:
                                pass
                            imagePath = f"./images/{self.schoolNumberLineEdit.text()}/{self.nameLineEdit.text()}.png"
                            cv2.imwrite(imagePath, optimizedPhoto)
                            self.imagePathLineEdit.setText(imagePath)
                            print("optimize edilmiş foto kaydedildi")
                            self.frameList.clear()
            else:
                print("not found")
        cap.release()
        cv2.destroyAllWindows()


app = QtWidgets.QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())
