from PyQt5.QtWidgets import QWidget, QApplication,QToolTip, QWidget, QAction , QPushButton, QDialog
from PyQt5.QtCore import Qt,QBasicTimer, QCoreApplication
from PyQt5 import QtGui
from paintTetris import *
import sys
from settingsTetris import Setting as st

class Example(QDialog):
    '''Диалоговое окно изменения размера'''
    SizeSignal = pyqtSignal()
    OutSignal = pyqtSignal()
    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        btn = QPushButton('Yes', self)
        btn.clicked.connect(self.buttonYesClicked)
        btn.resize(180, 40)
        btn.move(20, 35)

        qbtn = QPushButton('No', self)
        qbtn.clicked.connect(self.buttonNoClicked)
        qbtn.resize(180, 40)
        qbtn.move(20, 80)

        self.setWindowTitle('Test')

    def buttonYesClicked(self):
        st.board_h=20
        st.board_w=25
        self.SizeSignal.emit()
        self.close()

    def buttonNoClicked(self):
        self.OutSignal.emit()
        self.close()


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        '''Создаем наше главное окно'''
        super(MyWindow,self).__init__()
        self.setWindowTitle('Tetris')
        self.setWindowIcon(QtGui.QIcon('Korn.jpg'))

        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        # Диалоговое окно Size
        self.ex = Example()
        self.ex.SizeSignal.connect(self.update_paint)
        self.ex.OutSignal.connect(self.startTimeAgain)

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
        settings = QAction(QtGui.QIcon('Korn.jpg'), 'Size', self)
        settings.setShortcut('Ctrl+O')
        settings.triggered.connect(self.showDialogSize)

        fileMenu = self.ui.menubar.addMenu('&Settings')
        fileMenu.addAction(settings)

        # Сигнал в статусбар
        self.ui.widget.msg2Statusbar[str].connect(self.ui.statusbar.showMessage)
    def showDialogSize(self):
        ''' Диалог '''
        self.timer.stop()
        print(self.ui.widget.pause)
        self.ex.show()

    def startTimeAgain(self):
        self.timer.start(1000, self)

    def update_paint(self):
        '''Обновляем поле'''
        Painter.BoardH = st.board_h
        Painter.BoardW = st.board_w
        CurrentState.BoardH = st.board_h
        CurrentState.BoardW= st.board_w

        self.ui.widget.fail=False
        self.ui.widget.pause=False
        self.ui.widget.clearBoard()
        self.ui.widget.newFigure()
        self.ui.widget.curshape.cury -= 1
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



