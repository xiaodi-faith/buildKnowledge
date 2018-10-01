#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from os import walk, path
import os
import pickle
import string

class ExampleWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.fname = 'f:/'
        self.selectedFold = ''
        self.selectedFile = ''
        self.selectedTypeFile = ''
        self.selectedTypeFold = ''
        self.saveFlag = False

        self.setMinimumSize(QSize(970, 500))
        self.setMaximumSize(QSize(970, 500))
        self.setWindowTitle("buildKnowledge")

        self.textEdit = QPlainTextEdit(self)
        self.textEdit.setStyleSheet(
            """QPlainTextEdit {background-color: #333;
                               color: #ffffff;
                               font-family: Courier;}""")
        self.textEdit.setTabStopWidth(32)
        self.textEdit.insertPlainText('this is a test')
        self.textEdit.move(390,30)
        self.textEdit.resize(570,440)

        self.treeWidget = QTreeWidget(self)
        self.treeWidget.setObjectName('treeWidget')
        self.treeWidget.setHeaderLabel('paper')

        self.treeWidget.itemClicked['QTreeWidgetItem*', 'int'].connect(self.treeSelected)

        self.treeWidget.move(180, 30)
        self.treeWidget.resize(200,440)

        self.treeWidgetType = QTreeWidget(self)
        self.treeWidgetType.setObjectName('treeWidgetType')
        self.treeWidgetType.setHeaderLabel('paperType')

        self.treeWidgetType.itemClicked['QTreeWidgetItem*', 'int'].connect(self.treeTypeSelected)

        self.treeWidgetType.move(10, 30)
        self.treeWidgetType.resize(170, 440)

        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit Application')
        exitAct.triggered.connect(qApp.quit)

        openFile = QAction('&Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.openFile)

        saveFile = QAction('&Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.saveFile)

        refreshEditText = QAction('&Refrash', self)
        refreshEditText.setShortcut('Ctrl+E')
        refreshEditText.setStatusTip('Refrash Edit')
        refreshEditText.triggered.connect(self.refreshEditText)

        self.statusBar()

        self.openDefaultType()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(exitAct)
        fileMenu = menubar.addMenu('&Edit')
        fileMenu.addAction(refreshEditText)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.time)
        self.timer.start(7000)

    def refreshEditText(self):
        selectedFile = self.selectedFile[:self.selectedFile.find('.')]
        saveFileName = self.selectedTypeFold + '/' + self.selectedFold + '/' + selectedFile + '.pkl'
        try:
            with open(saveFileName, 'rb') as file:
                editText = pickle.load(file)
                self.textEdit.clear()
                self.textEdit.insertPlainText(editText)
                file.close()
        except:
            self.statusBar().showMessage('null file')

    def openFile(self):
        self.fname = QFileDialog.getExistingDirectory(self, 'open file', 'f:/readWrite')
        if(self.fname):
            self.treeWidget.clear()

        for (dirpath, dirnames, filenames) in walk(self.fname):
            for fold in dirnames:
                root = QtWidgets.QTreeWidgetItem(self.treeWidgetType)
                root.setText(0, fold)
            break

    def openDefaultType(self):
        self.fname = 'f:/readWrite'
        if(self.fname):
            self.treeWidget.clear()

        for (dirpath, dirnames, filenames) in walk(self.fname):
            for fold in dirnames:
                root = QtWidgets.QTreeWidgetItem(self.treeWidgetType)
                root.setText(0, fold)
            break

    def saveFile(self):
        #saveFileName = QFileDialog.getSaveFileName(self, 'save file', 'f:/')
        selectedFile = self.selectedFile[:self.selectedFile.find('.')]
        saveFileName = self.selectedTypeFold+'/'+self.selectedFold +'/'+selectedFile+'.pkl'
        file = open(saveFileName, 'wb')
        pickle.dump(self.textEdit.document().toPlainText(), file)
        file.close()

        #self.treeTypeSelected()
        self.statusBar().showMessage('save successfully')

    def treeSelected(self):
        list_selected = self.treeWidget.selectedItems()
        for li in list_selected:
            self.statusBar().showMessage(li.text(0))
            if(li.parent()):
                self.selectedFold = li.parent().text(0)
            self.selectedFile = li.text(0)
            selectedFile = self.selectedFile[self.selectedFile.find('.')+1:]
            if(selectedFile == 'pkl'):
                self.refreshEditText()
                self.saveFlag = True
            if(selectedFile == 'pdf'):
                pdfFile = self.selectedTypeFold + '/' + self.selectedFold + '/' + self.selectedFile
                os.startfile(pdfFile)

    def treeTypeSelected(self):
        listType_selected = self.treeWidgetType.selectedItems()
        for li in listType_selected:
            self.statusBar().showMessage(li.text(0))
            self.selectedTypeFile = li.text(0)
            self.selectedTypeFold = self.fname +'/'+self.selectedTypeFile
            self.treeWidget.clear()
            for (dirpath, dirnames, filenames) in walk(self.selectedTypeFold):
                root = None
                index_f = dirpath.find('\\')
                if (index_f == -1):
                    continue
                else:
                    root = QtWidgets.QTreeWidgetItem(self.treeWidget)
                    root.setText(0, dirpath[index_f + 1:])
                    for child_file in filenames:
                        child = QTreeWidgetItem(root)
                        child.setText(0, child_file)
        self.saveFlag = False


    def time(self):
        if(self.saveFlag):
            self.saveFile()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = ExampleWindow()
    mainWin.show()
    sys.exit( app.exec_() )