from settingsTetris import Setting as st
from settingsTetris import Shape,Tetro
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont,QPen
from PyQt5.QtCore import Qt, pyqtSignal

class CurrentState(QtWidgets.QFrame):
    '''Рисует текущую фигуру'''
    #sett = st()
    BoardH = st.board_h
    BoardW = st.board_w
    widgetSize=0
    def __init__(self,parent):
        '''Создаем обьек Shape тот же, что и вглавном окне'''
        super().__init__(parent)
        self.currentcolor=0
        self.curshape = Shape()
        self.curshape.setShape(self.curshape.shape)
        self.curshape.curx=1
        self.curshape.cury=3

    def paintEvent(self,event):
        '''Рисуем фигуру, что и на главном экране'''
        self.curshape.setShape(self.curshape.shape)
        sirina=-self.curshape.checkMinSizeX()+self.curshape.checkMaxSizeX()+1
        self.curshape.curx=(sirina//2)
        self.curshape.cury = 3
        #Красивая расстановка
        if self.curshape.shape==Tetro.Square:
            self.curshape.curx+=0.5
            self.curshape.cury+=1
        elif self.curshape.shape==Tetro.Line:
            self.curshape.curx+=1
            self.curshape.cury+=1
        elif self.curshape.shape==Tetro.zFigure :
            self.curshape.curx-=0.5

        elif self.curshape.shape==Tetro.lFigure:
            self.curshape.curx -=0.5
            self.curshape.cury += 1

        elif  self.curshape.shape == Tetro.MirroredZFigure  or self.curshape.shape == Tetro.MirroredLShape:
            self.curshape.curx += 0.5


        qp = QPainter()
        qp.begin(self)
        self.drawShape(qp)
        qp.end()

    def drawShape(self,qp):
        size_paint = CurrentState.widgetSize
        colorTable = ((0, 0, 0, 0), (200, 0, 0, 230), (0, 255, 0, 230), (0, 0, 205, 230),
                      (230, 230, 0, 230), (153, 50, 204, 230), (72, 61, 139, 230), (230, 140, 0, 230))

        color = QColor.fromRgb(colorTable[self.curshape.shape][0],colorTable[self.curshape.shape][1],
                               colorTable[self.curshape.shape][2],colorTable[self.curshape.shape][3])
        for i in range(4):
            x = (size_paint.width()//CurrentState.BoardW) * (self.curshape.coords[i][0]+self.curshape.curx)
            y = (size_paint.height() //CurrentState.BoardH) * (self.curshape.coords[i][1]+self.curshape.cury)
            qp.fillRect(x+1, y+1, (size_paint.width() // CurrentState.BoardW)-2, (size_paint.height() // CurrentState.BoardH)-2, color)


class Painter(QWidget):
    '''Класс ,рисующий основное окно'''
    #sett=st()
    BoardH=st.board_h
    BoardW=st.board_w

    msg2Statusbar = pyqtSignal(str)

    def __init__(self,parent):
        '''Создаем первую фигуру'''
        super().__init__(parent)
        self.fail=False
        self.pause=False
        self.count=0
        self.clearBoard()
        self.curshape = Shape()
        self.newFigure()
        msg2Statusbar = pyqtSignal(str)

    def clearBoard(self):
        '''Создаем чистое поле'''
        Painter.BoardH = st.board_h
        Painter.BoardW = st.board_w
        CurrentState.BoardH = st.board_h
        CurrentState.BoardW = st.board_w
        self.board = []
        for i in range(Painter.BoardH):
            cols = []
            for j in range(Painter.BoardW):
                cols.append(0)
            self.board.append(cols)


    def paintEvent(self,event):
        '''Рисуем фигуру'''
        size = self.size()
        CurrentState.widgetSize = size
        qp = QPainter()
        qp.begin(self)
        self.drawShape(qp,size)
        self.drawFall(qp,size)
        qp.end()

    def drawFall(self, qp,size):
        '''Ищет где рисовать оставшиеся фигуры'''
        color = QtGui.QColor.fromRgb(75, 0, 130, 255)
        pen = QtGui.QPen(color, 8, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawRect(0, 0, self.size().width(), self.size().height())

        for i in range(Painter.BoardH):
            for j in range(Painter.BoardW):
                if self.board[i][j] != Tetro.NoShape:
                    color=self.setColor(self.board[i][j])

                    x = (size.width() // Painter.BoardW) * j
                    y = (size.height() // Painter.BoardH) * i
                    qp.fillRect(x+1, y+1 , (size.width() // Painter.BoardW) - 2, (size.height() // Painter.BoardH) - 2,
                                color)

    def drawShape(self,qp,size):
        '''Рисует основную фигуру'''
        color=self.setColor(self.curshape.shape)
        for i in range(4):
            x = (size.width()//Painter.BoardW) * (self.curshape.coords[i][0]+self.curshape.curx)
            y = (size.height() // Painter.BoardH) * (self.curshape.coords[i][1]+self.curshape.cury)
            qp.fillRect(x+1, y+1, (size.width() // Painter.BoardW)-2, (size.height() // Painter.BoardH)-2, color)


    def setColor(self,table):
        '''Ставит цвета'''
        colorTable = ((0, 0, 0, 0), (200, 0, 0, 230), (0, 255, 0, 230), (0, 0, 205, 230),
                      (230, 230, 0, 230), (153, 50, 204, 230), (72, 61, 139, 230), (230, 140, 0, 230))

        color = QColor.fromRgb(colorTable[table][0],colorTable[table][1],
                               colorTable[table][2],colorTable[table][3])
        return color

    def gravity(self):
        '''Функция гравитации'''
        newY = self.curshape.cury + 1 + self.curshape.checkMaxSizeY()
        if newY < Painter.BoardH:
            if not self.curshape.checkCollision(self.board,0, 1):
                self.curshape.cury += 1
            else:
                self.recordShape()

        else:
            self.recordShape()



    def drop(self):
        '''Функция резкого падения '''
        while True:
            newY=self.curshape.cury+1+self.curshape.checkMaxSizeY()
            if newY < Painter.BoardH:
                if not self.curshape.checkCollision(self.board,0,1):
                    self.curshape.cury+=1
                else:
                    self.update()
                    self.recordShape()
                    break
            else:
                self.update()
                self.recordShape()
                break

        self.update()

    def tryMoveX(self,direction):
        '''Движение по X'''
        xRight=self.curshape.curx+direction+self.curshape.checkMaxSizeX()
        xLeft=self.curshape.curx+direction+self.curshape.checkMinSizeX()
        if xRight < Painter.BoardW and xLeft >= 0:
            if not self.curshape.checkCollision(self.board,direction, 0):
                self.curshape.curx+=direction
        self.update()


    def newFigure(self):
        '''Создание новой фигуры сверху'''
        self.curshape.setRandomShape()
        self.curshape.setShape(self.curshape.shape)
        self.curshape.curx = Painter.BoardW // 2
        self.curshape.cury = -self.curshape.checkMinSizeY()
        if self.curshape.checkCollision(self.board,0, 0):
            self.fail=True


    def recordShape(self):
        '''Запись в список упавших'''

        for i in range(4):
            x = (self.curshape.coords[i][0] + self.curshape.curx)
            y = (self.curshape.coords[i][1] + self.curshape.cury)
            self.board[y][x] = self.curshape.shape

        self.checkFullLine()
        self.newFigure()

    def checkFullLine(self):
        '''Ищем полную линию'''
        for i in range (len(self.board)):
            count=0
            for j in range (len(self.board[0])):
                if self.board[i][j] != Tetro.NoShape:
                    count+=1
            if count==len(self.board[0]):
                self.removeFullLine(i)


    def removeFullLine(self,y):
        '''Удаляем полную линию'''
        for i in range (y):
            if self.board[y-i]== [[0,0] for i in range (len(self.board[0]))]:
                break
            for j in range(len(self.board[0])):
                cols=self.board[y-i-1][j]
                self.board[y-i][j]=cols

        self.count+=len(self.board[0])





class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(766, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Наш Grid
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # Наш правый виджет, где рисуем
        self.widget = Painter(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout.addWidget(self.widget, 0, 1, 1, 3)

        # Создаем левый Layout
        self.Vertical = QtWidgets.QGroupBox(self.centralwidget)
        self.Vertical.setObjectName("Vertical")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Vertical)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Создаем слева окно, где рисуем нынешнюю фигуру
        self.frame = CurrentState(self.Vertical)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2.addWidget(self.frame)

        #Создаем Line
        self.lineEdit = QtWidgets.QLineEdit(self.Vertical)
        self.lineEdit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit, 0, QtCore.Qt.AlignHCenter)

        # Создаем кнопку
        self.pushButton = QtWidgets.QPushButton(self.Vertical)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)

        # Добавляем левый Layout в Grid
        self.gridLayout.addWidget(self.Vertical, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 766, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tetris 2.0  by I1ya Be1yan0v"))
        self.Vertical.setTitle(_translate("MainWindow", "   Следующая фигура"))
        self.pushButton.setText(_translate("MainWindow", " Начать"))

if __name__ == "__main__":
    print('It is module for Tetris')