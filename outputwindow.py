# -*- coding: utf-8 -*-
import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QApplication, QDialog
import resource
import cv2


class Ui_OutputDialog(QDialog):
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        loadUi("outputwindow.ui", self)
        self.image = None

    @pyqtSlot()
    def startVideo(self, filename):
        # print(filename)
        self.capture = cv2.VideoCapture(filename)
        # self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # print("timer start")
        self.timer = QTimer(self)  # Create Timer
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(40)  # emit the timeout() signal at x=40ms

    def update_frame(self):
        ret, self.image = self.capture.read()
        # print("Frame Updated")
        self.displayImage(self.image, 1)
        # print("Frame Displayed")

    def displayImage(self, image, window=1):
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    oui = Ui_OutputDialog()
    oui.show()
    sys.exit(app.exec_())
