# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../qt/video_player/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(831, 461)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.play = QtWidgets.QPushButton(self.centralWidget)
        self.play.setGeometry(QtCore.QRect(360, 370, 89, 25))
        self.play.setObjectName("play")
        self.video_view = QtWidgets.QLabel(self.centralWidget)
        self.video_view.setGeometry(QtCore.QRect(20, 20, 541, 261))
        self.video_view.setAlignment(QtCore.Qt.AlignCenter)
        self.video_view.setObjectName("video_view")
        self.res_list = QtWidgets.QListWidget(self.centralWidget)
        self.res_list.setGeometry(QtCore.QRect(600, 20, 201, 261))
        self.res_list.setObjectName("res_list")
        self.pause = QtWidgets.QPushButton(self.centralWidget)
        self.pause.setGeometry(QtCore.QRect(470, 370, 89, 25))
        self.pause.setObjectName("pause")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 831, 28))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.play.setText(_translate("MainWindow", "play"))
        self.video_view.setText(_translate("MainWindow", "drag video here"))
        self.pause.setText(_translate("MainWindow", "pause"))

