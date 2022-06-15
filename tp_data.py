################################################################
# Modified by Nizzah
# Application: Object Detection
# Interface  : PyQT5
################################################################

# Imports for Object Detection Task
from ctypes import *
import math
import random
import os
import cv2
from cv2 import threshold
import numpy as np
import time
import darknet
import sys

import urllib.request as urllib
import json

# Imports for PyQT5 interface
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
# from mainwindow import Ui_Dialog


# Create class "Ui_OutputDialog" for each application we've made within the course
class Ui_DataDialog(QDialog):
    """
    This class is inhertied from QDialog as we're using QDialog for our GUI Interface. 
    """
    def __init__(self):
        super(Ui_DataDialog, self).__init__()
        # Load the ui of output window
        loadUi("tp.ui", self)

        self.backButton.clicked.connect(self.backSlot)

        self.image = None
        self.frame_read = None
        self.netMain = None
        self.metaMain = None
        self.altNames = None

        channelIDA = "1575829"
        channelIDB = "1735123"
        channelIDC = "1735124"

        with urllib.urlopen("https://api.thingspeak.com/channels/" + channelIDA + "/feeds.json?results=5") as f:
            data = json.load(f)
        
        with urllib.urlopen("https://api.thingspeak.com/channels/" + channelIDB + "/feeds.json?results=5") as f2:
            data2 = json.load(f2)

        with urllib.urlopen("https://api.thingspeak.com/channels/" + channelIDC + "/feeds.json?results=5") as f3:
            data3 = json.load(f3)

        # print(data)

        # Get entries from the response
        entries = data["feeds"]
        entries2 = data2["feeds"]
        entries3 = data3["feeds"]

        # Iterate through each measurement and print value
        for entry in entries:
            # print("field 2 = "+entry['field2'])
            # self.suhu1.label("field 2 = "+entry['field2'])
            # suhu1 = QLabel("field 2 = "+entry['field2'])
            self.suhu1.setText(entry['field1'])
            self.kelembapan1.setText(entry['field2'])
            self.suhu2.setText(entry['field3'])
            self.kelembapan2.setText(entry['field4'])
            self.suhu3.setText(entry['field5'])
            self.kelembapan3.setText(entry['field6'])
            self.ppm.setText(entry['field7'])
            # self.estppm.setText(entry['field8'])

        # Iterate through each measurement and print value
        for entry in entries2:
            # print("field 2 = "+entry['field2'])
            # self.suhu1.label("field 2 = "+entry['field2'])
            # suhu1 = QLabel("field 2 = "+entry['field2'])
            self.suhu1_3.setText(entry['field1'])
            self.kelembapan1_3.setText(entry['field2'])
            self.suhu2_3.setText(entry['field3'])
            self.kelembapan2_3.setText(entry['field4'])
            self.suhu3_3.setText(entry['field5'])
            self.kelembapan3_3.setText(entry['field6'])
            self.ppm_3.setText(entry['field7'])
            # self.estppm_3.setText(entry['field8'])


        # Iterate through each measurement and print value
        for entry in entries3:
            # print("field 2 = "+entry['field2'])
            # self.suhu1.label("field 2 = "+entry['field2'])
            # suhu1 = QLabel("field 2 = "+entry['field2'])
            self.suhu1_4.setText(entry['field1'])
            self.kelembapan1_4.setText(entry['field2'])
            self.suhu2_4.setText(entry['field3'])
            self.kelembapan2_4.setText(entry['field4'])
            self.suhu3_4.setText(entry['field5'])
            self.kelembapan3_4.setText(entry['field6'])
            self.ppm_4.setText(entry['field7'])
            self.estppm_4.setText(entry['field8'])
    
    @pyqtSlot()
    def backSlot(self):
        """
        Called when the user presses the Run button
        """
        print("Clicked Run")
        self.hide()  # hide the main window
        self.back()  # Create and open new data window

    def back(self):
        """
        Created new window for vidual output of the video in GUI
        """
        # self._new_window = Ui_Dialog()
        self.hide()
        print("Homepage")

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    oui = Ui_DataDialog()
    oui.show()
    sys.exit(app.exec_())
