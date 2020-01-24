from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication,QAction
from PyQt5.QtCore import Qt,QBasicTimer, QCoreApplication
from PyQt5 import QtGui
from windowTetris import Ui_MainWindow
from dialogWindows import *
import sys

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        '''Create main window'''
        super(MyWindow,self).__init__()
        self.setWindowTitle('Tetris')
        self.setWindowIcon(QtGui.QIcon('Photo/TIcon.jpg'))

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Dialog window Size
        self.ex = ChangeSize()
        self.ex.SizeSignal.connect(self.update_paint)

        # Focus on the main window
        self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)

        # Create timer
        self.timer = QBasicTimer()
        self.curSpeed = 1000
        self.timer.start(self.curSpeed, self)
        # Timer level
        self.timerLevel = QBasicTimer()
        self.timerLevel.start(20000, self)

        self.ui.pushButton.clicked.connect(self.update_paint)

        #Сразу устанавливаем что рисовать в левом окне
        self.ui.frame.curshape.shape = self.ui.widget.curshape.futureShape
        self.ui.frame.update()

        # Верхняя панель
        settings = QAction(QtGui.QIcon('Photo/Settings.jpg'), 'Size', self)
        settings.setShortcut('Ctrl+S')
        settings.triggered.connect(self.showDialogSize)
        settings.setStatusTip('Change size')
        fileMenu = self.ui.menubar.addMenu('&Settings')
        fileMenu.addAction(settings)

        # Сигнал в статусбар
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


    def update_paint(self):
        '''Update Frame'''
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
        if  self.ui.widget.fail or self.ui.widget.pause:
            pass
        if not self.ui.widget.fail and not self.ui.widget.pause:
            # Drop down
            if key == Qt.Key_Space:
                self.ui.widget.drop()

            # Move to right and to left
            if key == Qt.Key_Right:
                self.ui.widget.tryMoveX(1)

            if key == Qt.Key_Left:
                self.ui.widget.tryMoveX(-1)

            # Made rotate
            if key == Qt.Key_Down:
                self.ui.widget.curshape.coords = self.ui.widget.curshape.rotateShape(1,self.ui.widget.curshape,self.ui.widget.board)
                self.ui.widget.update()
            if key == Qt.Key_Up:
                self.ui.widget.curshape.coords = self.ui.widget.curshape.rotateShape(-1,self.ui.widget.curshape,self.ui.widget.board)
                self.ui.widget.update()

        if key == Qt.Key_P:
                # Pause
                self.ui.widget.pause = not self.ui.widget.pause
                if self.ui.widget.pause:
                    self.stopTime()
                    self.ui.widget.msg2Statusbar.emit(' Pause')
                elif not self.ui.widget.fail:
                    self.startTimeAgain()
        if key == Qt.Key_Escape:
            self.ex.close()
            self.close()

    def timerEvent(self, event):
        '''Update Level and Frame'''
        if event.timerId() == self.timerLevel.timerId():
                self.curSpeed=self.curSpeed//1.2
                self.ui.widget.curLevel+=1
                self.startTimeAgain()


        if event.timerId() == self.timer.timerId():

            if self.ui.widget.fail:
                self.ui.widget.msg2Statusbar.emit('Try Again')
                self.stopTime()
                self.ui.lineEdit.setText('FAIL: All count - '+ str(self.ui.widget.count))
                self.ui.pushButton.setText('Return?')
            else:
                self.ui.widget.msg2Statusbar.emit('Game Start!')
                self.ui.widget.gravity()
                self.setTextLine()
                self.ui.frame.curshape.shape = self.ui.widget.curshape.futureShape
                self.ui.widget.update()
                self.ui.frame.update()

    def setTextLine(self):
        '''Stand text on  LineEdit'''
        text = 'Count - '
        text += str(self.ui.widget.count)

        level = 'Level: '
        level += str(self.ui.widget.curLevel)

        self.ui.lineEdit_1.setText(level)
        self.ui.lineEdit.setText(text)
        self.ui.pushButton.setText('GO')


    def setChildrenFocusPolicy(self, policy):
        '''Focus on the main window'''
        def recursiveSetChildFocusPolicy(parentQWidget):
            for childQWidget in parentQWidget.findChildren(QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)

        recursiveSetChildFocusPolicy(self)




app = QtWidgets.QApplication([])
application = MyWindow()
application.show()
sys.exit(app.exec())



