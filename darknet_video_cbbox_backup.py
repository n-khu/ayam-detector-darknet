################################################################
# Modified by Augmented Startups & Geeky Bee AI
# Application: Object Detection
# Interface  : PyQT5
#belum bisa threshold slider, checkbox uncompleted
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

# Imports for PyQT5 interface
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QLCDNumber
from PyQt5.uic import loadUi


# Create class "Ui_OutputDialog" for each application we've made within the course
class Ui_OutputDialog(QDialog):
    """
    This class is inhertied from QDialog as we're using QDialog for our GUI Interface. 
    """
    def __init__(self):
        super(Ui_OutputDialog, self).__init__()
        # Load the ui of output window
        loadUi("outputwindow.ui", self)
        self.image = None
        self.frame_read = None
        self.netMain = None
        self.metaMain = None
        self.altNames = None

    def convertBack(self, x, y, w, h):
        xmin = int(round(x - (w / 2)))
        xmax = int(round(x + (w / 2)))
        ymin = int(round(y - (h / 2)))
        ymax = int(round(y + (h / 2)))
        return xmin, ymin, xmax, ymax


    def cvDrawBoxes(self, detections, img):
        # Colored labels dictionary
        color_dict = {
            'person' : [0, 255, 255], 'bicycle': [238, 123, 158], 'car' : [24, 245, 217], 'motorbike' : [224, 119, 227],
            'aeroplane' : [154, 52, 104], 'bus' : [179, 50, 247], 'train' : [180, 164, 5], 'truck' : [82, 42, 106],
            'boat' : [201, 25, 52], 'traffic light' : [62, 17, 209], 'fire hydrant' : [60, 68, 169], 'stop sign' : [199, 113, 167],
            'parking meter' : [19, 71, 68], 'bench' : [161, 83, 182], 'bird' : [75, 6, 145], 'cat' : [100, 64, 151],
            'dog' : [156, 116, 171], 'horse' : [88, 9, 123], 'sheep' : [181, 86, 222], 'cow' : [116, 238, 87],'elephant' : [74, 90, 143],
            'bear' : [249, 157, 47], 'zebra' : [26, 101, 131], 'giraffe' : [195, 130, 181], 'backpack' : [242, 52, 233],
            'umbrella' : [131, 11, 189], 'handbag' : [221, 229, 176], 'tie' : [193, 56, 44], 'suitcase' : [139, 53, 137],
            'frisbee' : [102, 208, 40], 'skis' : [61, 50, 7], 'snowboard' : [65, 82, 186], 'sports ball' : [65, 82, 186],
            'kite' : [153, 254, 81],'baseball bat' : [233, 80, 195],'baseball glove' : [165, 179, 213],'skateboard' : [57, 65, 211],
            'surfboard' : [98, 255, 164],'tennis racket' : [205, 219, 146],'bottle' : [140, 138, 172],'wine glass' : [23, 53, 119],
            'cup' : [102, 215, 88],'fork' : [198, 204, 245],'knife' : [183, 132, 233],'spoon' : [14, 87, 125],
            'bowl' : [221, 43, 104],'banana' : [181, 215, 6],'apple' : [16, 139, 183],'sandwich' : [150, 136, 166],'orange' : [219, 144, 1],
            'broccoli' : [123, 226, 195],'carrot' : [230, 45, 209],'hot dog' : [252, 215, 56],'pizza' : [234, 170, 131],
            'donut' : [36, 208, 234],'cake' : [19, 24, 2],'chair' : [115, 184, 234],'sofa' : [125, 238, 12],
            'pottedplant' : [57, 226, 76],'bed' : [77, 31, 134],'diningtable' : [208, 202, 204],'toilet' : [208, 202, 204],
            'tvmonitor' : [208, 202, 204],'laptop' : [159, 149, 163],'mouse' : [148, 148, 87],'remote' : [171, 107, 183],
            'keyboard' : [33, 154, 135],'cell phone' : [206, 209, 108],'microwave' : [206, 209, 108],'oven' : [97, 246, 15],
            'toaster' : [147, 140, 184],'sink' : [157, 58, 24],'refrigerator' : [117, 145, 137],'book' : [155, 129, 244],
            'clock' : [53, 61, 6],'vase' : [145, 75, 152],'scissors' : [8, 140, 38],'teddy bear' : [37, 61, 220],
            'hair drier' : [129, 12, 229],'toothbrush' : [11, 126, 158]
        }
        
        # for detection in detections:
        #     x, y, w, h = detection[2][0],\
        #         detection[2][1],\
        #         detection[2][2],\
        #         detection[2][3]
        #     name_tag = str(detection[0].decode())
        for label, confidence, bbox in detections:
            x, y, w, h = (bbox[0],
                    bbox[1],
                    bbox[2],
                    bbox[3])
            name_tag = label
            for name_key, color_val in color_dict.items():
                if name_key == name_tag:

                    if(self.personCheckBox.isChecked()):
                        print("people are checked")
                    if(self.carCheckBox.isChecked()):
                        print("car are checked")

                    # name_tag = name_tag +  " (" + str(round(detection[1] * 100, 2)) + "%)"
                    name_tag = name_tag +  " (" + str(round(bbox[1] * 100, 2)) + "%)"
                    color = color_val 
                    xmin, ymin, xmax, ymax = self.convertBack(
                    float(x), float(y), float(w), float(h))
                    pt1 = (xmin, ymin)
                    pt2 = (xmax, ymax)
                    # Create bbox
                    cv2.rectangle(img, pt1, pt2, color, 1)
                    (test_width, text_height), baseline = cv2.getTextSize(name_tag, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                    # Create filled bbox
                    cv2.rectangle(img,
                          pt1,(pt1[0] + test_width, pt1[1] - text_height - baseline),
                          color,
                          thickness=cv2.FILLED)
                    cv2.putText(img,
                                name_tag, 
                                (pt1[0], pt1[1] - baseline), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (0,0,0), 2)
        return img


    # netMain = None
    # metaMain = None
    # altNames = None


    def YOLO(self, filename):
        """
        Perform Object detection
        """
        global metaMain, netMain, altNames
        configPath = "./cfg/yolov3-tiny.cfg"
        weightPath = "./yolov3-tiny.weights"
        metaPath = "./cfg/coco.data"
        if not os.path.exists(configPath):
            raise ValueError("Invalid config path `" +
                             os.path.abspath(configPath) + "`")
        if not os.path.exists(weightPath):
            raise ValueError("Invalid weight path `" +
                             os.path.abspath(weightPath) + "`")
        if not os.path.exists(metaPath):
            raise ValueError("Invalid data file path `" +
                             os.path.abspath(metaPath) + "`")

        self.network, self.class_names, self.class_colors = darknet.load_network(configPath,  metaPath, weightPath, batch_size=1)
        # if self.netMain is None:
        #     self.netMain = darknet.load_net_custom(configPath.encode(
        #         "ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
        # if self.metaMain is None:
        #     self.metaMain = darknet.load_meta(metaPath.encode("ascii"))
        if self.altNames is None:
            try:
                with open(metaPath) as metaFH:
                    metaContents = metaFH.read()
                    import re
                    match = re.search("names *= *(.*)$", metaContents,
                                      re.IGNORECASE | re.MULTILINE)
                    if match:
                        result = match.group(1)
                    else:
                        result = None
                    try:
                        if os.path.exists(result):
                            with open(result) as namesFH:
                                namesList = namesFH.read().strip().split("\n")
                                self.altNames = [x.strip() for x in namesList]
                    except TypeError:
                        pass
            except Exception:
                pass
        self.cap = cv2.VideoCapture(filename)
        # cap = cv2.VideoCapture("./Input/test1.mp4")
        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))
        # self.new_height, self.new_width = self.frame_height // 2, self.frame_width // 2
        self.new_height, self.new_width = self.frame_height, self.frame_width
        # print("Video Reolution: ",(width, height))
        self.output_filename = os.path.join(os.path.dirname(filename), os.path.basename(filename)[:-4]) + "_output.avi"
        self.out = cv2.VideoWriter(
            self.output_filename, cv2.VideoWriter_fourcc(*"MJPG"), 10.0,
            (self.new_width, self.new_height))

        # print("Starting the YOLO loop...")

        # Create an image we reuse for each detect
        self.darknet_image = darknet.make_image(self.new_width, self.new_height, 3)

        # Create QTimer for Frame updating Frames
        self.timer = QTimer(self)  # Create Timer
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(40)  # emit the timeout() signal at x=40ms                                
    
    def update_frame(self):
        ret, self.frame_read = self.cap.read() 
        if not ret:
            sys.exit() 
        self.displayImage(self.frame_read, 1)

    def displayImage(self, frame_read, window=1):
        self.frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
        self.frame_resized = cv2.resize(self.frame_rgb,
                                        (self.new_width, self.new_height),
                                        interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(self.darknet_image, self.frame_resized.tobytes())

        # threshValue = self.ThresSlider.value()/100
        # print(str(self.ThresSlider.value()))

        # self.detections = darknet.detect_image(self.netMain, self.metaMain, self.darknet_image, thresh=0.25)
        self.detections = darknet.detect_image(self.network, self.class_names, self.darknet_image, thresh=0.25)

        # print(len(self.detections))
        self.lcdNumber.display(len(self.detections))

        self.image = self.cvDrawBoxes(self.detections, self.frame_resized)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # cv2.imshow("window", self.image)
        
        # Note: QT doesn't support cv2 image directly
        # We've to convert that into QImage
        qformat = QImage.Format_Indexed8
        if len(self.image.shape) == 3:
            if self.image is None:
                sys.exit()
            if self.image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(self.image, self.new_width, self.new_height, self.image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)

        self.out.write(self.image)

        # self.cap.release()
        # self.out.release()
        print(":::Video Write Completed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    oui = Ui_OutputDialog()
    oui.show()
    sys.exit(app.exec_())
