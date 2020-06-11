import sys
import numpy as np

import cv2
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView
from PyQt5.uic import loadUi
from database import database
import facerecognition as fr


def get_gray_scale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


class camera(QDialog):
    def __init__(self):
        super(camera, self).__init__()
        loadUi("ui/camera.ui", self)
        self.cap = cv2.VideoCapture(-1)
        self.capture = False
        self.value = 1
        self.db = database()
        self.fillCourses()
        self.buttonCloseCamera.clicked.connect(self.closeCamera)
        self.buttonOpenCamera.clicked.connect(self.onclicked)
        self.buttonTakeAttendance.clicked.connect(self.takeAttendance)

    def takeAttendance(self):
        self.capture = True

    def closeCamera(self):
        self.imgLabel.clear()
        self.cap.release()
        cv2.destroyAllWindows()

    def fillCourses(self):
        # get all files' and folders' names in the current directory
        self.listWidget.clear()
        self.listWidget.addItems(self.db.getCourses())

    # @pyqtSlot
    def onclicked(self):
        courseId = self.db.getCourseId(self.listWidget.currentItem().text())
        self.db.createSession(courseId)
        self.listWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                bound, croppedFace = fr.detect_faces(frame)
                self.displayImage(cv2.rectangle(frame, (bound[0], bound[1]), (bound[0] + bound[2], bound[1] + bound[3]),
                                                (0, 255, 0), 2))
                if self.capture:
                    lbp = fr.get_lbp(croppedFace)
                    courseId = self.db.getCourseId(self.listWidget.currentItem().text())
                    histogram = fr.cal_histogram(lbp)
                    ids = self.db.getStudentIdsForCourse(courseId)
                    size = len(ids)
                    mindistance = fr.compare_histograms(histogram, np.loadtxt("histograms/"+str(ids[0])+".txt"))
                    minindex = 0
                    for index in range(size-1):
                        studentNo = ids[index+1]
                        data = np.loadtxt("histograms/"+str(studentNo)+".txt")
                        distance = fr.compare_histograms(histogram, data)
                        if distance < mindistance:
                            mindistance = distance
                            minindex = index

                    if mindistance > 1.0:
                        print('similar face not found')
                    else:
                        print(ids[minindex])

                    self.capture = False
                '''gray = get_gray_scale(frame)
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

                if self.capture:
                    print("capture is clicked")
                    self.value += 1
                    grayScale = get_gray_scale(frame)
                    print(type(grayScale))
                    cv2.imwrite("./images/%s.png" % self.value, grayScale[y:bound[1] + bound[3], x:bound[0] + bound[2]])
                    self.capture = False
                    print("image saved")'''
            else:
                print("not found")
        self.cap.release()
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


app = QtWidgets.QApplication(sys.argv)
window = camera()
window.show()
sys.exit(app.exec_())
