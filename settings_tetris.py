import random

class Setting():
    size_painter = 0
    def __init__(self):
        '''Настройки и параметры'''
        self.board_h=15
        self.board_w=10


class Tetro():
    '''  Набор фигур '''
    NoShape=0
    Square=1
    Piramid=2
    zFigure=3
    Line=4
    lFigure=5
    MirroredLShape = 6
    MirroredZFigure=7

class Shape():
    '''Фигура'''
    coordsTable=(
            ((0,0),(0,0),(0,0),(0,0)),
            ((0,0),(-1,-1),(0,-1),(-1,0)),
            ((0,0),(-1,1),(0,1),(1,1)),
            ((0, 0), (0,1), (1 , 1), (1, 2)),
            ((0, 0), (0, -1), (0, -2), (0, 1)),
            ((0, 0), (0, 1), (0, 2), (1, 0)),
            ((0, 0), (0, 1), (0, 2), (-1, 0)),
            ((0, 0), (0, 1), (-1, 1), (-1, 2))
    )
    def __init__(self):
        '''Инициализируем начальное положение и тип фигуры'''
        self.curx=0
        self.cury=0
        self.coords = [[0, 0] for i in range(4)]
        self.shape=Tetro.NoShape
        self.futureShape=random.randint(1,7)
        self.setRandomShape()

    def setShape(self,shape):
        '''Устанавливаем координаты для фигуры'''
        self.shape=shape
        table=Shape.coordsTable[self.shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j]=table[i][j]

    def setRandomShape(self):
        '''Рандомизируем выбор фигуры'''
        self.shape=self.futureShape
        self.futureShape = random.randint(1, 7)


    def checkMaxSizeX(self):
        '''Поиск Мах икса'''
        maxX=[]
        for i in range(4):
            maxX.append(self.coords[i][0])
        return max(maxX)

    def checkMinSizeX(self):
        '''Поиск Мin икса'''
        minX=[]
        for i in range(4):
            minX.append(self.coords[i][0])
        return min(minX)

    def checkMinSizeY(self):
        '''Поиск Мin y'''
        minY=[]
        for i in range(4):
            minY.append(self.coords[i][1])
        return min(minY)

    def checkMaxSizeY(self):
        '''Поиск Max y'''
        maxY=[]
        for i in range(4):
            maxY.append(self.coords[i][1])
        return max(maxY)

    def rotateShape(self, direction,curshape,board):
        '''Поворот фигуры'''
        if curshape.shape==Tetro.Square:
            return curshape.coords
        result=Shape()
        result.shape=curshape.shape
        result.setShape(result.shape)
        result.curx = curshape.curx
        result.cury = curshape.cury
        for i in range(4):
            result.coords[i][0]=  curshape.coords[i][1] * direction
            result.coords[i][1] = -curshape.coords[i][0] * direction

        st=Setting()
        # Проверяем на нахождение за границей
        xRight = result.curx  + result.checkMaxSizeX()
        xLeft = result.curx  + result.checkMinSizeX()

        YUp = result.cury + result.checkMaxSizeY()
        YDown = result.cury  + result.checkMinSizeY()


        if xRight < st.board_w and xLeft >= 0 and YUp < st.board_h and YDown >= 0:
            if not result.checkCollision(board,0,0):
                return result.coords
            else:
                return curshape.coords
        else:
            return curshape.coords

    def checkCollision(self,board,dopX,dopY):
        '''Проверяем на столкновения'''
        for i in range(4):
            x=(self.coords[i][0]+self.curx)+dopX
            y=(self.coords[i][1]+self.cury)+dopY
            if board[y][x] != Tetro.NoShape:
                return True
        return False


