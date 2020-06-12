import sys
from addcoursedialog import Ui_Dialog
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialogButtonBox
from PyQt5.uic import loadUi
from database import database
import os
import cv2
import facerecognition as fr


def get_gray_scale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


"""
    The main class that communicates with UI and includes helper functions in it.
"""
class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        # Opens the default camera, the parameter can be change for different OS
        self.cap = cv2.VideoCapture(0)
        # loads whole UI to the class
        loadUi("ui/App.ui", self)

        # flag that to see if the capture button is clicked
        self.capture = False
        # instance of database connection
        self.db = database()
        # creates the tables if they not exists
        self.db.createTableQueries()
        # capture count for keep record of how many images needed to find and store the optimized image
        self.captureCount = 0

        # Signal / Slot connections, necessarily signals have been connected to functions
        self.buttonCloseCamera.clicked.connect(self.closeCamera)
        self.buttonOpenCamera.clicked.connect(self.onclicked)
        self.buttonCapture.clicked.connect(self.captureClicked)

        self.pBOpenCourseAddDialog.clicked.connect(self.addCourseClicked)  # to open a dialog for entering a new course
        self.buttonDbSave.clicked.connect(self.insertStudent)  # to save the student into db

        # if the current tab changes it's triggers the function, and the function fills the UI
        self.tabWidget.currentChanged.connect(self.getDataForList)
        # in same way any signal triggers the function that fills the related table
        self.listWidget.itemClicked.connect(self.getCourseStudents)
        # to confirm that selected student will be assigned to the selected course
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.assignStudentToCourse)

        # for protection the path that the image is stored will not be editable, but can be seen for confirmation
        self.imagePathLineEdit.setEnabled(False)
        # in the beginning of the app, to fill the UI
        self.getDataForList()

        # a list that keeps the student face credentials up to 4 images.
        # this list is used for finding the optimized image for recognizing the person
        self.frameList = []

        self.courseHistory.addItems(self.db.getCourses())
        self.courseHistory.itemClicked.connect(self.getCourseSessions)
        self.sessionHistory.itemClicked.connect(self.getSessionStudents)
        #self.studentHistory

    # closes the camera
    def closeCamera(self):
        self.imgLabel.clear()
        self.cap.release()
        cv2.destroyAllWindows()

    # for showing the dialog that enables the course insertion
    def addCourseClicked(self):
        ui = Ui_Dialog()
        ui.show()
        ui.exec_()
        self.fillCourses()
        QApplication.processEvents()

    def getCourseSessions(self):
        self.sessionHistory.clear()
        courseId = self.db.getCourseId(self.courseHistory.currentItem().text())
        print(courseId)
        print(self.db.getSessionByCourseId(courseId))
        self.sessionHistory.addItems(self.db.getSessionByCourseId(courseId))

    def getSessionStudents(self):
        self.studentHistory.clear()
        sessionId = self.db.getSessionId(self.sessionHistory.currentItem().text())
        print(sessionId)
        self.studentHistory.addItems(self.db.getStudentsBySession(sessionId))

    # function sets the table of attendances for selected course
    def getCourseStudents(self):
        # table headers is settled
        self.courseStudentTable.setHorizontalHeaderLabels(self.db.getStudentsTableHeaders())
        courseId = self.db.getCourseId(self.listWidget.currentItem().text())
        cur = self.db.getStudentsForCourse(courseId)
        self.courseStudentTable.setRowCount(0)
        for i, row in enumerate(cur):
            self.courseStudentTable.insertRow(i)
            for j, val in enumerate(row):
                # the db query includes a join so the j-3 would fill the table
                self.courseStudentTable.setItem(i, j - 3, QtWidgets.QTableWidgetItem(str(val)))

    # function sets the table of students
    def fillStudents(self):
        self.allStudentTable.setHorizontalHeaderLabels(self.db.getStudentsTableHeaders())
        cur = self.db.getAllStudents()
        self.allStudentTable.setRowCount(0)
        for i, row in enumerate(cur):
            self.allStudentTable.insertRow(i)
            for j, val in enumerate(row):
                self.allStudentTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))

    # to assign any student to any course just function is triggered
    def assignStudentToCourse(self):
        studentId = self.allStudentTable.item(self.allStudentTable.currentRow(), 0).text()
        courseId = self.db.getCourseId(self.listWidget.currentItem().text())
        # for i in self.db.getStudentsForCourse(courseId):
        # i[3] is the studentid

        result = self.db.insertCourseStudent(courseId, studentId)
        if result:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Student is successfully inserted into Course")
            msgBox.setWindowTitle("Success")
            msgBox.exec()
        # lastly updates the UI
        self.getCourseStudents()

    # changes the state of the capture variable. With this variable we can understand that an image from video will be
    # captured.
    def captureClicked(self):
        self.capture = True

    # to display the video into UI,
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

    # for inserting the student into db
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

    # helper function that clears all the form elements for inserting student into db
    def clearStudentLineEdits(self):
        self.nameLineEdit.clear()
        self.surnameLineEdit.clear()
        self.schoolNumberLineEdit.clear()
        self.facultyLineEdit.clear()
        self.departmentLineEdit.clear()
        self.imagePathLineEdit.clear()

    # to pass the first tab will trigger this function
    def getDataForList(self):
        if self.tabWidget.currentIndex() == 0:
            self.listWidget.clear()
            self.fillCourses()
            self.fillStudents()
            self.cap.release()
            self.imgLabel.clear()
            cv2.destroyAllWindows()
            QtWidgets.QApplication.processEvents()

    def fillCourses(self):
        # get all files' and folders' names in the current directory
        self.listWidget.clear()
        self.listWidget.addItems(self.db.getCourses())

    # function that runs when the camera is open
    def onclicked(self):
        print("on clicked")
        self.cap = cv2.VideoCapture(-1)
        while self.cap.isOpened():
            # the read function returns two variables; one for availability and second the frame itself
            ret, frame = self.cap.read()
            # if return value is okay
            if ret:
                # bound of the faces and new cropped image is assigned
                bound, croppedFrame = fr.detect_faces(frame)
                # to see in the UI a rectangle has drawn on image
                self.displayImage(cv2.rectangle(frame, (bound[0], bound[1]), (bound[0] + bound[2], bound[1] + bound[3]),
                                                (0, 255, 0), 2))
                if self.capture:  #
                    print("capture is clicked")
                    self.imageCountLabel.setText(
                        "Please take " + str(3 - self.captureCount) + " images for finding the optimum image")
                    if self.captureCount < 4:
                        self.captureCount += 1
                        bound, capturedFace = fr.detect_faces(frame)
                        self.frameList.append(capturedFace)  # captured face is added to the list.
                        self.capture = False

                        if self.captureCount == 4:
                            print(self.frameList)
                            self.captureCount = 0
                            optimizedPhoto = fr.optimize(self.frameList)  # finds the optimized image
                            lbp = fr.get_lbp(
                                optimizedPhoto)  # implements the Local Binary Pattern Histograms algorithm to image
                            histogram = fr.cal_histogram(lbp)  # histogram that is calculated with the help of LBPH
                            try:
                                # it's creates a file onto images folder with uniquely selected schoolNumber
                                os.mkdir(f"./images/{self.schoolNumberLineEdit.text()}")
                                # the histogram values is also stored into histograms folder
                                with open(f"./histograms/{self.schoolNumberLineEdit.text()}.txt", 'w') as file_handler:
                                    file_handler.write("\n".join(str(item) for item in histogram))
                            except FileExistsError:
                                pass
                            # imagePath is created
                            imagePath = f"./images/{self.schoolNumberLineEdit.text()}/{self.nameLineEdit.text()}.png"
                            cv2.imwrite(imagePath, optimizedPhoto)  # optimized image will be saved
                            self.imagePathLineEdit.setText(imagePath)  # to see the path
                            print("optimize edilmiş foto kaydedildi")
                            self.frameList.clear()  # clear the list
            else:
                print("not found")  # if any frame could not be catched
        self.cap.release()
        cv2.destroyAllWindows()


app = QtWidgets.QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())
