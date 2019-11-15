from PyQt5.QtWidgets import QWidget, QApplication,QAction
from PyQt5.QtCore import Qt,QBasicTimer, QCoreApplication
from PyQt5 import QtGui
from paintTetris import *
from dialogWindows import *
import sys

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        '''Создаем наше главное окно'''
        super(MyWindow,self).__init__()
        self.setWindowTitle('Tetris 2.0               I1ya Be1yan0v')
        self.setWindowIcon(QtGui.QIcon('Photo/TIcon.jpg'))

        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        # Диалоговое окно Size
        self.ex = ChangeSize()
        self.ex.SizeSignal.connect(self.update_paint)


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

        # Верхняя панель
        settings = QAction(QtGui.QIcon('Photo/Settings.jpg'), 'Size', self)
        settings.setShortcut('Ctrl+S')
        settings.triggered.connect(self.showDialogSize)
        settings.setStatusTip('Change size')
        fileMenu = self.ui.menubar.addMenu('&Settings')
        fileMenu.addAction(settings)

        # Сигнал в статусбар
        self.ui.widget.msg2Statusbar[str].connect(self.ui.statusbar.showMessage)
    def showDialogSize(self):
        ''' Диалог '''
        self.ui.widget.pause = True
        self.ui.widget.msg2Statusbar.emit(' Pause')
        self.timer.stop()
        self.ex.show()

    def startTimeAgain(self):
        self.timer.start(1000, self)

    def update_paint(self):
        '''Обновляем поле'''
        self.timer.stop()

        self.ui.widget.fail=False
        self.ui.widget.pause=False
        self.ui.widget.clearBoard()
        self.ui.widget.newFigure()
        self.ui.widget.update()
        self.ui.frame.curshape.shape = self.ui.widget.curshape.futureShape
        self.ui.frame.update()
        self.ui.widget.count=0
        self.startTimeAgain()

    def keyPressEvent(self, event):
        '''Обрабатываем нажатия'''
        key = event.key()
        if  self.ui.widget.fail or self.ui.widget.pause:
            pass
        if not self.ui.widget.fail and not self.ui.widget.pause:
            # Дроп вниз
            if key == Qt.Key_Space:
                self.ui.widget.drop()

            # Движение влево и вправо
            if key == Qt.Key_Right:
                self.ui.widget.tryMoveX(1)

            if key == Qt.Key_Left:
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
                    self.ui.widget.msg2Statusbar.emit(' Pause')
                elif not self.ui.widget.fail:
                    self.startTimeAgain()
        if key == Qt.Key_Escape:
            # Закрытие
            self.ex.close()
            self.close()

    def timerEvent(self, event):
        '''Обновляем окна через t промежуток'''
        if event.timerId() == self.timer.timerId():
            if self.ui.widget.fail:
                self.ui.widget.msg2Statusbar.emit('Попробуйте еще')
                self.timer.stop()
                self.ui.lineEdit.setText('FAIL: Все очки- '+ str(self.ui.widget.count))
                self.ui.pushButton.setText('Заново?')
            else:
                self.ui.widget.msg2Statusbar.emit('Игра началась')
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



