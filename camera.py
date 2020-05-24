import sys
import numpy as np

import cv2
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi 


class camera(QDialog):
    def __init__(self):
        super(camera, self).__init__()
        loadUi("ui/camera.ui", self)
        self.capture = False
        self.value = 1
        self.buttonOpenCamera.clicked.connect(self.onclicked)
        self.buttonCapture.clicked.connect(self.captureClicked)

    #@pyqtSlot
    def onclicked(self):
        cap = cv2.VideoCapture(0)
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                gray = self.get_gray_scale(frame)
                faces = faceCascade.detectMultiScale(
                    gray, 
                    scaleFactor =1.1,
                    minNeighbors =5,
                    minSize =(30,30),
                    flags =cv2.CASCADE_SCALE_IMAGE
                )
                bound = (0,0,0,0)
                for (x, y, w, h) in faces:    
                    self.displayImage(cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2), 1)
                    bound=(x, y, w, h)
                
                if(self.capture):
                    print("capture is clicked")
                    self.value += 1
                    grayScale = self.get_gray_scale(frame)
                    cv2.imwrite("./%s.png" % (self.value), grayScale[y:bound[1]+bound[3], x:bound[0]+bound[2]])
                    self.capture = False
                    print("image saved")
            else:
                print("not found")
        cap.release()
        cv2.destroyAllWindows()


    def get_gray_scale(self,frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    def captureClicked(self):
        self.capture = True

    def displayImage(self, img, window=1):
        
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if(img.shape[2]) == 4:
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
