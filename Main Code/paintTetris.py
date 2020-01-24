from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QColor, QFont,QPen
from PyQt5.QtCore import Qt, pyqtSignal

from settingsTetris import Setting as st
from settingsTetris import Shape,Tetro

class CurrentState(QtWidgets.QFrame):
    '''Draw Future shape'''
    BoardH = st.board_h
    BoardW = st.board_w
    widgetSize = 0  # changing in Painter
    def __init__(self,parent):
        super().__init__(parent)
        self.currentcolor = 0
        self.curshape = Shape()
        self.curshape.setShape(self.curshape.shape)
        self.curshape.curx = 1
        self.curshape.cury = 3

        self.modeList = (1, 2, 3)
        self.curMode = self.modeList[0]

    def paintEvent(self,event):
        self.curshape.setShape(self.curshape.shape)
        meadle = -self.curshape.checkMinSizeX()+self.curshape.checkMaxSizeX()+1
        self.curshape.curx = (meadle // 2)
        self.curshape.cury = 3
        #beauty componate
        if self.curshape.shape == Tetro.Square:
            self.curshape.curx += 1
            self.curshape.cury += 1

        elif self.curshape.shape == Tetro.Piramid:
            self.curshape.curx += 0.5

        elif self.curshape.shape == Tetro.Line:
            self.curshape.curx += 1.5
            self.curshape.cury += 1
        elif self.curshape.shape == Tetro.zFigure :
            #self.curshape.curx += 0.5
            pass
        elif self.curshape.shape == Tetro.lFigure:
            #self.curshape.curx += 0.5
            self.curshape.cury += 1

        elif  self.curshape.shape == Tetro.MirroredZFigure  or self.curshape.shape == Tetro.MirroredLShape:
            self.curshape.curx += 1


        qp = QPainter()
        qp.begin(self)
        self.drawMode(qp)
        self.drawShape(qp)
        qp.end()

    def drawShape(self,qp):
        size_paint = CurrentState.widgetSize
        colorTable = ((0, 0, 0, 0), (200, 0, 0, 255), (0, 255, 0, 255), (0, 0, 205, 255),
                      (230, 230, 0, 255), (153, 50, 204, 255), (72, 61, 139, 255), (230, 140, 0, 255))

        color = QColor.fromRgb(colorTable[self.curshape.shape][0],colorTable[self.curshape.shape][1],
                               colorTable[self.curshape.shape][2],colorTable[self.curshape.shape][3])
        for i in range(4):
            x = (size_paint.width()//CurrentState.BoardW) * (self.curshape.coords[i][0]+self.curshape.curx)
            y = (size_paint.height() //CurrentState.BoardH) * (self.curshape.coords[i][1]+self.curshape.cury)
            qp.fillRect(x+1, y+1, (size_paint.width() // CurrentState.BoardW)-2, (size_paint.height() // CurrentState.BoardH)-2, color)

    def drawMode(self,qp):
        if self.curMode == 1:
            pass
        elif self.curMode == 2:
            qp.fillRect(0, 0, self.size().width(), self.size().height(), QtGui.QColor.fromRgb(0, 255, 255, 255))

class Painter(QtWidgets.QFrame):
    '''Main window for drawing'''
    BoardH = st.board_h
    BoardW = st.board_w

    msg2Statusbar = pyqtSignal(str)

    def __init__(self,parent):
        super().__init__(parent)
        self.fail = False
        self.pause = False
        self.count = 0
        self.curLevel = 1
        self.clearBoard()
        self.curshape = Shape()
        self.newFigure()
        msg2Statusbar = pyqtSignal(str)

        self.modeList = (1,2,3)
        self.curMode = self.modeList[0]

    def clearBoard(self):
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


    def setColor(self,table):
        colorTable = ((0, 0, 0, 0), (200, 0, 0, 255), (0, 255, 0, 255), (0, 0, 205, 255),
                      (230, 230, 0, 255), (153, 50, 204, 255), (72, 61, 139, 255), (230, 140, 0, 255))

        color = QColor.fromRgb(colorTable[table][0],colorTable[table][1],
                               colorTable[table][2],colorTable[table][3])
        return color

    def gravity(self):
        newY = self.curshape.cury + 1 + self.curshape.checkMaxSizeY()
        if newY < Painter.BoardH:
            if not self.curshape.checkCollision(self.board,0, 1):
                self.curshape.cury += 1
            else:
                self.recordShape()

        else:
            self.recordShape()


    def drop(self):
        while True:
            newY = self.curshape.cury + 1 + self.curshape.checkMaxSizeY()
            if newY < Painter.BoardH:
                if not self.curshape.checkCollision(self.board,0,1):
                    self.curshape.cury += 1
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
        xRight = self.curshape.curx+direction+self.curshape.checkMaxSizeX()
        xLeft = self.curshape.curx+direction+self.curshape.checkMinSizeX()
        if xRight < Painter.BoardW and xLeft >= 0:
            if not self.curshape.checkCollision(self.board,direction, 0):
                self.curshape.curx += direction
        self.update()


    def newFigure(self):
        self.curshape.setRandomShape()
        self.curshape.setShape(self.curshape.shape)
        self.curshape.curx = Painter.BoardW // 2
        self.curshape.cury = -self.curshape.checkMinSizeY()
        if self.curshape.checkCollision(self.board,0, 0):
            self.fail = True


    def recordShape(self):
        for i in range(4):
            x = (self.curshape.coords[i][0] + self.curshape.curx)
            y = (self.curshape.coords[i][1] + self.curshape.cury)
            self.board[y][x] = self.curshape.shape

        self.checkFullLine()
        self.newFigure()

    def checkFullLine(self):
        for i in range (len(self.board)):
            count = 0
            for j in range (len(self.board[0])):
                if self.board[i][j] != Tetro.NoShape:
                    count += 1
            if count == len(self.board[0]):
                self.removeFullLine(i)


    def removeFullLine(self,y):
        for i in range (y):
            if self.board[y-i] == [[0,0] for i in range (len(self.board[0]))]:
                break
            for j in range(len(self.board[0])):
                cols = self.board[y-i-1][j]
                self.board[y-i][j] = cols

        self.count += (len(self.board[0])*self.curLevel)


    def paintEvent(self,event):
        size = self.size()
        CurrentState.widgetSize = size
        qp = QPainter()
        qp.begin(self)
        self.drawGrid(qp,size)
        self.drawMode(qp)
        self.drawShape(qp,size)
        self.drawFall(qp,size)
        qp.end()

    def drawGrid(self,qp,size):
        color = QtGui.QColor.fromRgb(50, 50, 50, 255)
        pen = QtGui.QPen(color, 5, Qt.SolidLine)
        qp.setPen(pen)
        qp.fillRect(0, 0, (size.width() // Painter.BoardW) * Painter.BoardW,
                    (size.height() // Painter.BoardH) * Painter.BoardH, color)
        
        color = QtGui.QColor.fromRgb(0, 0, 0, 255)
        pen = QtGui.QPen(color,0.2, QtCore.Qt.SolidLine)
        pen.setStyle(Qt.DashLine)
        qp.setPen(pen)

        for j in range(Painter.BoardH + 1):
                y = j * (size.height() // Painter.BoardH)
                qp.drawLine(0,y,size.width(),y)

        for i in range(Painter.BoardW + 1):
                x = i * (size.width() // Painter.BoardW)
                qp.drawLine(x,0,x,size.height())


    def drawFall(self, qp,size):
        '''Draw fall shape'''
        for i in range(Painter.BoardH):
            for j in range(Painter.BoardW):
                if self.board[i][j] != Tetro.NoShape:
                    color = self.setColor(self.board[i][j])

                    x = (size.width() // Painter.BoardW) * j
                    y = (size.height() // Painter.BoardH) * i
                    qp.fillRect(x+1, y+1 , (size.width() / Painter.BoardW) - 2, (size.height() / Painter.BoardH) - 2,
                                color)

    def drawShape(self,qp,size):
        '''Draw main shape'''
        color = self.setColor(self.curshape.shape)
        for i in range(4):
            x = int(size.width()/Painter.BoardW) * (self.curshape.coords[i][0]+self.curshape.curx)
            y = int(size.height()/ Painter.BoardH) * (self.curshape.coords[i][1]+self.curshape.cury)
            qp.fillRect(x + 1, y +1, (size.width() / Painter.BoardW) -2, (size.height() / Painter.BoardH) -2, color)


    def drawMode(self,qp):
        if self.curMode == 1:
           pass

        elif self.curMode == 2:
            qp.fillRect(0, 0, self.size().width(), self.size().height(), QtGui.QColor.fromRgb(0, 245, 245, 245))
            qp.drawEllipse(QtCore.QRect(self.size().width()//Painter.BoardW,self.size().heigt()//Painter.BoardH,25,25))



if __name__ == "__main__":
    print('It is module for Tetris')