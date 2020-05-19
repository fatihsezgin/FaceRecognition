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
        loadUi("camera.ui", self)
        self.capture = False
        self.value = 1
        self.buttonOpenCamera.clicked.connect(self.onclicked)
        self.buttonCapture.clicked.connect(self.captureClicked)

    #@pyqtSlot
    def onclicked(self):
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                print("here")
                cv2.waitKey()
                self.displayImage(frame, 1)
                if(self.capture):
                    print("capture is clicked")
                    self.value = self.value + 1
                    cv2.imwrite("./%s.png" % (self.value), frame)
                    self.capture = False
                    print("image saved")
            else:
                print("not found")
        cap.release()
        cv2.destroyAllWindows()

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
