# -*- coding: utf-8 -*-

import sys
from piczip import *
from imaging import Imaging
from pyvin.core import Processor

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

def _toString(qtString):
    return unicode(qtString.toUtf8(),'utf8', 'ignore').encode('gb2312')

version = '1.0.1'
resPath = "res"

class MainWindow(QMainWindow):
    (COLUMN_NAME, COLUMN_PROGRESS, COLUMN_DONE) = range(0, 3)
    SCALE = [0, 2, 4, 8, 16]

    def __init__(self):
        self.tag = MainWindow.__name__
        super( MainWindow, self ).__init__()

        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)

        self.scale = 0
        self.processIdx = 0
        self.img = Imaging()

        # support drag drop
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(QMainWindow, self).dragEnterEvent(event)

    # def dragMoveEvent(self, event):
    #     super(QMainWindow, self).dragMoveEvent(event)

    def dropEvent(self, event):
        print(event.mimeData().text())

        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                path = url.toLocalFile()

                print(_toString(path))
                self.appendItem(path)
            event.acceptProposedAction()
        else:
            super(QMainWindow,self).dropEvent(event)

    def on_scaleChanged(self, scale):
        print(scale)
        if scale < len(MainWindow.SCALE):
            self.scale = MainWindow.SCALE[scale]

    def on_actionTriggered(self, action):
        # print action
        if action == self.ui.actionOpen:
            print('open')
            self.loadFromFile()
        elif action == self.ui.actionClear:
            print('clear')
            self.clearAll()
        elif action == self.ui.actionStart:
            print('start')
            self.startZip()
        elif action == self.ui.actionStop:
            print('stop')
            self.stopZip()
        elif action == self.ui.actionAbout:
            print('about')

    def clearAll(self):
        # self.emit(QtCore.SIGNAL("when_clear()"))
        while self.ui.tableWidget.rowCount() > 0:
            self.ui.tableWidget.removeRow(0)

    def loadFromFile(self):
        fileNames = QtGui.QFileDialog.getOpenFileNames(self,
                "Select picture files", '',
                "Picture Files(*.jpg;*.jpeg;*.png;*.bmp);;All Files (*)")

        if not fileNames:
            return
        for f in fileNames:
            self.appendItem(f)

    def appendItem(self, name, progress='==========', done=''):
        idx = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(idx)

        newItem = QTableWidgetItem(name)
        self.ui.tableWidget.setItem(idx, MainWindow.COLUMN_NAME, newItem)
        newItem = QTableWidgetItem(progress)
        self.ui.tableWidget.setItem(idx, MainWindow.COLUMN_PROGRESS, newItem)
        newItem = QTableWidgetItem(done)
        self.ui.tableWidget.setItem(idx, MainWindow.COLUMN_DONE, newItem)

    def setProgress(self, idx, prog):
        if idx < self.ui.tableWidget.rowCount():
            ppp = ''
            prog /= 10
            for i in range(prog):
                ppp += '>'
            for i in range(10 - prog):
                ppp += '='
            item = self.ui.tableWidget.item(idx, MainWindow.COLUMN_PROGRESS)
            item.setText(ppp)

    def setDone(self, idx, done=True):
        if idx < self.ui.tableWidget.rowCount():
            if done:
                doneStr = ' ^_^ '
            else:
                doneStr = ''
            item = self.ui.tableWidget.item(idx, MainWindow.COLUMN_DONE)
            item.setText(doneStr)

    def showFinishMsgbox(self):
        QMessageBox.information(self, 'Finish', 'Compress Picture')

    def showFinish(self):
        self.emit(QtCore.SIGNAL("show_finish_msg()"))

    def startZip(self):
        self.process = Processor()
        self.process.bind(Processor.EVT_START, self.onStart)
        self.process.bind(Processor.EVT_LOOP, self.onLoop)
        self.process.bind(Processor.EVT_STOP, self.onStop)
        QtCore.QObject.connect(self, QtCore.SIGNAL(_fromUtf8("show_finish_msg()")), self.showFinishMsgbox)

        self.process.start()

    def stopZip(self):
        if self.process:
            self.process.stop()
            self.process = None

    # for callback
    def onStart(self, event):
        print('onStart')

        # clear status
        for i in range(self.ui.tableWidget.rowCount()):
            self.setProgress(i, 0)
            self.setDone(i, False)

        self.processIdx = 0
        return True

    # for callback
    def onLoop(self, event):
        print('onLoop')
        if self.processIdx < self.ui.tableWidget.rowCount():
            item = self.ui.tableWidget.item(self.processIdx, MainWindow.COLUMN_NAME)
            name = item.text()

            path = _toString(name)
            if self.scale == 0:
                self.img.resizeTaobao(path)
            else:
                self.img.resize(path, self.scale)

            self.setProgress(self.processIdx, 100)
            self.setDone(self.processIdx, True)
            self.processIdx += 1
            return True
        else:
            return False

    # for callback
    def onStop(self, event):
        print('onStop')
        self.showFinish()
        return True

if __name__ == '__main__':
    app = QtGui.QApplication( sys.argv )
    win = MainWindow()
    win.show()
    app.exec_()
