#!/usr/bin/python

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import sys

from Models import *

UNIT_SIZE = 20
GAME_SIZE = 30
GAME_MARGIN = 20

class Display(QWidget):
    
    def __init__(self, snake, apple):
        super().__init__()
        self.snake = snake
        self.apple = apple
        self.initUI()
        
    def initUI(self):      
        display_size = GAME_SIZE * UNIT_SIZE + GAME_MARGIN * 2
        self.setGeometry(0, 0, display_size, display_size)
        self.setWindowTitle('Snake')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawYard(qp)
        self.drawApple(qp)
        self.drawSnake(qp)
        qp.end()

    def drawYard(self, qp):
        qp.setPen(Qt.green)
        yard_size = GAME_SIZE * UNIT_SIZE
        qp.drawRect(GAME_MARGIN, GAME_MARGIN, yard_size, yard_size)

    def drawApple(self, qp):
        qp.setPen(Qt.red)
        x = self.apple.x * UNIT_SIZE
        y = self.apple.y * UNIT_SIZE
        qp.drawEllipse(x, y, UNIT_SIZE, UNIT_SIZE)

        
    def drawSnake(self, qp):
        qp.setPen(Qt.black)
        cursor = snake.head

        while cursor is not None:
            x,y = cursor.getPos()
            x *= UNIT_SIZE
            y *= UNIT_SIZE
            # print(f'draw node {i}: x={x}, y={y}')
            qp.drawRect(x, y, UNIT_SIZE, UNIT_SIZE)
            cursor = cursor.next


    def keyPressEvent(self, event):
        gey = event.key()
        # self.func = (None, None)
        if gey == Qt.Key_Up:
            self.snake.move('up')
        elif gey == Qt.Key_Right:
            self.snake.move('right')
        elif gey == Qt.Key_Left:
            self.snake.move('left')
        elif gey == Qt.Key_Down:
            self.snake.move('down')
        elif gey == Qt.Key_G:
            self.snake.grow()
        elif gey == Qt.Key_A:
            self.apple.respawn()
        elif gey == Qt.Key_R:
            self.snake.respawn()
            self.apple.respawn()
        self.update()


if __name__ == '__main__':
    yard = Yard(GAME_SIZE)
    snake = yard.getSnake()
    apple = yard.getApple()
    app = QApplication(sys.argv)
    window = Display(snake, apple)
    sys.exit(app.exec_())
