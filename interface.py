from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QAction
from PyQt5.QtCore import QBasicTimer

from dialogWindows import *
from windowTetris import Ui_MainWindow


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle('Tetris')
        self.setWindowIcon(QtGui.QIcon('Photo/TIcon.jpg'))

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ex = ChangeSize()
        self.ex.SizeSignal.connect(self.updateFrame)

        self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)

        self.timer = QBasicTimer()
        self.curSpeed = 1000
        self.timer.start(self.curSpeed, self)

        self.timerLevel = QBasicTimer()
        self.timerLevel.start(20000, self)

        self.ui.pushButton.clicked.connect(self.updateFrame)

        self.ui.frame.curshape.shape = self.ui.widget.curshape.futureShape
        self.ui.frame.update()

        # Верхняя панель
        settings = QAction(QtGui.QIcon('Photo/Settings.jpg'), 'Size', self)
        settings.setShortcut('Ctrl+S')
        settings.triggered.connect(self.showDialogSize)
        settings.setStatusTip('Change size')
        fileMenu = self.ui.menubar.addMenu('&Settings')
        fileMenu.addAction(settings)

        self.ui.widget.msg2Statusbar[str].connect(self.ui.statusbar.showMessage)

        self.loadStyleSheets()

    def loadStyleSheets(self):
        style = "static/style.css"
        with open(style, "r") as f:
            self.setStyleSheet(f.read())

    def showDialogSize(self):
        self.ui.widget.pause = True
        self.ui.widget.msg2Statusbar.emit(' Pause')
        self.stopTime()
        self.ex.show()

    def startTimeAgain(self):
        self.timer.start(self.curSpeed, self)
        self.timerLevel.start(20000, self)

    def stopTime(self):
        self.timer.stop()
        self.timerLevel.stop()

    def updateFrame(self):
        self.stopTime()

        self.curSpeed = 1000
        self.ui.widget.fail = False
        self.ui.widget.pause = False
        self.ui.widget.clearBoard()
        self.ui.widget.newFigure()
        self.ui.widget.update()
        self.ui.frame.curshape.shape = self.ui.widget.curshape.futureShape
        self.ui.frame.update()
        self.ui.widget.count = 0
        self.ui.widget.curLevel = 1

        self.startTimeAgain()

    def keyPressEvent(self, event):
        key = event.key()
        if self.ui.widget.fail or self.ui.widget.pause:
            pass
        if not self.ui.widget.fail and not self.ui.widget.pause:
            if key == QtCore.Qt.Key_Space:
                self.ui.widget.drop()

            if key == QtCore.Qt.Key_Right:
                self.ui.widget.tryMoveX(1)

            if key == QtCore.Qt.Key_Left:
                self.ui.widget.tryMoveX(-1)

            if key == QtCore.Qt.Key_Down:
                self.ui.widget.curshape.coords = self.ui.widget.curshape.rotateShape(1, self.ui.widget.curshape,
                                                                                     self.ui.widget.board)
                self.ui.widget.update()
            if key == QtCore.Qt.Key_Up:
                self.ui.widget.curshape.coords = self.ui.widget.curshape.rotateShape(-1, self.ui.widget.curshape,
                                                                                     self.ui.widget.board)
                self.ui.widget.update()

        if key == QtCore.Qt.Key_P:
            self.ui.widget.pause = not self.ui.widget.pause
            if self.ui.widget.pause:
                self.stopTime()
                self.ui.widget.msg2Statusbar.emit(' Pause')
            elif not self.ui.widget.fail:
                self.startTimeAgain()

        if key == QtCore.Qt.Key_Escape:
            self.ex.close()
            self.close()

    def timerEvent(self, event):
        if event.timerId() == self.timerLevel.timerId():
            self.curSpeed = self.curSpeed // 1.2
            self.ui.widget.curLevel += 1
            self.startTimeAgain()

        if event.timerId() == self.timer.timerId():

            if self.ui.widget.fail:
                self.ui.widget.msg2Statusbar.emit('Try Again')
                self.stopTime()
                self.ui.lineEdit.setText('FAIL: All count - ' + str(self.ui.widget.count))
                self.ui.pushButton.setText('Return?')
            else:
                self.ui.widget.msg2Statusbar.emit('Game Start!')
                self.ui.widget.gravity()
                self.setTextLine()
                self.ui.frame.curshape.shape = self.ui.widget.curshape.futureShape
                self.ui.widget.update()
                self.ui.frame.update()

    def setTextLine(self):
        text = 'Count - '
        text += str(self.ui.widget.count)

        level = 'Level: '
        level += str(self.ui.widget.curLevel)

        self.ui.lineEdit_1.setText(level)
        self.ui.lineEdit.setText(text)
        self.ui.pushButton.setText('GO')

    def setChildrenFocusPolicy(self, policy):
        def recursiveSetChildFocusPolicy(parentQWidget):
            for childQWidget in parentQWidget.findChildren(QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)

        recursiveSetChildFocusPolicy(self)



