# -*- coding: utf-8 -*-
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
import resource
from model import Model
from darknet_video_cbbox import Ui_OutputDialog
from tp_data import Ui_DataDialog


class Ui_Dialog(QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        loadUi("mainwindow.ui", self)

        self.model = Model()
        # Creates clicks events for Browse and Run
        self.browseButton.clicked.connect(self.browseSlot)
        self.runButton.clicked.connect(self.runSlot)
        self.dataButton.clicked.connect(self.dataSlot)
        
        self._new_window = None
        self.filename = None

    def refreshAll(self):
        """
        Set the text of lineEdit once it's valid
        """
        self.lineEdit.setText(self.model.getFileName())

    @pyqtSlot()
    def browseSlot(self):
        """
        Called when the user presses the Browse button
        """
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Browse File",
            "",
            "Video Files (*.mp4)",
            options=options)
        if fileName:
            self.model.setFileName(fileName)
            self.refreshAll()
            self.filename = fileName

    @pyqtSlot()
    def runSlot(self):
        """
        Called when the user presses the Run button
        """
        print("Clicked Run")
        # ui.hide()  # hide the main window
        self.outputWindow()  # Create and open new output window

    @pyqtSlot()
    def dataSlot(self):
        """
        Called when the user presses the Run button
        """
        print("Clicked Run")
        # ui.hide()  # hide the main window
        self.outputWindow2()  # Create and open new data window

    def outputWindow(self):
        """
        Created new window for vidual output of the video in GUI
        """
        self._new_window = Ui_OutputDialog()
        self._new_window.show()
        self._new_window.YOLO(self.filename)
        print("Video Played")

    def outputWindow2(self):
        """
        Created new window for vidual output of the video in GUI
        """
        self._new_window = Ui_DataDialog()
        self._new_window.show()
        print("Data Showed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())
