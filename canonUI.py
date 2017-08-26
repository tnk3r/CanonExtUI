#!/usr/bin/python
import serial, time, os, sys, socket

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal, QThread

class canonController(QThread):
    connected = pyqtSignal(str)
    sliderInt = pyqtSignal(int)
    closer = 0

    def __init__(self):
        QThread.__init__(self, parent=None)
        self.connected = 0
        self.openConnectionUSB()

    def openConnectionUSB(self):
        try:
            for i in range(4):
                self.serial = serial.Serial("/dev/ttyUSB"+str(i), 9600)
                break
        except StandardError as msg:
            print str(msg)

    def send(self, command):
        try:
            self.serial.write(str(command)+"\n")
        except StandardError as msg:
            print str(msg)

    def openIris(self):
        self.send("o")
        self.closer = self.closer + 50
        self.sliderInt.emit(self.closer)

    def closeIris(self):
        self.send("c")
        self.closer = self.closer - 50
        self.sliderInt.emit(self.closer)

    def openIrisSlider(self):
        for i in range(1):
            self.send("o")

    def closeIrisSlider(self):
        for i in range(1):
            self.send("c")

    def wideOpen(self):
        self.send("f")
        self.sliderInt.emit(1000)
        self.closer = 1000

class Window(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setFixedSize(800, 480)
        self.bg = QtGui.QLabel("", self)
        self.bg.setFixedSize(800, 480)
        self.bg.setStyleSheet("background-image: url(frank2.jpeg);")
        self.bg2 = QtGui.QLabel("", self)
        self.bg2.setFixedSize(800, 480)
        self.bg2.setStyleSheet("border: 8px solid green;")

        self.openIrisButton = QtGui.QPushButton(" Open ", self)
        self.openIrisButton.setStyleSheet(self.buttonstyle())
        self.openIrisButton.move(100, 120)

        self.closeIrisButton = QtGui.QPushButton(" Close  ", self)
        self.closeIrisButton.setStyleSheet(self.buttonstyle())
        self.closeIrisButton.move(300, 120)

        self.wideOpenButton = QtGui.QPushButton(" Wide open ", self)
        self.wideOpenButton.setStyleSheet(self.buttonstyle())
        self.wideOpenButton.move(500, 120)

        self.titleLabel = QtGui.QLabel("CanonEXT Kontrol", self)
        self.titleLabel.move(250, 50)
        self.titleLabel.setStyleSheet("color: orange; font-size: 30px;")

        self.titleLabel2= QtGui.QLabel("by Alex/tinker", self)
        self.titleLabel2.move(650, 450)
        self.titleLabel2.setStyleSheet("color: lime; font-size: 15px;")

        self.slider = QtGui.QSlider(self)
        self.slider.setMaximum(1000)
        self.slider.setMinimum(0)
        self.slider.move(100, 280)
        self.slider.setFixedSize(600, 150)
        self.slider.setStyleSheet(self.Sliderstylesheet())
        self.slider.sliderMoved.connect(self.setIrisFromSlider)
        self.slider.setOrientation(1)

        self.oldValue = 0
        self.show()
        self.raise_()

        try:
            self.lensController = canonController()
            self.assignFunctions()
        except StandardError as msg:
            print str(msg)

    def assignFunctions(self):
        self.openIrisButton.clicked.connect(self.lensController.openIris)
        self.closeIrisButton.clicked.connect(self.lensController.closeIris)
        self.wideOpenButton.clicked.connect(self.lensController.wideOpen)
        self.lensController.sliderInt.connect(self.slider.setValue)

    def setIrisFromSlider(self):
        if self.oldValue < self.slider.value():
            self.lensController.openIrisSlider()
        if self.oldValue > self.slider.value():
            self.lensController.closeIrisSlider()
        self.oldValue = self.slider.value()

    def buttonstyle(self):
        return """
                QPushButton {
                    color: white;
                    background-color: rgb(50, 50, 50);
                    border-style: solid;
                    border-width: 2px;
                    border-radius: 5px;
                    border-color: white;
                    font: bold 35px;
                    font-style: italic;
                }
                QPushButton::pressed {
                    background-color: rgb(200, 200, 200);
                    border-style: inset;
                }
            """
    def Sliderstylesheet(self):
        return """
            QSlider::groove:horizontal {
                height: 150px;
                border: 0px solid #abc;
                }
            QSlider::sub-page:horizontal {
                background-color: black;
            background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
                    stop: 0 #333, stop: 1 #aaa);
                background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
                    stop: 0 #333, stop: 1 #aaa);
                height: 40px;
            }
            QSlider::add-page:horizontal {
                background: #222;
                border: 2px solid gray;
                height: 40px;
            }
            QSlider::handle:horizontal {
                background-color: black;
                width: 40px;
                border: 2px solid white;
                margin-top: 0px;
                margin-bottom: 0px;
                border-radius: 10px;
            }
        """

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
