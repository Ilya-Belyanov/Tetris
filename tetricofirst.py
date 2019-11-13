from PyQt5.QtWidgets import QWidget, QApplication,QToolTip, QWidget
from PyQt5.QtCore import Qt,QBasicTimer
from PyQt5 import QtGui
from tetrico import *
import sys


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        '''Создаем наше главное окно'''
        super(MyWindow,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        # Фокус на главное окно
        self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)

        # Создаем таймер
        self.timer = QBasicTimer()
        self.timer.start(1000, self)

        # Подключаем кнопку к обновлению фигуры
        self.ui.pushButton.clicked.connect(self.update_paint)

        #Сразу устанавливаем что рисовать в левом окне
        self.ui.frame.curshape.shape = self.ui.widget.curshape.futureShape
        self.ui.frame.update()

    def update_paint(self):
        '''Обновляем фигуру'''
        self.ui.widget.fail=False
        self.ui.widget.clearBoard()
        self.ui.widget.newFigure()
        self.ui.frame.curshape.shape = self.ui.widget.curshape.shape
        self.ui.frame.update()
        self.ui.widget.count=0
        self.timer.start(1000, self)

    def keyPressEvent(self, event):
        '''Обрабатываем нажатия'''
        if  self.ui.widget.fail:
            pass
        else:

            key = event.key()
            if key == Qt.Key_Space:
                self.ui.widget.drop()
            if key == Qt.Key_D:
                self.ui.widget.tryMoveX(1)

            if key == Qt.Key_A:
                self.ui.widget.tryMoveX(-1)

            # Совершаем повороты
            if key == Qt.Key_Down:
                self.ui.widget.curshape.coords = self.ui.widget.curshape.rotateShape(1,self.ui.widget.curshape,self.ui.widget.board)
                self.ui.widget.update()
            if key == Qt.Key_Up:
                self.ui.widget.curshape.coords = self.ui.widget.curshape.rotateShape(-1,self.ui.widget.curshape,self.ui.widget.board)
                self.ui.widget.update()

            if key == Qt.Key_P:
                #Пауза
                self.ui.widget.pause = not self.ui.widget.pause
                if self.ui.widget.pause:
                    self.timer.stop()
                else:
                    self.timer.start(1000, self)

    def timerEvent(self, event):
        '''Обновляем окна через t промежуток'''
        if event.timerId() == self.timer.timerId():
            if self.ui.widget.fail:
                self.timer.stop()
                self.ui.lineEdit.setText('FAIL: Все очки- '+ str(self.ui.widget.count))
                self.ui.pushButton.setText('Заново?')
            else:
                self.ui.widget.gravity()
                self.setTextLine()
                self.ui.frame.curshape.shape = self.ui.widget.curshape.futureShape
                self.ui.widget.update()
                self.ui.frame.update()


    def setTextLine(self):
        '''Устанавливаем текст на LineEdit'''
        text='Очки - '
        text+= str(self.ui.widget.count)
        self.ui.lineEdit.setText(text)
        self.ui.pushButton.setText('Поехали')

    def setChildrenFocusPolicy(self, policy):
        '''Фокусируем нажатие на кнопки в главном окне'''
        def recursiveSetChildFocusPolicy(parentQWidget):
            for childQWidget in parentQWidget.findChildren(QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)

        recursiveSetChildFocusPolicy(self)


app=QtWidgets.QApplication([])
application=MyWindow()
application.show()


sys.exit(app.exec())