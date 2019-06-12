#!/usr/bin/python

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import sys, random

from Models import *

UNIT_SIZE = 20

class Display(QWidget):
    
    def __init__(self, snake):
        super().__init__()
        self.snake = snake
        self.initUI()
        
    def initUI(self):      

        self.setGeometry(0, 0, 1000, 600)
        self.setWindowTitle('Snake')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawSnake(qp)
        qp.end()
        
    def drawSnake(self, qp):
        qp.setPen(Qt.red)
        cursor = snake.head

        while cursor is not None:
            x,y = cursor.getPos()
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
            self.snake.grow('up')
        self.update()


if __name__ == '__main__':
    snake = Snake(100, UNIT_SIZE)
    app = QApplication(sys.argv)
    window = Display(snake)
    sys.exit(app.exec_())
